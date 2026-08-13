from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.paper_crud import get_papers, get_paper_by_id
from app.schemas.paper_schema import PaperListResponse, PaperResponse


router = APIRouter(
    prefix="/api/papers",
    tags=["Papers"],
)


@router.get("/", response_model=PaperListResponse)
def list_papers(
    search: str | None = Query(default=None),
    topic: str | None = Query(default=None),
    year: int | None = Query(default=None),
    author: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=6, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return paginated papers with optional search and filters.
    """

    papers, total = get_papers(
        db=db,
        search=search,
        topic=topic,
        year=year,
        author=author,
        page=page,
        limit=limit,
    )

    return {
    "items": papers,
    "total": total,
    "page": page,
    "limit": limit,
    }


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a single paper by its database ID.
    """

    paper = get_paper_by_id(
        db=db,
        paper_id=paper_id,
    )

    if paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found",
        )

    return paper