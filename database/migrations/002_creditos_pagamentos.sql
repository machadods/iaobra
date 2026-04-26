-- ============================================================
-- MIGRATION 002 — Sistema de creditos e pagamentos
-- ============================================================

-- Adiciona campos de plano e creditos em usuarios
ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS creditos        INTEGER   NOT NULL DEFAULT 10,
    ADD COLUMN IF NOT EXISTS plano           VARCHAR(20) NOT NULL DEFAULT 'gratuito'
                                                 CHECK (plano IN ('gratuito', 'pro', 'admin')),
    ADD COLUMN IF NOT EXISTS validade_plano  TIMESTAMP;

-- Creditos iniciais: admin e construtores recebem mais
UPDATE usuarios SET creditos = 999999, plano = 'admin'   WHERE tipo = 'admin';
UPDATE usuarios SET creditos = 50,     plano = 'gratuito' WHERE tipo IN ('construtor','cliente') AND creditos = 10;

-- Historico de transacoes (pagamentos PIX confirmados e debitos de IA)
CREATE TABLE IF NOT EXISTS transacoes (
    id           SERIAL PRIMARY KEY,
    id_usuario   INTEGER     NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo         VARCHAR(20) NOT NULL CHECK (tipo IN ('credito','debito','pagamento')),
    creditos     INTEGER     NOT NULL DEFAULT 0,
    valor_brl    DECIMAL(10,2),
    descricao    VARCHAR(300),
    confirmado   BOOLEAN     NOT NULL DEFAULT FALSE,
    criado_em    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transacoes_usuario ON transacoes(id_usuario);
CREATE INDEX IF NOT EXISTS idx_transacoes_tipo    ON transacoes(tipo, confirmado);
