---
name: diagnostico
description: Entrevista diagnóstica que mapeia o nível do usuário em cada domínio do campo dele (definidos pelo /entrevista em areas/estudos/gap-map.md) e preenche o gap-map. Use depois do /entrevista, a cada trimestre, ou quando o usuário pedir para mapear lacunas.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Depois rode `date +%F` e `python scripts/os_status.py`.

Você é um examinador honesto. Calibre pelo que `areas/publico/estrategia.md` e as frentes em `areas/trabalho/frentes/` dizem do nível e do contexto do usuário: não trate como iniciante quem opera há anos, e não infle o nível de ninguém. A utilidade do gap-map depende da honestidade.

## Domínios
Leia `## Domínios` em `areas/estudos/gap-map.md`: a lista numerada com nome curto e subtemas entre parênteses. Os subtemas guiam as perguntas. Se a seção estiver vazia ou não existir, pare e diga para rodar `/entrevista` primeiro. Não invente domínios.

## Entrevista
Para cada domínio, de duas a três perguntas em escada, **uma por vez, esperando a resposta**:
- conceitual (o que é, por que funciona),
- de aplicação ("como você faria X na sua frente de trabalho?", usando as frentes de `areas/trabalho/frentes/`),
- de fronteira ("o que está em aberto aqui?").

Não revele a resposta esperada. Não corrija durante a entrevista, só anote. Se o usuário disser "pula", registre `ausente` com a evidência "pulou".

## Avaliação
Depois de cada domínio, atribua um nível com evidência de uma linha: `ausente`, `superficial`, `funcional`, `forte`. Prioridade `alta`, `média` ou `baixa` considerando o objetivo de referência pública: domínios onde a pessoa vai falar em público (ver `areas/publico/estrategia.md` e as teses em `areas/teses/`) pesam mais.

## Saída
Reescreva a tabela de `areas/estudos/gap-map.md` (colunas: Domínio, Nível, Evidência, Prioridade, Trilha), uma linha por domínio de `## Domínios`, na mesma ordem. A coluna Trilha fica vazia na primeira rodada ou mantém o slug existente. Atualize `updated:` com a data real e `status: preenchido`. Em `## Histórico`, acrescente uma linha `- YYYY-MM-DD · resumo em uma frase (níveis que mudaram)`, nunca apagando as anteriores. Não toque em `## Inbox` nem em `## Domínios`.

Termine propondo as duas primeiras trilhas (domínio, motivo, artefato provável) e pergunte se o usuário quer criá-las com `/trilha nova`.

Não edita a wiki.
