from pydantic import BaseModel, ConfigDict, constr
from datetime import datetime

from app.schemas.answer import AnswerInQuestion

class QuestionBase(BaseModel):
    text: constr(min_length=1)

class QuestionCreate(QuestionBase):
    
    pass

class QuestionRead(QuestionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class QuestionWithAnswers(QuestionRead):
    answers: list[AnswerInQuestion] = []