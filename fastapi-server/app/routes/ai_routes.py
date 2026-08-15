from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.paper_crud import get_papers, get_paper_by_id
from app.services.similarity_service import get_similar_papers
from app.schemas.paper_schema import PaperResponse


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
)


@router.get("/papers/{paper_id}/similar", response_model=list[PaperResponse])
def get_similar_papers_route(
    paper_id: int,
    db: Session = Depends(get_db),
):
    # Get the target paper
    target_paper = get_paper_by_id(
        db=db,
        paper_id=paper_id,
    )

    if target_paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found",
        )

    # Get all papers from the corpus
    all_papers, _ = get_papers(
        db=db,
        limit=10000,
    )

    # Find the 5 most similar papers
    similar_papers = get_similar_papers(
        target_paper,
        all_papers,
        limit=5,
    )

    return similar_papers