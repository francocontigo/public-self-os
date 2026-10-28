---
name: dia
description: Abre e fecha o dia. Sem argumento, lê o estado do sistema e escreve o diário de hoje em journal/ com um plano de no máximo três itens. Com "fechar", registra o que saiu e o que não saiu em dois minutos. Use toda manhã ("abre o dia", "bom dia", "o que faço hoje") e no fim do dia ("fecha o dia").
argument-hint: "[fechar]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F` e `python scripts/os_status.py`. Argumento: `$ARGUMENTS`.

## Abrir (sem argumento)
1. Se `journal/<hoje>.md` já existe, mostre o `## Plano` e pergunte se quer ajustar. Pare aí.
2. Leia o diário anterior (o `last_day` do script), em especial `## Fechamento`. A linha "Amanhã:" de lá, se existir, é o primeiro candidato a item de hoje.
3. Leia as pendências: `## Pendências` em `areas/trabalho/frentes/*.md` e `areas/pessoal/metas.md`, posts abertos, projetos em andamento (`next_step`), trilhas ativas (`next_step`), cards vencidos (`due_now`).
4. Proponha **no máximo três itens** para hoje, no geral:
   - um de estudo (cards vencidos via `/study`, ou `/trilha continuar <slug>`),
   - um de público (rascunho aberto, post via `/post`, ou `/projeto continuar <slug>`),
   - um livre (trabalho ou pessoal, vindo das pendências ou do fechamento de ontem).
   Se não há trilha ativa, diga isso e sugira `/diagnostico` (ou `/entrevista`, se `## Domínios` do gap-map estiver vazio) como item de estudo. Se o mês não tem produção pública, o item de público é obrigatório. Se `inbox_items` for maior que cinco, lembre `/process-inbox`.
5. Crie `journal/<hoje>.md` a partir de `templates/diario.md`, trocando `{{date:YYYY-MM-DD}}` pela data real, `## Plano` preenchido com checkboxes, `## Notas` e `## Fechamento` vazios.
6. Imprima o plano e, na última linha, o comando do primeiro item, pronto para rodar.

## Fechar (`fechar`)
Dois minutos. Se `journal/<hoje>.md` não existe, crie com `## Plano` vazio e siga.
1. Mostre o `## Plano` e pergunte, **uma por vez**: o que saiu, o que não saiu e por quê, uma linha para amanhã.
2. Marque os checkboxes do plano conforme a resposta. Escreva em `## Fechamento`:
```
Saiu: ...
Não saiu: ... (por quê)
Amanhã: ...
```
3. Se algo dito for conhecimento reutilizável, acrescente uma linha em `raw/inbox.md`. Se for pendência de trabalho ou pessoal, acrescente em `## Pendências` da frente ou de `metas.md`.
4. Imprima o fechamento em três linhas.

Não edita a wiki. Não incrementa o contador de sessão (isso é do `/study`).
