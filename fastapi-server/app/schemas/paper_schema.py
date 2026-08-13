from pydantic import BaseModel


class AuthorResponse(BaseModel):
    """Response schema for an author."""

    id: int
    openalex_id: str
    name: str

    model_config = {
        "from_attributes": True
    }


class TopicResponse(BaseModel):
    """Response schema for a topic."""

    id: int
    openalex_id: str
    name: str

    model_config = {
        "from_attributes": True
    }


class PaperResponse(BaseModel):
    """Response schema for a research paper and its relationships."""

    id: int
    openalex_id: str
    title: str
    abstract: str | None
    year: int | None
    authors: list[AuthorResponse]
    topics: list[TopicResponse]

    model_config = {
        "from_attributes": True
    }

class PaperListResponse(BaseModel):
    items: list[PaperResponse]
    total: int
    page: int
    limit: int


