"""Heuristic AI-generated-text detector for the report section files,
combining two signals real AI-detection tools are built on:

1. Burstiness - human writing varies sentence length a lot; LLM output tends
   to be more uniform. Measured as the coefficient of variation (stdev/mean)
   of sentence word-counts. Low CV -> more uniform -> more "AI-like".
2. Stock phrases - common LLM transition/filler clichés ("it is important to
   note that", "delve into", etc.), matched as plain substrings.

Caveat that applies regardless of technique: this is the same category of
method commercial AI detectors (GPTZero, Turnitin's AI score, etc.) use, and
those tools still have high false-positive/false-negative rates - notably
against non-native English writers, who structure sentences more uniformly
for the same reason LLMs do: both learned formal English from similar
sources. A flag here is "this reads statistically unusual, go look closer
and rewrite for specificity" - not a verdict on who wrote it, and a clean
run is not proof of human authorship either.

Usage: .venv/bin/python scripts/detect_ai_text.py [section-file ...]
       (no args = check every section file that exists)

Exit code 0 if nothing is flagged in any checked file, 1 otherwise.
"""
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_section import SECTIONS, is_started, strip_comments  # noqa: E402

PHRASES = [
    "it is important to note that",
    "it's important to note that",
    "it is worth noting that",
    "it is crucial to",
    "it's crucial to",
    "cannot be overstated",
    "in today's fast-paced",
    "in today's digital age",
    "plays a crucial role",
    "plays a vital role",
    "plays a pivotal role",
    "delve into",
    "delving into",
    "navigate the complexities",
    "navigating the complexities",
    "underscores the importance",
    "this underscores",
    "a testament to",
    "stands as a testament",
    "ever-evolving landscape",
    "in the ever-evolving",
    "paradigm shift",
    "unlock the potential",
    "unleash the potential",
    "game-changer",
    "game changer",
    "holistic approach",
    "seamless integration",
    "seamlessly integrate",
    "robust and scalable",
    "myriad of",
    "plethora of",
    "tapestry of",
    "embark on a journey",
    "foster a culture",
    "fosters collaboration",
    "in conclusion,",
    "to sum up,",
    "in summary,",
    "boasts a",
    "leverage the power of",
    "leveraging the power of",
    "elevate the",
]
PHRASE_RE = re.compile("|".join(re.escape(p) for p in PHRASES), re.IGNORECASE)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
MIN_SENTENCES_FOR_BURSTINESS = 5
BURSTINESS_CV_THRESHOLD = 0.45  # below this, sentence lengths read as unusually uniform


def find_phrase_matches(body: str) -> list[tuple[int, str]]:
    matches = []
    for lineno, line in enumerate(body.splitlines(), start=1):
        for m in PHRASE_RE.finditer(line):
            matches.append((lineno, m.group(0)))
    return matches


def burstiness(body: str) -> tuple[float | None, int]:
    flat = " ".join(body.split())
    sentences = [s for s in SENTENCE_SPLIT_RE.split(flat) if s.strip()]
    lengths = [len(s.split()) for s in sentences if s.split()]
    if len(lengths) < MIN_SENTENCES_FOR_BURSTINESS:
        return None, len(lengths)
    mean = statistics.mean(lengths)
    if mean == 0:
        return None, len(lengths)
    cv = statistics.pstdev(lengths) / mean
    return cv, len(lengths)


def check_file(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = []

    if not is_started(text):
        return False, ["not started yet - skipping"]

    body = strip_comments(text)
    phrase_matches = find_phrase_matches(body)
    cv, n_sentences = burstiness(body)

    flagged = False

    if phrase_matches:
        flagged = True
        for lineno, phrase in phrase_matches:
            lines.append(f'FLAG (stock phrase) line {lineno}: "{phrase}"')
    else:
        lines.append("OK no stock phrases matched")

    if cv is None:
        lines.append(f"-- burstiness: skipped (only {n_sentences} sentences, need >= {MIN_SENTENCES_FOR_BURSTINESS})")
    elif cv < BURSTINESS_CV_THRESHOLD:
        flagged = True
        lines.append(
            f"FLAG (low burstiness) sentence-length CV = {cv:.2f} across {n_sentences} sentences "
            f"(< {BURSTINESS_CV_THRESHOLD} threshold - unusually uniform sentence lengths)"
        )
    else:
        lines.append(f"OK burstiness normal (CV = {cv:.2f} across {n_sentences} sentences)")

    return flagged, lines


def main():
    args = sys.argv[1:]
    targets = [Path(a) for a in args] if args else [Path(s) for s in SECTIONS if Path(s).exists()]

    if not targets:
        print("No section files found to check.")
        sys.exit(0)

    print(
        "Heuristic AI-text detector (burstiness + stock-phrase signal).\n"
        "Same category of method real AI detectors use - and those still have\n"
        "high error rates, especially against non-native English writers.\n"
        "A flag is a cue to look closer and rewrite for specificity, not a\n"
        "verdict. See scripts/detect_ai_text.py's module docstring.\n"
    )

    any_flagged = False
    for path in targets:
        flagged, lines = check_file(path)
        print(path.name)
        for line in lines:
            prefix = "  " if not line.startswith(("FLAG", "OK", "--")) else "  "
            print(f"{prefix}{line}")
        print()
        any_flagged = any_flagged or flagged

    if any_flagged:
        print("Some signals flagged - review and rewrite flagged passages to be more specific.")
        sys.exit(1)
    print("No AI-writing signals flagged in any checked file.")


if __name__ == "__main__":
    main()
