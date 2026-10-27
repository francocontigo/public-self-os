---
name: tese
description: Cria, revisa, desafia e lista as posições que o usuário sustenta em público, em areas/teses/. Use quando o usuário quiser formalizar uma opinião, testá-la contra evidência nova, ser contestado, ou ver quais teses sustenta.
argument-hint: nova <enunciado> | revisar <slug> | desafiar <slug> | listar
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F`. Subcomando: `$ARGUMENTS` (sem argumento, `listar`).

Uma tese é uma afirmação sobre o mundo que pode estar errada, não um tema. Status: `rascunho`, `sustentada` (publicada ao menos uma vez), `revisada`, `abandonada`.

## `nova <enunciado>`
Pergunte, **uma por vez**:
1. O enunciado em uma frase. Se vier um tema e não uma afirmação, peça para reformular.
2. O argumento em um parágrafo.
3. A evidência que ele tem hoje, com `[[wikilinks]]` quando já está na wiki.
4. O que o faria mudar de ideia.
5. Quem no mercado discorda e por quê (pessoas públicas pelo nome e handle, ou posições sem nome).

Crie `areas/teses/<slug>.md` a partir de `templates/tese.md` com `status: rascunho`, `created` e `updated` reais, e acrescente a linha na tabela de `areas/teses/_index.md`. Se o enunciado estava em `## Candidatas` do índice, remova de lá. Uma tese só passa a `sustentada` quando há ao menos uma linha em `## Onde foi sustentada` (feito por `/post publicado` ou `/projeto publicar`).

## `revisar <slug>`
Leia a tese, as páginas da wiki ligadas a ela e o que entrou em `wiki/log.md` desde a última linha de `## Revisões`. Pergunte se a evidência nova fortalece, enfraquece ou muda a tese. Acrescente `- YYYY-MM-DD · o que mudou` em `## Revisões`, atualize `updated` e, se o status mudar, o `_index.md`. Se a tese caiu, `status: abandonada` com o porquê em `## Revisões`, **sem apagar nada**: mudar de ideia em público com registro é parte do posicionamento.

## `desafiar <slug>`
Assuma o melhor argumento contrário e debata com o usuário, **uma rodada por vez**, até no máximo cinco rodadas. Ao final, registre em `## Objeções` as objeções que ficaram sem resposta boa, com a data. Não edite o resto da tese sem o usuário pedir.

## `listar`
Imprima a saída de `python scripts/os_status.py` filtrada em `teses`: contagem por status e, para as sustentadas, quantas vezes foram sustentadas em público (`cited_by`).

Não edita a wiki, mas qualquer fato novo que apareceu no debate vai como uma linha em `raw/inbox.md`.
