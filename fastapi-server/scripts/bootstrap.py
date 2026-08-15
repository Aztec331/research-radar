import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import subprocess

from sqlalchemy import func

from app.database import SessionLocal
from app.models.paper_model import Paper
from app.models.author_model import Author
from app.models.topic_model import Topic
from app.models.association_models import PaperAuthor, PaperTopic


def database_has_papers() -> bool:
    '''
    Check whether the database already contains papers.
    '''
    db = SessionLocal()

    try:
        count = db.query(func.count(Paper.id)).scalar()
        return count > 0
    finally:
        db.close()


def main():
    '''
    Initialize the database with papers if it is empty.
    '''
    if database_has_papers():
        print("Database already contains papers. Skipping ingestion.")
        return

    print("Database is empty. Running paper ingestion...")

    result = subprocess.run(
        [sys.executable, "scripts/ingest.py"],
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(result.returncode)

    print("Paper ingestion completed.")


if __name__ == "__main__":
    main()