def reconstruct_abstract(inverted_index: dict | None) -> str | None:
    """
    Convert OpenAlex's abstract inverted index into normal readable text.

    OpenAlex stores abstracts like:
    {
        "Machine": [0],
        "learning": [1],
        "is": [2],
        "useful": [3]
    }

    We convert that structure into:
    "Machine learning is useful"
    """

    if not inverted_index:
        return None

    # Create a list large enough to hold every word at its
    # position in the original abstract.
    words = []

    for word, positions in inverted_index.items():
        for position in positions:
            words.append((position, word))

    # Sort words by their original position.
    words.sort(key=lambda item: item[0])

    return " ".join(word for _, word in words)


def transform_paper(raw_paper: dict) -> dict:
    """
    Extract the fields we need from one raw OpenAlex paper.

    Returns a simple dictionary containing:
    - paper information
    - authors
    - OpenAlex topics
    """

    abstract = reconstruct_abstract(
        raw_paper.get("abstract_inverted_index")
    )

    authors = []

    for authorship in raw_paper.get("authorships", []):
        author = authorship.get("author")

        if not author:
            continue

        authors.append(
            {
                "openalex_id": author.get("id"),
                "name": author.get("display_name"),
            }
        )

    topics = []

    for topic in raw_paper.get("topics", []):
        topics.append(
            {
                "openalex_id": topic.get("id"),
                "name": topic.get("display_name"),
            }
        )

    return {
        "paper": {
            "openalex_id": raw_paper.get("id"),
            "title": raw_paper.get("title"),
            "abstract": abstract,
            "year": raw_paper.get("publication_year"),
        },
        "authors": authors,
        "topics": topics,
    }