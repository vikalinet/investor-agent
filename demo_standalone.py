"""
Автономная демонстрация на SQLite (без PostgreSQL)

Запуск:
    python demo_standalone.py
"""

import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, BestPractice, InvestmentPotential, SupportMeasure, DocumentTemplate
from datetime import datetime as dt


def create_test_session():
    """Создаёт in-memory SQLite базу с данными"""
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    
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


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title: str):
    print(f"\n📌 {title}")
    print("-" * 50)


def demo_database_mcp(session):
    """Демонстрация Database MCP"""
    from src.mcp.database_server import (
        get_best_practices,
        search_investment_potential,
        get_support_measures,
        analyze_best_practices_summary
    )
    
    print_header("🗄️  DATABASE MCP — Работа с данными")
    
    # Лучшие практики
    print_section("1. Лучшие инвестиционные практики")
    practices = get_best_practices(limit=3)
    for i, p in enumerate(practices, 1):
        print(f"\n   {i}. {p['company_name']} ({p['industry']})")
        print(f"      📍 {p['location']}")
        print(f"      💰 {p['investment_amount']} млн руб.")
        print(f"      👥 {p['jobs_created']} рабочих мест")
        desc = p['description'][:80] + "..." if len(p['description']) > 80 else p['description']
        print(f"      📝 {desc}")
    
    # Территории
    print_section("2. Инвестиционный потенциал территорий")
    territories = search_investment_potential(min_infrastructure_score=7.0)
    for t in territories[:3]:
        print(f"\n   🏙️  {t['territory_name']} ({t['territory_type']})")
        print(f"      📊 Инфраструктура: {t['infrastructure_score']}/10")
        print(f"      🏗️  Участков: {t['available_lots']}")
        print(f"      💼 Отрасли: {', '.join(t['key_industries'][:3])}")
    
    # Меры поддержки
    print_section("3. Меры поддержки инвесторов")
    measures = get_support_measures(include_documents=False)
    for m in measures:
        print(f"\n   ✓ {m['name']}")
        print(f"      Тип: {m['measure_type']}")
        if m['max_amount']:
            print(f"      Сумма: до {m['max_amount']} млн руб.")
        print(f"      📧 {m['contact_email']}")
    
    # Аналитика
    print_section("4. Аналитика лучших практик")
    summary = analyze_best_practices_summary()
    print(f"\n   📈 Всего проектов: {summary['total_projects']}")
    print(f"   💰 Инвестиций: {summary['total_investment_mlrd']} млрд руб.")
    print(f"   👥 Рабочих мест: {summary['total_jobs_created']}")
    print(f"\n   🏆 Топ факторов успеха:")
    for f in summary['top_success_factors'][:3]:
        print(f"      • {f['factor']} ({f['count']} проектов)")


def demo_search_mcp(session):
    """Демонстрация Search MCP"""
    from src.mcp.search_server import search_knowledge_base
    
    print_header("🔍 SEARCH MCP — Поиск по базе знаний")
    
    print_section("Поиск: \"металлургия\"")
    results = search_knowledge_base("металлургия", limit=3)
    
    print(f"\n   Найдено: {results['total_found']} результатов")
    
    if results['best_practices']:
        print(f"\n   📂 Лучшие практики:")
        for item in results['best_practices']:
            snippet = item['snippet'][:60] + "..." if item['snippet'] and len(item['snippet']) > 60 else item['snippet']
            print(f"      • {item['title']} — {snippet}")
    
    if results['territories']:
        print(f"\n   📂 Территории:")
        for item in results['territories']:
            print(f"      • {item['title']}")
    
    if results['support_measures']:
        print(f"\n   📂 Меры поддержки:")
        for item in results['support_measures']:
            print(f"      • {item['title']}")


def demo_documents_mcp(session):
    """Демонстрация Documents MCP"""
    from src.mcp.documents_server import (
        validate_document,
        check_documents_completeness,
        get_document_checklist,
        verify_support_measure_eligibility
    )
    
    print_header("📋 DOCUMENTS MCP — Работа с документами")
    
    print_section("1. Валидация заявления (корректное)")
    valid_result = validate_document(
        document_type="заявление",
        content={
            "заявитель": "ООО \"ИнвестПроект\"",
            "инн": "1234567890",
            "дата": "2025-01-15"
        }
    )
    print(f"   Статус: {'✅ Валиден' if valid_result['is_valid'] else '❌ Не валиден'}")
    if valid_result['errors']:
        print(f"   Ошибки: {', '.join(valid_result['errors'])}")
    if valid_result['warnings']:
        print(f"   Предупреждения: {', '.join(valid_result['warnings'])}")
    if not valid_result['errors'] and not valid_result['warnings']:
        print(f"   {valid_result['recommendations'][0]}")
    
    print_section("2. Валидация заявления (невалидный ИНН)")
    invalid_result = validate_document(
        document_type="заявление",
        content={
            "заявитель": "ООО \"ИнвестПроект\"",
            "инн": "123",
            "дата": "2025-01-15"
        }
    )
    print(f"   Статус: {'✅ Валиден' if invalid_result['is_valid'] else '❌ Не валиден'}")
    if invalid_result['errors']:
        print(f"   Ошибки: {', '.join(invalid_result['errors'])}")
    
    print_section("3. Проверка соответствия критериям меры поддержки")
    eligibility = verify_support_measure_eligibility(
        measure_id=1,
        applicant_data={
            "industry": "manufacturing",
            "investment_amount": 150,
            "location": "Екатеринбург",
            "jobs_created": 50
        }
    )
    print(f"   Мера: {eligibility['measure_name']}")
    print(f"   Соответствие: {'✅ Да' if eligibility['is_eligible'] else '❌ Нет'}")
    print(f"\n   Проверки критериев:")
    for check in eligibility['criteria_checks']:
        status = "✅" if check['passed'] else "❌"
        print(f"      {status} {check['criterion']}")
    print(f"\n   💡 {eligibility['recommendations'][0]}")
    
    print_section("4. Чек-лист документов")
    checklist = get_document_checklist(support_measure_id=1)
    print(f"   Мера: {checklist['measure_name']}")
    print(f"\n   Необходимые документы:")
    for doc in checklist['documents']:
        print(f"      □ {doc['name']}")
        desc = doc['description'][:60] + "..." if len(doc['description']) > 60 else doc['description']
        print(f"        {desc}")


def demo_integration(session):
    """Интеграционная демонстрация"""
    from src.mcp.database_server import (
        get_best_practices,
        search_investment_potential,
        get_support_measures
    )
    
    print_header("🤖 ИНТЕГРАЦИЯ: Помощник инвестора")
    
    print_section("Задача 1: Анализ лучших практик для IT-отрасли")
    it_practices = get_best_practices(industry="IT", limit=2)
    if it_practices:
        for p in it_practices:
            print(f"\n   💻 {p['company_name']}")
            print(f"      📍 {p['location']} • 💰 {p['investment_amount']} млн руб.")
            print(f"      Факторы успеха: {', '.join(p['success_factors'])}")
    else:
        print("   Практик по IT не найдено")
    
    print_section("Задача 2: Поиск территории для IT-проекта")
    it_territories = search_investment_potential(industry="IT", min_infrastructure_score=8.0)
    if it_territories:
        print(f"\n   Найдено {len(it_territories)} подходящих территорий:")
        for t in it_territories:
            print(f"\n   🏙️  {t['territory_name']}")
            print(f"      Инфраструктура: {t['infrastructure_score']}/10")
            льготы = t['tax_benefits'][:70] + "..." if len(t['tax_benefits']) > 70 else t['tax_benefits']
            print(f"      Льготы: {льготы}")
            print(f"      Контакты: {t['contact']['email']}")
    else:
        print("   Территорий с инфраструктурой 8+ для IT не найдено")
        # Показываем все IT-территории
        it_territories = search_investment_potential(industry="IT")
        if it_territories:
            print(f"\n   Все территории для IT ({len(it_territories)}):")
            for t in it_territories:
                print(f"      • {t['territory_name']} (инфраструктура: {t['infrastructure_score']})")
    
    print_section("Задача 3: Подготовка заявки на финансовую поддержку")
    measures = get_support_measures(measure_type="financial", include_documents=True)
    if measures:
        m = measures[0]
        print(f"\n   📋 {m['name']}")
        print(f"   💰 до {m['max_amount']} млн руб.")
        print(f"   📄 Документы: {', '.join(m['required_documents'])}")
        print(f"   📧 {m['contact_email']}")
    else:
        print("   Финансовых мер поддержки не найдено")


def main():
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  ПОМОЩНИК ИНВЕСТОРА В СВЕРДЛОВСКОЙ ОБЛАСТИ".center(68) + "█")
    print("█" + "  Прототип AI-агента с MCP (автономная версия)".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    print(f"\n📅 Дата демонстрации: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("💾 База данных: SQLite in-memory")
    
    # Создаём сессию
    session, engine = create_test_session()
    
    # Подменяем сессию во всех MCP-серверах
    from src.mcp.database_server import set_session_override
    set_session_override(session)
    
    try:
        # Демонстрация каждого MCP-сервера
        demo_database_mcp(session)
        demo_search_mcp(session)
        demo_documents_mcp(session)
        
        # Интеграционная демонстрация
        demo_integration(session)
        
        print_header("✅ Демонстрация завершена!")
        print("\n📚 Исходный код:")
        print("   • src/mcp/database_server.py  — Database MCP")
        print("   • src/mcp/search_server.py    — Search MCP")
        print("   • src/mcp/documents_server.py — Documents MCP")
        print("   • src/agent/core.py           — Ядро агента")
        print("   • src/main.py                 — Точка входа (требует PostgreSQL)")
        print("\n🚀 Запуск с PostgreSQL:")
        print("   docker-compose up -d db")
        print("   python -m src.database.seed_data")
        print("   python -m src.main")
    finally:
        session.close()
    
    print()


if __name__ == "__main__":
    main()
