from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PaperAuthor(Base):
    __tablename__ = "paper_author"

    paper_id: Mapped[int] = mapped_column(
        ForeignKey("papers.id"),
        primary_key=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        primary_key=True
    )


class PaperTopic(Base):
    __tablename__ = "paper_topic"

    paper_id: Mapped[int] = mapped_column(
        ForeignKey("papers.id"),
        primary_key=True
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        primary_key=True
    )