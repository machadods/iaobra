# ============================================================
# IAOBRA — Script PowerShell (substituto do Makefile no Windows)
# Uso: .\iaobra.ps1 <comando>
# ============================================================

param([string]$cmd = "help")

switch ($cmd) {
    "help" {
        Write-Host ""
        Write-Host "  IAOBRA — Comandos disponiveis:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  .\iaobra.ps1 dev        Roda local (streamlit run app.py)"
        Write-Host "  .\iaobra.ps1 up         Sobe Docker em background"
        Write-Host "  .\iaobra.ps1 down       Para Docker"
        Write-Host "  .\iaobra.ps1 restart    Reinicia Docker"
        Write-Host "  .\iaobra.ps1 logs       Logs em tempo real"
        Write-Host "  .\iaobra.ps1 backup     Backup do banco"
        Write-Host "  .\iaobra.ps1 db         Shell do PostgreSQL"
        Write-Host "  .\iaobra.ps1 migrate    Aplica migrations"
        Write-Host ""
    }
    "dev" {
        streamlit run app.py --server.port 8502
    }
    "up" {
        docker compose --env-file .env.production up -d --build
        Write-Host ""
        Write-Host "  App rodando em http://localhost" -ForegroundColor Green
        Write-Host "  Logs: .\iaobra.ps1 logs"
    }
    "down" {
        docker compose down
    }
    "restart" {
        docker compose down
        docker compose --env-file .env.production up -d --build
    }
    "logs" {
        docker compose logs -f
    }
    "logs-app" {
        docker compose logs -f app
    }
    "backup" {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $file = "backups\backup_$timestamp.sql"
        New-Item -ItemType Directory -Force -Path backups | Out-Null
        docker compose exec postgres pg_dump -U iaobra iaobras_db > $file
        Write-Host "Backup salvo em $file" -ForegroundColor Green
    }
    "db" {
        docker compose exec postgres psql -U iaobra iaobras_db
    }
    "migrate" {
        docker compose exec app python -c "from database.migrate import rodar; from config import DATABASE_URL; print(rodar(DATABASE_URL))"
    }
    default {
        Write-Host "Comando desconhecido: $cmd. Use .\iaobra.ps1 help" -ForegroundColor Red
    }
}
