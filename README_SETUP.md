# 📋 GUIA DE SETUP - IAOBRAS v0.1.0

## ✅ Estrutura Criada

A estrutura segue **arquitetura profissional por camadas**:

```
IAOBRAS/
├── src/                          # Núcleo da aplicação
│   ├── models/                   # Entidades do domínio
│   ├── repositories/             # Acesso a dados (CRUD)
│   ├── services/                 # Lógica de negócio
│   ├── ui/
│   │   ├── pages/               # Páginas Streamlit
│   │   ├── components/          # Componentes reutilizáveis
│   │   └── styles.py
│   └── utils/                    # Ferramentas (logging, validação, etc)
│
├── database/                     # Infraestrutura de BD
│   ├── migrations/              # Scripts SQL
│   └── init_db.py
│
├── config.py                     # Configurações globais
├── requirements.txt              # Dependências
├── .env.example                  # Template de variáveis
└── app.py                        # Entry point refatorado
```

---

## 🚀 PRÓXIMOS PASSOS

### 1️⃣ Instalar Dependências

```powershell
cd "C:\Users\wagner\Desktop\CIENCIA DE DADOS\IAOBRAS"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2️⃣ Copiar .env

```powershell
Copy-Item .env.example .env
```

Editar `.env` com suas credenciais PostgreSQL:
```ini
DATABASE_URL=postgresql://seu_user:sua_senha@localhost:5432/iaobras_db
```

### 3️⃣ Criar Banco de Dados (PostgreSQL)

```sql
-- No DBeaver ou psql:
CREATE DATABASE iaobras_db;
```

Depois rodar as migrations:
```powershell
# TODO: Implementar com Alembic na Fase 2
# Por enquanto, rodar SQL manualmente em database/migrations/
```

### 4️⃣ Rodar Aplicação

```powershell
streamlit run app.py
```

---

## 📊 Arquitetura - Explicação Rápida

| Camada | Responsabilidade | Arquivos |
|--------|-----------------|----------|
| **Models** | Definir estrutura de dados | `obra.py`, `diario.py`, etc |
| **Repositories** | CRUD genérico (banco) | `*_repository.py` |
| **Services** | Lógica de negócio (regras) | `*_service.py` |
| **UI** | Interface Streamlit | `pages/`, `components/` |

**Fluxo**: UI → Service → Repository → Database

---

## 🎯 Fase 1 - O Que Funciona

✅ Criar obras  
✅ Registrar diários de obra  
✅ Gerenciar orçamento de materiais  
✅ Publicar sobras (mercado)  
✅ Interface completa com Streamlit  

❌ Banco de Dados (usar em memória por agora)  
❌ Upload de archivos (Fase 2)  
❌ IA/Chatbot (Fase 3)  
❌ Simulador temporal (Fase 4)  

---

## 💡 Dicas de Desenvolvimento

### Adicionar Nova Página (Fase 1)

1. Criar `src/ui/pages/minha_pagina.py`:
```python
def render():
    st.markdown("<div class='title'>Minha Página</div>", unsafe_allow_html=True)
    # seu código aqui
```

2. Adicionar no `app.py`:
```python
elif pagina_atual == "Meu Menu":
    from src.ui.pages.minha_pagina import render
    render()
```

### Adicionar Novo Service

1. Criar `src/services/meu_service.py`
2. Importar em `src/services/__init__.py`
3. Usar na página:
```python
from src.services.meu_service import MeuService
service = MeuService()
```

---

## 📞 Estrutura Pronta Para:

- ✅ Testar lógica sem BD real (repositories em memória)
- ✅ Adicionar novos serviços incrementalmente
- ✅ Migrar para PostgreSQL na Fase 2 sem refatorar UI
- ✅ Integrar IA/LLM na Fase 3
- ✅ Escalar para múltiplos usuários (com auth)

---

**Status:** Pronto para começar a programar! 🎉
