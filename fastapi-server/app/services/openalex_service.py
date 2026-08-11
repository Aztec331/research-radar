import requests
from datetime import date, timedelta


OPENALEX_URL = "https://api.openalex.org/works"

# We want a recent research corpus, not old papers.
RECENT_YEARS = 2

# The assignment asks for 300–500 papers.
TARGET_PAPERS = 400

# OpenAlex allows up to 100 results per page.
PER_PAGE = 100


def fetch_papers(topic: str, target_count: int = TARGET_PAPERS) -> list[dict]:
    """
    Fetch recent research papers from OpenAlex for a given topic.

    The function handles pagination and keeps requesting pages until
    the requested number of papers has been collected or OpenAlex
    has no more matching results.
    """

    papers = []
    page = 1

    # Calculate the date range for our "recent papers" corpus.
    today = date.today()
    from_date = today - timedelta(days=365 * RECENT_YEARS)

    while len(papers) < target_count:

        remaining = target_count - len(papers)

        # Never request more than OpenAlex's maximum page size
        # or more papers than we still need.
        per_page = min(PER_PAGE, remaining)

        params = {
            "search": topic,
            "filter": (
                f"from_publication_date:{from_date.isoformat()},"
                f"to_publication_date:{today.isoformat()},"
                "type:article"
            ),
            "sort": "publication_date:desc",
            "page": page,
            "per-page": per_page,
        }

        response = requests.get(
            OPENALEX_URL,
            params=params,
            timeout=30,
        )

        # Raise an exception if OpenAlex returns an HTTP error.
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        # Stop if OpenAlex has no more papers to return.
        if not results:
            break

        papers.extend(results)

        # Move to the next OpenAlex page.
        page += 1

    return papers[:target_count]