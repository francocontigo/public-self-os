#!/usr/bin/env python3
"""Deterministic state of the personal OS (see docs/personal-os-spec.md, section 6.0).

Prints JSON on stdout, or a human summary with --human. No dependencies.
Runs from anywhere: the vault is resolved from this file's location.
"""
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

DEFAULT_VAULT = Path(__file__).resolve().parent.parent
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
NEXT_RE = re.compile(r"Pr[óo]ximo passo:[ \t]*(.+)")  # not \s*: it would swallow the newline of an empty template line


def frontmatter(text):
    """Simple `key: value` pairs between the leading --- fences. Not full YAML."""
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip("\"'")
    return fm


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def last_date(text):
    ds = DATE_RE.findall(text)
    return max(ds) if ds else None


def next_step(text):
    ms = NEXT_RE.findall(text)
    return (ms[-1].strip() or None) if ms else None


def notes(vault, folder):
    d = vault / folder
    if not d.is_dir():
        return []
    out = []
    for p in sorted(d.glob("*.md")):
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8")
        out.append((p.stem, frontmatter(text), text))
    return out


def review(vault):
    p = vault / "review/queue.md"
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    m = re.search(r"^session:\s*(\d+)", text, re.M)
    session = int(m.group(1)) if m else 0
    cards = []
    for block in re.split(r"^## Card: ", text, flags=re.M)[1:]:
        slug = block.splitlines()[0].strip()

        def field(k, default):
            f = re.search(rf"^- {k}:\s*(\d+)", block, re.M)
            return int(f.group(1)) if f else default

        # ponytail: `- misses: N` is optional; /study may add it. Without it stuck_box1 is empty.
        cards.append((slug, field("box", 1), field("due", 0), field("misses", 0)))
    return {
        "session": session,
        "total_cards": len(cards),
        "due_now": sum(1 for c in cards if c[2] <= session + 1),
        "box_distribution": {str(b): n for b, n in sorted(Counter(c[1] for c in cards).items())},
        "stuck_box1": [c[0] for c in cards if c[1] == 1 and c[3] > 0],
    }


def tracks(vault):
    return [
        {
            "slug": slug,
            "status": fm.get("status", ""),
            "scope": fm.get("scope", ""),
            "last_session": last_date(section(text, "Sessões")),
            "next_step": next_step(text),
        }
        for slug, fm, text in notes(vault, "areas/estudos/trilhas")
    ]


def posts(vault):
    items = notes(vault, "areas/publico/posts")
    return {
        "by_status": dict(Counter(fm.get("status", "") for _, fm, _ in items)),
        "open": [
            {"slug": slug, "platform": fm.get("platform", ""), "date": fm.get("date", "")}
            for slug, fm, _ in items
            if fm.get("status") in ("rascunho", "agendado")
        ],
    }


def teses(vault):
    items = notes(vault, "areas/teses")
    citing = Counter(
        fm.get("thesis", "")
        for folder in ("areas/publico/posts", "areas/projetos")
        for _, fm, _ in notes(vault, folder)
    )
    return {
        "by_status": dict(Counter(fm.get("status", "") for _, fm, _ in items)),
        "sustentadas": [
            {"slug": slug, "updated": fm.get("updated", ""), "cited_by": citing.get(slug, 0)}
            for slug, fm, _ in items
            if fm.get("status") == "sustentada"
        ],
    }


def projetos(vault):
    items = notes(vault, "areas/projetos")
    return {
        "by_status": dict(Counter(fm.get("status", "") for _, fm, _ in items)),
        "em_andamento": [
            {"slug": slug, "last_log": last_date(section(text, "Log")), "next_step": next_step(text)}
            for slug, fm, text in items
            if fm.get("status") == "em-andamento"
        ],
    }


def producao_publica(vault, today):
    y, m = int(today[:4]), int(today[5:7])
    prev = f"{y - 1}-12" if m == 1 else f"{y}-{m - 1:02d}"
    out = {
        today[:7]: {"projetos": 0, "artigos": 0, "posts": 0},
        prev: {"projetos": 0, "artigos": 0, "posts": 0},
    }
    for _, fm, _ in notes(vault, "areas/projetos"):
        month = fm.get("published", "")[:7]
        if fm.get("status") == "publicado" and month in out:
            out[month]["projetos"] += 1
    for _, fm, _ in notes(vault, "areas/publico/posts"):
        month = fm.get("published", "")[:7]
        if fm.get("status") != "publicado" or month not in out:
            continue
        artigo = fm.get("kind") == "artigo" and fm.get("platform") in ("medium", "linkedin")
        out[month]["artigos" if artigo else "posts"] += 1
    return out


def journal(vault):
    def latest(folder):
        d = vault / folder
        names = sorted(p.stem for p in d.glob("*.md")) if d.is_dir() else []
        return names[-1] if names else None

    return {"last_day": latest("journal"), "last_week": latest("journal/semanas")}


def inbox_items(vault):
    p = vault / "raw/inbox.md"
    if not p.exists():
        return 0
    # ponytail: the header block (first "# " heading through the first "---") is not an item;
    # captures are prepended above it or appended below it.
    count, in_header, seen_header = 0, False, False
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("# ") and not seen_header:
            in_header = seen_header = True
        if in_header:
            if s == "---":
                in_header = False
            continue
        if s and not s.startswith("#") and s != "---":
            count += 1
    return count


def collect(vault=DEFAULT_VAULT, today=None):
    today = today or date.today().isoformat()
    iso = date.fromisoformat(today).isocalendar()
    return {
        "today": today,
        "week": f"{iso[0]}-W{iso[1]:02d}",
        "producao_publica": producao_publica(vault, today),
        "review": review(vault),
        "tracks": tracks(vault),
        "posts": posts(vault),
        "teses": teses(vault),
        "projetos": projetos(vault),
        "journal": journal(vault),
        "inbox_items": inbox_items(vault),
    }


def human(s):
    lines = [f"Hoje: {s['today']} ({s['week']})", "", "PRODUÇÃO PÚBLICA (métrica central)"]
    for month, c in s["producao_publica"].items():
        lines.append(f"  {month}: {c['projetos']} projetos, {c['artigos']} artigos, {c['posts']} posts")
    r = s["review"]
    lines += [
        "",
        f"Review: sessão {r['session']}, {r['total_cards']} cards, {r['due_now']} vencidos, "
        f"caixas {r['box_distribution'] or '{}'}, travados: {', '.join(r['stuck_box1']) or 'nenhum'}",
    ]
    active = [t for t in s["tracks"] if t["status"] == "ativa"]
    lines.append("Trilhas ativas: " + (", ".join(
        f"{t['slug']} ({t['scope'] or '?'}, última {t['last_session'] or '-'}, próximo: {t['next_step'] or '-'})"
        for t in active) or "nenhuma"))
    lines.append(f"Posts: {s['posts']['by_status'] or 'nenhum'}; abertos: "
                 + (", ".join(p['slug'] for p in s['posts']['open']) or "nenhum"))
    lines.append(f"Teses: {s['teses']['by_status'] or 'nenhuma'}; sustentadas: "
                 + (", ".join(f"{t['slug']} ({t['cited_by']}x)" for t in s['teses']['sustentadas']) or "nenhuma"))
    lines.append(f"Projetos: {s['projetos']['by_status'] or 'nenhum'}; em andamento: "
                 + (", ".join(f"{p['slug']} (próximo: {p['next_step'] or '-'})" for p in s['projetos']['em_andamento']) or "nenhum"))
    j = s["journal"]
    lines.append(f"Journal: último diário {j['last_day'] or '-'}, última semana {j['last_week'] or '-'}")
    lines.append(f"Inbox: {s['inbox_items']} itens")
    return "\n".join(lines)


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    s = collect()
    if "--human" in argv:
        print(human(s))
    else:
        print(json.dumps(s, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
