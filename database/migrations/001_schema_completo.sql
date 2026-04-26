-- ============================================================
-- MIGRATION 001 — Schema completo IAOBRA
-- Criado automaticamente pelo sistema de migrations
-- ============================================================

-- ── USUARIOS ─────────────────────────────────────────────────────────
-- Substitui o arquivo JSON. Suporta 3 perfis: admin, construtor, cliente
CREATE TABLE IF NOT EXISTS usuarios (
    id               SERIAL PRIMARY KEY,
    nome             VARCHAR(150) NOT NULL,
    username         VARCHAR(30)  NOT NULL UNIQUE,
    senha_hash       VARCHAR(64)  NOT NULL,
    tipo             VARCHAR(20)  NOT NULL DEFAULT 'cliente'
                         CHECK (tipo IN ('admin', 'construtor', 'cliente')),
    ativo            BOOLEAN      NOT NULL DEFAULT TRUE,
    bloqueado        BOOLEAN      NOT NULL DEFAULT FALSE,
    tentativas_login SMALLINT     NOT NULL DEFAULT 0,
    criado_em        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_tipo     ON usuarios(tipo);

-- ── OBRAS ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS obras (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(200) NOT NULL,
    endereco        VARCHAR(255) NOT NULL,
    descricao       TEXT,
    status          VARCHAR(50)  NOT NULL DEFAULT 'em_andamento'
                        CHECK (status IN ('em_andamento', 'paralisada', 'finalizada')),
    data_inicio     DATE,
    data_fim        DATE,
    proprietario    VARCHAR(150),
    responsavel     VARCHAR(150),
    orcamento_total DECIMAL(14,2) DEFAULT 0,
    id_construtor   INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    criado_em       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_obras_status      ON obras(status);
CREATE INDEX IF NOT EXISTS idx_obras_construtor  ON obras(id_construtor);

-- ── OBRAS_CLIENTES — quais clientes podem ver quais obras ─────────────
CREATE TABLE IF NOT EXISTS obras_clientes (
    id_obra    INTEGER NOT NULL REFERENCES obras(id)    ON DELETE CASCADE,
    id_cliente INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_cliente)
);

-- ── DIARIO ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS diario (
    id              SERIAL PRIMARY KEY,
    id_obra         INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    data_registro   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registro_texto  TEXT,
    analise_ia      TEXT,      -- auditoria gerada pela IA
    criado_em       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_diario_obra ON diario(id_obra);
CREATE INDEX IF NOT EXISTS idx_diario_data ON diario(data_registro DESC);

-- ── MIDIA — arquivos vinculados a entradas do diario ─────────────────
CREATE TABLE IF NOT EXISTS midia (
    id            SERIAL PRIMARY KEY,
    id_diario     INTEGER NOT NULL REFERENCES diario(id) ON DELETE CASCADE,
    id_obra       INTEGER NOT NULL REFERENCES obras(id)  ON DELETE CASCADE,
    tipo          VARCHAR(10) NOT NULL CHECK (tipo IN ('foto', 'video', 'audio')),
    nome_arquivo  VARCHAR(255) NOT NULL,
    caminho       VARCHAR(512),
    tamanho_bytes BIGINT,
    criado_em     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_midia_diario ON midia(id_diario);
CREATE INDEX IF NOT EXISTS idx_midia_obra   ON midia(id_obra);

-- ── ORCAMENTO ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orcamento (
    id             SERIAL PRIMARY KEY,
    id_obra        INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    material       VARCHAR(200) NOT NULL,
    quantidade     DECIMAL(12,3) DEFAULT 0,
    unidade        VARCHAR(30),
    preco_unitario DECIMAL(14,2) DEFAULT 0,
    preco_total    DECIMAL(14,2) GENERATED ALWAYS AS
                       (quantidade * preco_unitario) STORED,
    loja           VARCHAR(150),
    observacoes    TEXT,
    criado_em      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_orcamento_obra ON orcamento(id_obra);

-- ── SOBRAS — marketplace de materiais ────────────────────────────────
CREATE TABLE IF NOT EXISTS sobras (
    id               SERIAL PRIMARY KEY,
    id_obra          INTEGER NOT NULL REFERENCES obras(id)    ON DELETE CASCADE,
    id_vendedor      INTEGER REFERENCES usuarios(id)          ON DELETE SET NULL,
    material         VARCHAR(200) NOT NULL,
    quantidade       DECIMAL(12,3) DEFAULT 0,
    unidade          VARCHAR(30),
    preco            DECIMAL(14,2) DEFAULT 0,
    descricao        TEXT,
    status           VARCHAR(20) NOT NULL DEFAULT 'disponivel'
                         CHECK (status IN ('disponivel', 'reservado', 'vendido')),
    data_publicacao  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_venda       TIMESTAMP,
    criado_em        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sobras_obra    ON sobras(id_obra);
CREATE INDEX IF NOT EXISTS idx_sobras_status  ON sobras(status);

-- ── CRONOGRAMA — gerado pela IA ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS cronograma (
    id          SERIAL PRIMARY KEY,
    id_obra     INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    etapa       VARCHAR(200) NOT NULL,
    duracao     VARCHAR(100),
    descricao   TEXT,
    ordem       SMALLINT DEFAULT 0,
    status      VARCHAR(20) DEFAULT 'pendente'
                    CHECK (status IN ('pendente', 'em_andamento', 'concluida')),
    criado_em   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cronograma_obra ON cronograma(id_obra);
