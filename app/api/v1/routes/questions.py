from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionRead, QuestionWithAnswers

questions_router = APIRouter(prefix="/questions", tags=["questions"])

@questions_router.post("/", response_model=QuestionRead, status_code=201)
def create_question(data: QuestionCreate, db: Session = Depends(get_db)):
    question = Question(text=data.text)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@questions_router.get("/", response_model=list[QuestionRead])
def list_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()

@questions_router.get("/{question_id}", response_model=QuestionWithAnswers)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@questions_router.delete("/{question_id}", status_code=204)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()
    return Response(status_code=204)