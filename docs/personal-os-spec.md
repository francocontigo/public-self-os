> Nota do template: spec original, escrita para o vault de origem. Referências a pastas legadas, a `app/` e ao conteúdo já existente da wiki não se aplicam a este repositório.

# Personal OS sobre o vault `obsidian-notes`: instruções para o agente

Este documento é a especificação de implementação para um agente (the coding agent) rodando dentro do vault `obsidian-notes`. Ele descreve o que já existe, o que construir por cima, e como verificar. Leia tudo antes de tocar em qualquer arquivo. O dono do vault é o usuário. Salve este arquivo em `docs/personal-os-spec.md` dentro do vault antes de começar, para que ele fique versionado junto com o que você construir.

Prompt sugerido para abrir a sessão no the coding agent, a partir da raiz do vault:

```
Leia docs/personal-os-spec.md e CLAUDE.md por completo. Execute a Fase 1 inteira, na ordem das seções 3 a 10, numa branch chamada personal-os. Não execute a Fase 2. Ao final, rode a verificação da seção 11 e me mostre o relatório.
```

---

## 0. O que já existe (leia antes de construir)

O vault já é um "second brain" no padrão LLM Wiki do Karpathy, com uma camada de estudo em cima. Não reconstrua nada disso. O trabalho é estender.

Estrutura atual:

- `raw/` é imutável (`inbox.md` para captura rápida, `assets/`). As pastas legadas `0 Notebook/`, `1 Books&Courses/`, `2 Files/`, `3 Templates/` também são fonte e não podem ser editadas.
- `wiki/` é mantida pelo agente, em inglês, dividida em `sources/`, `entities/`, `concepts/`, `synthesis/`, mais `index.md` (catálogo) e `log.md` (append-only). Toda página cita fonte em `## Source(s)`, conecta por `[[wikilink]]`, e páginas de `concepts/` e `synthesis/` terminam com `## Recall`.
- `review/queue.md` é o deck de repetição espaçada, Leitner com 5 caixas, intervalos contados em sessões, contador `session:` no topo. Está em `session: 0`, ou seja, a máquina de estudo existe mas nunca rodou.
- `output/` recebe respostas de `/query` e o plano de `/gaps`.
- `.claude/commands/` tem sete slash commands: `ingest`, `process-inbox`, `query`, `lint`, `study`, `gaps`, `explain`. Estão bem escritos. Mantenha-os.
- `CLAUDE.md` é o contrato do agente, em inglês. Ele é lido automaticamente em cada sessão.
- `Makefile` (macOS/Linux) e `sb.ps1` (Windows) são wrappers finos que chamam `claude -p "/comando"`.
- `app/` é uma UI Streamlit opcional com busca híbrida e RAG. Fora do escopo desta fase. Não modifique.
- Conteúdo real da wiki hoje: duas fontes ingeridas (SQL e estruturas de dados), 11 conceitos, 1 síntese, 9 cards. As notas legadas somam cerca de 400 palavras.

Problemas conhecidos que esta fase corrige:

- Os comandos dizem "you don't have today's date" e escrevem `date: unknown`. O agente tem Bash, portanto tem `date`. Isso passa a ser obrigatório.
- Não existe uma camada operacional. A wiki guarda conhecimento, mas nada guarda o estado da vida do usuário: o que ele está estudando e por quê, o que vai publicar, decisões de trabalho, metas pessoais. O `process-inbox` hoje deixa todos os "todos" no inbox porque não tem para onde mandá-los.
- Não existe um diagnóstico de lacunas nem a noção de trilha de estudo com começo, meio, fim e artefato de saída. O `/gaps` olha só para a saúde da wiki, não para o objetivo do usuário.
- Nada liga o que ele aprende ao que ele publica.

## 1. Objetivo e decisões de design (não negociáveis)

Objetivo do usuário: usar o agente como guia em todas as áreas da vida (estudos, trabalho, pessoal, imagem pública) para preencher lacunas e se tornar uma das maiores referências de IA do Brasil, com ambição de topo mundial. O vault é a única fonte de verdade. O the coding agent é o executor principal. O Cowork (Claude no desktop, com a pasta do vault conectada) deve conseguir operar o mesmo sistema lendo o mesmo `CLAUDE.md`.

Arquétipo e métrica. O sistema otimiza, nos próximos 12 a 18 meses, para o arquétipo "referência técnica que constrói e ensina em público" (Karpathy), porque é o que se constrói a partir da posição atual do usuário e é o que abre as portas do arquétipo "operador" (Altman) mais adiante. Por isso a métrica central do sistema não é quanto ele aprende, e sim quanto do que aprende vira produção pública que outras pessoas usam ou citam. Em ordem de peso: projeto que roda e é usado (código, benchmark, ferramenta, paper), artigo longo, post. Toda revisão semanal começa por essa métrica. Cards revisados e páginas na wiki são meios, nunca o placar.

Decisões:

1. Três camadas, cada uma com um papel só. Conhecimento vai para `wiki/` (em inglês, como já é). Estado operacional, planos e artefatos vão para `areas/` (em português). Cronologia vai para `journal/` (em português). Uma informação nunca mora em duas camadas, ela é referenciada por `[[wikilink]]`.
   Dentro de `areas/`, três áreas existem especificamente para o objetivo de referência: `teses/` (as posições que o usuário sustenta em público, com argumento, evidência e o que o faria mudar de ideia), `projetos/` (o que ele constrói em público) e `rede/` (com quem ele quer debater, aprender e colaborar, de forma deliberada). Posts nascem de teses e de projetos, não só do que foi estudado.
2. O padrão Karpathy continua valendo para a wiki: `raw/` imutável, o agente mantém a wiki, `index.md` e `log.md` sempre atualizados, contradições sinalizadas e nunca apagadas.
3. Novos procedimentos nascem como skills em `.claude/skills/<nome>/SKILL.md`, porque skills aceitam arquivos de apoio (templates, scripts) e podem ser invocadas tanto por `/nome` quanto pela descrição. Os sete commands existentes ficam onde estão. Não migre commands para skills nesta fase.
4. O que é determinístico vira script, e o modelo apenas orquestra. Contagem de cards vencidos, listagem de trilhas ativas, posts por status, data de hoje: tudo isso vem de um script Python em `scripts/`, não da leitura do modelo.
5. Comece pequeno. Esta fase entrega o esqueleto, o contrato, as skills e os templates. Ela não cria dashboards, não cria automações agendadas, e não produz conteúdo de estudo. O conteúdo nasce na Fase 2, em sessões interativas com o usuário.
6. Privacidade e LGPD. A área `trabalho/` guarda decisões, raciocínios e aprendizados, nunca dados pessoais de criadores, clientes ou funcionários da empresa (nomes de pessoas físicas, e-mails, telefones, documentos, métricas individuais identificáveis). Quando o contexto exigir uma pessoa, use o papel (por exemplo "o CTO", "um criador da base"). Essa regra entra no `CLAUDE.md` e em toda skill que escreve em `areas/trabalho/`. A área `rede/` segue o mesmo princípio de minimização: só pessoas com presença pública, identificadas por nome e handle público, com o motivo do interesse e o histórico de interações públicas. Nada de contato privado, nada de avaliação pessoal, nada sobre a vida da pessoa.

## 2. Pré-requisito que só o usuário decide (não execute, apenas sinalize)

O repositório `o repositório` é público hoje. Com `areas/pessoal/`, `areas/trabalho/` e `areas/rede/` dentro dele, ele passa a conter metas pessoais, decisões de produto da empresa e um mapa de relações. Antes de o usuário começar a usar o sistema, uma destas opções precisa ser escolhida:

- Tornar o repositório privado (`gh repo edit <usuario>/<repo> --visibility private`). É a opção mais simples e a recomendada.
- Manter público e adicionar `areas/pessoal/`, `areas/trabalho/` e `areas/rede/` ao `.gitignore`, aceitando que essas áreas não terão backup via git.

Não execute nenhuma das duas. Inclua este ponto no relatório final como a primeira pendência.

## 3. Estrutura de pastas a criar

Crie apenas as pastas e os arquivos listados. Arquivos marcados como "semente" recebem o conteúdo descrito na seção 9. Os demais nascem apenas com cabeçalho e frontmatter.

```
docs/
  personal-os-spec.md              # este documento

areas/
  estudos/
    gap-map.md                     # mapa de lacunas (preenchido pelo /diagnostico na Fase 2)
    trilhas/                       # uma trilha por tema, criadas pelo /trilha
      .gitkeep
  publico/
    estrategia.md                  # semente: posicionamento, plataformas, cadência, pilares
    voz.md                         # semente: regras de voz e estilo
    ideias.md                      # backlog de ideias de post
    posts/                         # um arquivo por post, criados pelo /post
      .gitkeep
  teses/
    _index.md                      # lista das teses com status (rascunho / sustentada / revisada / abandonada)
    .gitkeep                       # uma tese por arquivo, criadas pelo /tese
  projetos/
    _index.md                      # lista dos projetos públicos com status
    .gitkeep                       # um projeto por arquivo, criados pelo /projeto
  rede/
    mapa.md                        # semente: estrutura vazia (ver regra de minimização na seção 1)
  trabalho/
    frentes/
      <frente>.md                # semente: estrutura vazia
      atribuicao.md                # semente: estrutura vazia
      pricing.md                   # semente: estrutura vazia
    aprendizados.md                # o que o trabalho ensinou e ainda não virou wiki
  pessoal/
    metas.md
    habitos.md

journal/
  .gitkeep                         # YYYY-MM-DD.md criados pelo /dia
  semanas/
    .gitkeep                       # YYYY-Www.md criados pelo /semana

templates/                         # novos templates do Obsidian (a pasta "3 Templates" é legado, não mexa)
  diario.md
  semana.md
  trilha.md
  post.md
  decisao.md
  tese.md
  projeto.md

scripts/
  os_status.py                     # estado determinístico do sistema (seção 6.0)

.claude/skills/
  diagnostico/SKILL.md
  trilha/SKILL.md
  dia/SKILL.md
  semana/SKILL.md
  ideias/SKILL.md
  post/SKILL.md
  decisao/SKILL.md
  tese/SKILL.md
  projeto/SKILL.md
```

Convenções de arquivo nas novas camadas: nomes em minúsculas com hífen, frontmatter YAML sempre presente com pelo menos `type:` e `status:` (para Dataview futuro e para o `os_status.py`), texto em português, termos técnicos em inglês, wikilinks para a wiki quando o assunto já tem página lá.

## 4. Mudanças no `CLAUDE.md`

Não reescreva o arquivo. Faça três alterações cirúrgicas.

4.1. Atualize o bloco "Folder map" para incluir `areas/`, `journal/`, `templates/`, `scripts/` e `docs/`, com um comentário de uma linha cada, no mesmo estilo do bloco atual.

4.2. Acrescente, depois da seção "Learning layer (study pipeline)" e antes de "Commands available", uma nova seção. Escreva em inglês, para manter o contrato uniforme. O conteúdo deve cobrir exatamente estes pontos:

```
## Operational layer (areas/ + journal/)
The wiki stores KNOWLEDGE. The operational layer stores STATE: what o usuário is studying and why, what he
will publish, work decisions, personal goals, and the chronology of all of it.

- `areas/estudos/`   gap-map.md (skill levels per AI domain) and trilhas/<slug>.md (one study track each).
- `areas/teses/`     one file per public position o usuário holds: argument, evidence, what would change his
                     mind, revision history. Posts and articles are born here, not only from study.
- `areas/projetos/`  one file per public project (code, benchmark, tool, paper): goal, status, what shipped,
                     who uses it. The strongest form of public output.
- `areas/publico/`   estrategia.md, voz.md, ideias.md (post backlog) and posts/<date>-<slug>.md.
- `areas/rede/`      mapa.md: people with a public presence o usuário wants to debate, learn from or work with.
                     Name + public handle + why + public interactions only. Nothing private about anyone.
- `areas/trabalho/`  frentes/<front>.md (decisions and learnings per work front) and aprendizados.md.
- `areas/pessoal/`   metas.md and habitos.md.
- `journal/`         one note per day (YYYY-MM-DD.md) and one per week (semanas/YYYY-Www.md).

Routing rule: a reusable idea, concept or fact goes to the wiki (via raw/inbox.md or /ingest). A plan, a
status, a decision or an artifact goes to areas/. What happened on a given day goes to journal/. Never
duplicate; link with [[wikilinks]].

North-star metric: public output that other people use or cite, weighted project > long article > post.
The weekly review opens with it. Cards reviewed and wiki pages are means, never the score.

Language: wiki in English (unchanged). areas/ and journal/ in Portuguese, technical terms in English.

Dates: you DO have the date. Run `date +%F` (Bash) at the start of any operation that writes a date and
use it in log.md, journal/, posts and track sessions. Never write `date: unknown` again.

Privacy (LGPD): areas/trabalho/ holds decisions and reasoning, never personal data of creators, clients
or employees (names of natural persons, emails, phones, IDs, individually identifiable metrics). Refer
to people by role. If o usuário pastes such data, keep it out of the file and say so.

Deterministic state comes from `python scripts/os_status.py` (due cards, active tracks, posts by status,
today's date). Skills call it instead of recomputing by reading files.
```

4.3. Na seção "Commands available", acrescente ao final a lista das nove skills novas com uma linha cada (os nomes e descrições estão na seção 6).

## 5. Correções nos commands existentes

5.1. Datas. Em `ingest.md`, `process-inbox.md`, `lint.md`, `study.md`, `explain.md` e `gaps.md`: adicione `Bash(date:*)` a `allowed-tools` e substitua a instrução sobre data desconhecida por "run `date +%F` and use the real date". Em `wiki/log.md` o formato continua `- [date] operation — source — pages touched`, agora com data real.

5.2. Roteamento do inbox. Em `process-inbox.md`, substitua a regra "A pure todo/reminder with no knowledge value → leave it in the inbox" por roteamento por marcador. Um item do inbox pode começar com um marcador de área:

- `@estudo <texto>` vai para `## Inbox` em `areas/estudos/gap-map.md` (ou para a trilha ativa, se o texto citar seu slug).
- `@post <texto>` vira uma entrada em `areas/publico/ideias.md` com status `ideia` e data.
- `@trabalho <frente> <texto>` vai para `## Pendências` em `areas/trabalho/frentes/<frente>.md`, ou para `aprendizados.md` se for um aprendizado e não uma pendência.
- `@pessoal <texto>` vai para `## Pendências` em `areas/pessoal/metas.md`.
- `@tese <texto>` vai para `## Candidatas` em `areas/teses/_index.md` (uma posição ainda não formalizada) ou para `## Evidência` da tese citada pelo slug.
- `@projeto <slug> <texto>` vai para `## Log` do projeto, ou para `## Candidatos` em `areas/projetos/_index.md` se o projeto não existe.
- `@rede <texto>` vai para `## Inbox` em `areas/rede/mapa.md`, respeitando a regra de minimização da seção 1.
- Sem marcador, o comportamento atual continua: conhecimento vai para a wiki, e um todo sem área fica no inbox com aviso.

Itens com marcador também passam pelo teste de conhecimento: se contêm um conceito reutilizável, o conceito vai para a wiki e o item operacional vai para a área, com link entre os dois.

5.3. `gaps.md`. Além da auditoria atual da wiki, o comando deve ler `areas/estudos/gap-map.md` e as trilhas ativas, e o plano em `output/study-plan.md` passa a ser ordenado pelas prioridades do gap-map, não só pela saúde da wiki.

5.4. `study.md`. No início da sessão, imprima o estado vindo de `scripts/os_status.py` (cards vencidos e trilha ativa) e, ao final, se alguma trilha ativa tiver cards com desempenho ruim, sugira `/trilha continuar <slug>`.

## 6. Scripts e skills novas

Toda skill começa com "First read `CLAUDE.md`", roda `date +%F` quando escreve datas, e termina com uma linha em `wiki/log.md` quando toca a wiki (operações que só tocam `areas/` ou `journal/` não precisam logar na wiki). Toda skill tem frontmatter com `name`, `description` (uma frase que descreve quando usar, porque a descrição é o gatilho), `argument-hint` quando recebe argumento, e `allowed-tools` mínimos. Skills interativas fazem uma pergunta por vez e esperam a resposta.

### 6.0. `scripts/os_status.py`

Python 3.10+, sem dependências externas, roda da raiz do vault ou de qualquer lugar (resolva o vault pela posição do próprio script). Imprime JSON em stdout com:

- `today` (YYYY-MM-DD) e `week` (YYYY-Www, ISO).
- `review`: `session`, `total_cards`, `due_now` (cards com `due <= session + 1`, porque `/study` incrementa antes de selecionar), `box_distribution` (contagem por caixa), `stuck_box1` (slugs de cards em box 1 que já aparecem no histórico de erro, se houver).
- `tracks`: lista de trilhas em `areas/estudos/trilhas/` com `slug`, `status`, `scope`, `last_session` (data da última sessão registrada) e `next_step` (texto da linha "Próximo passo" mais recente).
- `posts`: contagem por `status` e lista dos que estão em `rascunho` ou `agendado` com `slug`, `platform` e `date`.
- `teses`: contagem por `status` e lista das `sustentada` com `slug`, `updated` e número de posts/projetos que a citam.
- `projetos`: contagem por `status` (`ideia`, `em-andamento`, `publicado`, `arquivado`) e lista dos `em-andamento` com `slug`, `last_log` e `next_step`.
- `producao_publica`: para o mês corrente e o anterior, contagem de projetos publicados, artigos (posts com `platform: medium` ou `linkedin` e `kind: artigo`) e posts publicados. É a métrica central e deve vir primeiro no modo `--human`.
- `journal`: data do último diário e da última semana.
- `inbox_items`: quantidade de linhas não vazias e não comentadas em `raw/inbox.md`.

Parse de frontmatter simples (chave: valor entre `---`), sem YAML completo. Com `--human` imprime um resumo legível em vez de JSON. Escreva testes mínimos em `scripts/test_os_status.py` usando apenas `unittest` e um vault temporário de exemplo.

### 6.1. `/diagnostico`

Descrição: entrevista diagnóstica que mapeia o nível do usuário em cada domínio de IA e escreve `areas/estudos/gap-map.md`. Rode na primeira vez e a cada trimestre.

Interativa. Domínios (nesta ordem, cada um com nome curto para o gap-map):

1. Fundamentos de ML e otimização (viés/variância, regularização, gradiente, generalização)
2. Transformers e pré-treino (atenção, tokenização, scaling laws, dados)
3. Pós-treino e RL (SFT, RLHF, DPO, GRPO, reward models)
4. Avaliação e evals (benchmarks, evals de produto, LLM-as-judge, estatística de avaliação)
5. Busca, retrieval e representação (embeddings, BM25, rerank, RAG, avaliação de busca)
6. Inferência, infra e custo (quantização, serving, latência, caching, custos)
7. Agentes e sistemas (tool use, orquestração, memória, falhas típicas)
8. Mercado, estratégia e história da área (labs, modelos de negócio, o que já falhou, o que está em disputa)
9. Comunicação pública e ensino (explicar bem, escrever, posicionar-se com evidência)

Para cada domínio, faça de duas a três perguntas em escada: uma conceitual, uma de aplicação ("como você faria X no sua frente de trabalho?"), uma de fronteira ("o que está em aberto aqui?"). Não revele a resposta esperada. Depois das respostas, atribua um nível com evidência de uma linha: `ausente`, `superficial`, `funcional`, `forte`. Seja honesto, a utilidade do mapa depende disso. O o usuário é sênior e não deve ser tratado como iniciante, mas também não deve receber nível inflado.

Saída: `areas/estudos/gap-map.md` com frontmatter (`type: gap-map`, `updated:`), uma tabela com domínio, nível, evidência, prioridade (alta/média/baixa, considerando o objetivo de referência pública, ou seja, domínios onde ele vai falar em público pesam mais) e trilha vinculada (vazia no início), seguida de uma seção `## Histórico` onde cada rodada do diagnóstico acrescenta uma linha com data e resumo, nunca apagando as anteriores. Termine propondo as duas primeiras trilhas e pergunte se o usuário quer criá-las com `/trilha nova`.

Não edita a wiki.

### 6.2. `/trilha`

Descrição: cria, continua, lista e encerra trilhas de estudo em `areas/estudos/trilhas/`. Subcomandos: `nova <tema>`, `continuar <slug>`, `listar`, `fechar <slug>`.

`nova <tema>`: pergunta, uma de cada vez, a motivação (o que ele quer conseguir fazer ou dizer ao final), as horas por semana, e o artefato de saída. A ordem de preferência do artefato é projeto público (código, benchmark, ferramenta, paper) primeiro, artigo longo depois, post por último, e a skill deve propor a opção mais forte que couber no escopo e só aceitar post como artefato de trilha `quick`. Se o artefato for projeto, cria também o arquivo em `areas/projetos/` via a lógica de `/projeto novo` e linka os dois. Pergunta também qual tese a trilha sustenta ou testa, se houver, e linka. Classifica o escopo em `quick` (menos de 5 h), `standard` (5 a 20 h) ou `deep` (mais de 20 h). Cria `areas/estudos/trilhas/<slug>.md` a partir de `templates/trilha.md`, vincula ao domínio do gap-map (e escreve o slug na coluna "trilha" do gap-map), propõe de três a seis fontes (livros, papers, cursos, posts) com uma linha de justificativa cada, e sugere qual ingerir primeiro com `/ingest`. Para fontes que são URLs, não ingere automaticamente, apenas lista.

`continuar <slug>`: lê a trilha e decide o tipo da sessão. A regra é alternar teoria e aplicação, e nunca duas sessões de teoria seguidas. Sessão de teoria: aula socrática sobre o próximo conceito do mapa da trilha, apoiada nas páginas da wiki (se a página não existe, propõe ingerir a fonte antes). Sessão aplicada: um exercício conectado ao trabalho atual do usuário (as frentes em `areas/trabalho/frentes/`) ou ao artefato de saída da trilha. Toda sessão abre com duas ou três perguntas de recall sobre sessões anteriores da trilha e fecha registrando em `## Sessões` a data, o tipo, o que foi feito, o que ficou fraco e o próximo passo (linha começando com `Próximo passo:` para o script achar). Conceitos novos ganham `## Recall` na wiki e cards em `review/queue.md`, seguindo o mecanismo já existente.

`listar`: imprime a saída de `os_status.py` filtrada em trilhas.

`fechar <slug>`: só fecha se duas condições forem satisfeitas. Primeira, um teste de Feynman sobre o escopo inteiro da trilha, com o usuário explicando o domínio como se ensinasse, e o agente pontuando clareza, completude e precisão (reaproveite o fluxo de `/explain`). Segunda, o artefato de saída existe e está linkado na trilha (um post em `areas/publico/posts/`, um arquivo em `output/`, ou uma URL). Se passar, muda `status: concluida`, registra a nota em `## Encerramento`, atualiza o nível no gap-map (perguntando antes de mudar), e loga na wiki.

### 6.3. `/dia`

Descrição: abre o dia. Lê o estado e escreve o diário de hoje com um plano de no máximo três itens.

Roda `os_status.py`. Lê o diário anterior (seção `## Fechamento`, se preenchida) e as pendências das áreas. Propõe no máximo três itens para hoje, no geral um de estudo (cards vencidos ou sessão de trilha), um de público (rascunho ou post do dia) e um livre (trabalho ou pessoal). Cria `journal/YYYY-MM-DD.md` a partir de `templates/diario.md` com `## Plano` preenchido, `## Notas` e `## Fechamento` vazios. Se o diário de hoje já existe, apenas mostra o plano e pergunta se quer ajustar. Não edita a wiki. Não incrementa o contador de sessão (isso é do `/study`).

### 6.4. `/semana`

Descrição: revisão semanal que olha todas as áreas juntas, escreve `journal/semanas/YYYY-Www.md` e define o foco da próxima semana.

Lê os diários dos últimos sete dias, as entradas de `wiki/log.md` da semana, o `os_status.py` (produção pública do mês, distribuição das caixas e cards travados), as sessões das trilhas na semana, os projetos em andamento, as teses sustentadas, os posts publicados na semana e seus resultados, o mapa de rede e o gap-map. A nota semanal abre obrigatoriamente pela métrica central, o que saiu em público esta semana e este mês (projetos, artigos, posts) e quem usou ou citou, antes de qualquer outra seção. Faz no máximo quatro perguntas ao usuário, uma de cada vez: o que saiu em público e teve resposta, o que funcionou, o que travou, e com quem ele falou ou deveria ter falado (esta alimenta `areas/rede/mapa.md`). Escreve a nota semanal com: produção pública (primeiro), o que aconteceu por área, teses que ganharam ou perderam evidência na semana, o que foi aprendido e ainda não está na wiki (cada item vira uma linha em `raw/inbox.md` para o `/process-inbox`), mudanças propostas no gap-map (pergunta antes de alterar níveis), foco da próxima semana com no máximo três itens, dos quais pelo menos um é de produção pública, e três ideias de post derivadas das teses e do que foi aprendido (acrescentadas em `areas/publico/ideias.md`, reaproveitando a lógica de `/ideias`). Se o mês corrente ainda não tem nenhum projeto ou artigo publicado, a nota diz isso explicitamente no topo. Loga na wiki se tocou nela.

### 6.5. `/ideias [n]`

Descrição: gera ideias de post a partir do que o usuário aprendeu recentemente e da estratégia pública. Padrão: cinco ideias.

Lê `areas/publico/estrategia.md`, `voz.md`, `ideias.md` (para não repetir), as teses em `areas/teses/` (fonte primária), os projetos em `areas/projetos/`, as páginas da wiki tocadas nos últimos 14 dias (via `log.md`), as sessões recentes das trilhas e os diários da semana. Pelo menos três das cinco ideias devem sustentar, testar ou provocar uma tese existente, e pelo menos uma deve sair de um projeto (o que ele construiu, o que descobriu construindo). Cada ideia traz: título de trabalho, ângulo em duas frases, por que agora, justificativa (por que isso serve ao posicionamento), a tese ou projeto de origem, plataforma sugerida e wikilinks das páginas que sustentam. Os temas devem ser expansivos, sobre o mercado e a área, não sobre o trabalho passado do usuário nem sobre os projetos dele. Acrescenta as ideias em `## Backlog` de `ideias.md` com data e `status: ideia`. Não edita a wiki.

### 6.6. `/post`

Descrição: escreve, acompanha e fecha posts em `areas/publico/posts/`. Subcomandos: `<ideia ou tema> [x|linkedin|medium]`, `publicado <slug> <url>`, `resultado <slug>`.

Escrever: lê `voz.md` e `estrategia.md` (obrigatório), a ideia no backlog se existir, a tese ou o projeto de origem, e as páginas da wiki relevantes. Cria `areas/publico/posts/YYYY-MM-DD-<slug>.md` a partir de `templates/post.md` com duas versões (uma curta, uma longa), `status: rascunho`, `kind: post` ou `kind: artigo`, e os campos `thesis:` e `project:` preenchidos quando houver origem. Quando o post é publicado, a tese de origem ganha uma linha em `## Onde foi sustentada` e o projeto ganha uma linha em `## Divulgação`. As regras de voz de `voz.md` são regras duras, não sugestões. O agente nunca publica, só o usuário publica. Se a ideia veio do backlog, muda o status dela para `rascunho` e linka o post.

`publicado <slug> <url>`: atualiza `status: publicado`, `url` e `published:`. `resultado <slug>`: pergunta os números que o usuário quer registrar (impressões, reações, respostas, o que chamou atenção) e escreve em `## Resultado`, sem inventar métricas.

### 6.7. `/decisao <frente>`

Descrição: registra uma decisão ou aprendizado de trabalho em `areas/trabalho/frentes/<frente>.md`. Frentes iniciais: `smartmatch`, `atribuicao`, `pricing`. Uma frente nova é criada se o usuário pedir.

Interativa: contexto, opções consideradas, decisão, por quê, data de revisão. Escreve um bloco em `## Decisões` com data. Se a decisão contém conhecimento reutilizável (um conceito, uma técnica, uma referência), acrescenta uma linha em `raw/inbox.md` para o `/process-inbox` levar à wiki, e linka. Regra LGPD da seção 1 aplicada à risca, com recusa explícita e explicação curta se aparecer dado pessoal.

### 6.8. `/tese`

Descrição: cria, revisa e lista as posições que o usuário sustenta em público, em `areas/teses/`. Subcomandos: `nova <enunciado>`, `revisar <slug>`, `listar`, `desafiar <slug>`.

`nova <enunciado>`: pergunta, uma de cada vez, o enunciado em uma frase (uma tese é uma afirmação sobre o mundo que pode estar errada, não um tema), o argumento em um parágrafo, a evidência que ele tem hoje (com wikilinks quando a evidência já está na wiki), o que o faria mudar de ideia, e quem no mercado discorda e por quê. Cria `areas/teses/<slug>.md` a partir de `templates/tese.md` com `status: rascunho` e registra em `_index.md`. Uma tese só passa a `sustentada` depois de ter sido publicada ao menos uma vez (um post, artigo ou projeto linkado em `## Onde foi sustentada`).

`revisar <slug>`: lê a tese, as páginas da wiki ligadas a ela e o que foi ingerido desde a última revisão, e pergunta se a evidência nova fortalece, enfraquece ou muda a tese. Acrescenta uma linha datada em `## Revisões` com o que mudou. Se o usuário decidir que a tese caiu, muda para `abandonada` e escreve por quê, sem apagar nada, porque mudar de ideia em público com registro é parte do posicionamento.

`desafiar <slug>`: o agente assume o melhor argumento contrário e debate com o usuário, uma rodada por vez, até no máximo cinco rodadas. Ao final, registra em `## Objeções` as objeções que ficaram sem resposta boa. Não edita a tese sem o usuário pedir.

`listar`: imprime a saída de `os_status.py` filtrada em teses, com o número de vezes que cada uma foi sustentada em público.

Não edita a wiki, mas manda para `raw/inbox.md` qualquer fato novo que apareceu no debate.

### 6.9. `/projeto`

Descrição: cria e acompanha projetos públicos em `areas/projetos/`, que são a forma mais forte de produção pública. Subcomandos: `novo <nome>`, `continuar <slug>`, `publicar <slug>`, `listar`.

`novo <nome>`: pergunta, uma de cada vez, o que o projeto demonstra ou resolve, qual tese ele sustenta ou testa (se houver), qual trilha ele exercita (se houver), quem é o usuário ou leitor, qual é a menor versão que já vale publicar, e onde vai viver (repositório, artigo, benchmark público). Cria `areas/projetos/<slug>.md` a partir de `templates/projeto.md` com `status: ideia` e registra em `_index.md`. Recusa escopo que não tenha uma primeira versão publicável em até quatro semanas, pedindo para reduzir.

`continuar <slug>`: lê o projeto, pergunta o que foi feito desde a última vez, registra em `## Log` com data, e termina definindo a linha `Próximo passo:` (que o `os_status.py` lê). Se o trabalho produziu um aprendizado reutilizável, ele vai para `raw/inbox.md`. Se o usuário pedir ajuda técnica na sessão, o agente ajuda, mas o código do projeto vive no repositório do projeto, não no vault.

`publicar <slug>`: registra URL, data e o que foi publicado, muda `status: publicado`, sugere a divulgação (`/post` com `project:` apontando para ele) e, se o projeto sustenta uma tese, acrescenta a linha em `## Onde foi sustentada` da tese. Depois, cada menção, uso ou citação externa que o usuário quiser registrar vai em `## Uso e citações`, sem inventar nada.

`listar`: imprime a saída de `os_status.py` filtrada em projetos e produção pública do mês.

## 7. Templates e configuração do Obsidian

Crie os cinco templates em `templates/` com frontmatter e seções exatamente como as skills esperam. Os campos mínimos:

- `diario.md`: frontmatter `type: diario`, `date:`. Seções `## Plano`, `## Notas`, `## Fechamento`.
- `semana.md`: frontmatter `type: semana`, `week:`. Seções `## O que aconteceu` (com subtítulos por área), `## Aprendizados para a wiki`, `## Gap-map`, `## Foco da próxima semana`, `## Ideias de post`.
- `trilha.md`: frontmatter `type: trilha`, `status: ativa`, `scope:`, `started:`, `domain:`, `artifact:`. Seções `## Motivação e resultado esperado`, `## Escopo (entra / fica fora)`, `## Fontes`, `## Mapa de conceitos`, `## Sessões`, `## Artefato`, `## Encerramento`.
- `post.md`: frontmatter `type: post`, `kind: post`, `status: rascunho`, `platform:`, `date:`, `published:`, `url:`, `track:`, `idea:`, `thesis:`, `project:`. Seções `## Ideia e justificativa`, `## Versão curta`, `## Versão longa`, `## Versão final`, `## Resultado`.
- `decisao.md`: bloco com `### YYYY-MM-DD <título>`, e linhas `Contexto`, `Opções`, `Decisão`, `Por quê`, `Revisar em`.
- `tese.md`: frontmatter `type: tese`, `status: rascunho`, `created:`, `updated:`. Seções `## Enunciado`, `## Argumento`, `## Evidência`, `## O que me faria mudar de ideia`, `## Quem discorda e por quê`, `## Objeções`, `## Onde foi sustentada`, `## Revisões`.
- `projeto.md`: frontmatter `type: projeto`, `status: ideia`, `created:`, `published:`, `url:`, `thesis:`, `track:`. Seções `## O que demonstra ou resolve`, `## Usuário ou leitor`, `## Menor versão publicável`, `## Log`, `## Divulgação`, `## Uso e citações`.

Configuração do Obsidian, editando só o necessário:

- `.obsidian/templates.json`: mude `folder` para `templates`. A pasta `3 Templates` permanece intocada.
- Crie `.obsidian/daily-notes.json` com `{"folder": "journal", "format": "YYYY-MM-DD", "template": "templates/diario"}` para o plugin core de daily notes (já ativado) abrir no lugar certo.

## 8. `Makefile` e `sb.ps1`

Acrescente verbos para as skills novas, seguindo o padrão existente. Interativas (sem `-p`): `diagnostico`, `trilha`, `dia`, `semana`, `decisao`, `tese`, `projeto`. Headless (com `-p`): `ideias`, `post` quando for só escrever rascunho, `status` (roda `python scripts/os_status.py --human`, sem o agente). Atualize o `help` dos dois arquivos. Mantenha os dois espelhados.

## 9. Conteúdo semente

Escreva estes arquivos como rascunho para o usuário confirmar. Não invente fatos sobre o trabalho dele. Marque no topo de cada um `status: rascunho-para-confirmar`.

`areas/publico/estrategia.md`:

- Posicionamento: referência pública em IA, provocativa mas palatável, do tipo que YC, big techs e labs de IA querem por perto. Nunca se posicionar como júnior nem como quem sofre o problema que critica. Falar como quem opera e decide.
- Plataformas e cadência: X (@seu-handle), um post por dia, iniciado em outubro de 2026, com X Premium (posts podem passar de 280 caracteres, mas devem continuar curtos). LinkedIn para artigos sobre engenharia de IA (evals, o papel do AI engineer, empresas usando IA mal), com o link do artigo nos comentários. Medium (@seu-handle) para os artigos longos.
- Arquétipo: referência técnica que constrói e ensina em público nos próximos 12 a 18 meses, preparando a virada para operador. Posts e artigos nascem de teses e projetos.
- Pilares (a confirmar com o usuário): engenharia de IA na prática, busca e representação, avaliação, o mercado de IA visto por quem opera, aprendizado e ensino em IA.
- Referências de voz: Karpathy, Sam Altman, ensaios estilo YC.
- Seção `## Métricas que importam` já preenchida com a métrica central (produção pública usada ou citada, peso projeto > artigo > post) e com espaço para o usuário acrescentar as de plataforma.

`areas/teses/_index.md` e `areas/projetos/_index.md`: frontmatter, título, uma tabela vazia com slug, status e data, e as seções `## Candidatas` (teses) e `## Candidatos` (projetos) para o inbox alimentar.

`areas/rede/mapa.md`: frontmatter `type: rede`, um lembrete de uma linha da regra de minimização, e as seções `## Quero debater`, `## Quero aprender com`, `## Quero colaborar`, `## Interações públicas` (log datado) e `## Inbox`. Tudo vazio.

`areas/publico/voz.md`, regras duras de estilo para tudo que for escrito em nome do usuário:

- Prosa limpa e fluida, narrativa, agradável de ler. Frases completas, não sentenças curtas e secas.
- Sem travessão (em-dash). Usar vírgula ou dividir a frase.
- Sem ponto e vírgula dentro de frases.
- Sem dispositivos aforísticos de fragmento curto no meio do texto (exemplo do que evitar: "Trilho, não muro."). Dizer o ponto em frase completa.
- Sem encenação de dois-pontos seguido de revelação ("o detalhe que faz tudo valer: ..."). Dois-pontos apenas para introduzir lista ou exemplo.
- Sem conclusões curtas e impactantes que saltam para um fecho dramático. Sem linhas de veredito como "A ideia é simples e verdadeira." Sem estrutura "se X, então Y" ou "o rótulo foi X, mas...".
- Voz: mistura de Karpathy, Sam Altman e o próprio usuário. Ensaio estilo YC com inspiração em Karpathy.
- Nunca enquadrar o usuário como júnior, aprendiz, ou alguém que está do lado de quem sofre o problema.
- Em texto, a empresa se escreve "o a empresa" (masculino, uma palavra).
- Temas de post são expansivos, sobre o mercado e a área, não sobre projetos passados do usuário.

`areas/trabalho/frentes/{<frente>}.md`: frontmatter `type: frente`, `status: ativa`, uma linha de descrição a confirmar (sua frente de trabalho: busca semântica e representação de criadores. Atribuição: medição e atribuição. Pricing: precificação), seções `## Contexto atual`, `## Decisões`, `## Aprendizados`, `## Pendências`, e um lembrete de uma linha da regra LGPD.

`areas/trabalho/aprendizados.md`, `areas/pessoal/metas.md`, `areas/pessoal/habitos.md`, `areas/publico/ideias.md`, `areas/estudos/gap-map.md`: apenas frontmatter, título, e as seções que as skills esperam (`## Backlog` em ideias, `## Pendências` em metas, tabela vazia e `## Histórico` no gap-map).

## 10. O que não fazer

- Não edite, mova ou apague nada em `raw/`.
- Não reescreva `wiki/log.md`, apenas acrescente.
- Não migre os commands existentes para skills, não os apague, não renomeie.
- Não toque em `app/` nem em `app/requirements.txt`.
- Não crie dashboards, hooks, automações agendadas, nem integrações externas (Anki, Notion, etc.).
- Não rode `/diagnostico`, `/trilha nova`, `/tese nova`, `/projeto novo` nem `/ideias` nesta fase. Eles dependem do usuário presente.
- Não faça `git push`. Trabalhe na branch `personal-os`, faça commits pequenos com mensagens claras, e deixe o usuário revisar e mesclar.
- Não escreva dados pessoais de terceiros em lugar nenhum.

## 11. Verificação (obrigatória antes do relatório)

1. `git diff --stat main..personal-os` não mostra nenhum arquivo em `raw/`, nas pastas legadas, em `app/`, nem reescrita de `wiki/log.md` (apenas linhas acrescentadas).
2. `python scripts/os_status.py` roda sem erro e imprime JSON válido com todas as chaves da seção 6.0. `python -m unittest scripts/test_os_status.py` passa.
3. Cada um dos nove `SKILL.md` tem frontmatter válido com `name` e `description`, e cada um é listado no `CLAUDE.md`.
4. Os templates contêm exatamente as seções que as skills referenciam (confira skill por skill).
5. `/lint` roda limpo, ou lista apenas problemas que já existiam antes desta fase.
6. `/dia` executado uma vez, de verdade, cria `journal/<hoje>.md` com um plano coerente a partir de um vault quase vazio (deve dizer que não há trilhas e sugerir `/diagnostico`). Apague esse diário de teste antes do commit final, ou mantenha-o se o usuário preferir.
7. `make help` e `./sb.ps1 help` listam os verbos novos.

Relatório final, em português, com: lista de arquivos criados e alterados, pendência número um (visibilidade do repositório, seção 2), o que foi deixado como rascunho para confirmar (seção 9), e o roteiro da Fase 2 abaixo.

## 12. Fase 2 (não executar agora, apenas incluir no relatório)

Com o usuário presente, nesta ordem:

1. Decidir a visibilidade do repositório.
2. Confirmar `estrategia.md` e `voz.md`.
3. Escrever as três primeiras teses com `/tese nova`, porque elas orientam o resto. Uma tese boa é uma afirmação que pode estar errada e que o usuário está disposto a defender em público por meses.
4. Rodar `/diagnostico` e sair com o gap-map preenchido, com a prioridade de cada domínio pesada por quais teses dependem dele.
5. Escolher o primeiro projeto público com `/projeto novo`, com uma primeira versão publicável em até quatro semanas, ligado a uma tese.
6. Criar as duas primeiras trilhas com `/trilha nova`, uma delas tendo o projeto como artefato, e ingerir a primeira fonte de cada.
7. Rodar `/ideias` e escrever o primeiro post com `/post`, sustentando uma das teses.
8. Começar a rotina: `/dia` toda manhã, `/study` todo dia, `/trilha continuar` e `/projeto continuar` somando três ou quatro sessões por semana, `/semana` toda sexta ou domingo, `/tese revisar` quando a semana apontar evidência nova.

Só depois de duas semanas de rotina decidir se vale construir algo a mais (UI, automações, Anki). A regra é que uso precede ferramenta.
