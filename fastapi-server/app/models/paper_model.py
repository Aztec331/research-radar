from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.author_model import Author
    from app.models.topic_model import Topic


class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(primary_key=True)

    # OpenAlex's unique identifier for this research paper.
    openalex_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str | None] = mapped_column(Text, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Many-to-many relationship with authors through paper_author.
    authors: Mapped[list["Author"]] = relationship(
        secondary="paper_author",
        back_populates="papers"
    )

    # Many-to-many relationship with topics through paper_topic.
    topics: Mapped[list["Topic"]] = relationship(
        secondary="paper_topic",
        back_populates="papers"
    )