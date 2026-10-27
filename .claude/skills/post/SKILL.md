---
name: post
description: Escreve, acompanha e fecha posts em areas/publico/posts/. Use quando o usuário quiser rascunhar um post ou artigo, registrar que publicou, ou anotar o resultado de um post.
argument-hint: <ideia ou tema> [x|linkedin|medium] | publicado <slug> <url> | resultado <slug>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F`. Argumento: `$ARGUMENTS`.

**O agente nunca publica. Só o usuário publica.** As regras de `areas/publico/voz.md` são regras duras, não sugestões. Releia-as antes de escrever e revise o texto contra elas antes de salvar.

## Escrever: `<ideia ou tema> [x|linkedin|medium]`
1. Leia `areas/publico/voz.md` e `areas/publico/estrategia.md` (obrigatório).
2. Procure a ideia em `## Backlog` de `areas/publico/ideias.md`. Se existe, use a origem dela (tese ou projeto) e os wikilinks.
3. Leia a tese em `areas/teses/<slug>.md` ou o projeto em `areas/projetos/<slug>.md` de origem, e as páginas relevantes da wiki. Não invente fatos nem números.
4. Plataforma: a informada, ou a sugerida na ideia, ou X por padrão. `kind: artigo` para LinkedIn ou Medium quando for texto longo, senão `kind: post`.
5. Crie `areas/publico/posts/YYYY-MM-DD-<slug>.md` a partir de `templates/post.md`: `status: rascunho`, `platform`, `date` real, `thesis:` e `project:` preenchidos quando houver origem, `idea:` com o título da ideia, `track:` se veio de uma trilha. Preencha `## Ideia e justificativa`, `## Versão curta` e `## Versão longa`. `## Versão final` fica vazia para o usuário.
6. Se a ideia veio do backlog, mude o status dela para `rascunho` e linke o post.
7. Imprima as duas versões e pergunte qual direção ele prefere.

## `publicado <slug> <url>`
Atualize no post: `status: publicado`, `url`, `published:` com a data real. Se há `thesis:`, acrescente em `## Onde foi sustentada` da tese a linha `- YYYY-MM-DD · [[post]] · url`, e se a tese estava em `rascunho`, pergunte se pode passar a `sustentada` (e atualize `_index.md`). Se há `project:`, acrescente a mesma linha em `## Divulgação` do projeto. Se a ideia do backlog existe, mude o status dela para `publicado`.

## `resultado <slug>`
Pergunte, uma por vez, os números que o usuário quer registrar (impressões, reações, respostas, o que chamou atenção) e escreva em `## Resultado` com a data. Sem inventar métricas: só o que ele disser.

Não edita a wiki.
