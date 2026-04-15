from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class JokeRecord:
    id: str
    english: str
    chinese: str
    author: str
    description: str


TOPIC_KEYWORDS: Dict[str, List[str]] = {
    "Debugging": [
        "debug",
        "bug",
        "fix",
        "error",
        "trace",
        "stack",
        "crash",
        "incident",
        "troubleshoot",
    ],
    "Code Quality": [
        "code",
        "readability",
        "maintain",
        "refactor",
        "clean",
        "review",
        "implementation",
        "explain",
        "documentation",
        "comment",
    ],
    "Planning": [
        "plan",
        "design",
        "architecture",
        "roadmap",
        "spec",
        "problem",
        "priorit",
        "strategy",
        "product",
    ],
    "Optimization": [
        "optimiz",
        "performance",
        "latency",
        "speed",
        "fast",
        "cache",
        "efficient",
        "efficiency",
    ],
    "Shipping": [
        "ship",
        "release",
        "launch",
        "deploy",
        "deliver",
        "done",
        "complete",
        "production",
    ],
    "AI & Future": [
        "ai",
        "llm",
        "model",
        "machine learning",
        "artificial intelligence",
        "future",
        "quantum",
        "blockchain",
        "cloud",
    ],
}

CURATED_TOPIC_IDS: Dict[str, List[str]] = {
    "Debugging": ["22", "68", "122", "133", "150", "38", "102"],
    "Code Quality": ["21", "29", "35", "42", "72", "112", "137", "18"],
    "Planning": ["30", "18", "19", "34", "107", "115", "167"],
    "Optimization": ["16", "39", "66", "76", "83", "96", "178"],
    "Shipping": ["6", "7", "21", "25", "66", "100", "145"],
    "AI & Future": ["20", "127", "136", "141", "142", "146", "163"],
}

DEFAULT_CLASSIC_IDS = ["21", "29", "16", "30", "22", "42"]
STANDALONE_SKILL_DIRNAME = "learn-english-by-programmer-jokes"
SENSITIVE_CONTEXT_KEYWORDS = {
    "medical",
    "legal",
    "death",
    "suicide",
    "violence",
    "abuse",
    "self-harm",
    "crisis",
    "funeral",
    "grief",
}


def load_jokes(csv_path: str | Path) -> List[JokeRecord]:
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            JokeRecord(
                id=(row.get("ID") or "").strip(),
                english=(row.get("English") or "").strip(),
                chinese=(row.get("Chinese") or "").strip(),
                author=(row.get("Author") or "").strip(),
                description=(row.get("Description") or "").strip(),
            )
            for row in reader
            if (row.get("ID") or "").strip()
        ]


def _joke_text(joke: JokeRecord) -> str:
    return " ".join([joke.english, joke.chinese, joke.description, joke.author]).lower()


def _index_by_id(jokes: Iterable[JokeRecord]) -> Dict[str, JokeRecord]:
    return {joke.id: joke for joke in jokes}


def classify_topics(jokes: List[JokeRecord]) -> Dict[str, List[JokeRecord]]:
    by_id = _index_by_id(jokes)
    classified: Dict[str, List[JokeRecord]] = {}
    for topic, curated_ids in CURATED_TOPIC_IDS.items():
        seen = set()
        bucket: List[JokeRecord] = []
        for joke_id in curated_ids:
            joke = by_id.get(joke_id)
            if joke:
                bucket.append(joke)
                seen.add(joke.id)

        topic_terms = [kw.lower() for kw in TOPIC_KEYWORDS.get(topic, [])]
        for joke in jokes:
            if joke.id in seen:
                continue
            text = _joke_text(joke)
            if any(term in text for term in topic_terms):
                bucket.append(joke)
                seen.add(joke.id)
        classified[topic] = bucket
    return classified


def infer_topic(context: str) -> str | None:
    lowered = (context or "").lower()
    scores: Dict[str, int] = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in lowered:
                score += 2 if " " in keyword else 1
        if score:
            scores[topic] = score
    if not scores:
        return None
    return max(scores, key=scores.get)


def is_sensitive_context(context: str) -> bool:
    lowered = (context or "").lower()
    return any(keyword in lowered for keyword in SENSITIVE_CONTEXT_KEYWORDS)


def select_joke(jokes: List[JokeRecord], context: str = "") -> JokeRecord:
    if not jokes:
        raise ValueError("No jokes available")

    topic = infer_topic(context)
    by_id = _index_by_id(jokes)
    if topic:
        for joke_id in CURATED_TOPIC_IDS.get(topic, []):
            joke = by_id.get(joke_id)
            if joke:
                return joke

        lowered = (context or "").lower()
        ranked = []
        for joke in jokes:
            text = _joke_text(joke)
            score = sum(1 for keyword in TOPIC_KEYWORDS.get(topic, []) if keyword in lowered and keyword in text)
            if score:
                ranked.append((score, joke))
        if ranked:
            ranked.sort(key=lambda item: (-item[0], int(item[1].id)))
            return ranked[0][1]

    for joke_id in DEFAULT_CLASSIC_IDS:
        joke = by_id.get(joke_id)
        if joke:
            return joke
    return jokes[0]


def format_final_joke(joke: JokeRecord) -> str:
    lines = [
        "技术段子 / Tech Joke",
        f"EN: {joke.english}",
        f"ZH: {joke.chinese}",
    ]
    if joke.author:
        lines.append(f"— {joke.author}")
    return "\n".join(lines)


def build_topic_reference(jokes: List[JokeRecord]) -> str:
    classified = classify_topics(jokes)
    lines = [
        "# Jokes by Topic",
        "",
        "This file is generated from `jokes_with_id.csv` and organized for quick Hermes skill lookup.",
        "When the agent needs a final bilingual joke, it should prefer the relevant section below instead of scanning the full CSV.",
        "",
    ]
    for topic, topic_jokes in classified.items():
        lines.append(f"## {topic}")
        lines.append("")
        for joke in topic_jokes[:12]:
            author = joke.author or "Unknown"
            lines.append(f"- {joke.id} | {joke.english} | {joke.chinese} | {author}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_selection_rules(jokes: List[JokeRecord]) -> str:
    classified = classify_topics(jokes)
    lines = [
        "# Joke Selection Rules",
        "",
        "Use these rules when the main task is already complete and you want to append one concise bilingual tech joke.",
        "",
        "## Global Rules",
        "",
        "- Only add one joke after the main answer is done.",
        "- Keep the joke short and avoid stealing focus from the real answer.",
        "- Skip the joke in sensitive, crisis, medical, legal, or grief-related contexts.",
        "- Prefer the relevant topic bucket below; if no topic matches, use a classic fallback.",
        "",
        "## Topic Routing",
        "",
    ]
    for topic, topic_jokes in classified.items():
        keywords = ", ".join(TOPIC_KEYWORDS.get(topic, []))
        lines.append(f"### {topic}")
        lines.append(f"Trigger hints: {keywords}")
        lines.append("Preferred quotes:")
        for joke in topic_jokes[:5]:
            lines.append(f"- {joke.id}: {joke.english} — {joke.author or 'Unknown'}")
        lines.append("")
    lines.append("## Classic Fallbacks")
    lines.append("")
    by_id = _index_by_id(jokes)
    for joke_id in DEFAULT_CLASSIC_IDS:
        joke = by_id.get(joke_id)
        if joke:
            lines.append(f"- {joke.id}: {joke.english} | {joke.chinese}")
    lines.append("")
    return "\n".join(lines)


def generate_skill_assets(csv_path: str | Path, references_dir: str | Path) -> None:
    jokes = load_jokes(csv_path)
    references_path = Path(references_dir)
    references_path.mkdir(parents=True, exist_ok=True)
    (references_path / "jokes-by-topic.md").write_text(build_topic_reference(jokes), encoding="utf-8")
    (references_path / "joke-selection-rules.md").write_text(build_selection_rules(jokes), encoding="utf-8")


def build_standalone_skill_readme() -> str:
    return (
        "# Standalone Hermes Skill Bundle\n\n"
        "This folder is a self-contained Hermes skill package for `learn-english-by-programmer-jokes`.\n\n"
        "## Local install\n\n"
        "Copy the whole `learn-english-by-programmer-jokes/` folder into your local Hermes skills directory:\n\n"
        "```bash\n"
        "cp -a learn-english-by-programmer-jokes ~/.hermes/skills/\n"
        "hermes skills list | grep -i learn-english-by-programmer-jokes\n"
        "```\n\n"
        "Then preload it with:\n\n"
        "```bash\n"
        "hermes chat -s learn-english-by-programmer-jokes -q 'Summarize what I just fixed'\n"
        "```\n\n"
        "## Publish\n\n"
        "This directory is also suitable as a standalone skill artifact for skill hubs such as ClawHub, because it already contains:\n\n"
        "- `SKILL.md`\n"
        "- generated `references/`\n"
        "- `templates/`\n"
        "- helper `scripts/`\n"
        "- minimal `utils/` runtime code\n"
        "- local `jokes_with_id.csv` data source\n"
    )


def generate_standalone_skill_bundle(repo_root: str | Path, output_root: str | Path) -> Path:
    repo_path = Path(repo_root)
    output_path = Path(output_root)
    bundle_path = output_path / STANDALONE_SKILL_DIRNAME

    if bundle_path.exists():
        shutil.rmtree(bundle_path)

    (bundle_path / "references").mkdir(parents=True, exist_ok=True)
    (bundle_path / "templates").mkdir(parents=True, exist_ok=True)
    (bundle_path / "scripts").mkdir(parents=True, exist_ok=True)
    (bundle_path / "utils").mkdir(parents=True, exist_ok=True)

    shutil.copy2(repo_path / "SKILL.md", bundle_path / "SKILL.md")
    shutil.copy2(repo_path / "jokes_with_id.csv", bundle_path / "jokes_with_id.csv")
    shutil.copy2(repo_path / "scripts" / "pick_joke.py", bundle_path / "scripts" / "pick_joke.py")
    shutil.copy2(repo_path / "templates" / "final-joke-template.txt", bundle_path / "templates" / "final-joke-template.txt")
    shutil.copy2(repo_path / "utils" / "joke_skill.py", bundle_path / "utils" / "joke_skill.py")

    generate_skill_assets(bundle_path / "jokes_with_id.csv", bundle_path / "references")
    (bundle_path / "README.md").write_text(build_standalone_skill_readme(), encoding="utf-8")
    (bundle_path / ".gitignore").write_text("**/__pycache__/\n*.pyc\n.pytest_cache/\n", encoding="utf-8")
    return bundle_path
