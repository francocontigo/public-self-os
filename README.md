# public-self-os

Template de um vault Obsidian operado pelo the coding agent: uma wiki de conhecimento mantida por LLM (padrão "LLM Wiki" do Karpathy) mais uma camada operacional para estudar com método, defender posições em público e publicar com regularidade. Sem dados pessoais, pronto para clonar e começar.

Três camadas, cada uma com um papel só:

| Camada | Pasta | Idioma | Guarda |
|---|---|---|---|
| Conhecimento | `wiki/` | inglês | o que você aprendeu, interligado, com cards de recall |
| Estado | `areas/` | português | o que você está estudando e por quê, o que vai publicar, decisões de trabalho, metas |
| Cronologia | `journal/` | português | o que aconteceu em cada dia e em cada semana |

A métrica central é produção pública que outras pessoas usam ou citam, com peso projeto > artigo longo > post. Cards revisados e páginas na wiki são meios, nunca o placar.

O contrato do agente está em `CLAUDE.md` (lido automaticamente em toda sessão). A spec completa está em `docs/personal-os-spec.md`.

---

## Primeiro uso (uma tarde)

Pré-requisitos: the coding agent CLI no PATH e logado, Python 3.10+, Obsidian apontando para a pasta. No Windows, uma vez: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` para o `./sb.ps1` rodar.

```
git clone https://github.com/francocontigo/public-self-os meu-vault
cd meu-vault
claude
```

Dentro da sessão, nesta ordem. Cada skill pergunta uma coisa por vez.

1. **Estratégia e voz.** Abra `areas/publico/estrategia.md` e `areas/publico/voz.md` com o agente e preencha: posicionamento, arquétipo, plataformas, pilares, regras de escrita. Marque `status: confirmada`. Todo post é checado contra `voz.md`.
2. **Frentes de trabalho e metas.** `/decisao nova` para cada frente do seu trabalho atual, criando `areas/trabalho/frentes/<frente>.md` com o contexto. Depois, `areas/pessoal/metas.md` com as metas do trimestre. O diagnóstico, as sessões aplicadas das trilhas e o `/dia` leem esses arquivos. Regra de `areas/trabalho/`: decisões e raciocínios, nunca dados pessoais de clientes ou funcionários. Pessoas aparecem pelo papel.
3. **`/tese nova <enunciado>`** para duas ou três posições que você defende. Posts e projetos nascem das teses, não só do que foi estudado.
4. **`/diagnostico`** (40 min). Entrevista sobre nove domínios de IA. Escreve `areas/estudos/gap-map.md` com nível e prioridade por domínio e propõe as duas primeiras trilhas. Vem depois da estratégia, das frentes e das teses porque as perguntas de aplicação usam as frentes e a prioridade de cada domínio pesa onde você vai falar em público.
5. **`/trilha nova <tema>`** para as trilhas propostas no diagnóstico. Cada trilha tem um artefato de saída (projeto, artigo ou post), fontes e um mapa de conceitos. Se o artefato for projeto, a skill já cria `areas/projetos/<slug>.md`.
6. **`/ingest <arquivo ou URL>`** nas primeiras fontes das trilhas. Cada ingest cria páginas na wiki e cards de recall.
7. **`/dia`** no dia seguinte. A partir daí vale a rotina abaixo.

Se o repositório for ficar no GitHub, torne-o privado antes de preencher `areas/pessoal/`, `areas/trabalho/` e `areas/rede/`.

---

## O que fazer todo dia

Abra um terminal na pasta do vault, digite `claude`, e rode:

1. **`/dia`** (5 min). Lê o estado e escreve `journal/<hoje>.md` com no máximo três itens: um de estudo, um de público, um livre.
2. **`/study`** (15 a 20 min). Repetição espaçada dos cards vencidos. Responda em texto livre, o agente corrige.
3. **Um dos dois**, alternando ao longo da semana, somando três ou quatro sessões por semana:
   - `/trilha continuar <slug>` (1 a 2 h). Sessão de estudo, alternando teoria e aplicação.
   - `/projeto continuar <slug>` (1 a 2 h). Avança o projeto público e registra o próximo passo.
4. **Um post** a partir do backlog com `/post <tema> x`. Você publica, o agente nunca publica. Depois: `/post publicado <slug> <url>`.
5. Ao longo do dia, capture no `raw/inbox.md` com marcador de área: `@estudo`, `@post`, `@trabalho <frente>`, `@pessoal`, `@tese`, `@projeto <slug>`, `@rede`. Sem marcador vai para a wiki. `/process-inbox` drena.

Para ver o estado sem abrir o agente: `make status` ou `./sb.ps1 status`.

## O que fazer toda semana

Sexta ou domingo, **`/semana`** (30 min). Abre pela produção pública do mês, pergunta quatro coisas, escreve `journal/semanas/<semana>.md`, define três focos para a semana seguinte (pelo menos um de produção pública) e gera três ideias de post.

Quando a semana apontar evidência nova para uma tese: `/tese revisar <slug>`. Quando quiser ser contestado: `/tese desafiar <slug>`.

A cada trimestre: `/diagnostico` para refazer o gap-map.

---

## Todos os comandos

Dentro da sessão `claude`:

| Comando | Faz |
|---|---|
| `/dia` | abre o dia, escreve o diário com plano de até três itens |
| `/semana` | revisão semanal, foco da próxima semana, ideias de post |
| `/study [N]` | repetição espaçada dos cards vencidos |
| `/trilha nova <tema>` · `continuar <slug>` · `listar` · `fechar <slug>` | trilhas de estudo com artefato de saída |
| `/projeto novo <nome>` · `continuar <slug>` · `publicar <slug>` · `listar` | projetos públicos |
| `/tese nova <enunciado>` · `revisar <slug>` · `desafiar <slug>` · `listar` | posições públicas |
| `/ideias [n]` | ideias de post a partir das teses, projetos e do que foi aprendido |
| `/post <tema> [x\|linkedin\|medium]` · `publicado <slug> <url>` · `resultado <slug>` | rascunha, registra, mede posts |
| `/decisao <frente>` | registra decisão de trabalho |
| `/diagnostico` | entrevista que refaz o gap-map |
| `/ingest <arquivo ou URL>` | ingere uma fonte na wiki e gera cards |
| `/process-inbox` | drena `raw/inbox.md` para a wiki e para as áreas |
| `/query <pergunta>` | responde a partir da wiki, salva em `output/` |
| `/explain <conceito>` | modo Feynman, você explica e o agente corrige |
| `/gaps` | plano de estudo ordenado pelo gap-map, em `output/study-plan.md` |
| `/lint` | saúde estrutural da wiki |

Fora da sessão (macOS e Linux com `make`, Windows com `./sb.ps1`), mesmos verbos: `status`, `dia`, `semana`, `study`, `trilha A="..."`, `projeto A="..."`, `tese A="..."`, `ideias`, `post A="..."`, `decisao A="..."`, `diagnostico`, `ingest SRC=...`, `process-inbox`, `query Q=...`, `lint`, `gaps`, `capture TEXT=...`. `make help` lista tudo.

`python scripts/os_status.py --human` imprime o estado determinístico (produção pública, cards, trilhas, posts, teses, projetos, inbox) sem LLM. As skills usam ele em vez de reler os arquivos. `python scripts/test_os_status.py` roda os testes.

---

## Como está organizado

```
raw/              fontes imutáveis; inbox.md para captura rápida
wiki/             conhecimento mantido pelo agente: sources, entities, concepts, synthesis, index, log
review/queue.md   deck de repetição espaçada (Leitner, contado em sessões)
areas/
  estudos/        gap-map.md e trilhas/<slug>.md
  teses/          uma tese por arquivo, _index.md
  projetos/       um projeto por arquivo, _index.md
  publico/        estrategia.md, voz.md, ideias.md, posts/<data>-<slug>.md
  rede/           mapa.md (só pessoas públicas, nome e handle, nada privado)
  trabalho/       frentes/<frente>.md e aprendizados.md (decisões, nunca dados pessoais)
  pessoal/        metas.md, habitos.md
journal/          YYYY-MM-DD.md e semanas/YYYY-Www.md
templates/        templates do Obsidian usados pelas skills
scripts/          os_status.py e teste
docs/             personal-os-spec.md
.claude/          commands/ (wiki) e skills/ (camada operacional)
```

Regras que o agente sempre segue: nunca edita `raw/`, toda página da wiki cita a fonte, tudo conecta por `[[wikilink]]`, `index.md` e `log.md` sempre atualizados, contradições são sinalizadas e nunca apagadas, datas reais via `date +%F`. `areas/trabalho/` e `areas/rede/` nunca recebem dados pessoais de terceiros.

## Só depois de duas semanas de rotina

Decidir se vale construir mais alguma coisa (dashboard, automações, Anki, UI). A regra é que uso precede ferramenta.
