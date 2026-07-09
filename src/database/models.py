"""Модели данных для базы знаний инвестора"""

from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class BestPractice(Base):
    """Лучшие инвестиционные практики в регионе"""
    __tablename__ = "best_practices"
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    location = Column(String(100))  # Район/город
    investment_amount = Column(Float)  # млн руб.
    jobs_created = Column(Integer)
    description = Column(Text)
    success_factors = Column(Text)  # JSON-строка с факторами успеха
    implementation_date = Column(Date)
    status = Column(String(50), default="active")  # active, completed, ongoing
    created_at = Column(DateTime, default=datetime.utcnow)


class InvestmentPotential(Base):
    """Инвестиционный потенциал территорий"""
    __tablename__ = "investment_potential"
    
    id = Column(Integer, primary_key=True)
    territory_name = Column(String(255), nullable=False)
    territory_type = Column(String(50))  # город, район, ОЭЗ, ТОСЭР
    area_km2 = Column(Float)
    population = Column(Integer)
    key_industries = Column(Text)  # JSON-строка
    available_lots = Column(Integer)
    infrastructure_score = Column(Float)  # 1-10
    tax_benefits = Column(Text)  # Описание льгот
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class SupportMeasure(Base):
    """Меры поддержки инвесторов"""
    __tablename__ = "support_measures"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    measure_type = Column(String(50))  # financial, tax, infrastructure, advisory
    description = Column(Text)
    eligibility_criteria = Column(Text)  # JSON-строка с критериями
    max_amount = Column(Float)  # млн руб. или процент
    application_deadline = Column(Date)
    required_documents = Column(Text)  # JSON-строка со списком документов
    responsible_agency = Column(String(255))
    contact_email = Column(String(255))
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentTemplate(Base):
    """Шаблоны документов для мер поддержки"""
    __tablename__ = "document_templates"
    
    id = Column(Integer, primary_key=True)
    support_measure_id = Column(Integer, ForeignKey("support_measures.id"))
    document_type = Column(String(100))  # application, business_plan, financial_report
    template_name = Column(String(255))
    template_content = Column(Text)  # Шаблон с плейсхолдерами
    required_fields = Column(Text)  # JSON-строка с обязательными полями
    created_at = Column(DateTime, default=datetime.utcnow)
    
    support_measure = relationship("SupportMeasure")


class InvestmentProject(Base):
    """Проекты инвесторов (для трекинга)"""
    __tablename__ = "investment_projects"
    
    id = Column(Integer, primary_key=True)
    investor_name = Column(String(255))
    project_name = Column(String(255))
    industry = Column(String(100))
    territory = Column(String(100))
    investment_amount = Column(Float)
    stage = Column(String(50))  # idea, planning, approved, implemented
    applied_measures = Column(Text)  # JSON-строка с ID мер поддержки
    documents_status = Column(String(50))  # draft, submitted, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
