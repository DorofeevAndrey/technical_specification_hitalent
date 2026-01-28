from fastapi import FastAPI
from app.api.v1.routes.questions import questions_router
from app.api.v1.routes.answers import router, answers_router

app = FastAPI()

app.include_router(router)
app.include_router(answers_router)
app.include_router(questions_router)