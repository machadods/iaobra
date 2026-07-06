# IAOBRA — Plataforma de Gestão de Obras com Inteligência Artificial

> Plataforma web para gestão, acompanhamento e capacitação de profissionais da construção civil, com IA integrada para análise de progresso, geração de cronogramas e consulta de preços.

---

## Sobre o Projeto

O **IAOBRA** é uma solução desenvolvida para digitalizar e inteligencializar o acompanhamento de obras. O Mestre de Obras registra o progresso diário com texto, fotos, vídeos e áudios. A IA analisa os registros automaticamente, gera cronograma, detecta problemas e sugere ações.

**Desenvolvido como projeto extensionista — Práticas Extensionistas III**

---

## Funcionalidades

### Para o Mestre de Obras
- Cadastro de obras com cliente vinculado
- Diário de obra com upload de fotos, vídeos e áudios
- Análise automática do progresso via IA (Gemini)
- Cronograma gerado automaticamente pela IA
- Orçamento com consulta de preços por IA (estimativas de referência — validar com fornecedores/SINAPI)
- Mercado de sobras de materiais
- Canal "Fale Conosco" para contato com os desenvolvedores

### Para o Cliente / Proprietário
- Painel de acompanhamento em tempo real (somente leitura)
- Visualização do diário, cronograma e orçamento
- Acesso por login próprio criado pelo Mestre

### Para o Administrador
- Gerenciamento de construtores e clientes
- Controle de créditos de IA
- Confirmação de pagamentos via PIX
- Painel de usuários e segurança
- Leitura das mensagens recebidas pelo "Fale Conosco"

---

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Interface | Python + Streamlit |
| Banco de Dados | PostgreSQL 15 |
| IA | OpenRouter API (Gemini Flash) |
| Infraestrutura | Docker + Nginx |
| Autenticação | Sistema próprio com PBKDF2-HMAC-SHA256 |

---

## Arquitetura

```
IAOBRA/
├── app.py                      # Entry point — roteamento e autenticação
├── config.py                   # Configurações e variáveis de ambiente
├── style.py                    # Design system (CSS global)
│
├── src/
│   ├── models/                 # Entidades do domínio (dataclasses)
│   │   ├── usuario.py
│   │   ├── obra.py
│   │   ├── diario.py
│   │   ├── orcamento.py
│   │   └── sobras.py
│   │
│   ├── services/               # Lógica de negócio
│   │   ├── auth_service.py     # Autenticação e perfis
│   │   ├── obra_service.py     # Gestão de obras
│   │   ├── diario_service.py   # Diário e registros
│   │   ├── orcamento_service.py
│   │   ├── sobras_service.py   # Marketplace
│   │   ├── ia_service.py       # Integração OpenRouter/Gemini
│   │   └── creditos_service.py # Sistema de créditos
│   │
│   ├── ui/
│   │   └── pages/              # Páginas da interface
│   │       ├── login_page.py
│   │       ├── cliente_page.py
│   │       └── planos_page.py
│   │
│   └── utils/
│       ├── db_connection.py    # Conexão PostgreSQL (psycopg2)
│       ├── file_handler.py     # Upload e gestão de arquivos
│       ├── security.py         # Validações e hardening
│       └── validators.py
│
├── database/
│   ├── migrate.py              # Runner de migrations (auto na subida)
│   └── migrations/
│       ├── 001_schema_completo.sql
│       ├── 002_creditos_pagamentos.sql
│       ├── 003_contatos.sql
│       └── 004_senha_hash_forte.sql
│
├── infra/
│   └── nginx.conf              # Proxy reverso + HTTPS
│
├── Diagramas/                  # Modelagem UML e ER
│   ├── Diagrama de Classe.png
│   ├── Diagrama de Caso de Uso.png
│   ├── Diagrama Sequencial.png
│   ├── Diagrama de Atividades.png
│   └── Diagrama Entidade-Relacionamento (DER).png
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Modelo de Dados

```
USUARIO ──< OBRA (como mestre)
USUARIO ──< OBRA (como cliente)
OBRA ──< DIARIO ──< MIDIA
OBRA ──< ORCAMENTO
OBRA ──< SOBRAS
OBRA ──< CRONOGRAMA
USUARIO ──< TRANSACOES (créditos/pagamentos)
```

---

## Como Executar

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+
- Chave de API no [OpenRouter](https://openrouter.ai/keys) (gratuita)

### 1. Clone o repositório
```bash
git clone https://github.com/machadods/iaobra.git
cd iaobra
```

### 2. Configure o ambiente
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

Variáveis necessárias no `.env`:
```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/iaobras_db
OPENROUTER_API_KEY=sua_chave_aqui
OPENROUTER_MODEL=google/gemini-2.5-flash-lite
ADMIN_USERNAME=admin
ADMIN_PASSWORD=sua_senha_segura
SECRET_KEY=chave_aleatoria_64_chars
PIX_CHAVE=+5511999999999
PIX_NOME=Seu Nome
PIX_BANCO=Seu banco
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute
```bash
streamlit run app.py
```

O banco de dados é criado automaticamente na primeira execução.

**Acesso inicial:** `admin` / `iaobras2024`

---

## Executar com Docker

```bash
# Preencha .env.production com suas credenciais reais
# Sobe app + PostgreSQL + Nginx
docker compose --env-file .env.production up -d --build
```

Acesse em `http://localhost`

---

## Perfis de Acesso

| Perfil | Descrição | Acesso |
|--------|-----------|--------|
| **Admin** | Gerencia construtores, clientes e pagamentos | Total |
| **Construtor** | Mestre de obras — registra e analisa obras | Ferramentas completas |
| **Cliente** | Proprietário — acompanha a obra | Somente leitura |

---

## Sistema de Créditos

O uso da IA consome créditos:

| Plano | Créditos | Valor |
|-------|----------|-------|
| Gratuito | 10 créditos | Teste |
| Pro | 500 créditos/mês | R$ 39,90 via PIX |

---

## Diagramas UML

Todos os diagramas de modelagem estão na pasta `/Diagramas`:

- **ER Lógico** — Estrutura do banco de dados com entidades e relacionamentos
- **Diagrama de Classes** — Classes, atributos, métodos e associações
- **Caso de Uso** — Atores e funcionalidades do sistema
- **Diagrama de Sequência** — Fluxo de registro de obra com IA
- **Diagrama de Atividades** — Fluxo completo de uso da plataforma

---

## Segurança

- Senhas armazenadas com hash PBKDF2-HMAC-SHA256 (salt individual por usuário, 600 mil iterações); hashes antigos são migrados automaticamente no login
- Bloqueio de conta após 5 tentativas de login
- Inputs sanitizados contra injeção
- Queries parametrizadas (sem SQL injection)
- Chaves de API apenas em variáveis de ambiente
- Usuário sem root no container Docker

---

## Licença

Projeto acadêmico — Práticas Extensionistas III  
Acadêmico de Ciência de Dados e Inteligência Artificial  

---

*Desenvolvido por Wagner Machado dos Santos*
