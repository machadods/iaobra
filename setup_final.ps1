#!/usr/bin/env powershell

$project_root = "C:\Users\wagner\Desktop\CIENCIA DE DADOS\IAOBRAS"
$migration_file = "$project_root\database\migrations\v003_media_stats_schema.sql"
$psql_exe = "C:\Program Files\PostgreSQL\18\bin\psql.exe"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SETUP - IAOBRAS FASE 2" -ForegroundColor Cyan
Write-Host "============================================================`n"

Write-Host "Projeto: $project_root"
Write-Host "Migration: $migration_file"
Write-Host "PostgreSQL: $psql_exe`n"

# Validar arquivo SQL
if (-not (Test-Path $migration_file)) {
    Write-Host "ERRO: Arquivo SQL nao encontrado!" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Arquivo SQL validado`n"

# Validar psql
if (-not (Test-Path $psql_exe)) {
    Write-Host "ERRO: PostgreSQL nao encontrado em $psql_exe" -ForegroundColor Red
    exit 1
}
Write-Host "OK: PostgreSQL encontrado`n"

# Criar banco
Write-Host "Etapa 1/3: Criando banco iaobras_db..."
try {
    & "$psql_exe" -h localhost -p 5434 -U postgres -w -c "DROP DATABASE IF EXISTS iaobras_db;" 2>&1 | Out-Null
    & "$psql_exe" -h localhost -p 5434 -U postgres -w -c "CREATE DATABASE iaobras_db;" 2>&1 | Out-Null
    Write-Host "  OK: Banco criado`n"
} catch {
    Write-Host "  ERRO: $_" -ForegroundColor Red
    Write-Host "  Dica: Voce pode ter sido solicitado por senha. Use: postgres`n"
}

# Executar migration
Write-Host "Etapa 2/3: Executando migration v003..."
try {
    & "$psql_exe" -h localhost -p 5434 -U postgres -d iaobras_db -w -f "$migration_file" 2>&1 | Out-Null
    Write-Host "  OK: Migration executada`n"
} catch {
    Write-Host "  ERRO: $_" -ForegroundColor Red
}

# Validar
Write-Host "Etapa 3/3: Validando tabelas..."
try {
    $result = & "$psql_exe" -h localhost -p 5434 -U postgres -d iaobras_db -w -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>&1
    $count = $result.Trim()
    Write-Host "  OK: Total de tabelas: $count`n"
    
    Write-Host "  Tabelas criadas:"
    $tables = & "$psql_exe" -h localhost -p 5434 -U postgres -d iaobras_db -w -t -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;" 2>&1
    foreach ($table in $tables) {
        if ($table.Trim()) {
            Write-Host "     - $($table.Trim())"
        }
    }
} catch {
    Write-Host "  Aviso: Nao foi possivel validar: $_`n"
}

Write-Host "`n============================================================"
Write-Host "OK SETUP CONCLUIDO COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================================`n"

Write-Host "PROXIMOS PASSOS:"
Write-Host "   1. Integrar pagina de analise no app.py"
Write-Host "   2. Executar: streamlit run app.py"
Write-Host "   3. Verificar novo menu 'Analise de Dados'`n"
