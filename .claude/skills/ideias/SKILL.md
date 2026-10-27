---
name: ideias
description: Gera ideias de post a partir das teses, dos projetos e do que o usuário aprendeu recentemente, e acrescenta ao backlog em areas/publico/ideias.md. Use quando o usuário pedir ideias de post ou estiver sem o que publicar.
argument-hint: "[n, padrão 5]"
allowed-tools: Read, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F`. Número de ideias: `$ARGUMENTS` (padrão cinco).

## Leitura obrigatória
- `areas/publico/estrategia.md` (posicionamento, pilares, plataformas) e `areas/publico/voz.md` (regras duras).
- `areas/publico/ideias.md`, para não repetir o que já está no backlog.
- As teses em `areas/teses/` (fonte primária) e os projetos em `areas/projetos/`.
- Páginas da wiki tocadas nos últimos 14 dias (via `wiki/log.md`).
- Sessões recentes em `areas/estudos/trilhas/` e os diários da semana em `journal/`.

## Regras
- Pelo menos três das cinco ideias sustentam, testam ou provocam uma tese existente. Pelo menos uma sai de um projeto (o que foi construído, o que foi descoberto construindo).
- Temas expansivos, sobre o mercado e a área, nunca sobre o trabalho passado do usuário nem sobre os projetos dele como autobiografia.
- Nunca enquadre o usuário como júnior ou como quem sofre o problema.
- Se não há teses nem projetos ainda, diga isso e gere as ideias a partir da estratégia e da wiki, marcando origem vazia e sugerindo `/tese nova`.

## Cada ideia traz
Título de trabalho, ângulo em duas frases, por que agora, justificativa (por que serve ao posicionamento), tese ou projeto de origem, plataforma sugerida (x, linkedin, medium) e wikilinks das páginas que sustentam.

## Saída
Acrescente em `## Backlog` de `areas/publico/ideias.md`, no formato definido no topo do arquivo, com a data real e `status: ideia`. Imprima as ideias. Não edita a wiki.
