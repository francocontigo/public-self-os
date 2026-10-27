---
name: trilha
description: Cria, continua, lista e encerra trilhas de estudo em areas/estudos/trilhas/. Use quando o usuário quiser começar a estudar um tema com começo, meio, fim e artefato de saída, ou retomar uma trilha existente.
argument-hint: nova <tema> | continuar <slug> | listar | fechar <slug>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F` e `python scripts/os_status.py` antes de qualquer coisa.

Subcomando: `$ARGUMENTS`. Sem argumento, trate como `listar`.

## `nova <tema>`
Interativa, **uma pergunta por vez**:
1. Motivação: o que ele quer conseguir fazer ou dizer ao final.
2. Horas por semana disponíveis.
3. Artefato de saída. Proponha a opção mais forte que couber no escopo, nesta ordem: projeto público (código, benchmark, ferramenta, paper), artigo longo, post. Só aceite post como artefato de trilha `quick`.
4. Qual tese em `areas/teses/` a trilha sustenta ou testa, se houver.

Depois:
- Classifique o escopo: `quick` (menos de 5 h), `standard` (5 a 20 h), `deep` (mais de 20 h).
- Crie `areas/estudos/trilhas/<slug>.md` a partir de `templates/trilha.md` (`status: ativa`, `scope`, `started` com a data real, `domain` com o nome curto do gap-map, `artifact`, `thesis`, `project`).
- Se o artefato for projeto, crie também `areas/projetos/<slug>.md` seguindo a lógica de `/projeto novo` (template, `status: ideia`, linha em `_index.md`) e linke os dois arquivos.
- Escreva o slug na coluna Trilha do domínio correspondente em `areas/estudos/gap-map.md`. Se o gap-map estiver vazio, só registre o domínio na trilha e sugira `/diagnostico`.
- Preencha `## Fontes` com três a seis fontes (livros, papers, cursos, posts), uma linha de justificativa cada. URLs são listadas, nunca ingeridas automaticamente. Sugira qual ingerir primeiro com `/ingest`.
- Preencha `## Mapa de conceitos` na ordem de estudo, com wikilink quando a página já existe em `wiki/`.

## `continuar <slug>`
Leia a trilha inteira. Decida o tipo da sessão: alterne teoria e aplicação, **nunca duas sessões de teoria seguidas** (olhe a última entrada de `## Sessões`).

Abra com duas ou três perguntas de recall sobre sessões anteriores da trilha, uma por vez.

- Sessão de **teoria**: aula socrática sobre o próximo conceito do mapa, apoiada nas páginas da wiki. Se a página não existe, proponha ingerir a fonte antes e pare aí se ele aceitar.
- Sessão **aplicada**: um exercício ligado ao trabalho atual do usuário (as frentes em `areas/trabalho/frentes/`, ver `areas/trabalho/frentes/`) ou ao artefato da trilha.

Feche registrando em `## Sessões` um bloco:
```
### YYYY-MM-DD · teoria|aplicada
Feito: ...
Ficou fraco: ...
Próximo passo: ...
```
A linha `Próximo passo:` é obrigatória, o script a lê. Conceitos novos ganham página ou `## Recall` na wiki e cards em `review/queue.md` (`box: 1`, `due: <session atual>`), pelo mecanismo existente. Se tocou a wiki, atualize `wiki/index.md` e acrescente uma linha em `wiki/log.md` com a data real.

## `listar`
Imprima a saída de `python scripts/os_status.py` filtrada em `tracks`: slug, status, escopo, última sessão, próximo passo.

## `fechar <slug>`
Só fecha se as duas condições passarem:
1. Teste de Feynman sobre o escopo inteiro: o usuário explica o domínio como se ensinasse, você pontua clareza, completude e precisão (mesmo fluxo de `/explain`), com perguntas de aprofundamento uma por vez.
2. O artefato existe e está linkado em `## Artefato` (post em `areas/publico/posts/`, arquivo em `output/`, projeto em `areas/projetos/` com status `publicado`, ou URL).

Se passar: `status: concluida`, nota e data em `## Encerramento`, proposta de novo nível no gap-map (**pergunte antes de mudar**), e uma linha em `wiki/log.md`. Se não passar, diga o que falta e mantenha `ativa`.
