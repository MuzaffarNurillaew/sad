"""Deterministic, non-AI checks for the report sections — the "run-tests"
step before anything goes to the reviewer/auditor subagents. Checks only
hard, countable constraints from the brief (word limits, diagram presence);
it will NOT catch content quality, correctness, or rubric nuance — that's
what the consistency-checker and rigorous-assessor subagents are for.

Usage: .venv/bin/python scripts/check_section.py [section-file ...]
       (no args = check every section file that exists)

Exit code 0 if every check in every checked file passes, 1 otherwise.
"""
import re
import sys
from pathlib import Path

DIAGRAM_RE = re.compile(r"```plantuml\n.*?\n```", re.DOTALL)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
PLACEHOLDER_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING_RE = re.compile(r"^#+\s+.*$", re.MULTILINE)

SECTIONS = [
    "0-business-case.md",
    "1-requirements-gathering-process.md",
    "2-use-case-diagram.md",
    "3-use-cases.md",
    "4-data-flow-diagram.md",
    "5-activity-diagram.md",
    "6-sequence-diagram.md",
    "7-requirements-catalogue.md",
]

DIAGRAM_SECTIONS = {
    "2-use-case-diagram.md",
    "4-data-flow-diagram.md",
    "5-activity-diagram.md",
    "6-sequence-diagram.md",
}


def strip_comments(text: str) -> str:
    return PLACEHOLDER_COMMENT_RE.sub("", text)


def strip_headings_and_comments(text: str) -> str:
    return HEADING_RE.sub("", strip_comments(text))


def body_word_count(text: str) -> int:
    body = strip_headings_and_comments(text)
    body = DIAGRAM_RE.sub(" ", body)
    return len(body.split())


def has_diagram(text: str) -> bool:
    return bool(DIAGRAM_RE.search(text) or IMAGE_RE.search(text))


def is_started(text: str) -> bool:
    return bool(strip_headings_and_comments(text).strip()) or has_diagram(text)


def check_file(path: Path) -> list[tuple[bool, str]]:
    name = path.name
    text = path.read_text(encoding="utf-8")
    results = []

    if not is_started(text):
        results.append((None, "not started yet (only the placeholder comment) - skipping further checks"))
        return results

    if name == "0-business-case.md":
        count = body_word_count(text)
        results.append((count <= 500, f"word count {count} (limit 500)"))

    if name in DIAGRAM_SECTIONS:
        results.append((has_diagram(text), "contains at least one diagram (```plantuml block or image)"))

    if name == "7-requirements-catalogue.md":
        row_count = len(re.findall(r"^\|", strip_comments(text), re.MULTILINE))
        results.append((row_count >= 3, f"requirements catalogue has a markdown table ({row_count} table lines found)"))

    if not results:
        results.append((None, "no automated checks defined for this section - rely on reviewer/auditor"))

    return results


def main():
    args = sys.argv[1:]
    targets = [Path(a) for a in args] if args else [Path(s) for s in SECTIONS if Path(s).exists()]

    if not targets:
        print("No section files found to check.")
        sys.exit(0)

    any_failed = False
    for path in targets:
        print(f"\n{path.name}")
        for passed, message in check_file(path):
            if passed is None:
                print(f"  .  {message}")
            elif passed:
                print(f"  OK {message}")
            else:
                print(f"  FAIL {message}")
                any_failed = True

    print()
    if any_failed:
        print("Some checks FAILED - fix before sending to reviewer/auditor.")
        sys.exit(1)
    print("All deterministic checks passed.")


if __name__ == "__main__":
    main()
