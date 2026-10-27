---
name: decisao
description: Registra uma decisão ou aprendizado de trabalho em areas/trabalho/frentes/<frente>.md. Use quando o usuário tomar ou quiser documentar uma decisão em uma frente de trabalho.
argument-hint: <frente> (<frente existente> | nova)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*)
---

First read `CLAUDE.md`. Rode `date +%F`. Frente: `$ARGUMENTS`.

## LGPD (regra dura)
`areas/trabalho/` guarda decisões e raciocínios, nunca dados pessoais de criadores, clientes ou funcionários: nomes de pessoas físicas, e-mails, telefones, documentos, métricas individuais identificáveis. Pessoas aparecem pelo papel ("o CTO", "um criador da base"). Se o usuário colar dado pessoal, **recuse escrever aquele trecho**, explique em uma frase e registre a decisão sem o dado.

## Fluxo
1. Abra `areas/trabalho/frentes/<frente>.md`. Se não existe e o usuário pediu uma frente nova, crie com o mesmo formato das existentes (frontmatter `type: frente`, `status: ativa`, seções `## Contexto atual`, `## Decisões`, `## Aprendizados`, `## Pendências`, lembrete LGPD). Se não existe e ele não pediu, liste as frentes e pergunte.
2. Pergunte, **uma por vez**: contexto, opções consideradas, decisão, por quê, data de revisão.
3. Escreva em `## Decisões` um bloco no formato de `templates/decisao.md`:
```
### YYYY-MM-DD <título>
Contexto: ...
Opções: ...
Decisão: ...
Por quê: ...
Revisar em: YYYY-MM-DD
```
4. Se for um aprendizado e não uma decisão, escreva em `## Aprendizados` da frente (ou em `areas/trabalho/aprendizados.md` se for transversal).
5. Se a decisão contém conhecimento reutilizável (um conceito, uma técnica, uma referência), acrescente uma linha em `raw/inbox.md` para o `/process-inbox` levar à wiki, e deixe no bloco um `[[wikilink]]` para a página futura.

Não edita a wiki diretamente.
