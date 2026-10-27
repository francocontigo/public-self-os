---
name: entrevista
description: Primeira conversa do sistema com o usuário. Descobre campo de atuação, papel, frentes de trabalho, objetivo público e metas, e a partir disso escreve a estratégia, as frentes, as metas e os domínios que o /diagnostico vai examinar. Use na primeira sessão, antes de tudo, ou quando o usuário mudar de campo ou de objetivo.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(date:*)
---

First read `CLAUDE.md`. Rode `date +%F`.

Esta é a primeira conversa. O sistema não sabe nada sobre a pessoa e não assume campo nenhum: pode ser IA, direito, medicina, design, finanças, qualquer coisa. Tudo que vem depois (`/diagnostico`, trilhas, teses, posts) depende do que sair daqui.

## Entrevista (uma pergunta por vez, esperando a resposta)
1. Campo de atuação e papel atual. O que você faz, há quanto tempo, em que tipo de empresa ou contexto.
2. Frentes de trabalho atuais: as duas a quatro coisas pelas quais você responde hoje. Nome curto e uma frase cada. Sem nomes de clientes ou pessoas.
3. Objetivo público: pelo que você quer ser reconhecido em 12 a 18 meses, e por quem (que público, que empresas, que comunidade).
4. Onde você já publica ou quer publicar, em que idioma, com que frequência realista.
5. Quem escreve ou fala bem no seu campo, que você gostaria de soar parecido. Duas ou três referências.
6. Metas do trimestre: no trabalho e fora dele. No máximo cinco.
7. Autoavaliação: o que você já faz bem, e onde sente que falta base. Resposta livre.

Se a resposta vier curta, peça um exemplo concreto. Não corrija nem avalie. Anote.

## Domínios do campo
Com as respostas, proponha de sete a nove domínios que cobrem o campo da pessoa no nível em que ela quer ser referência. Cada domínio: nome curto para a tabela e, entre parênteses, três a cinco subtemas que o `/diagnostico` vai perguntar. Inclua sempre dois domínios transversais, no fim: o mercado e a história do campo (quem são os atores, o que já falhou, o que está em disputa) e comunicação pública e ensino (explicar bem, escrever, posicionar-se com evidência).

Mostre a lista inteira e pergunte o que tirar, juntar ou acrescentar. **Uma rodada.** Depois confirme.

## Saída
Escreva, com a data real:
- `areas/publico/estrategia.md`: posicionamento, arquétipo (quem a pessoa quer ser daqui a 12 a 18 meses), plataformas e cadência, pilares (três a seis temas derivados dos domínios e do objetivo), referências de voz, métricas que importam. `status: rascunho`.
- `areas/publico/voz.md`: mantenha as regras genéricas que já estão no arquivo e acrescente em `## Referências` as pessoas citadas na pergunta 5 e, em `## Regras`, o que a pessoa disse sobre como quer soar. `status: rascunho`.
- `areas/trabalho/frentes/<slug>.md` para cada frente, no formato de `/decisao` (frontmatter `type: frente`, `status: ativa`, seções `## Contexto atual` com a frase da pessoa, `## Decisões`, `## Aprendizados`, `## Pendências`, lembrete LGPD).
- `areas/pessoal/metas.md`: as metas em `## Metas`, uma linha cada, com prazo.
- `areas/estudos/gap-map.md`: a lista confirmada em `## Domínios` (numerada, nome e subtemas) e a tabela com uma linha vazia por domínio, só o nome na primeira coluna. `status: vazio`. Na linha de abertura do arquivo, troque "domínio de IA" pelo campo da pessoa.

Termine com três linhas: o que foi escrito, o que falta confirmar em `estrategia.md` e `voz.md`, e os dois próximos comandos: `/tese nova <enunciado>` para as posições que a pessoa já defende, depois `/diagnostico`.

Não edita a wiki.
