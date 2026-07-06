-- ============================================================
-- MIGRATION 003 — Mensagens de contato com os desenvolvedores
-- ============================================================

CREATE TABLE IF NOT EXISTS contatos (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150) NOT NULL,
    email       VARCHAR(150) NOT NULL,
    assunto     VARCHAR(200),
    mensagem    TEXT NOT NULL,
    respondido  BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_contatos_criado ON contatos(criado_em DESC);
