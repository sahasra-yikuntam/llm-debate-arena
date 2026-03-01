from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Debate(Base):
    __tablename__ = "debates"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(500), nullable=False)
    rounds = Column(Integer, default=3)
    agent_pro = Column(String(100), default="claude")
    agent_con = Column(String(100), default="openai")
    winner = Column(String(100), nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    arguments = relationship("Argument", back_populates="debate", cascade="all, delete-orphan")

class Argument(Base):
    __tablename__ = "arguments"
    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, ForeignKey("debates.id"), nullable=False)
    round_number = Column(Integer, nullable=False)
    agent = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    stance = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    logical_coherence = Column(Float, nullable=True)
    factual_grounding = Column(Float, nullable=True)
    rhetorical_strength = Column(Float, nullable=True)
    fallacy_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    ml_score = Column(Float, nullable=True)
    raw_judge_response = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    debate = relationship("Debate", back_populates="arguments")
