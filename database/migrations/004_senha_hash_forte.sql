-- ============================================================
-- MIGRATION 004 — Hash de senha mais forte (PBKDF2)
-- Amplia a coluna para comportar o formato "pbkdf2_sha256$iter$salt$hash".
-- Hashes SHA-256 antigos continuam validos e sao migrados no proximo login.
-- ============================================================

ALTER TABLE usuarios ALTER COLUMN senha_hash TYPE VARCHAR(255);
