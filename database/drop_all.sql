-- ============================================================
-- DROP ALL — apaga tudo e recria do zero via migrations
-- Execute no DBeaver antes de subir o app pela primeira vez
-- ============================================================

DROP TABLE IF EXISTS _migrations      CASCADE;
DROP TABLE IF EXISTS midia             CASCADE;
DROP TABLE IF EXISTS diario            CASCADE;
DROP TABLE IF EXISTS orcamento         CASCADE;
DROP TABLE IF EXISTS sobras            CASCADE;
DROP TABLE IF EXISTS obras_clientes    CASCADE;
DROP TABLE IF EXISTS obras             CASCADE;
DROP TABLE IF EXISTS usuarios          CASCADE;
DROP TABLE IF EXISTS cronograma        CASCADE;
DROP TABLE IF EXISTS eventos_obra      CASCADE;
DROP TABLE IF EXISTS analise_imagem    CASCADE;
DROP TABLE IF EXISTS analise_video     CASCADE;
DROP TABLE IF EXISTS extracao_audio    CASCADE;
DROP TABLE IF EXISTS stats_obra        CASCADE;
DROP TABLE IF EXISTS cache_analise     CASCADE;
DROP TABLE IF EXISTS timeline_stats    CASCADE;

-- Confirma
SELECT 'Banco limpo. Suba o app para aplicar as migrations.' AS status;
