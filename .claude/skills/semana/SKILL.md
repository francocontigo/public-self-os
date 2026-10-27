---
name: semana
description: Revisão semanal que olha todas as áreas juntas, escreve journal/semanas/YYYY-Www.md e define o foco da próxima semana. Use toda sexta ou domingo, ou quando o usuário pedir a revisão da semana.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F` e `python scripts/os_status.py` (o campo `week` dá o nome do arquivo).

## Leitura (antes de perguntar)
- Diários dos últimos sete dias em `journal/`.
- Entradas de `wiki/log.md` da semana.
- Do script: produção pública do mês e do anterior, distribuição das caixas, cards travados, trilhas, posts, teses, projetos.
- Sessões das trilhas na semana, projetos em andamento, teses sustentadas, posts publicados na semana e seus `## Resultado`.
- `areas/rede/mapa.md` e `areas/estudos/gap-map.md`.

## Perguntas (no máximo quatro, uma por vez)
1. O que saiu em público e teve resposta?
2. O que funcionou?
3. O que travou?
4. Com quem você falou ou deveria ter falado? (alimenta `areas/rede/mapa.md`, respeitando a regra de minimização: só pessoas públicas, nome e handle, interação pública).

## Nota semanal
Crie `journal/semanas/<week>.md` a partir de `templates/semana.md`. A seção `## Produção pública` vem **primeiro e é obrigatória**: o que saiu esta semana e este mês (projetos, artigos, posts) e quem usou ou citou. Se o mês corrente ainda não tem nenhum projeto ou artigo publicado, diga isso explicitamente no topo.

Depois:
- `## O que aconteceu` por área (estudos, projetos, público, teses, trabalho, pessoal, rede).
- Teses que ganharam ou perderam evidência na semana (sugira `/tese revisar <slug>`).
- `## Aprendizados para a wiki`: cada item vira também uma linha em `raw/inbox.md` para o `/process-inbox`.
- `## Gap-map`: mudanças propostas. **Pergunte antes de alterar níveis.**
- `## Foco da próxima semana`: no máximo três itens, pelo menos um de produção pública.
- `## Ideias de post`: três, derivadas das teses e do que foi aprendido, seguindo a lógica e o formato de `/ideias`, e acrescentadas em `## Backlog` de `areas/publico/ideias.md` com data e `status: ideia`.

Se tocou a wiki, acrescente uma linha em `wiki/log.md` com a data real. Só tocar `areas/`, `journal/` e `raw/inbox.md` não exige log.
