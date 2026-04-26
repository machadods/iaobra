"""
INIT_DB
Script para inicializar schema do banco de dados.
TODO: Implementar com SQLAlchemy na Fase 2
"""

DB_SCHEMA = """
-- ============================================================
-- SCHEMA IAOBRAS - FASE 1 (IMPLEMENTAR NA FASE 2)
-- ============================================================

-- Tabela: obras
CREATE TABLE IF NOT EXISTS obras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'em_andamento',
    data_inicio DATE,
    data_fim DATE,
    proprietario VARCHAR(255),
    responsavel VARCHAR(255),
    orcamento_total DECIMAL(12, 2),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: diario
CREATE TABLE IF NOT EXISTS diario (
    id SERIAL PRIMARY KEY,
    id_obra INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    data_registro TIMESTAMP,
    registro_texto TEXT,
    fotos TEXT[],
    videos TEXT[],
    audio VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: orcamento
CREATE TABLE IF NOT EXISTS orcamento (
    id SERIAL PRIMARY KEY,
    id_obra INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    material VARCHAR(255) NOT NULL,
    quantidade DECIMAL(10, 2),
    unidade VARCHAR(50),
    preco_unitario DECIMAL(10, 2),
    preco_total DECIMAL(12, 2),
    loja VARCHAR(255),
    data_cotacao DATE,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: sobras
CREATE TABLE IF NOT EXISTS sobras (
    id SERIAL PRIMARY KEY,
    id_obra INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    material VARCHAR(255) NOT NULL,
    quantidade DECIMAL(10, 2),
    unidade VARCHAR(50),
    preco DECIMAL(10, 2),
    descricao TEXT,
    foto VARCHAR(255),
    status VARCHAR(50) DEFAULT 'disponivel',
    data_publicacao TIMESTAMP,
    data_venda TIMESTAMP,
    vendedor VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_obras_status ON obras(status);
CREATE INDEX IF NOT EXISTS idx_diario_obra ON diario(id_obra);
CREATE INDEX IF NOT EXISTS idx_orcamento_obra ON orcamento(id_obra);
CREATE INDEX IF NOT EXISTS idx_sobras_obra ON sobras(id_obra);
CREATE INDEX IF NOT EXISTS idx_sobras_status ON sobras(status);
"""

def inicializar_banco():
    """Executa o schema no banco."""
    # TODO: Conectar ao PostgreSQL e executar queries
    print("[DB] Schema para inicializar foi definido acima")
    print("[DB] Implementar conexão real na Fase 2 com SQLAlchemy")

if __name__ == "__main__":
    inicializar_banco()
