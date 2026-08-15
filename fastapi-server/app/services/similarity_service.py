from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.paper_model import Paper


def get_similar_papers(
    target_paper: Paper,
    papers: list[Paper],
    limit: int = 5,
) -> list[Paper]:
    """
    Return papers most similar to the target paper using
    TF-IDF and cosine similarity.
    """

    # The target paper itself should not appear in the results.
    candidate_papers = [
        paper for paper in papers
        if paper.id != target_paper.id
    ]

    if not candidate_papers:
        return []

    # Combine title and abstract because both contain useful
    # information about the paper's content.
    documents = [
        f"{paper.title} {paper.abstract or ''}"
        for paper in candidate_papers
    ]

    target_document = (
        f"{target_paper.title} {target_paper.abstract or ''}"
    )

    # Create TF-IDF vectors for the target paper and candidates.
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [target_document] + documents
    )

    # Compare the target paper against every candidate paper.
    similarities = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    # Pair each paper with its similarity score.
    scored_papers = list(
        zip(candidate_papers, similarities)
    )

    # Highest similarity first.
    scored_papers.sort(
        key=lambda item: item[1],
        reverse=True
    )

    # Return only the requested number of papers.
    return [
        paper
        for paper, score in scored_papers[:limit]
    ]