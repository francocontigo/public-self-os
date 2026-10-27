---
name: projeto
description: Cria e acompanha projetos públicos em areas/projetos/ (código, benchmark, ferramenta, paper), a forma mais forte de produção pública. Use quando o usuário quiser começar, retomar ou publicar um projeto, ou ver o estado dos projetos.
argument-hint: novo <nome> | continuar <slug> | publicar <slug> | listar
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*), Bash(python:*)
---

First read `CLAUDE.md`. Rode `date +%F`. Subcomando: `$ARGUMENTS` (sem argumento, `listar`).

Status: `ideia`, `em-andamento`, `publicado`, `arquivado`. O código do projeto vive no repositório do projeto, nunca no vault.

## `novo <nome>`
Pergunte, **uma por vez**:
1. O que o projeto demonstra ou resolve.
2. Qual tese em `areas/teses/` ele sustenta ou testa, se houver.
3. Qual trilha em `areas/estudos/trilhas/` ele exercita, se houver.
4. Quem é o usuário ou leitor.
5. Qual é a menor versão que já vale publicar.
6. Onde vai viver (repositório, artigo, benchmark público).

**Recuse escopo sem uma primeira versão publicável em até quatro semanas** e peça para reduzir, até caber. Crie `areas/projetos/<slug>.md` a partir de `templates/projeto.md` com `status: ideia`, `created` real, `thesis` e `track`, e acrescente a linha na tabela de `areas/projetos/_index.md`. Se veio de `## Candidatos`, remova de lá. Se há trilha, escreva o slug do projeto em `project:` e `## Artefato` da trilha.

## `continuar <slug>`
Leia o projeto. Pergunte o que foi feito desde a última vez. Se o status era `ideia`, mude para `em-andamento` (e no `_index.md`). Registre em `## Log`:
```
### YYYY-MM-DD
Feito: ...
Próximo passo: ...
```
A linha `Próximo passo:` é obrigatória, o script a lê. Aprendizado reutilizável vai como linha em `raw/inbox.md`. Se o usuário pedir ajuda técnica, ajude na sessão, mas não grave código no vault.

## `publicar <slug>`
Pergunte URL e o que foi publicado. Atualize `status: publicado`, `published` real, `url`, uma linha em `## Log`, e o `_index.md`. Se há `thesis:`, acrescente em `## Onde foi sustentada` da tese a linha `- YYYY-MM-DD · [[projeto]] · url` e pergunte se a tese pode passar a `sustentada`. Sugira a divulgação com `/post <tema> ` apontando `project:` para ele. Depois, cada menção, uso ou citação externa que o usuário quiser registrar vai em `## Uso e citações` com data e link, sem inventar nada.

## `listar`
Imprima a saída de `python scripts/os_status.py` filtrada em `projetos` e `producao_publica` (mês corrente e anterior).

Não edita a wiki.
