from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.answer import Answer
from app.models.question import Question
from app.schemas.answer import AnswerCreate, AnswerRead

router = APIRouter(tags=["answers"])
answers_router = APIRouter(prefix="/answers", tags=["answers"])


@router.post("/questions/{question_id}/answers/", response_model=AnswerRead, status_code=201)
def create_answer(question_id: int, data: AnswerCreate, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    obj = Answer(question_id=question_id, user_id=data.user_id, text=data.text) 
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@answers_router.get("/{answer_id}", response_model=AnswerRead)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Answer).filter(Answer.id == answer_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return obj


@answers_router.delete("/{answer_id}", status_code=204)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    obj = db.query(Answer).filter(Answer.id == answer_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(obj)
    db.commit()
    return Response(status_code=204)