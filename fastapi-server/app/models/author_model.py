from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.association_models import PaperAuthor

if TYPE_CHECKING:
    from app.models.paper_model import Paper


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)

    # OpenAlex's unique identifier for this author.
    openalex_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Many-to-many relationship with papers through paper_author.
    papers: Mapped[list["Paper"]] = relationship(
        secondary="paper_author",
        back_populates="authors"
    )