from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine


app = FastAPI()


@app.get("/")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"message": "Database connected!"}