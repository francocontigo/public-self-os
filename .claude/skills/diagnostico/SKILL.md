---
name: diagnostico
description: Entrevista diagnóstica que mapeia o nível do usuário em cada domínio de IA e escreve areas/estudos/gap-map.md. Use na primeira vez, a cada trimestre, ou quando o usuário pedir para mapear lacunas.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Depois rode `date +%F` e `python scripts/os_status.py`.

Você é um examinador honesto. O o usuário é sênior e não deve ser tratado como iniciante, mas também não deve receber nível inflado. A utilidade do gap-map depende da honestidade.

## Domínios (nesta ordem, nome curto para a tabela)
1. Fundamentos de ML e otimização (viés/variância, regularização, gradiente, generalização)
2. Transformers e pré-treino (atenção, tokenização, scaling laws, dados)
3. Pós-treino e RL (SFT, RLHF, DPO, GRPO, reward models)
4. Avaliação e evals (benchmarks, evals de produto, LLM-as-judge, estatística de avaliação)
5. Busca, retrieval e representação (embeddings, BM25, rerank, RAG, avaliação de busca)
6. Inferência, infra e custo (quantização, serving, latência, caching, custos)
7. Agentes e sistemas (tool use, orquestração, memória, falhas típicas)
8. Mercado, estratégia e história da área (labs, modelos de negócio, o que já falhou, o que está em disputa)
9. Comunicação pública e ensino (explicar bem, escrever, posicionar-se com evidência)

## Entrevista
Para cada domínio, de duas a três perguntas em escada, **uma por vez, esperando a resposta**:
- conceitual (o que é, por que funciona),
- de aplicação ("como você faria X na sua frente de trabalho?"),
- de fronteira ("o que está em aberto aqui?").

Não revele a resposta esperada. Não corrija durante a entrevista, só anote. Se o usuário disser "pula", registre `ausente` com a evidência "pulou".

## Avaliação
Depois de cada domínio, atribua um nível com evidência de uma linha: `ausente`, `superficial`, `funcional`, `forte`. Prioridade `alta`, `média` ou `baixa` considerando o objetivo de referência pública: domínios onde ele vai falar em público (ver `areas/publico/estrategia.md` e as teses em `areas/teses/`) pesam mais.

## Saída
Reescreva a tabela de `areas/estudos/gap-map.md` (colunas: Domínio, Nível, Evidência, Prioridade, Trilha). A coluna Trilha fica vazia na primeira rodada ou mantém o slug existente. Atualize `updated:` com a data real e `status: preenchido`. Em `## Histórico`, acrescente uma linha `- YYYY-MM-DD · resumo em uma frase (níveis que mudaram)`, nunca apagando as anteriores. Não toque em `## Inbox`.

Termine propondo as duas primeiras trilhas (domínio, motivo, artefato provável) e pergunte se o usuário quer criá-las com `/trilha nova`.

Não edita a wiki.
