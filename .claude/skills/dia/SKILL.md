---
name: dia
description: Abre o dia. Lê o estado do sistema e escreve o diário de hoje em journal/ com um plano de no máximo três itens. Use toda manhã ou quando o usuário disser "abre o dia", "bom dia" ou "o que faço hoje".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F` e `python scripts/os_status.py`.

1. Se `journal/<hoje>.md` já existe, mostre o `## Plano` e pergunte se quer ajustar. Pare aí.
2. Leia o diário anterior (o `last_day` do script), em especial `## Fechamento` se estiver preenchido.
3. Leia as pendências: `## Pendências` em `areas/trabalho/frentes/*.md` e `areas/pessoal/metas.md`, posts abertos, projetos em andamento (`next_step`), trilhas ativas (`next_step`), cards vencidos (`due_now`).
4. Proponha **no máximo três itens** para hoje, no geral:
   - um de estudo (cards vencidos via `/study`, ou `/trilha continuar <slug>`),
   - um de público (rascunho aberto, post do dia via `/post`, ou `/projeto continuar <slug>`),
   - um livre (trabalho ou pessoal, vindo das pendências ou do fechamento de ontem).
   Se não há trilha ativa, diga isso e sugira `/diagnostico` como item de estudo. Se o mês não tem produção pública, o item de público é obrigatório.
5. Crie `journal/<hoje>.md` a partir de `templates/diario.md`, trocando `{{date:YYYY-MM-DD}}` pela data real, `## Plano` preenchido com checkboxes, `## Notas` e `## Fechamento` vazios.
6. Imprima o plano.

Não edita a wiki. Não incrementa o contador de sessão (isso é do `/study`).
