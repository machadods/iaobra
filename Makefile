# ============================================================
# IAOBRA — Makefile
# Uso: make <comando>
# ============================================================

.PHONY: help dev up down logs restart backup shell db clean

# Variaveis
COMPOSE = docker compose
APP     = iaobra_app
DB      = iaobra_db

help:
	@echo ""
	@echo "  IAOBRA — Comandos disponiveis:"
	@echo ""
	@echo "  Desenvolvimento"
	@echo "    make dev        Roda local sem Docker (streamlit run app.py)"
	@echo ""
	@echo "  Docker"
	@echo "    make up         Sobe todos os servicos em background"
	@echo "    make down       Para todos os servicos"
	@echo "    make restart    Para e sobe novamente"
	@echo "    make logs       Mostra logs em tempo real"
	@echo "    make logs-app   Logs so da aplicacao"
	@echo "    make logs-db    Logs so do banco"
	@echo ""
	@echo "  Banco"
	@echo "    make backup     Faz backup do PostgreSQL"
	@echo "    make db         Abre shell do PostgreSQL"
	@echo "    make migrate    Aplica migrations pendentes"
	@echo ""
	@echo "  Outros"
	@echo "    make shell      Shell dentro do container da app"
	@echo "    make clean      Remove containers e volumes (CUIDADO)"
	@echo ""

# ── DESENVOLVIMENTO ───────────────────────────────────────────────────
dev:
	streamlit run app.py --server.port 8502

# ── DOCKER ────────────────────────────────────────────────────────────
up:
	$(COMPOSE) --env-file .env.production up -d --build
	@echo ""
	@echo "  App rodando em http://localhost"
	@echo "  Logs: make logs"

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f

logs-app:
	$(COMPOSE) logs -f app

logs-db:
	$(COMPOSE) logs -f postgres

# ── BANCO ─────────────────────────────────────────────────────────────
backup:
	@mkdir -p backups
	$(COMPOSE) exec postgres pg_dump -U $${POSTGRES_USER:-iaobra} $${POSTGRES_DB:-iaobras_db} \
		> backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup salvo em backups/"

db:
	$(COMPOSE) exec postgres psql -U $${POSTGRES_USER:-iaobra} $${POSTGRES_DB:-iaobras_db}

migrate:
	$(COMPOSE) exec app python -c "from database.migrate import rodar; from config import DATABASE_URL; print(rodar(DATABASE_URL))"

# ── OUTROS ────────────────────────────────────────────────────────────
shell:
	$(COMPOSE) exec app bash

clean:
	@echo "ATENCAO: isso remove TODOS os containers e volumes!"
	@read -p "Tem certeza? (s/N) " confirm && [ "$$confirm" = "s" ] && \
		$(COMPOSE) down -v --remove-orphans || echo "Cancelado."
