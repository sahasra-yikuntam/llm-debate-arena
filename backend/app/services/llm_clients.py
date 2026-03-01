import json
import re
from app.core.config import settings

class MockLLMClient:
    DEMO_ARGUMENTS = {
        "pro": [
            "The evidence clearly supports this position. Historically, technological revolutions have consistently displaced workers in specific sectors while simultaneously creating entirely new industries. The net effect on employment has been positive, but this time the speed and breadth of AI adoption may outpace the economy's ability to adapt.",
            "Furthermore, AI systems are now encroaching on cognitive tasks previously considered uniquely human. Legal research, radiology, and financial analysis are being augmented or replaced. The question is not whether displacement occurs, but whether new job creation keeps pace.",
            "In conclusion, economic modeling from Goldman Sachs to MIT labor economists suggests a net negative employment effect in the near term, with recovery possible over decades if retraining infrastructure is built at scale.",
        ],
        "con": [
            "This position fundamentally misunderstands how economic transformation works. The Luddite fallacy has been disproven repeatedly — steam engines, electricity, and computers all triggered fears of mass unemployment, yet global employment and living standards rose dramatically.",
            "Moreover, AI is primarily an augmentation tool rather than a replacement mechanism in most sectors. Doctors using AI see more patients. Lawyers do higher-value work. Productivity gains will expand markets and create new categories of human labor.",
            "The empirical data supports optimism: sectors with the highest AI adoption have shown positive employment effects. The real challenge is transition speed and retraining capacity — solvable with policy.",
        ]
    }

    async def generate_argument(self, system_prompt, user_prompt, model_name):
        import random
        stance = "pro" if "affirmative" in system_prompt.lower() or "supporting" in system_prompt.lower() else "con"
        return random.choice(self.DEMO_ARGUMENTS[stance])

    async def judge_argument(self, argument, topic, stance):
        import random
        return {
            "logical_coherence": round(random.uniform(0.6, 0.95), 3),
            "factual_grounding": round(random.uniform(0.5, 0.90), 3),
            "rhetorical_strength": round(random.uniform(0.55, 0.92), 3),
            "fallacy_score": round(random.uniform(0.0, 0.3), 3),
            "overall_score": round(random.uniform(0.6, 0.92), 3),
            "reasoning": "Demo mode — set API keys to enable real scoring."
        }

class AnthropicClient:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def generate_argument(self, system_prompt, user_prompt, model_name="claude-haiku-20240307"):
        response = self.client.messages.create(model=model_name, max_tokens=600, system=system_prompt, messages=[{"role": "user", "content": user_prompt}])
        return response.content[0].text

    async def judge_argument(self, argument, topic, stance):
        import re
        prompt = f"Score this debate argument as JSON only.\nTopic: {topic}\nStance: {stance}\nArgument: {argument}\n\nReturn ONLY valid JSON: {{\"logical_coherence\": 0.0-1.0, \"factual_grounding\": 0.0-1.0, \"rhetorical_strength\": 0.0-1.0, \"fallacy_score\": 0.0-1.0, \"overall_score\": 0.0-1.0, \"reasoning\": \"brief\"}}"
        response = self.client.messages.create(model="claude-haiku-20240307", max_tokens=300, messages=[{"role": "user", "content": prompt}])
        text = response.content[0].text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse: {text}")

class OpenAIClient:
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def generate_argument(self, system_prompt, user_prompt, model_name="gpt-4o-mini"):
        response = self.client.chat.completions.create(model=model_name, max_tokens=600, messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])
        return response.choices[0].message.content

    async def judge_argument(self, argument, topic, stance):
        import re
        prompt = f"Score as JSON only. Topic: {topic} Stance: {stance} Argument: {argument}\nReturn ONLY: {{\"logical_coherence\": 0.0-1.0, \"factual_grounding\": 0.0-1.0, \"rhetorical_strength\": 0.0-1.0, \"fallacy_score\": 0.0-1.0, \"overall_score\": 0.0-1.0, \"reasoning\": \"brief\"}}"
        response = self.client.chat.completions.create(model="gpt-4o-mini", max_tokens=300, messages=[{"role": "user", "content": prompt}])
        text = response.choices[0].message.content
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse: {text}")

def get_llm_client(provider):
    if provider == "claude" and settings.anthropic_api_key and settings.anthropic_api_key != "your_anthropic_key_here":
        return AnthropicClient()
    if provider == "openai" and settings.openai_api_key and settings.openai_api_key != "your_openai_key_here":
        return OpenAIClient()
    return MockLLMClient()
