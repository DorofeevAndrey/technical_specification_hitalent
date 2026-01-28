from sqlalchemy import Column, DateTime, Integer, Text, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )