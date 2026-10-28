#!/usr/bin/env python3
"""Mechanical wiki lint, no LLM: broken wikilinks, orphans, index gaps, missing sources.

Exit code 1 when there are broken links or index gaps (the two that break navigation).
`/lint` runs this first and keeps the judgment work (contradictions, merges) for the model.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.S)  # placeholders like `[[frente]]` live in code spans
SKIP = ("raw", ".obsidian", ".claude", "output", "0 Notebook", "1 Books&Courses", "2 Files", "3 Templates", "app")


def lint(vault=VAULT):
    rel = lambda p: str(p.relative_to(vault)).replace("\\", "/")
    pages = [p for p in vault.rglob("*.md") if not any(part in SKIP for part in p.relative_to(vault).parts)]
    stems = {p.stem for p in pages} | {rel(p)[:-3] for p in pages}
    wiki = [p for p in pages if p.relative_to(vault).parts[0] == "wiki" and p.name not in ("index.md", "log.md")]
    index = (vault / "wiki/index.md").read_text(encoding="utf-8") if (vault / "wiki/index.md").exists() else ""
    incoming = set()
    broken = []
    for p in pages:
        for target in LINK_RE.findall(CODE_RE.sub("", p.read_text(encoding="utf-8"))):
            t = target.strip()
            if t in stems or t.split("/")[-1] in stems:
                if p.name != "index.md":  # a page only listed in the index is still an orphan
                    incoming.add(t.split("/")[-1])
            else:
                broken.append((rel(p), t))
    return {
        "broken_links": broken,
        "orphans": [rel(p) for p in wiki if p.stem not in incoming],
        "index_gaps": [rel(p) for p in wiki if f"[[{p.stem}]]" not in index],
        "missing_sources": [rel(p) for p in wiki if "## Source(s)" not in p.read_text(encoding="utf-8")],
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = lint()
    for k, v in r.items():
        print(f"{k}: {len(v)}")
        for item in v:
            print(f"  {item}")
    sys.exit(1 if r["broken_links"] or r["index_gaps"] else 0)


if __name__ == "__main__":
    main()
