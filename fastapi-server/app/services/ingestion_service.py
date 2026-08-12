from sqlalchemy.orm import Session

from app.models.paper_model import Paper
from app.models.author_model import Author
from app.models.topic_model import Topic

def get_or_create_paper(
    db: Session,
    openalex_id: str,
    title: str,
    abstract: str | None,
    year: int | None,
) -> Paper:
    """
    Find an existing paper by its OpenAlex ID or create it if it does not exist.
    This keeps the ingestion process idempotent and prevents duplicate papers.
    """

    paper = db.query(Paper).filter(
        Paper.openalex_id == openalex_id
    ).first()

    if paper:
        return paper

    paper = Paper(
        openalex_id=openalex_id,
        title=title,
        abstract=abstract,
        year=year,
    )

    db.add(paper)
    db.flush()

    return paper

def get_or_create_author(
    db: Session,
    openalex_id: str,
    name: str,
) -> Author:
    """
    Find an existing author by their OpenAlex ID or create them if they do not exist.
    This prevents the same author from being stored multiple times.
    """

    author = db.query(Author).filter(
        Author.openalex_id == openalex_id
    ).first()

    if author:
        return author

    author = Author(
        openalex_id=openalex_id,
        name=name,
    )

    db.add(author)
    db.flush()

    return author

def get_or_create_topic(
    db: Session,
    openalex_id: str,
    name: str,
) -> Topic:
    """
    Find an existing topic by its unique ID or create it if it does not exist.
    This works for both OpenAlex topics and our synthetic NLP/Computer Vision topics.
    """

    topic = db.query(Topic).filter(
        Topic.openalex_id == openalex_id
    ).first()

    if topic:
        return topic

    topic = Topic(
        openalex_id=openalex_id,
        name=name,
    )

    db.add(topic)
    db.flush()

    return topic

def ingest_paper(
    db: Session,
    paper_data: dict,
) -> Paper:

    paper_info = paper_data["paper"]

    # 1. Get or create the paper
    paper = get_or_create_paper(
        db=db,
        openalex_id=paper_info["openalex_id"],
        title=paper_info["title"],
        abstract=paper_info["abstract"],
        year=paper_info["year"],
    )

    # 2. Get or create and attach authors
    for author_data in paper_data["authors"]:
        author = get_or_create_author(
            db=db,
            openalex_id=author_data["openalex_id"],
            name=author_data["name"],
        )

        if author not in paper.authors:
            paper.authors.append(author)

    # 3. Get or create and attach OpenAlex topics
    for topic_data in paper_data["topics"]:
        topic = get_or_create_topic(
            db=db,
            openalex_id=topic_data["openalex_id"],
            name=topic_data["name"],
        )

        if topic not in paper.topics:
            paper.topics.append(topic)

    return paper
