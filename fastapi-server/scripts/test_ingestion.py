import sys
from pathlib import Path
import json

# Add fastapi-server/ to Python's import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal
from app.models import association_models
from app.services.openalex_transform_service import transform_paper
from app.services.ingestion_service import ingest_paper


def main():
    """
    Test ingestion of one real OpenAlex paper into PostgreSQL.
    """

    # Load our saved OpenAlex response.
    json_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "openalex_sample.json"
    )

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Take the first paper from OpenAlex's results.
    raw_paper = data["results"][0]

    # Transform the raw OpenAlex paper into our application format.
    transformed = transform_paper(raw_paper)

    # Open a database session.
    db = SessionLocal()

    try:
        # Ingest the transformed paper.
        paper = ingest_paper(db, transformed)

        # If the paper had no OpenAlex ID, ingestion skips it.
        if paper is None:
            print("Paper skipped: no OpenAlex ID.")
            return

        # Save everything to PostgreSQL.
        db.commit()

        print("Paper ingested successfully!")
        print("Database ID:", paper.id)
        print("OpenAlex ID:", paper.openalex_id)
        print("Title:", paper.title)
        print("Authors:", [author.name for author in paper.authors])
        print("Topics:", [topic.name for topic in paper.topics])

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()