from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.debate import Debate
from app.models.schemas import DebateCreate, DebateOut, DebateListItem, ScoreRequest, ScoreResponse
from app.services.debate_engine import run_debate
from app.services.train_scorer import scorer

router = APIRouter(prefix="/api/debates", tags=["debates"])

@router.post("/", response_model=DebateOut, status_code=201)
async def create_debate(payload: DebateCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    debate = Debate(topic=payload.topic, rounds=payload.rounds, agent_pro=payload.agent_pro, agent_con=payload.agent_con, status="pending")
    db.add(debate); db.commit(); db.refresh(debate)
    background_tasks.add_task(run_debate, debate, db)
    return debate

@router.get("/", response_model=List[DebateListItem])
def list_debates(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Debate).order_by(Debate.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    from app.models.debate import Argument
    from sqlalchemy import func
    total_debates = db.query(Debate).count()
    complete_debates = db.query(Debate).filter(Debate.status == "complete").count()
    total_arguments = db.query(Argument).count()
    avg_score = db.query(func.avg(Argument.overall_score)).scalar()
    wins = db.query(Debate.winner, func.count(Debate.winner)).filter(Debate.status == "complete", Debate.winner != "draw").group_by(Debate.winner).all()
    return {"total_debates": total_debates, "complete_debates": complete_debates, "total_arguments": total_arguments, "avg_argument_score": round(float(avg_score or 0), 3), "wins_by_agent": {w: c for w, c in wins}}

@router.get("/{debate_id}", response_model=DebateOut)
def get_debate(debate_id: int, db: Session = Depends(get_db)):
    debate = db.query(Debate).filter(Debate.id == debate_id).first()
    if not debate: raise HTTPException(status_code=404, detail="Debate not found")
    return debate

@router.delete("/{debate_id}", status_code=204)
def delete_debate(debate_id: int, db: Session = Depends(get_db)):
    debate = db.query(Debate).filter(Debate.id == debate_id).first()
    if not debate: raise HTTPException(status_code=404, detail="Debate not found")
    db.delete(debate); db.commit()

@router.post("/score", response_model=ScoreResponse)
def score_argument(payload: ScoreRequest):
    result = scorer.score(f"[Topic: {payload.topic}] [Stance: {payload.stance}] {payload.argument_text}")
    return ScoreResponse(**result)
