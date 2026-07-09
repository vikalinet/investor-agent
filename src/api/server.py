"""
FastAPI сервер для веб-интерфейса

Запуск:
    python -m src.api.server

Сервер запускается на http://localhost:8000
CORS разрешён для http://localhost:3000 (Next.js)
"""

import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, BestPractice, InvestmentPotential, SupportMeasure, DocumentTemplate
from src.mcp.database_server import set_session_override
from datetime import datetime as dt


# ============================================================================
#  Инициализация SQLite с тестовыми данными
# ============================================================================

def create_sqlite_session():
    """Создаёт file-based SQLite базу с данными"""
    engine = create_engine("sqlite:///./investor_data.db", echo=False, future=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    
    # Проверяем, есть ли уже данные
    if session.query(BestPractice).count() > 0:
        return session, engine
    
    # Заполняем данными
    practices = [
        BestPractice(
            company_name="Уральская Сталь",
            industry="Металлургия",
            location="Екатеринбург",
            investment_amount=2500.0,
            jobs_created=450,
            description="Модернизация металлургического производства с внедрением технологий Industry 4.0",
            success_factors='["господдержка", "квалифицированные кадры", "логистика"]',
            implementation_date=dt(2023, 6, 15).date(),
            status="completed"
        ),
        BestPractice(
            company_name="АгроТех Средний Урал",
            industry="Сельское хозяйство",
            location="Сысертский район",
            investment_amount=350.0,
            jobs_created=120,
            description="Создание тепличного комплекса с круглогодичным циклом производства",
            success_factors='["налоговые льготы", "близость к рынку сбыта", "инфраструктура"]',
            implementation_date=dt(2023, 3, 1).date(),
            status="active"
        ),
        BestPractice(
            company_name="Логистика Урал",
            industry="Логистика",
            location="Арамиль",
            investment_amount=800.0,
            jobs_created=200,
            description="Логистический хаб класса А с автоматизированным складом",
            success_factors='["ТОСЭР льготы", "транспортная доступность", "земельный участок"]',
            implementation_date=dt(2022, 11, 20).date(),
            status="active"
        ),
        BestPractice(
            company_name="ИТ-Кластер Екатеринбург",
            industry="IT и телекоммуникации",
            location="Екатеринбург",
            investment_amount=150.0,
            jobs_created=300,
            description="Технопарк для IT-стартапов с акселерационной программой",
            success_factors='["кадровый потенциал", "университеты", "льготы для IT"]',
            implementation_date=dt(2024, 1, 10).date(),
            status="ongoing"
        ),
    ]
    
    territories = [
        InvestmentPotential(
            territory_name="Екатеринбург",
            territory_type="город",
            area_km2=495.0,
            population=1540000,
            key_industries='["машиностроение", "IT", "финансы", "торговля"]',
            available_lots=25,
            infrastructure_score=9.2,
            tax_benefits="Льготы для резидентов ОЭЗ, поддержка инноваций",
            contact_person="Иванов Петр Сергеевич",
            contact_email="invest@ekburg.ru"
        ),
        InvestmentPotential(
            territory_name="Нижний Тагил",
            territory_type="город",
            area_km2=298.0,
            population=345000,
            key_industries='["металлургия", "машиностроение", "химия"]',
            available_lots=18,
            infrastructure_score=7.8,
            tax_benefits="Поддержка промышленных предприятий",
            contact_person="Петров Иван Иванович",
            contact_email="invest@ntagil.ru"
        ),
        InvestmentPotential(
            territory_name="ТОСЭР Краснотурьинск",
            territory_type="ТОСЭР",
            area_km2=58.0,
            population=55000,
            key_industries='["алюминий", "деревообработка", "пищевая промышленность"]',
            available_lots=12,
            infrastructure_score=6.5,
            tax_benefits="Налог на прибыль 0-5%, страховые взносы 7.6%, земля в аренду без торгов",
            contact_person="Сидорова Анна Петровна",
            contact_email="toser@krasnoturinsk.ru"
        ),
        InvestmentPotential(
            territory_name="Сысертский район",
            territory_type="район",
            area_km2=3520.0,
            population=52000,
            key_industries='["сельское хозяйство", "туризм", "пищевая промышленность"]',
            available_lots=35,
            infrastructure_score=7.0,
            tax_benefits="Льготы для агропромышленных проектов",
            contact_person="Козлов Дмитрий Михайлович",
            contact_email="invest@sysert.ru"
        ),
        InvestmentPotential(
            territory_name="Арамиль",
            territory_type="город",
            area_km2=25.0,
            population=18000,
            key_industries='["логистика", "легкая промышленность", "пищевая промышленность"]',
            available_lots=8,
            infrastructure_score=7.5,
            tax_benefits="Близость к Екатеринбургу, льготная аренда",
            contact_person="Новикова Елена Владимировна",
            contact_email="invest@aramil.ru"
        ),
    ]
    
    measures = [
        SupportMeasure(
            name="Субсидия на компенсацию части затрат на оборудование",
            measure_type="financial",
            description="Компенсация до 20% затрат на приобретение оборудования для промышленных проектов",
            eligibility_criteria='{"min_investment": 50, "industry": ["manufacturing", "agriculture"], "jobs_min": 25}',
            max_amount=100.0,
            application_deadline=dt(2025, 12, 31).date(),
            required_documents='["заявление", "бизнес-план", "договоры поставки", "финансовая отчетность"]',
            responsible_agency="Министерство инвестиций и развития Свердловской области",
            contact_email="support@mininvest.mid.ural.ru",
            status="active"
        ),
        SupportMeasure(
            name="Налоговые льготы для резидентов ТОСЭР",
            measure_type="tax",
            description="Снижение налога на прибыль до 0-5%, страховые взносы 7.6% в течение 10 лет",
            eligibility_criteria='{"location": ["ТОСЭР"], "industry_excluded": ["mining", "oil_gas"]}',
            max_amount=None,
            application_deadline=None,
            required_documents='["заявление", "бизнес-план", "подтверждение локации"]',
            responsible_agency="Корпорация развития Среднего Урала",
            contact_email="toser@krsu.mid.ural.ru",
            status="active"
        ),
        SupportMeasure(
            name="Субсидия на инфраструктуру",
            measure_type="infrastructure",
            description="Компенсация затрат на подключение к инженерным сетям (электричество, газ, вода)",
            eligibility_criteria='{"min_investment": 100, "priority_industries": ["manufacturing", "agriculture", "logistics"]}',
            max_amount=50.0,
            application_deadline=dt(2025, 10, 31).date(),
            required_documents='["заявление", "технические условия", "сметы", "договоры с ресурсоснабжающими организациями"]',
            responsible_agency="Министерство инвестиций и развития Свердловской области",
            contact_email="infra@mininvest.mid.ural.ru",
            status="active"
        ),
        SupportMeasure(
            name="Консультационная поддержка",
            measure_type="advisory",
            description="Бесплатные консультации по ведению бизнеса, правовым вопросам, поиску партнёров",
            eligibility_criteria='{"investor_type": ["smo", "startup", "foreign"]}',
            max_amount=None,
            application_deadline=None,
            required_documents='["заявление", "описание проекта"]',
            responsible_agency="Центр поддержки предпринимательства",
            contact_email="consult@business-ural.ru",
            status="active"
        ),
        SupportMeasure(
            name="Грант для начинающих предпринимателей",
            measure_type="financial",
            description="Грант до 500 тыс. рублей на запуск бизнеса",
            eligibility_criteria='{"experience_years": 0, "age_max": 35, "unemployed": true}',
            max_amount=0.5,
            application_deadline=dt(2025, 6, 30).date(),
            required_documents='["заявление", "бизнес-план", "диплом/сертификат обучения"]',
            responsible_agency="Центр занятости населения",
            contact_email="grant@czn.mid.ural.ru",
            status="active"
        ),
    ]
    
    templates = [
        DocumentTemplate(
            support_measure_id=1,
            document_type="application",
            template_name="Заявление на субсидию оборудования",
            template_content="ЗАЯВЛЕНИЕ\nЗаявитель: {{applicant_name}}\nИНН: {{inn}}\nПроект: {{project_name}}",
            required_fields='["applicant_name", "inn", "project_name"]'
        ),
        DocumentTemplate(
            support_measure_id=1,
            document_type="business_plan",
            template_name="Структура бизнес-плана",
            template_content="БИЗНЕС-ПЛАН\nПроект: {{project_name}}\n1. Резюме\n2. Финансовый план",
            required_fields='["project_name", "goal", "investment_amount"]'
        ),
    ]
    
    session.add_all(practices + territories + measures + templates)
    session.commit()
    
    return session, engine


# Инициализируем сессию и подменяем во всех MCP-модулях
sqlite_session, sqlite_engine = create_sqlite_session()
set_session_override(sqlite_session)


# ============================================================================
#  FastAPI приложение
# ============================================================================

app = FastAPI(
    title="Investor Assistant API",
    description="API для веб-интерфейса инвестиционного помощника",
    version="1.0.0"
)

# CORS для Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
#  Pydantic модели для API
# ============================================================================

class SupportMeasureResponse(BaseModel):
    id: int
    name: str
    type: str
    maxAmount: Optional[float] = None


class InvestmentProjectResponse(BaseModel):
    id: str
    name: str
    industry: str
    location: str
    imageUrl: str
    investmentAmount: float
    irr: float
    npv: float
    paybackPeriod: int
    jobsCreated: int
    status: str
    progress: int
    supportMeasures: List[SupportMeasureResponse]


class KPIResponse(BaseModel):
    id: str
    label: str
    value: str
    unit: Optional[str] = None
    trend: Optional[dict] = None


class ChatMessageRequest(BaseModel):
    message: str


# ============================================================================
#  Эндпоинты
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Проверка доступности API"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/kpi", response_model=List[KPIResponse])
async def get_kpi():
    """Получить KPI для дашборда"""
    # В реальности здесь были бы запросы к MCP-серверам
    return [
        {"id": "projects", "label": "Активные проекты", "value": "24", "trend": {"direction": "up", "value": "12%"}},
        {"id": "budget", "label": "Общий бюджет", "value": "3.65", "unit": "млрд ₽", "trend": {"direction": "up", "value": "8%"}},
        {"id": "grants", "label": "Доступные гранты", "value": "12", "trend": {"direction": "stable", "value": "0%"}},
        {"id": "jobs", "label": "Создано рабочих мест", "value": "770", "trend": {"direction": "up", "value": "15%"}},
    ]


@app.get("/api/projects", response_model=List[InvestmentProjectResponse])
async def get_projects(industry: Optional[str] = None, limit: int = 10):
    """Получить список инвестиционных проектов"""
    # Импортируем здесь, чтобы избежать циклических импортов
    from src.mcp.database_server import get_best_practices, search_investment_potential, get_support_measures
    
    # Получаем лучшие практики
    practices = get_best_practices(industry=industry, limit=limit)
    
    # Получаем меры поддержки
    measures = get_support_measures()
    
    # Маппинг изображений по отраслям (placehold.co — надёжный placeholder)
    image_map = {
        "Металлургия": "https://placehold.co/600x400/1a3a6b/ffffff?text=Металлургия",
        "Сельское хозяйство": "https://placehold.co/600x400/2E9B72/ffffff?text=Сельское+хозяйство",
        "Логистика": "https://placehold.co/600x400/3B7CC8/ffffff?text=Логистика",
        "IT и телекоммуникации": "https://placehold.co/600x400/8B5CF6/ffffff?text=IT",
    }
    
    # Конвертируем в формат InvestmentProject
    projects = []
    for p in practices:
        # Находим подходящие меры поддержки
        project_measures = []
        if "металлург" in p.get("industry", "").lower():
            project_measures = [m for m in measures if m["measure_type"] in ["financial", "tax"]][:2]
        elif "сельск" in p.get("industry", "").lower():
            project_measures = [m for m in measures if m["measure_type"] in ["financial", "infrastructure"]][:2]
        elif "логист" in p.get("industry", "").lower():
            project_measures = [m for m in measures if m["measure_type"] in ["tax", "infrastructure"]][:2]
        elif "it" in p.get("industry", "").lower() or "телеком" in p.get("industry", "").lower():
            project_measures = [m for m in measures if m["measure_type"] in ["tax", "financial"]][:2]
        
        # Определяем статус и прогресс
        status_map = {
            "completed": "implemented",
            "active": "ongoing",
            "ongoing": "ongoing"
        }
        progress_map = {
            "completed": 100,
            "active": 65,
            "ongoing": 40
        }
        
        # Генерируем метрики на основе данных
        investment = p.get("investment_amount", 100)
        projects.append({
            "id": str(p["id"]),
            "name": p["company_name"],
            "industry": p["industry"],
            "location": p["location"],
            "imageUrl": image_map.get(p["industry"], "https://placehold.co/600x400/0B1F3B/C8A96E?text=ИнвестПроект"),
            "investmentAmount": investment,
            "irr": round(15 + (investment / 1000) * 5, 1),  # Имитация IRR
            "npv": round(investment * 0.18, 0),  # Имитация NPV
            "paybackPeriod": int(36 - (investment / 100)),  # Имитация срока окупаемости
            "jobsCreated": p.get("jobs_created", 0),
            "status": status_map.get(p.get("status", "active"), "ongoing"),
            "progress": progress_map.get(p.get("status", "active"), 50),
            "supportMeasures": [
                {"id": str(m["id"]), "name": m["name"], "type": m["measure_type"], "maxAmount": m.get("max_amount")}
                for m in project_measures
            ],
        })
    
    return projects


@app.get("/api/territories")
async def get_territories(min_infra: Optional[float] = None, industry: Optional[str] = None):
    """Получить территории с инвестиционным потенциалом"""
    from src.mcp.database_server import search_investment_potential
    
    territories = search_investment_potential(
        min_infrastructure_score=min_infra,
        industry=industry
    )
    return territories


@app.get("/api/support-measures")
async def get_support_measures(measure_type: Optional[str] = None):
    """Получить меры поддержки"""
    from src.mcp.database_server import get_support_measures
    
    measures = get_support_measures(measure_type=measure_type, include_documents=True)
    return measures


@app.get("/api/search")
async def search(query: str):
    """Поиск по базе знаний"""
    from src.mcp.search_server import search_knowledge_base
    
    results = search_knowledge_base(query, limit=5)
    return results


@app.post("/api/chat")
async def chat(request: ChatMessageRequest):
    """Обработка сообщения чата (имитация)"""
    # В реальности здесь был бы вызов LLM через MCP
    message = request.message.lower()
    
    response = {
        "role": "agent",
        "content": "Спасибо за ваш вопрос! Я анализирую информацию...",
        "timestamp": datetime.utcnow().isoformat(),
        "embeddedCards": []
    }
    
    if "проект" in message or "инвестиц" in message:
        response["content"] = "Нашёл несколько перспективных инвестиционных проектов:"
        # Возвращаем проекты для встраивания в чат
        from src.mcp.database_server import get_best_practices
        practices = get_best_practices(limit=2)
        response["embeddedCards"] = practices
    
    elif "территор" in message or "район" in message:
        response["content"] = "В Свердловской области есть несколько территорий с высоким инвестиционным потенциалом:"
        from src.mcp.database_server import search_investment_potential
        territories = search_investment_potential(min_infrastructure_score=8.0)
        response["embeddedCards"] = territories
    
    elif "поддержк" in message or "субсид" in message or "грант" in message:
        response["content"] = "Доступные меры поддержки для вашего проекта:"
        from src.mcp.database_server import get_support_measures
        measures = get_support_measures()
        response["embeddedCards"] = measures[:3]
    
    return response


# ============================================================================
#  Запуск сервера
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("  🚀 Investor Assistant API Server")
    print("=" * 60)
    print(f"\n  📅 Запуск: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("  💾 База данных: SQLite (investor_data.db)")
    print("\n  🌐 API доступен:")
    print("     http://localhost:8000")
    print("     http://localhost:8000/docs — Swagger UI")
    print("\n  📡 Эндпоинты:")
    print("     GET  /api/health          — проверка статуса")
    print("     GET  /api/kpi             — KPI дашборда")
    print("     GET  /api/projects        — список проектов")
    print("     GET  /api/territories     — территории")
    print("     GET  /api/support-measures — меры поддержки")
    print("     GET  /api/search?q=...    — поиск")
    print("     POST /api/chat            — чат с агентом")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
