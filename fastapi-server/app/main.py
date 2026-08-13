from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.models import association_models
from app.routes.paper_routes import router as paper_router


app = FastAPI()

app.include_router(paper_router)


@app.get("/")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"message": "Database connected!"}