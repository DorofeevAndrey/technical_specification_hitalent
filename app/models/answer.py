from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(64), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    question = relationship("Question", back_populates="answers")