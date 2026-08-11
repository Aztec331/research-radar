import sys
from pathlib import Path

# Add fastapi-server/ to Python's import path so we can import app/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.paper_model import Paper
from app.models.author_model import Author
from app.models.topic_model import Topic
from app.models.association_models import PaperAuthor, PaperTopic


def main():
    """Verify that all database models can be imported successfully."""

    print("Paper model:", Paper.__tablename__)
    print("Author model:", Author.__tablename__)
    print("Topic model:", Topic.__tablename__)
    print("PaperAuthor model:", PaperAuthor.__tablename__)
    print("PaperTopic model:", PaperTopic.__tablename__)

    print("\nModel imports successful!")


if __name__ == "__main__":
    main()