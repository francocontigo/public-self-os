---
name: brag
description: Mantém o brag document do trabalho em areas/trabalho/brag.md: o que o usuário entregou, com impacto e evidência. Colhe de GitHub (gh), de Linear ou Jira via conector, ou de uma lista colada. Use para registrar uma entrega, colher o período, ou montar o resumo para avaliação ou promoção.
argument-hint: add <o que fez> | colher [desde YYYY-MM-DD] | revisar <período> | listar
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(gh:*)
---

First read `CLAUDE.md`. Rode `date +%F`. Argumentos: `$ARGUMENTS`.

Brag document (Julia Evans): um registro contínuo do que você entregou no trabalho, escrito na hora, porque na avaliação ninguém lembra. Uma linha por item, sempre com impacto e, quando houver, evidência pública ou interna (link de PR, issue, documento).

## LGPD (regra dura)
Mesma regra de `areas/trabalho/`: nunca dados pessoais de criadores, clientes ou funcionários. Títulos de PR e issues trazem nomes de clientes e de pessoas. Reescreva pelo papel ("o maior cliente da base", "o time de dados"). Nunca cole o dump bruto de uma fonte no arquivo.

## Formato de cada entrada
```
- YYYY-MM-DD · [[frente]] · o que fiz · impacto (número quando houver) · evidência: <link ou "interno">
```
Entradas ficam em `## <ano>`, mais recente no topo. `## Colheitas` registra cada colheita (data, fonte, desde quando, quantos itens) e é de onde `colher` tira a data padrão.

## `add <o que fez>`
1. Pergunte, **uma por vez** e só o que faltou no texto: frente, impacto, evidência.
2. Escreva a linha em `## <ano>` de `areas/trabalho/brag.md`. Se a frente não existe em `areas/trabalho/frentes/`, use a mais próxima ou `geral`.

## `colher [desde YYYY-MM-DD]`
Data padrão: a última linha de `## Colheitas`, ou 30 dias atrás se não houver.

Fontes, nesta ordem, usando o que existir:
1. GitHub, via `gh` (verifique com `gh auth status`):
   ```
   gh search prs --author=@me --merged --merged-at=">=<data>" --limit 100 --json title,url,repository,closedAt
   gh search issues --assignee=@me --state=closed --closed=">=<data>" --limit 100 --json title,url,repository,closedAt
   ```
2. Linear ou Jira, se a sessão tiver um conector (ferramentas `mcp__*Linear*` ou `mcp__*Atlassian*`): issues concluídas pelo usuário desde a data. Se não tiver, não invente, pule.
3. Se nenhuma fonte responder, peça ao usuário uma lista colada (título e link por linha).

Depois:
- Agrupe por frente, junte PRs do mesmo tema em um item só, descarte ruído (bump de dependência, typo, revert).
- Proponha a lista inteira de uma vez, cada item já no formato, com impacto preenchido quando der para inferir e `impacto: ?` quando não der. Pergunte o que cortar e os impactos que faltam, **uma rodada só**.
- Escreva as linhas em `## <ano>` e uma linha em `## Colheitas`: `- YYYY-MM-DD · gh (+ linear) · desde YYYY-MM-DD · N itens`.

## `revisar <período>`
Período: `2026-Q4`, `2026-H1`, `2026` ou um intervalo de datas. Pergunte o público (gestor, comitê de promoção, autoavaliação) e o formato pedido pela empresa, se houver.

Escreva `output/brag-<período>.md`: por frente, as três a cinco entregas de maior impacto, cada uma com o número e a evidência. Depois uma seção `## Padrões` (o que se repete: tipo de problema que você resolve, escopo crescente, o que ninguém mais fez) e `## Lacunas` (o que a avaliação vai perguntar e o brag não responde). Não infle. Entrada sem impacto medido fica como está, com `impacto: não medido`.

## `listar`
Imprima `## <ano>` corrente agrupado por frente, com contagem por frente.

Não edita a wiki. Só toca `areas/trabalho/brag.md` e `output/`.
