from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.debate import Debate, Argument
from app.services.llm_clients import get_llm_client

SYSTEM_PROMPT_PRO = "You are a skilled debater arguing the AFFIRMATIVE / PRO position. Construct a compelling, well-reasoned argument supporting the topic. Be specific, cite evidence, and rebut opposing arguments. Keep under 200 words."
SYSTEM_PROMPT_CON = "You are a skilled debater arguing the NEGATIVE / CON position. Construct a compelling, well-reasoned argument opposing the topic. Be specific, cite evidence, and rebut the affirmative. Keep under 200 words."
MODEL_MAP = {"claude": "claude-haiku-20240307", "openai": "gpt-4o-mini"}

async def run_debate(debate: Debate, db: Session) -> Debate:
    debate.status = "running"
    db.commit()
    pro_client = get_llm_client(debate.agent_pro)
    con_client = get_llm_client(debate.agent_con)
    judge_client = get_llm_client(debate.agent_pro)
    pro_arguments = []
    con_arguments = []
    try:
        for round_num in range(1, debate.rounds + 1):
            context = _build_context(pro_arguments, con_arguments, round_num)
            pro_prompt = f"Topic: {debate.topic}\n\nRound {round_num} of {debate.rounds}.\n{context}\nGive your argument now."
            pro_text = await pro_client.generate_argument(SYSTEM_PROMPT_PRO, pro_prompt, MODEL_MAP[debate.agent_pro])
            pro_scores = await judge_client.judge_argument(pro_text, debate.topic, "pro")
            pro_arg = Argument(debate_id=debate.id, round_number=round_num, agent="pro", model=MODEL_MAP[debate.agent_pro], stance="pro", content=pro_text, logical_coherence=pro_scores.get("logical_coherence"), factual_grounding=pro_scores.get("factual_grounding"), rhetorical_strength=pro_scores.get("rhetorical_strength"), fallacy_score=pro_scores.get("fallacy_score"), overall_score=pro_scores.get("overall_score"), raw_judge_response=pro_scores)
            db.add(pro_arg)
            db.commit()
            pro_arguments.append(pro_text)
            con_context = _build_context(pro_arguments, con_arguments, round_num, latest_pro=pro_text)
            con_prompt = f"Topic: {debate.topic}\n\nRound {round_num} of {debate.rounds}.\n{con_context}\nGive your rebuttal now."
            con_text = await con_client.generate_argument(SYSTEM_PROMPT_CON, con_prompt, MODEL_MAP[debate.agent_con])
            con_scores = await judge_client.judge_argument(con_text, debate.topic, "con")
            con_arg = Argument(debate_id=debate.id, round_number=round_num, agent="con", model=MODEL_MAP[debate.agent_con], stance="con", content=con_text, logical_coherence=con_scores.get("logical_coherence"), factual_grounding=con_scores.get("factual_grounding"), rhetorical_strength=con_scores.get("rhetorical_strength"), fallacy_score=con_scores.get("fallacy_score"), overall_score=con_scores.get("overall_score"), raw_judge_response=con_scores)
            db.add(con_arg)
            db.commit()
            con_arguments.append(con_text)
        db.refresh(debate)
        debate.winner = _determine_winner(debate)
        debate.status = "complete"
        debate.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(debate)
    except Exception as e:
        debate.status = "failed"
        db.commit()
        raise e
    return debate

def _build_context(pro_args, con_args, round_num, latest_pro=None):
    if round_num == 1 and not latest_pro:
        return "This is the opening round. Make your opening argument."
    parts = []
    if latest_pro:
        parts.append(f"The PRO side just argued:\n{latest_pro}")
    elif pro_args:
        parts.append(f"PRO's last argument:\n{pro_args[-1]}")
    if con_args:
        parts.append(f"Your last argument (CON):\n{con_args[-1]}")
    return "\n\n".join(parts)

def _determine_winner(debate):
    pro_scores = [a.overall_score for a in debate.arguments if a.stance == "pro" and a.overall_score]
    con_scores = [a.overall_score for a in debate.arguments if a.stance == "con" and a.overall_score]
    if not pro_scores or not con_scores:
        return "draw"
    pro_avg = sum(pro_scores) / len(pro_scores)
    con_avg = sum(con_scores) / len(con_scores)
    if abs(pro_avg - con_avg) < 0.05:
        return "draw"
    return debate.agent_pro if pro_avg > con_avg else debate.agent_con
