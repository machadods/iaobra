# Script de setup usando arquivo SQL direto

$project_root = "C:\Users\wagner\Desktop\CIENCIA DE DADOS\IAOBRAS"
$migration_file = "$project_root\database\migrations\v003_media_stats_schema.sql"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 SETUP - Usando abordagem DBeaver" -ForegroundColor Cyan
Write-Host "============================================================`n"

Write-Host "📁 Projeto: $project_root"
Write-Host "📄 Migration: $migration_file"

if (Test-Path $migration_file) {
    Write-Host "✅ Arquivo SQL encontrado`n"
} else {
    Write-Host "❌ ERRO: Arquivo SQL não encontrado!`n"
    exit 1
}

# Procurar pelo executável psql
$possible_paths = @(
    "C:\Program Files\PostgreSQL\14\bin\psql.exe",
    "C:\Program Files\PostgreSQL\15\bin\psql.exe",
    "C:\Program Files\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files`(x86`)\PostgreSQL\14\bin\psql.exe",
)

$psql_path = $null
foreach ($path in $possible_paths) {
    if (Test-Path $path) {
        $psql_path = $path
        Write-Host "✅ Encontrado psql em: $psql_path`n"
        break
    }
}

if ($null -eq $psql_path) {
    Write-Host "❌ psql não encontrado nas localizações padrão`n"
    Write-Host "Caminho esperado:"
    foreach ($path in $possible_paths) {
        Write-Host "   - $path"
    }
    Write-Host "`nPor favor, forneça o caminho manualmente:"
    Write-Host "   Get-ChildItem 'C:\Program Files*' -Filter 'psql.exe' -Recurse`n"
    exit 1
}

# Criar banco de dados
Write-Host "🔧 Criando banco de dados..."
Write-Host "   (Pode pedir por senha, use: postgres)"
Write-Host ""

& $psql_path -h localhost -p 5434 -U postgres -c "DROP DATABASE IF EXISTS iaobras_db;"
& $psql_path -h localhost -p 5434 -U postgres -c "CREATE DATABASE iaobras_db;"

Write-Host "`n✅ Banco criado!"

Write-Host "`n🔧 Executando migration v003..."
& $psql_path -h localhost -p 5434 -U postgres -d iaobras_db -f $migration_file

Write-Host "`n✅ Migration concluída!"

Write-Host "`n🔧 Validando tabelas..."
$table_count = & $psql_path -h localhost -p 5434 -U postgres -d iaobras_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 

Write-Host "✅ Tabelas criadas: $($table_count.Trim())`n"

Write-Host "============================================================"
Write-Host "✅ SETUP COMPLETO COM SUCESSO!"
Write-Host "============================================================`n"
