"""Тестовые данные для Свердловской области"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, BestPractice, InvestmentPotential, SupportMeasure, DocumentTemplate
from src.utils.config import get_settings
from datetime import date, datetime


def get_session():
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_best_practices(session):
    """Лучшие практики региона"""
    practices = [
        BestPractice(
            company_name="Уральская Сталь",
            industry="Металлургия",
            location="Екатеринбург",
            investment_amount=2500.0,
            jobs_created=450,
            description="Модернизация металлургического производства с внедрением технологий Industry 4.0",
            success_factors='["господдержка", "квалифицированные кадры", "логистика"]',
            implementation_date=date(2025, 6, 15),
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
            implementation_date=date(2025, 3, 1),
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
            implementation_date=date(2024, 11, 20),
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
            implementation_date=date(2026, 1, 10),
            status="ongoing"
        ),
    ]
    
    for practice in practices:
        session.add(practice)
    session.commit()
    print(f"✓ Добавлено {len(practices)} лучших практик")


def seed_investment_potential(session):
    """Инвестиционный потенциал территорий"""
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
    
    for territory in territories:
        session.add(territory)
    session.commit()
    print(f"✓ Добавлено {len(territories)} территорий с инвестпотенциалом")


def seed_support_measures(session):
    """Меры поддержки инвесторов"""
    measures = [
        SupportMeasure(
            name="Субсидия на компенсацию части затрат на оборудование",
            measure_type="financial",
            description="Компенсация до 20% затрат на приобретение оборудования для промышленных проектов",
            eligibility_criteria='{"min_investment": 50, "industry": ["manufacturing", "agriculture"], "jobs_min": 25}',
            max_amount=100.0,
            application_deadline=date(2026, 12, 31),
            required_documents='["заявление", "бизнес-план", "договоры поставки", "финансовая отчетность"]',
            responsible_agency="Министерство инвестиций и развития Свердловской области",
            contact_email="support@mininvest.mid.ural.ru"
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
            contact_email="toser@krsu.mid.ural.ru"
        ),
        SupportMeasure(
            name="Субсидия на инфраструктуру",
            measure_type="infrastructure",
            description="Компенсация затрат на подключение к инженерным сетям (электричество, газ, вода)",
            eligibility_criteria='{"min_investment": 100, "priority_industries": ["manufacturing", "agriculture", "logistics"]}',
            max_amount=50.0,
            application_deadline=date(2026, 10, 31),
            required_documents='["заявление", "технические условия", "сметы", "договоры с ресурсоснабжающими организациями"]',
            responsible_agency="Министерство инвестиций и развития Свердловской области",
            contact_email="infra@mininvest.mid.ural.ru"
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
            contact_email="consult@business-ural.ru"
        ),
        SupportMeasure(
            name="Грант для начинающих предпринимателей",
            measure_type="financial",
            description="Грант до 500 тыс. рублей на запуск бизнеса",
            eligibility_criteria='{"experience_years": 0, "age_max": 35, "unemployed": true}',
            max_amount=0.5,
            application_deadline=date(2027, 6, 30),
            required_documents='["заявление", "бизнес-план", "диплом/сертификат обучения"]',
            responsible_agency="Центр занятости населения",
            contact_email="grant@czn.mid.ural.ru"
        ),
    ]
    
    for measure in measures:
        session.add(measure)
    session.commit()
    print(f"✓ Добавлено {len(measures)} мер поддержки")


def seed_document_templates(session):
    """Шаблоны документов"""
    templates = [
        DocumentTemplate(
            support_measure_id=1,
            document_type="application",
            template_name="Заявление на субсидию оборудования",
            template_content="""
ЗАЯВЛЕНИЕ
на предоставление субсидии на компенсацию части затрат на оборудование

Заявитель: {{applicant_name}}
ИНН: {{inn}}
Адрес: {{address}}

Прошу предоставить субсидию в размере {{requested_amount}} рублей
на компенсацию затрат по проекту: {{project_name}}

Приложения:
1. Бизнес-план
2. Договоры поставки оборудования
3. Финансовая отчетность
""",
            required_fields='["applicant_name", "inn", "address", "requested_amount", "project_name"]'
        ),
        DocumentTemplate(
            support_measure_id=1,
            document_type="business_plan",
            template_name="Структура бизнес-плана",
            template_content="""
БИЗНЕС-ПЛАН
Проект: {{project_name}}

1. Резюме проекта
   - Цель проекта: {{goal}}
   - Сумма инвестиций: {{investment_amount}}
   - Срок окупаемости: {{payback_period}}

2. Описание компании
3. Анализ рынка
4. Производственный план
5. Финансовый план
6. Оценка рисков
""",
            required_fields='["project_name", "goal", "investment_amount", "payback_period"]'
        ),
        DocumentTemplate(
            support_measure_id=2,
            document_type="application",
            template_name="Заявление на статус резидента ТОСЭР",
            template_content="""
ЗАЯВЛЕНИЕ
на получение статуса резидента ТОСЭР

Заявитель: {{applicant_name}}
ИНН: {{inn}}

Планируемая локация: {{location}}
Вид деятельности: {{activity_type}}
Объем инвестиций: {{investment_amount}} млн руб.
Количество рабочих мест: {{jobs_count}}

Приложения:
1. Бизнес-план
2. Подтверждение локации
""",
            required_fields='["applicant_name", "inn", "location", "activity_type", "investment_amount", "jobs_count"]'
        ),
    ]
    
    for template in templates:
        session.add(template)
    session.commit()
    print(f"✓ Добавлено {len(templates)} шаблонов документов")


def seed_all():
    """Заполнение базы всеми данными"""
    session = get_session()
    
    # Очищаем существующие данные
    session.query(DocumentTemplate).delete()
    session.query(InvestmentProject).delete()
    session.query(SupportMeasure).delete()
    session.query(InvestmentPotential).delete()
    session.query(BestPractice).delete()
    session.commit()
    
    print("🌱 Инициализация базы данных...")
    seed_best_practices(session)
    seed_investment_potential(session)
    seed_support_measures(session)
    seed_document_templates(session)
    
    session.close()
    print("\n✅ База данных успешно заполнена!")


if __name__ == "__main__":
    seed_all()
