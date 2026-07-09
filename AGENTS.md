# Инвестиционный помощник — Проект для AI-агентов

> Файл содержит контекст проекта для AI-ассистентов (Koda, Claude, и др.)

## 📋 О проекте

**Название:** Помощник инвестора в Свердловской области  
**Тип:** Full-stack приложение (Python FastAPI + Next.js)  
**Назначение:** AI-агент для поддержки инвесторов — анализ практик, поиск потенциала, подготовка документов

## 🏗️ Архитектура

```
investor-agent/
├── src/                     # Python бэкенд
│   ├── api/
│   │   └── server.py        # FastAPI сервер (REST API)
│   ├── mcp/
│   │   ├── database_server.py   # MCP: работа с БД
│   │   ├── search_server.py     # MCP: поиск по базе
│   │   └── documents_server.py  # MCP: валидация документов
│   ├── database/
│   │   ├── models.py        # SQLAlchemy модели
│   │   └── seed_data.py     # Тестовые данные
│   ├── agent/
│   │   ├── core.py          # Ядро AI-агента
│   │   └── prompts.py       # Промты для задач
│   └── utils/
│       └── config.py        # Конфигурация
│
├── frontend/                # Next.js фронтенд
│   ├── src/
│   │   ├── app/             # Страницы (App Router)
│   │   ├── components/      # UI-компоненты
│   │   ├── styles/          # SCSS переменные и миксины
│   │   └── types/           # TypeScript типы
│   └── package.json
│
├── run.py                   # Запуск бэк + фронт одной командой
├── demo_standalone.py       # Консольная демонстрация MCP
└── requirements.txt         # Python зависимости
```

## 🛠️ Технологический стек

### Бэкенд (Python 3.10+)
| Пакет | Версия | Назначение |
|-------|--------|------------|
| `fastapi` | ≥0.100.0 | REST API сервер |
| `uvicorn` | ≥0.23.0 | ASGI сервер |
| `sqlalchemy` | ≥2.0.0 | ORM для БД |
| `mcp` | ≥1.0.0 | Model Context Protocol |
| `pydantic` | ≥2.0.0 | Валидация данных |
| `psycopg2-binary` | ≥2.9.0 | PostgreSQL драйвер |

### Фронтенд (Node.js 18+)
| Пакет | Версия | Назначение |
|-------|--------|------------|
| `next` | 14.2.5 | React фреймворк |
| `react` | 18.3.1 | UI библиотека |
| `typescript` | 5.5.3 | Типизация |
| `sass` | 1.77.6 | SCSS препроцессор |
| `@phosphor-icons/react` | 2.1.7 | Иконки |

### Базы данных
- **Разработка/демо:** SQLite (`investor_data.db`)
- **Продакшен:** PostgreSQL (через `docker-compose.yml`)

## 🚀 Команды запуска

### Быстрый старт (рекомендуется)
```bash
# Создание venv (один раз)
python -m venv venv

# Активация
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt
cd frontend && npm install

# Запуск обоих серверов
python run.py
```

### Отдельный запуск
```bash
# Бэкенд (API :8000)
python -m src.api.server

# Фронтенд (Next.js :3000)
cd frontend && npm run dev

# Консольная демонстрация MCP
python demo_standalone.py
```

### API эндпоинты
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/health` | Проверка статуса |
| GET | `/api/kpi` | KPI для дашборда |
| GET | `/api/projects` | Инвестиционные проекты |
| GET | `/api/territories` | Территории с потенциалом |
| GET | `/api/support-measures` | Меры поддержки |
| GET | `/api/search?q=...` | Поиск по базе знаний |
| POST | `/api/chat` | Чат с агентом |

## 📁 Ключевые файлы

### Бэкенд
- `src/api/server.py` — FastAPI сервер, инициализация SQLite с тестовыми данными, 7 REST эндпоинтов
- `src/mcp/database_server.py` — MCP-инструменты: `get_best_practices`, `search_investment_potential`, `get_support_measures`
- `src/mcp/search_server.py` — MCP-инструменты: `search_knowledge_base`, `compare_territories`, `find_similar_practices`
- `src/mcp/documents_server.py` — MCP-инструменты: `validate_document`, `check_documents_completeness`, `generate_document_from_template`
- `src/agent/core.py` — Оркестрация MCP-инструментов для 3 задач агента
- `src/database/models.py` — SQLAlchemy модели: `BestPractice`, `InvestmentPotential`, `SupportMeasure`, `DocumentTemplate`

### Фронтенд
- `frontend/src/app/page.tsx` — Главная страница: загрузка данных из API, чат, карточки проектов
- `frontend/src/components/DashboardHeader/` — KPI-плитки с трендами
- `frontend/src/components/InvestmentCard/` — Карточка проекта с IRR, NPV, прогресс-баром
- `frontend/src/components/ChatInterface/` — Чат с поддержкой встроенных карточек
- `frontend/src/components/SupportProgramBadge/` — Цветные теги мер поддержки (financial/tax/infrastructure/advisory)
- `frontend/src/components/ApplicationStatus/` — Timeline этапов заявки
- `frontend/src/styles/_variables.scss` — Дизайн-токены (цвета, тени, радиусы)
- `frontend/src/types/index.ts` — TypeScript интерфейсы

## 🎨 Дизайн-система (фронтенд)

### Цвета
```scss
$color-primary: #0B1F3B;      // Тёмно-синий
$color-accent: #C8A96E;       // Золотой
$color-bg: #F5F6FA;           // Фон
$color-card: #FFFFFF;         // Карточки
```

### Типографика
- Заголовки: **Montserrat Bold** (700)
- Текст: **IBM Plex Sans** (400, 500, 600)
- Цифры: `tabular-nums`

### Эффекты
- Скругления: `8px` (карточки, кнопки)
- Тени: `0px 4px 12px rgba(0,0,0,0.04)` → `0px 8px 20px rgba(0,0,0,0.08)` при ховере
- Анимации: `cubic-bezier(0.4, 0, 0.2, 1) 0.3s`
- Ховер: подъём на `2px`

## 📊 Модель данных

### BestPractice (Лучшие практики)
```python
id, company_name, industry, location, investment_amount, 
jobs_created, description, success_factors, implementation_date, status
```

### InvestmentPotential (Территории)
```python
id, territory_name, territory_type, area_km2, population, 
key_industries, available_lots, infrastructure_score, tax_benefits
```

### SupportMeasure (Меры поддержки)
```python
id, name, measure_type, description, eligibility_criteria, 
max_amount, required_documents, responsible_agency
```

### DocumentTemplate (Шаблоны документов)
```python
id, support_measure_id, document_type, template_content, required_fields
```

## 🧩 MCP (Model Context Protocol)

Проект использует MCP для модульности бэкенда. Три MCP-сервера предоставляют инструменты:

### Database MCP
- `get_best_practices(industry, location, min_investment, limit)`
- `search_investment_potential(territory_name, territory_type, min_infra_score, industry)`
- `get_support_measures(measure_type, include_documents)`
- `get_document_templates(support_measure_id)`
- `analyze_best_practices_summary()`

### Search MCP
- `search_knowledge_base(query, search_scope, limit)`
- `find_similar_practices(company_name, industry)`
- `compare_territories(territory_ids)`
- `get_search_suggestions(query_prefix)`

### Documents MCP
- `validate_document(document_type, content, support_measure_id)`
- `check_documents_completeness(support_measure_id, submitted_documents)`
- `generate_document_from_template(template_id, field_values)`
- `verify_support_measure_eligibility(measure_id, applicant_data)`
- `get_document_checklist(support_measure_id)`

## ✅ Чеклист для новой сессии

При продолжении разработки проверьте:

- [ ] `venv/` существует и активирован
- [ ] `frontend/node_modules/` установлен
- [ ] Порт 8000 свободен (бэкенд)
- [ ] Порт 3000 свободен (фронтенд)
- [ ] `investor_data.db` не заблокирован

## 🔧 Распространённые задачи

### Добавить новый MCP-инструмент
1. Добавить функцию в соответствующий файл `src/mcp/*.py` с декоратором `@mcp.tool()`
2. Добавить вызов в `src/api/server.py` для REST-эндпоинта
3. Обновить типы в `frontend/src/types/index.ts` при необходимости

### Добавить новый UI-компонент
1. Создать папку `frontend/src/components/ComponentName/`
2. Добавить `ComponentName.tsx` с TypeScript типами
3. Добавить `ComponentName.module.scss` с импортом `_variables.scss`
4. Экспортировать из компонента

### Изменить дизайн-токены
1. Открыть `frontend/src/styles/_variables.scss`
2. Изменить переменную (например, `$color-primary`)
3. Перезапустить `npm run dev` для применения

### Добавить тестовые данные
1. Открыть `src/api/server.py` → `create_sqlite_session()`
2. Добавить запись в соответствующий список (practices/territories/measures)
3. Удалить `investor_data.db` для пересоздания БД

## ⚠️ Известные ограничения

- **SQLite для демо:** При одновременной записи возможны блокировки. Для продакшена использовать PostgreSQL.
- **CORS:** Настроен только для `localhost:3000`. Для продакшена добавить домен в `allow_origins`.
- **Чат:** Эндпоинт `/api/chat` возвращает моковые ответы. Для реального AI подключить LLM через MCP.
- **Изображения:** Используются заглушки Unsplash. Для продакшена добавить загрузку файлов.

## 📚 Ссылки

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [Phosphor Icons](https://phosphoricons.com)

## 🎯 Цели развития

### Краткосрочные
- [ ] Интеграция с реальным LLM (GPT-4, Claude) для чата
- [ ] Загрузка документов (PDF, DOCX) для валидации
- [ ] Экспорт отчётов в PDF
- [ ] Аутентификация пользователей (JWT)

### Долгосрочные
- [ ] PostgreSQL миграции (Alembic)
- [ ] Кеширование ответов (Redis)
- [ ] WebSocket для real-time обновлений чата
- [ ] Админ-панель для управления данными
- [ ] Деплой на Vercel (фронтенд) + Railway/Render (бэкенд)

---

**Последнее обновление:** Июль 2026  
**Статус:** Прототип готов к демонстрации
