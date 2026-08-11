from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.paper_model import Paper


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)

    # OpenAlex's unique identifier for this topic.
    openalex_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Many-to-many relationship with papers through paper_topic.
    papers: Mapped[list["Paper"]] = relationship(
        secondary="paper_topic",
        back_populates="topics"
    )