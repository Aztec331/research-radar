from types import SimpleNamespace

from app.services.similarity_service import get_similar_papers


target = SimpleNamespace(
    id=1,
    title="Large Language Models for Natural Language Processing",
    abstract=(
        "This paper studies large language models and their "
        "applications in natural language processing."
    ),
)

papers = [
    target,

    SimpleNamespace(
        id=2,
        title="Transformer Models for Natural Language Processing",
        abstract=(
            "We study transformer models and their applications "
            "in natural language processing and language understanding."
        ),
    ),

    SimpleNamespace(
        id=3,
        title="Deep Learning for Computer Vision",
        abstract=(
            "This paper explores convolutional neural networks "
            "for image classification and visual recognition."
        ),
    ),

    SimpleNamespace(
        id=4,
        title="Language Models and Text Generation",
        abstract=(
            "We investigate language models for text generation, "
            "language understanding, and natural language tasks."
        ),
    ),

    SimpleNamespace(
        id=5,
        title="Database Query Optimization",
        abstract=(
            "This paper presents techniques for optimizing "
            "database queries and improving database performance."
        ),
    ),
]


similar_papers = get_similar_papers(
    target_paper=target,
    papers=papers,
    limit=3,
)


print("\nTarget paper:")
print(target.title)

print("\nSimilar papers:")

for paper in similar_papers:
    print(f"- {paper.id}: {paper.title}")