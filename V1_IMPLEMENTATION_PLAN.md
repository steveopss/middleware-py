# Middleware WhatsApp ↔ GLPI

Middleware FastAPI que conecta o WhatsApp (via Evolution API) ao GLPI, permitindo que usuários abram e consultem chamados ITSM diretamente pelo chat.

## Arquitetura

```
            WhatsApp
                ↓
        Evolution API (Webhook)
                ↓
         FastAPI (Middleware)
        ├── Session (Redis)
        ├── DB (PostgreSQL)
        ├── GLPI Client
        └── Flow Engine
                ↓
           GLPI API
```

## Estrutura de Pastas

```
middleware/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic Settings (.env)
│   │   └── database.py          # SQLAlchemy engine + session
│   ├── api/
│   │   ├── __init__.py
│   │   ├── webhook.py           # POST /webhook/evolution
│   │   └── health.py            # GET /health
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── glpi.py              # GLPI REST API client
│   │   └── evolution.py         # Evolution API client
│   ├── services/
│   │   ├── __init__.py
│   │   ├── session.py           # Gerenciamento de sessão Redis
│   │   └── flow_engine.py       # Motor de fluxo do chatbot
│   ├── models/
│   │   ├── __init__.py
│   │   └── conversation.py      # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── webhook.py           # Pydantic schemas (entrada)
│   │   └── glpi.py              # Pydantic schemas (GLPI)
│   └── repositories/
│       ├── __init__.py
│       └── conversation.py      # DB queries
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures globais
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_glpi_client.py
│   │   ├── test_evolution_client.py
│   │   ├── test_session.py
│   │   ├── test_flow_engine.py
│   │   └── test_webhook.py
│   └── integration/
│       └── __init__.py
├── alembic/
│   └── ...
├── alembic.ini
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

---

## Componentes

### 1. GLPI Client (`app/clients/glpi.py`)

Client HTTP assíncrono para o GLPI REST API:

| Método | Endpoint GLPI | Descrição |
|--------|---------------|-----------|
| `init_session()` | `GET /initSession` | Autentica com `user_token` + `App-Token`, retorna `session_token` |
| `kill_session()` | `GET /killSession` | Encerra sessão |
| `search_tickets(criteria)` | `GET /search/Ticket` | Busca chamados com filtros |
| `get_ticket(id)` | `GET /Ticket/{id}` | Detalhe de um chamado |
| `create_ticket(input)` | `POST /Ticket` | Cria chamado |
| `add_followup(ticket_id, text)` | `POST /Ticket/{id}/ITILFollowup` | Adiciona acompanhamento |

Lógica de autenticação:
1. Na primeira chamada, faz `init_session()` com `App-Token` (header fixo) + `user_token`
2. Armazena `session_token` no objeto
3. Reutiliza até receber 401 → refaz `init_session()`

### 2. Evolution Client (`app/clients/evolution.py`)

| Método | Endpoint Evolution | Descrição |
|--------|-------------------|-----------|
| `send_text(number, text)` | `POST /message/sendText/{instance}` | Envia mensagem de texto |
| `send_buttons(number, title, buttons)` | `POST /message/sendButtons/{instance}` | Envia botões interativos |
| `send_list(number, title, sections)` | `POST /message/sendList/{instance}` | Envia lista de opções |

### 3. Session Manager (`app/services/session.py`)

Gerenciamento de sessão de conversa usando Redis:

- `get(phone)` → busca sessão
- `set(phone, data)` → salva sessão
- `delete(phone)` → remove sessão
- `update_step(phone, step)` → atualiza etapa do fluxo

TTL configurável (padrão: 30 min). Chave: `session:{phone_number}`.

### 4. Flow Engine (`app/services/flow_engine.py`)

Motor de fluxo baseado em máquina de estados:

```
[*] → WELCOME → AUTH_USERNAME → AUTH_PASSWORD → MAIN_MENU
MAIN_MENU → CREATE_TICKET_TITLE → CREATE_TICKET_DESC → MAIN_MENU
MAIN_MENU → LIST_TICKETS → MAIN_MENU
MAIN_MENU → TICKET_STATUS → MAIN_MENU
AUTH_PASSWORD (falha) → AUTH_USERNAME
```

| Estado | Entrada | Ação | Próximo estado |
|--------|---------|------|----------------|
| `WELCOME` | qualquer | Enviar boas-vindas | `AUTH_USERNAME` |
| `AUTH_USERNAME` | texto (login) | Salvar login na sessão | `AUTH_PASSWORD` |
| `AUTH_PASSWORD` | texto (senha) | `glpi.init_session()` | `MAIN_MENU` ou `AUTH_USERNAME` |
| `MAIN_MENU` | "1" | — | `CREATE_TICKET_TITLE` |
| `MAIN_MENU` | "2" | `glpi.search_tickets()` → lista | `MAIN_MENU` |
| `MAIN_MENU` | "3" | Pedir nº do chamado | `TICKET_STATUS` |
| `CREATE_TICKET_TITLE` | texto | Salvar título | `CREATE_TICKET_DESC` |
| `CREATE_TICKET_DESC` | texto | `glpi.create_ticket()` | `MAIN_MENU` |
| `TICKET_STATUS` | número | `glpi.get_ticket(id)` → status | `MAIN_MENU` |

O `FlowEngine` é **puro** — recebe dependências por injeção de dependências.

### 5. Webhook (`app/api/webhook.py`)

```
POST /webhook/evolution
  1. Extrair phone_number e message do payload
  2. Buscar/criar sessão no Redis
  3. Passar para FlowEngine.process()
  4. Atualizar sessão
  5. Enviar resposta via Evolution client
  6. Retornar 200
```

---

## Stack

- **Backend**: FastAPI + Uvicorn
- **HTTP Client**: httpx (async)
- **Cache/Sessão**: Redis
- **Banco**: PostgreSQL + SQLAlchemy 2.0 + Alembic
- **Mensageria**: Evolution API
- **ITSM**: GLPI REST API
- **Testes**: pytest + respx + fakeredis
