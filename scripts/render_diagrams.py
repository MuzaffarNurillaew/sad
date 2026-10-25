"""Concatenates the numbered report section files in order, rendering every
```plantuml fenced code block to a PNG (via PlantUML, cached by content hash
so unchanged diagrams never re-render) and replacing the fence with an image
reference. Writes the result to a single combined markdown file that pandoc
then converts to docx.

Usage: .venv/bin/python scripts/render_diagrams.py --out build/combined.md
       --diagrams-dir build/diagrams --plantuml-jar tools/plantuml.jar
       <section files in order...>
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

FENCE_RE = re.compile(r"```plantuml\n(.*?)\n```\n?", re.DOTALL)


def with_smetana_layout(source: str) -> str:
    """Force PlantUML's pure-Java Smetana layout engine instead of Graphviz's
    `dot`, which isn't installed and never will be (no-sudo pipeline). Only
    dot-based diagrams (use case, class, etc.) actually need this; sequence
    diagrams ignore the pragma harmlessly."""
    lines = source.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("@startuml"):
            lines.insert(i + 1, "!pragma layout smetana")
            break
    return "\n".join(lines)


def render_diagram(source: str, diagrams_dir: Path, plantuml_jar: Path) -> Path:
    digest = hashlib.sha1(source.encode("utf-8")).hexdigest()[:12]
    puml_path = diagrams_dir / f"diagram-{digest}.puml"
    png_path = diagrams_dir / f"diagram-{digest}.png"

    if png_path.exists():
        return png_path

    diagrams_dir.mkdir(parents=True, exist_ok=True)
    puml_path.write_text(with_smetana_layout(source), encoding="utf-8")

    result = subprocess.run(
        ["java", "-jar", str(plantuml_jar), "-tpng", "-charset", "UTF-8", str(puml_path)],
        capture_output=True,
        text=True,
    )
    # PlantUML can exit 0 and still write a PNG after a failure (e.g. missing
    # Graphviz `dot`) by baking the error message into the image itself as
    # if it were the diagram - so a clean returncode + an existing file is
    # not sufficient evidence of success; stderr must be clean too.
    if result.returncode != 0 or not png_path.exists() or result.stderr.strip():
        sys.exit(
            f"PlantUML failed to render a diagram (source saved at {puml_path}):\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return png_path


def process_file(path: Path, diagrams_dir: Path, plantuml_jar: Path, repo_root: Path) -> str:
    text = path.read_text(encoding="utf-8")

    def replace(match: re.Match) -> str:
        png_path = render_diagram(match.group(1), diagrams_dir, plantuml_jar)
        rel_path = png_path.relative_to(repo_root)
        return f"![Diagram]({rel_path.as_posix()})\n"

    return FENCE_RE.sub(replace, text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sections", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--diagrams-dir", required=True, type=Path)
    parser.add_argument("--plantuml-jar", required=True, type=Path)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    diagrams_dir = args.diagrams_dir.resolve()

    chunks = []
    for section in args.sections:
        chunks.append(process_file(section, diagrams_dir, args.plantuml_jar, repo_root))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n\n".join(chunks), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
