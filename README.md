# Помощник инвестора в Свердловской области

Прототип AI-агента для поддержки инвесторов, демонстрирующий работу с MCP (Model Context Protocol).

## Задачи агента

1. **Анализ лучших практик** — изучение успешных инвестиционных кейсов в регионе
2. **Поиск инвестиционного потенциала** — анализ территорий, отраслей и доступных ресурсов
3. **Подготовка и верификация документов** — помощь в оформлении заявок на меры поддержки

## Архитектура

```
┌──────────────────────────────────────────────────────────┐
│                    Веб-интерфейс (Next.js)                │
│                    localhost:3000                         │
└────────────────────────┬─────────────────────────────────┘
                         │  REST API (/api/*)
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  FastAPI сервер (:8000)                   │
└────────────────────────┬─────────────────────────────────┘
                         │  вызовы MCP-инструментов
                         ▼
┌──────────────────────────────────────────────────────────┐
│                      MCP Servers                          │
├──────────────────┬──────────────────┬────────────────────┤
│   Database MCP   │   Search MCP     │   Documents MCP    │
└──────────────────┴──────────────────┴────────────────────┘
                         │
                         ▼
              SQLAlchemy → SQLite / PostgreSQL
```

## Структура проекта

```
investor-agent/
├── src/
│   ├── agent/
│   │   ├── core.py              # Ядро агента
│   │   └── prompts.py           # Промты для задач
│   ├── api/
│   │   └── server.py            # FastAPI сервер для веб-интерфейса
│   ├── mcp/
│   │   ├── database_server.py   # MCP сервер БД
│   │   ├── search_server.py     # MCP сервер поиска
│   │   └── documents_server.py  # MCP сервер документов
│   ├── database/
│   │   ├── models.py            # SQLAlchemy модели
│   │   └── seed_data.py         # Тестовые данные
│   └── utils/
│       └── config.py            # Конфигурация
├── frontend/                    # Next.js + TypeScript + SCSS
│   ├── src/
│   │   ├── app/                 # Страницы
│   │   ├── components/          # UI-компоненты
│   │   ├── styles/              # _variables.scss, _mixins.scss
│   │   └── types/               # TypeScript типы
│   └── package.json
├── run.py                       # Запуск бэк + фронт одной командой
├── demo_standalone.py           # Демо MCP-серверов в консоли
├── requirements.txt
└── docker-compose.yml
```

## Быстрый старт

### Вариант 1: Всё сразу (бэкенд + фронтенд)

```bash
# Установка Python-зависимостей
pip install -r requirements.txt

# Запуск обоих серверов одной командой
python run.py
```

Откройте **http://localhost:3000** — веб-интерфейс с реальными данными.

### Вариант 2: В двух терминалах

**Терминал 1 — бэкенд:**
```bash
pip install -r requirements.txt
python -m src.api.server
```
API доступен на http://localhost:8000, Swagger UI — на http://localhost:8000/docs

**Терминал 2 — фронтенд:**
```bash
cd frontend
npm install
npm run dev
```
Веб-интерфейс — http://localhost:3000

### Вариант 3: Только консольная демонстрация MCP

```bash
python demo_standalone.py
```

### С PostgreSQL (опционально)

```bash
docker-compose up -d db
python -m src.database.seed_data
python -m src.main
```

## Команды

| Команда | Описание |
|---------|----------|
| `python run.py` | Запуск бэкенда + фронтенда |
| `python -m src.api.server` | Только FastAPI-сервер (:8000) |
| `cd frontend && npm run dev` | Только Next.js (:3000) |
| `python demo_standalone.py` | Консольная демонстрация MCP |
| `python -m src.main` | CLI-демо агента (требует PostgreSQL) |
| `python -m src.main --task 1` | Только анализ лучших практик |
| `python -m src.main --search "металлургия"` | Поиск по базе знаний |

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/health` | Проверка статуса |
| GET | `/api/kpi` | KPI для дашборда |
| GET | `/api/projects` | Инвестиционные проекты |
| GET | `/api/territories` | Территории с потенциалом |
| GET | `/api/support-measures` | Меры поддержки |
| GET | `/api/search?q=...` | Поиск по базе знаний |
| POST | `/api/chat` | Чат с агентом |

## MCP Серверы

### Database MCP
- Подключение к PostgreSQL
- CRUD операции для инвестиционных данных
- Примеры запросов для аналитики

### Search MCP
- Поиск по базе знаний
- Внешние API (если настроены)
- Ранжирование результатов

### Documents MCP
- Валидация документов
- Проверка полноты пакетов
- Генерация шаблонов

## Технологии

- Python 3.10+
- MCP SDK (FastMCP)
- SQLAlchemy
- PostgreSQL / SQLite (для демо)
- Pydantic Settings
