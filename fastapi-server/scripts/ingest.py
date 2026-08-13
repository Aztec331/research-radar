import sys
from pathlib import Path

# Add fastapi-server/ to Python's import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import association_models

from app.services.openalex_service import fetch_papers
from app.services.openalex_transform_service import transform_paper
from app.services.ingestion_service import (
    ingest_paper,
    get_or_create_topic,
)


# Each batch contains 200 papers, satisfying the assignment's
# requirement of 300–500 papers across two research topics.
BATCHES = [
    {
        "search_topic": "natural language processing",
        "topic_id": "custom:nlp",
        "topic_name": "NLP",
    },
    {
        "search_topic": "computer vision",
        "topic_id": "custom:computer-vision",
        "topic_name": "Computer Vision",
    },
]

def ingest_batch(
    db: Session,
    search_topic: str,
    topic_id: str,
    topic_name: str,
) -> int:
    """
    Fetch, transform, and ingest one batch of papers for a research topic.
    Returns the number of papers successfully ingested.
    """

    papers = fetch_papers(search_topic, 200)

    count = 0

    for raw_paper in papers:
        #transform each raw paper into a structured format suitable for ingestion
        transformed = transform_paper(raw_paper)

        #ingest the transformed paper into the database
        paper = ingest_paper(db, transformed)

        #if openalex_id is null, skip the paper and continue to the next one in the loop
        if paper is None:
            continue

        topic = get_or_create_topic(
            db=db,
            openalex_id=topic_id,
            name=topic_name,
        )

        if topic not in paper.topics:
            paper.topics.append(topic)

        count += 1

    return count

def main():
    """
    Run ingestion for all configured research topic batches.
    """

    db = SessionLocal()

    try:
        for batch in BATCHES:
            count = ingest_batch(
                db=db,
                search_topic=batch["search_topic"],
                topic_id=batch["topic_id"],
                topic_name=batch["topic_name"],
            )

            db.commit()

            print(
                f"{batch['topic_name']}: "
                f"{count} papers successfully ingested."
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()