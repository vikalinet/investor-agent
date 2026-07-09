"""
MCP Server для поисковых операций

Предоставляет инструменты для:
- Поиска по базе знаний
- Семантического поиска (заготовка)
- Агрегации результатов из разных источников
"""

import re
from typing import Any
from mcp.server.fastmcp import FastMCP

from src.database.models import Base, BestPractice, InvestmentPotential, SupportMeasure
from src.mcp.database_server import get_db_session

# Создаём MCP сервер
mcp = FastMCP("Investor Search MCP")


def get_session():
    """Получить сессию (использует подменённую если есть)"""
    return get_db_session()


def search_in_text(text: str | None, query: str) -> bool:
    """Простой поиск подстроки в тексте"""
    if not text:
        return False
    return query.lower() in text.lower()


@mcp.tool()
def search_knowledge_base(
    query: str,
    search_scope: list[str] | None = None,
    limit: int = 10
) -> dict[str, Any]:
    """
    Поиск по базе знаний инвестора.
    
    Args:
        query: Поисковый запрос
        search_scope: Где искать (best_practices, territories, support_measures)
                     Если None - искать везде
        limit: Максимальное количество результатов в каждой категории
    
    Returns:
        Результаты поиска по категориям
    """
    session = get_session()
    results = {
        "query": query,
        "best_practices": [],
        "territories": [],
        "support_measures": [],
        "total_found": 0
    }
    
    try:
        scope = search_scope or ["best_practices", "territories", "support_measures"]
        
        # Поиск в лучших практиках
        if "best_practices" in scope:
            practices = session.query(BestPractice).limit(100).all()
            for p in practices:
                if (search_in_text(p.company_name, query) or
                    search_in_text(p.industry, query) or
                    search_in_text(p.description, query) or
                    search_in_text(p.location, query)):
                    results["best_practices"].append({
                        "type": "best_practice",
                        "id": p.id,
                        "title": p.company_name,
                        "snippet": p.description[:200] + "..." if p.description and len(p.description) > 200 else p.description,
                        "relevance": calculate_relevance(query, [p.company_name, p.industry, p.description])
                    })
                    if len(results["best_practices"]) >= limit:
                        break
        
        # Поиск в территориях
        if "territories" in scope:
            territories = session.query(InvestmentPotential).limit(100).all()
            for t in territories:
                if (search_in_text(t.territory_name, query) or
                    search_in_text(t.territory_type, query) or
                    search_in_text(t.key_industries, query) or
                    search_in_text(t.tax_benefits, query)):
                    results["territories"].append({
                        "type": "territory",
                        "id": t.id,
                        "title": t.territory_name,
                        "snippet": f"{t.territory_type}: {t.tax_benefits[:150]}..." if t.tax_benefits and len(t.tax_benefits) > 150 else t.tax_benefits,
                        "relevance": calculate_relevance(query, [t.territory_name, t.territory_type, t.tax_benefits])
                    })
                    if len(results["territories"]) >= limit:
                        break
        
        # Поиск в мерах поддержки
        if "support_measures" in scope:
            measures = session.query(SupportMeasure).filter(SupportMeasure.status == "active").limit(100).all()
            for m in measures:
                if (search_in_text(m.name, query) or
                    search_in_text(m.description, query) or
                    search_in_text(m.measure_type, query)):
                    results["support_measures"].append({
                        "type": "support_measure",
                        "id": m.id,
                        "title": m.name,
                        "snippet": m.description[:200] + "..." if m.description and len(m.description) > 200 else m.description,
                        "relevance": calculate_relevance(query, [m.name, m.description, m.measure_type])
                    })
                    if len(results["support_measures"]) >= limit:
                        break
        
        results["total_found"] = (
            len(results["best_practices"]) +
            len(results["territories"]) +
            len(results["support_measures"])
        )
        
        return results
    finally:
        session.close()


@mcp.tool()
def find_similar_practices(company_name: str, industry: str | None = None) -> list[dict[str, Any]]:
    """
    Найти похожие лучшие практики по названию компании или отрасли.
    
    Args:
        company_name: Название компании для поиска аналогов
        industry: Отрасль для фильтрации
    
    Returns:
        Список похожих практик
    """
    session = get_session()
    try:
        query = session.query(BestPractice).filter(BestPractice.status.in_(["active", "completed", "ongoing"]))
        
        if industry:
            query = query.filter(BestPractice.industry.ilike(f"%{industry}%"))
        
        practices = query.all()
        
        # Вычисляем схожесть
        scored = []
        for p in practices:
            score = 0
            
            # Совпадение по отрасли
            if industry and p.industry and industry.lower() in p.industry.lower():
                score += 3
            
            # Совпадение по ключевым словам в названии
            company_words = company_name.lower().split()
            for word in company_words:
                if len(word) > 3 and word in p.company_name.lower():
                    score += 2
            
            # Бонус за规模 (масштаб)
            if p.investment_amount and p.investment_amount > 500:
                score += 1
            
            if score > 0:
                scored.append({
                    "practice": {
                        "id": p.id,
                        "company_name": p.company_name,
                        "industry": p.industry,
                        "location": p.location,
                        "investment_amount": p.investment_amount,
                        "description": p.description,
                        "success_factors": p.success_factors
                    },
                    "similarity_score": score
                })
        
        # Сортируем по релевантности
        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return [s["practice"] for s in scored[:5]]
    finally:
        session.close()


@mcp.tool()
def compare_territories(territory_ids: list[int]) -> dict[str, Any]:
    """
    Сравнить несколько территорий по ключевым параметрам.
    
    Args:
        territory_ids: Список ID территорий для сравнения
    
    Returns:
        Сравнительная таблица территорий
    """
    session = get_session()
    try:
        territories = session.query(InvestmentPotential).filter(
            InvestmentPotential.id.in_(territory_ids)
        ).all()
        
        if len(territories) < 2:
            return {"error": "Для сравнения нужно минимум 2 территории"}
        
        comparison = {
            "territories": [],
            "best_by_metric": {}
        }
        
        max_infra = 0
        max_lots = 0
        min_population = float('inf')
        
        for t in territories:
            t_data = {
                "name": t.territory_name,
                "type": t.territory_type,
                "area_km2": t.area_km2,
                "population": t.population,
                "infrastructure_score": t.infrastructure_score,
                "available_lots": t.available_lots,
                "key_industries": t.key_industries,
                "tax_benefits": t.tax_benefits
            }
            comparison["territories"].append(t_data)
            
            # Определяем лидеров по метрикам
            if t.infrastructure_score > max_infra:
                max_infra = t.infrastructure_score
                comparison["best_by_metric"]["infrastructure"] = t.territory_name
            if t.available_lots > max_lots:
                max_lots = t.available_lots
                comparison["best_by_metric"]["available_lots"] = t.territory_name
            if t.population < min_population:
                min_population = t.population
                comparison["best_by_metric"]["lowest_population"] = t.territory_name
        
        return comparison
    finally:
        session.close()


@mcp.tool()
def get_search_suggestions(query_prefix: str) -> list[str]:
    """
    Получить подсказки для поиска по префиксу.
    
    Args:
        query_prefix: Начало поискового запроса
    
    Returns:
        Список подсказок
    """
    session = get_session()
    suggestions = set()
    
    try:
        # Из названий компаний
        practices = session.query(BestPractice.company_name).limit(50).all()
        for p in practices:
            if p[0] and p[0].lower().startswith(query_prefix.lower()):
                suggestions.add(p[0])
        
        # Из названий территорий
        territories = session.query(InvestmentPotential.territory_name).limit(50).all()
        for t in territories:
            if t[0] and t[0].lower().startswith(query_prefix.lower()):
                suggestions.add(t[0])
        
        # Из названий мер поддержки
        measures = session.query(SupportMeasure.name).filter(SupportMeasure.status == "active").limit(50).all()
        for m in measures:
            if m[0] and m[0].lower().startswith(query_prefix.lower()):
                suggestions.add(m[0])
        
        return sorted(list(suggestions))[:10]
    finally:
        session.close()


def calculate_relevance(query: str, fields: list[str | None]) -> float:
    """Простой расчёт релевантности"""
    query_words = query.lower().split()
    score = 0.0
    
    for field in fields:
        if not field:
            continue
        field_lower = field.lower()
        for word in query_words:
            if word in field_lower:
                score += 1.0
            # Частичное совпадение
            if len(word) > 3 and word[:3] in field_lower:
                score += 0.3
    
    return round(score, 2)


if __name__ == "__main__":
    mcp.run()
