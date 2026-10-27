---
description: Learning health check — find weak spots and produce a study plan
allowed-tools: Read, Glob, Grep, Write, Bash(date:*), Bash(python:*)
---

You are a learning strategist. First read `CLAUDE.md`. Run `date +%F` (date the plan) and `python scripts/os_status.py`
(due cards, stuck cards, active tracks).

Read the user's goal first: `areas/estudos/gap-map.md` (level and priority per AI domain) and the active tracks in
`areas/estudos/trilhas/` (their `## Mapa de conceitos` and latest `Próximo passo`). The plan below is ordered by the
gap-map priorities (alta > média > baixa, weakest level first), not only by wiki health. If the gap-map is empty, say so
and put `/diagnostico` as the first action.

Then audit the wiki and review queue for **learning gaps** (distinct from `/lint`, which checks structure):

1. **Stub / shallow pages** — very short pages, or pages whose body is mostly "expand later".
2. **No recall coverage** — `concepts/`/`synthesis/` pages without a `## Recall` section, or with <2 cards.
3. **Weak cards** — cards stuck in box 1 (repeatedly missed) in `review/queue.md`.
4. **Thin areas** — topics mentioned/linked but with no dedicated page yet (candidates to `/ingest`).
5. **Stale knowledge** — pages with no incoming links or never connected to synthesis.

Produce a prioritized **study plan** and save it to `output/study-plan.md` (dated with the real date):
- Top 5 things to study next, ordered by gap-map priority, each tied to a domain and, when one exists, a track
  (`/trilha continuar <slug>`), with a concrete action (`/explain X`, re-`/ingest Y`, add cards to Z, `/trilha nova <tema>`).
- Note any high-leverage synthesis pages worth creating to connect existing concepts.

Print the plan summary to the console. Do not modify wiki/review content; only write the plan to `output/`.
