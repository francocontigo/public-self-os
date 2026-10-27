# Second Brain automation (macOS / Linux).
# Thin wrappers around the coding-agent CLI in headless mode, so ingestion can be
# scripted / scheduled without opening an interactive session.
# Windows users: use ./sb.ps1 instead (same verbs).
#
# Requires: the `claude` CLI on PATH.
# --permission-mode acceptEdits lets the agent write wiki files without prompting.

CLAUDE ?= claude
PERM   ?= --permission-mode acceptEdits

.PHONY: help ingest process-inbox query lint capture study gaps explain \
        status entrevista diagnostico trilha dia semana ideias post decisao brag tese projeto

help:
	@echo "Second Brain commands:"
	@echo "  make ingest SRC=\"path-or-URL\"   Ingest one source into the wiki"
	@echo "  make process-inbox               Triage raw/inbox.md into the wiki"
	@echo "  make query Q=\"your question\"     Ask the wiki; answer saved to output/"
	@echo "  make lint                        Health-check the wiki"
	@echo "  make capture TEXT=\"a thought\"    Append a line to raw/inbox.md (no LLM)"
	@echo "  -- learning --"
	@echo "  make study [N=10]                Spaced-repetition session (interactive)"
	@echo "  make explain C=\"a concept\"       Feynman mode (interactive)"
	@echo "  make gaps                        Learning health check -> output/study-plan.md"
	@echo "  -- personal OS --"
	@echo "  make status                      System state (python scripts/os_status.py --human, no LLM)"
	@echo "  make entrevista                  First conversation: field, fronts, goals, domains (interactive)"
	@echo "  make diagnostico                 Diagnostic interview -> areas/estudos/gap-map.md (interactive)"
	@echo "  make trilha A=\"nova <tema>\"      Study tracks: nova|continuar|listar|fechar (interactive)"
	@echo "  make dia                         Open the day -> journal/<today>.md (interactive)"
	@echo "  make semana                      Weekly review -> journal/semanas/<week>.md (interactive)"
	@echo "  make ideias [N=5]                Post ideas -> areas/publico/ideias.md"
	@echo "  make post A=\"<tema> [x|linkedin|medium]\"  Draft a post -> areas/publico/posts/"
	@echo "  make decisao A=\"<frente>\"        Record a work decision (interactive)"
	@echo "  make brag A=\"colher|add ...\"      Brag document: harvest, add, review (interactive)"
	@echo "  make tese A=\"nova <enunciado>\"   Theses: nova|revisar|desafiar|listar (interactive)"
	@echo "  make projeto A=\"novo <nome>\"     Public projects: novo|continuar|publicar|listar (interactive)"

ingest:
	@test -n "$(SRC)" || (echo "Usage: make ingest SRC=\"path-or-URL\"" && exit 1)
	$(CLAUDE) -p "/ingest $(SRC)" $(PERM)

process-inbox:
	$(CLAUDE) -p "/process-inbox" $(PERM)

query:
	@test -n "$(Q)" || (echo "Usage: make query Q=\"your question\"" && exit 1)
	$(CLAUDE) -p "/query $(Q)" $(PERM)

lint:
	$(CLAUDE) -p "/lint" $(PERM)

# Pure-text capture: no LLM, just prepend to the inbox under the header line.
capture:
	@test -n "$(TEXT)" || (echo "Usage: make capture TEXT=\"a thought\"" && exit 1)
	@printf '%s\n' "$(TEXT)" | cat - raw/inbox.md > raw/.inbox.tmp && mv raw/.inbox.tmp raw/inbox.md
	@echo "Captured to raw/inbox.md"

# Interactive (open a live agent session so it can ask you questions).
study:
	$(CLAUDE) "/study $(N)" $(PERM)

explain:
	@test -n "$(C)" || (echo "Usage: make explain C=\"a concept\"" && exit 1)
	$(CLAUDE) "/explain $(C)" $(PERM)

gaps:
	$(CLAUDE) -p "/gaps" $(PERM)


# ---- personal OS (areas/ + journal/) ----
# No LLM: deterministic state from the vault.
status:
	python scripts/os_status.py --human

# Interactive skills (live session, they ask one question at a time).
entrevista:
	$(CLAUDE) "/entrevista" $(PERM)

diagnostico:
	$(CLAUDE) "/diagnostico" $(PERM)

trilha:
	$(CLAUDE) "/trilha $(A)" $(PERM)

dia:
	$(CLAUDE) "/dia" $(PERM)

semana:
	$(CLAUDE) "/semana" $(PERM)

decisao:
	@test -n "$(A)" || (echo "Usage: make decisao A=\"<frente>\"" && exit 1)
	$(CLAUDE) "/decisao $(A)" $(PERM)

brag:
	@test -n "$(A)" || (echo "Usage: make brag A=\"add <texto>|colher|revisar <periodo>|listar\"" && exit 1)
	$(CLAUDE) "/brag $(A)" $(PERM)

tese:
	$(CLAUDE) "/tese $(A)" $(PERM)

projeto:
	$(CLAUDE) "/projeto $(A)" $(PERM)

# Headless.
ideias:
	$(CLAUDE) -p "/ideias $(N)" $(PERM)

post:
	@test -n "$(A)" || (echo "Usage: make post A=\"<tema> [x|linkedin|medium]\"" && exit 1)
	$(CLAUDE) -p "/post $(A)" $(PERM)
