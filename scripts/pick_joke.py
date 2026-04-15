#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils.joke_skill import format_final_joke, load_jokes, select_joke


def main() -> None:
    parser = argparse.ArgumentParser(description="Pick a bilingual programmer joke for a task context.")
    parser.add_argument("--query", default="", help="Task summary or context keywords")
    parser.add_argument("--csv", default="jokes_with_id.csv", help="Path to the joke CSV file")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.is_absolute():
        csv_path = REPO_ROOT / csv_path

    jokes = load_jokes(csv_path)
    joke = select_joke(jokes, args.query)

    if args.format == "text":
        print(format_final_joke(joke))
        return

    print(
        json.dumps(
            {
                "id": joke.id,
                "english": joke.english,
                "chinese": joke.chinese,
                "author": joke.author,
                "description": joke.description,
                "formatted": format_final_joke(joke),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
