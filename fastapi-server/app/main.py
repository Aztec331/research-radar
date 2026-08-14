from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine
from app.models import association_models
from app.routes.paper_routes import router as paper_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(paper_router)


@app.get("/")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"message": "Database connected!"}