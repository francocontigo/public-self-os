---
description: Triage raw/inbox.md fleeting notes into the wiki
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, Bash(date:*)
---

You are the librarian for this second brain. First read `CLAUDE.md` and follow its hard rules. Run `date +%F` once at the start and use the real date everywhere a date is written.

Drain the capture inbox at `raw/inbox.md`. Each non-empty, non-comment line (or block separated by `---`)
is one fleeting item: an idea, a todo, a link, or a quick note.

For each item, top to bottom:
1. Decide its kind: a **link/URL** → ingest like `/ingest` (summarize + extract). A **fact/idea/note** →
   route it to the right `wiki/` page (entities/concepts/synthesis), creating stubs and `[[wikilinks]]` as needed.
   An item that starts with an **area marker** is operational and goes to `areas/` (see the routing table
   below). A todo with **no marker and no knowledge value** → leave it in the inbox and say so in the report,
   suggesting the marker it should have had.
2. **Area routing** (write in Portuguese, add the real date, keep `[[wikilinks]]` to the wiki when the topic has a page):
   - `@estudo <text>` → `## Inbox` in `areas/estudos/gap-map.md`, or `## Mapa de conceitos` of the active track
     in `areas/estudos/trilhas/<slug>.md` if the text names its slug.
   - `@post <text>` → one entry in `## Backlog` of `areas/publico/ideias.md`, in the format defined at the top of that
     file, with `status: ideia` and the date.
   - `@trabalho <frente> <text>` → `## Pendências` in `areas/trabalho/frentes/<frente>.md`, or `## Aprendizados` there
     (or `areas/trabalho/aprendizados.md`) if it is a learning rather than a pending item. LGPD: never write personal
     data of creators, clients or employees; refer to people by role, and say so if you dropped something.
   - `@pessoal <text>` → `## Pendências` in `areas/pessoal/metas.md`.
   - `@tese <text>` → `## Candidatas` in `areas/teses/_index.md` (a position not yet formalized), or `## Evidência` of
     `areas/teses/<slug>.md` if the text names an existing thesis slug.
   - `@projeto <slug> <text>` → `## Log` of `areas/projetos/<slug>.md` (dated line), or `## Candidatos` in
     `areas/projetos/_index.md` if that project does not exist.
   - `@rede <text>` → `## Inbox` in `areas/rede/mapa.md`. Minimization rule: only people with a public presence,
     name + public handle + why; nothing private about anyone.
   Marked items still pass the knowledge test: if they contain a reusable concept, the concept goes to the wiki and the
   operational item goes to the area, with a link between the two.
3. Cite the inbox as the source on any wiki page you create (`## Source(s): raw/inbox.md`). On any new/expanded
   `concepts/` or `synthesis/` page, add a `## Recall` section and enqueue its cards in `review/queue.md`
   (`box: 1`, `due: <current session>`), per the Learning layer rules in `CLAUDE.md`.
4. Once an item is integrated (wiki or area), **remove that line from `raw/inbox.md`**. Keep items you intentionally left.

Then: update `wiki/index.md` (if the wiki was touched) and append ONE summary entry to `wiki/log.md` with the real
date (operation `process-inbox`, how many items processed/left, pages touched, including area files).

Print a short report: items processed (wiki vs areas), items left in inbox (with why), pages created/updated.
