from datetime import datetime
from pydantic import BaseModel, ConfigDict, constr

class AnswerBase(BaseModel):
    pass

class AnswerCreate(AnswerBase):
    user_id: constr(min_length=1)
    text: constr(min_length=1)

class AnswerRead(AnswerBase):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnswerInQuestion(AnswerBase):
    id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)