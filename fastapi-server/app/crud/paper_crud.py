from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.paper_model import Paper
from app.models.author_model import Author
from app.models.topic_model import Topic


def get_papers(
    db: Session,
    search: str | None = None,
    topic: str | None = None,
    year: int | None = None,
    author: str | None = None,
    page: int = 1,
    limit: int = 4,
) -> tuple[list[Paper], int]:
    """
    Fetch papers from the database with optional search, filters,
    and pagination. Returns the matching papers and total count.
    """

    query = db.query(Paper)

    # Search inside the paper title or abstract.
    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            or_(
                Paper.title.ilike(search_pattern),
                Paper.abstract.ilike(search_pattern),
            )
        )

    # Filter papers by topic name.
    if topic:
        query = query.join(Paper.topics).filter(
            Topic.name.ilike(f"%{topic}%")
        )

    # Filter papers by publication year.
    if year:
        query = query.filter(Paper.year == year)

    # Filter papers by author name.
    if author:
        query = query.join(Paper.authors).filter(
            Author.name.ilike(f"%{author}%")
        )

    # Count matching papers before pagination is applied.
    total = query.distinct().count()

    # Calculate how many records to skip.
    offset = (page - 1) * limit

    # Fetch only the requested page.
    papers = (
        query
        .distinct()
        .offset(offset)
        .limit(limit)
        .all()
    )

    return papers, total

def get_paper_by_id(
    db: Session,
    paper_id: int,
) -> Paper | None:
    """
    Fetch a single paper by its database ID.
    """

    return (
        db.query(Paper)
        .filter(Paper.id == paper_id)
        .first()
    )