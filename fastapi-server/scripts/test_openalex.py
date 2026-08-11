import sys
from pathlib import Path
import json

# Add fastapi-server/ to Python's import path so we can import app/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.normalization_service import normalize_paper


def main():
    """Test paper normalization using a real saved OpenAlex paper."""

    # Load our saved OpenAlex response.
    json_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "openalex_sample.json"
    )

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # OpenAlex puts papers inside the results list.
    papers = data["results"]

    # Take the first real paper.
    raw_paper = papers[0]

    # Normalize the complete OpenAlex paper.
    normalized = normalize_paper(raw_paper)

    print("NORMALIZED PAPER:")
    print(json.dumps(normalized, indent=2))


if __name__ == "__main__":
    main()