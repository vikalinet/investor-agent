"""
MCP Server для работы с базой данных

Предоставляет инструменты для:
- Чтения данных о лучших практиках
- Поиска инвестиционного потенциала территорий
- Получения информации о мерах поддержки
"""

import asyncio
import json
from typing import Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from mcp.server.fastmcp import FastMCP

from src.database.models import Base, BestPractice, InvestmentPotential, SupportMeasure, DocumentTemplate
from src.utils.config import get_settings

settings = get_settings()

# Создаём MCP сервер
mcp = FastMCP("Investor Database MCP")

# Инициализация SQLAlchemy (отложенная — позволяет подменить сессию для тестов/демо)
_engine = None
_SessionLocal = None
_session_override: Session | None = None


def _init_engine():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(settings.database_url)
        _SessionLocal = sessionmaker(bind=_engine)


def set_session_override(session: Session):
    """Подменить сессию (для демо/тестов на SQLite)"""
    global _session_override
    _session_override = session


def get_db_session():
    if _session_override is not None:
        return _session_override
    _init_engine()
    return _SessionLocal()


@mcp.tool()
def get_best_practices(
    industry: str | None = None,
    location: str | None = None,
    min_investment: float | None = None,
    limit: int = 10
) -> list[dict[str, Any]]:
    """
    Получить лучшие инвестиционные практики.
    
    Args:
        industry: Фильтр по отрасли (например, "металлургия", "IT")
        location: Фильтр по локации (город/район)
        min_investment: Минимальный объем инвестиций (млн руб.)
        limit: Максимальное количество результатов
    
    Returns:
        Список практик с деталями
    """
    session = get_db_session()
    try:
        query = session.query(BestPractice).filter(
            BestPractice.status.in_(["active", "completed", "ongoing"])
        )
        
        if industry:
            query = query.filter(BestPractice.industry.ilike(f"%{industry}%"))
        if location:
            query = query.filter(BestPractice.location.ilike(f"%{location}%"))
        if min_investment:
            query = query.filter(BestPractice.investment_amount >= min_investment)
        
        practices = query.order_by(BestPractice.investment_amount.desc()).limit(limit).all()
        
        return [{
            "id": p.id,
            "company_name": p.company_name,
            "industry": p.industry,
            "location": p.location,
            "investment_amount": p.investment_amount,
            "jobs_created": p.jobs_created,
            "description": p.description,
            "success_factors": json.loads(p.success_factors) if p.success_factors else [],
            "implementation_date": str(p.implementation_date) if p.implementation_date else None
        } for p in practices]
    finally:
        session.close()


@mcp.tool()
def search_investment_potential(
    territory_name: str | None = None,
    territory_type: str | None = None,
    min_infrastructure_score: float | None = None,
    industry: str | None = None
) -> list[dict[str, Any]]:
    """
    Поиск территорий с инвестиционным потенциалом.
    
    Args:
        territory_name: Название территории
        territory_type: Тип (город, район, ТОСЭР, ОЭЗ)
        min_infrastructure_score: Минимальный балл инфраструктуры (1-10)
        industry: Отрасль для поиска подходящих территорий
    
    Returns:
        Список территорий с характеристиками
    """
    session = get_db_session()
    try:
        query = session.query(InvestmentPotential)
        
        if territory_name:
            query = query.filter(InvestmentPotential.territory_name.ilike(f"%{territory_name}%"))
        if territory_type:
            query = query.filter(InvestmentPotential.territory_type.ilike(f"%{territory_type}%"))
        if min_infrastructure_score:
            query = query.filter(InvestmentPotential.infrastructure_score >= min_infrastructure_score)
        
        territories = query.order_by(InvestmentPotential.infrastructure_score.desc()).all()
        
        results = []
        for t in territories:
            # Если указана отрасль, проверяем соответствие
            if industry and t.key_industries:
                industries = json.loads(t.key_industries)
                if not any(industry.lower() in ind.lower() for ind in industries):
                    continue
            
            results.append({
                "id": t.id,
                "territory_name": t.territory_name,
                "territory_type": t.territory_type,
                "area_km2": t.area_km2,
                "population": t.population,
                "key_industries": json.loads(t.key_industries) if t.key_industries else [],
                "available_lots": t.available_lots,
                "infrastructure_score": t.infrastructure_score,
                "tax_benefits": t.tax_benefits,
                "contact": {
                    "person": t.contact_person,
                    "email": t.contact_email
                }
            })
        
        return results
    finally:
        session.close()


@mcp.tool()
def get_support_measures(
    measure_type: str | None = None,
    max_amount: float | None = None,
    include_documents: bool = False
) -> list[dict[str, Any]]:
    """
    Получить доступные меры поддержки инвесторов.
    
    Args:
        measure_type: Тип меры (financial, tax, infrastructure, advisory)
        max_amount: Максимальная сумма (для фильтрации по бюджету)
        include_documents: Включить список требуемых документов
    
    Returns:
        Список мер поддержки с деталями
    """
    session = get_db_session()
    try:
        query = session.query(SupportMeasure).filter(SupportMeasure.status == "active")
        
        if measure_type:
            query = query.filter(SupportMeasure.measure_type == measure_type)
        
        measures = query.all()
        
        results = []
        for m in measures:
            measure_data = {
                "id": m.id,
                "name": m.name,
                "measure_type": m.measure_type,
                "description": m.description,
                "eligibility_criteria": json.loads(m.eligibility_criteria) if m.eligibility_criteria else {},
                "max_amount": m.max_amount,
                "application_deadline": str(m.application_deadline) if m.application_deadline else None,
                "responsible_agency": m.responsible_agency,
                "contact_email": m.contact_email
            }
            
            if include_documents and m.required_documents:
                measure_data["required_documents"] = json.loads(m.required_documents)
            
            results.append(measure_data)
        
        return results
    finally:
        session.close()


@mcp.tool()
def get_document_templates(support_measure_id: int) -> list[dict[str, Any]]:
    """
    Получить шаблоны документов для конкретной меры поддержки.
    
    Args:
        support_measure_id: ID меры поддержки
    
    Returns:
        Список шаблонов документов
    """
    session = get_db_session()
    try:
        templates = session.query(DocumentTemplate).filter(
            DocumentTemplate.support_measure_id == support_measure_id
        ).all()
        
        return [{
            "id": t.id,
            "document_type": t.document_type,
            "template_name": t.template_name,
            "template_content": t.template_content,
            "required_fields": json.loads(t.required_fields) if t.required_fields else []
        } for t in templates]
    finally:
        session.close()


@mcp.tool()
def analyze_best_practices_summary() -> dict[str, Any]:
    """
    Получить сводную аналитику по лучшим практикам.
    
    Returns:
        Статистика и инсайты по успешным проектам
    """
    session = get_db_session()
    try:
        practices = session.query(BestPractice).filter(
            BestPractice.status.in_(["active", "completed", "ongoing"])
        ).all()
        
        if not practices:
            return {"error": "Нет данных для анализа"}
        
        # Аналитика по отраслям
        industries = {}
        total_investment = 0
        total_jobs = 0
        
        for p in practices:
            ind = p.industry or "Другое"
            if ind not in industries:
                industries[ind] = {"count": 0, "investment": 0, "jobs": 0}
            industries[ind]["count"] += 1
            industries[ind]["investment"] += p.investment_amount or 0
            industries[ind]["jobs"] += p.jobs_created or 0
            
            total_investment += p.investment_amount or 0
            total_jobs += p.jobs_created or 0
        
        # Топ факторов успеха
        all_factors = []
        for p in practices:
            if p.success_factors:
                all_factors.extend(json.loads(p.success_factors))
        
        factor_counts = {}
        for f in all_factors:
            factor_counts[f] = factor_counts.get(f, 0) + 1
        
        top_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_projects": len(practices),
            "total_investment_mlrd": round(total_investment / 1000, 2),
            "total_jobs_created": total_jobs,
            "avg_investment_per_project": round(total_investment / len(practices), 2),
            "by_industry": industries,
            "top_success_factors": [{"factor": f, "count": c} for f, c in top_factors],
            "locations": list(set(p.location for p in practices if p.location))
        }
    finally:
        session.close()


if __name__ == "__main__":
    # Запуск MCP сервера
    mcp.run()
