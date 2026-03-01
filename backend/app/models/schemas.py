from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DebateCreate(BaseModel):
    topic: str = Field(..., min_length=10, max_length=500)
    rounds: int = Field(default=3, ge=1, le=5)
    agent_pro: str = Field(default="claude", pattern="^(claude|openai)$")
    agent_con: str = Field(default="openai", pattern="^(claude|openai)$")

class ArgumentOut(BaseModel):
    id: int
    debate_id: int
    round_number: int
    agent: str
    model: str
    stance: str
    content: str
    logical_coherence: Optional[float]
    factual_grounding: Optional[float]
    rhetorical_strength: Optional[float]
    fallacy_score: Optional[float]
    overall_score: Optional[float]
    ml_score: Optional[float]
    created_at: datetime
    class Config:
        from_attributes = True

class DebateOut(BaseModel):
    id: int
    topic: str
    rounds: int
    agent_pro: str
    agent_con: str
    winner: Optional[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    arguments: List[ArgumentOut] = []
    class Config:
        from_attributes = True

class DebateListItem(BaseModel):
    id: int
    topic: str
    rounds: int
    agent_pro: str
    agent_con: str
    winner: Optional[str]
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ScoreRequest(BaseModel):
    argument_text: str = Field(..., min_length=20)
    topic: str = Field(..., min_length=5)
    stance: str = Field(..., pattern="^(pro|con)$")

class ScoreResponse(BaseModel):
    ml_score: float
    label: str
    confidence: float
