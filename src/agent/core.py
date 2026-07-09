"""
Ядро AI-агента

Оркестрирует вызовы MCP-серверов для решения трёх задач:
1. Анализ лучших практик
2. Поиск инвестиционного потенциала
3. Подготовка и верификация документов
"""

import json
from typing import Any
from datetime import datetime

from src.mcp.database_server import (
    get_best_practices,
    search_investment_potential,
    get_support_measures,
    get_document_templates,
    analyze_best_practices_summary
)
from src.mcp.search_server import (
    search_knowledge_base,
    find_similar_practices,
    compare_territories,
    get_search_suggestions
)
from src.mcp.documents_server import (
    validate_document,
    check_documents_completeness,
    generate_document_from_template,
    verify_support_measure_eligibility,
    get_document_checklist
)


class InvestorAssistantAgent:
    """AI-агент для поддержки инвесторов в Свердловской области"""
    
    def __init__(self):
        self.name = "Помощник инвестора в Свердловской области"
        self.version = "1.0.0"
        self.session_id = datetime.utcnow().isoformat()
    
    # ========== Задача 1: Анализ лучших практик ==========
    
    def analyze_best_practices(self, industry: str | None = None) -> dict[str, Any]:
        """
        Анализ лучших инвестиционных практик.
        
        Args:
            industry: Отрасль для фильтрации (опционально)
        
        Returns:
            Аналитический отчёт
        """
        # 1. Получаем общую сводку
        summary = analyze_best_practices_summary()
        
        # 2. Получаем практики по отрасли если указано
        practices = get_best_practices(
            industry=industry,
            limit=10
        )
        
        # 3. Формируем отчёт
        report = {
            "task": "Анализ лучших практик",
            "generated_at": datetime.utcnow().isoformat(),
            "filters": {"industry": industry},
            "summary": summary,
            "top_practices": practices[:5],
            "recommendations": self._generate_practice_recommendations(summary, practices)
        }
        
        return report
    
    def _generate_practice_recommendations(self, summary: dict, practices: list) -> list[str]:
        """Генерация рекомендаций на основе анализа"""
        recommendations = []
        
        if "top_success_factors" in summary:
            factors = [f["factor"] for f in summary["top_success_factors"][:3]]
            recommendations.append(
                f"Ключевые факторы успеха в регионе: {', '.join(factors)}"
            )
        
        if "by_industry" in summary:
            top_industry = max(summary["by_industry"].items(), 
                              key=lambda x: x[1]["investment"])
            recommendations.append(
                f"Лидер по инвестициям: {top_industry[0]} "
                f"({top_industry[1]['investment']/1000:.1f} млрд руб.)"
            )
        
        if practices:
            avg_jobs = sum(p.get("jobs_created", 0) for p in practices) / len(practices)
            recommendations.append(
                f"Среднее количество создаваемых рабочих мест: {avg_jobs:.0f}"
            )
        
        return recommendations
    
    # ========== Задача 2: Поиск инвестиционного потенциала ==========
    
    def find_investment_opportunities(
        self,
        industry: str | None = None,
        min_infra_score: float | None = None,
        territory_type: str | None = None
    ) -> dict[str, Any]:
        """
        Поиск территорий с инвестиционным потенциалом.
        
        Args:
            industry: Отрасль проекта
            min_infra_score: Минимальный балл инфраструктуры
            territory_type: Тип территории (город, район, ТОСЭР)
        
        Returns:
            Список подходящих территорий с рекомендациями
        """
        # 1. Поиск территорий
        territories = search_investment_potential(
            industry=industry,
            min_infrastructure_score=min_infra_score,
            territory_type=territory_type
        )
        
        # 2. Сравнение топ-3 территорий
        comparison = None
        if len(territories) >= 2:
            top_ids = [t["id"] for t in territories[:3]]
            comparison = compare_territories(top_ids)
        
        # 3. Поиск мер поддержки
        measures = get_support_measures(include_documents=False)
        
        # 4. Формируем отчёт
        report = {
            "task": "Поиск инвестиционного потенциала",
            "generated_at": datetime.utcnow().isoformat(),
            "filters": {
                "industry": industry,
                "min_infra_score": min_infra_score,
                "territory_type": territory_type
            },
            "found_territories": len(territories),
            "territories": territories,
            "comparison": comparison,
            "available_support_measures": len(measures),
            "recommendations": self._generate_territory_recommendations(territories, measures)
        }
        
        return report
    
    def _generate_territory_recommendations(self, territories: list, measures: list) -> list[str]:
        """Генерация рекомендаций по территориям"""
        recommendations = []
        
        if not territories:
            return ["Не найдено территорий по заданным критериям"]
        
        # Лучшая по инфраструктуре
        best_infra = max(territories, key=lambda t: t["infrastructure_score"])
        recommendations.append(
            f"Лучшая инфраструктура: {best_infra['territory_name']} "
            f"(оценка: {best_infra['infrastructure_score']})"
        )
        
        # Больше всего участков
        best_lots = max(territories, key=lambda t: t["available_lots"])
        recommendations.append(
            f"Наибольший выбор участков: {best_lots['territory_name']} "
            f"({best_lots['available_lots']} участков)"
        )
        
        # Доступные меры
        financial_measures = [m for m in measures if m["measure_type"] == "financial"]
        if financial_measures:
            recommendations.append(
                f"Доступно финансовых мер поддержки: {len(financial_measures)}"
            )
        
        return recommendations
    
    # ========== Задача 3: Подготовка и верификация документов ==========
    
    def prepare_support_application(
        self,
        applicant_data: dict[str, Any],
        preferred_measure_type: str | None = None
    ) -> dict[str, Any]:
        """
        Подготовка заявки на меру поддержки.
        
        Args:
            applicant_data: Данные заявителя (отрасль, инвестиции, локация, etc.)
            preferred_measure_type: Предпочтительный тип меры (financial, tax, etc.)
        
        Returns:
            Отчёт о готовности к подаче заявки
        """
        # 1. Получаем меры поддержки
        measures = get_support_measures(
            measure_type=preferred_measure_type,
            include_documents=True
        )
        
        # 2. Проверяем соответствие по каждой мере
        eligibility_results = []
        for measure in measures:
            eligibility = verify_support_measure_eligibility(
                measure_id=measure["id"],
                applicant_data=applicant_data
            )
            eligibility_results.append(eligibility)
        
        # 3. Для подходящих мер получаем чек-листы
        document_checklists = {}
        for result in eligibility_results:
            if result.get("is_eligible"):
                measure_id = None
                for m in measures:
                    if m["name"] == result.get("measure_name"):
                        measure_id = m["id"]
                        break
                
                if measure_id:
                    checklist = get_document_checklist(measure_id)
                    document_checklists[result["measure_name"]] = checklist
        
        # 4. Формируем отчёт
        eligible_measures = [r for r in eligibility_results if r.get("is_eligible")]
        
        report = {
            "task": "Подготовка заявки на меры поддержки",
            "generated_at": datetime.utcnow().isoformat(),
            "applicant_data": applicant_data,
            "total_measures_reviewed": len(measures),
            "eligible_measures": len(eligible_measures),
            "eligibility_results": eligibility_results,
            "document_checklists": document_checklists,
            "recommendations": self._generate_application_recommendations(
                eligible_measures, document_checklists
            )
        }
        
        return report
    
    def _generate_application_recommendations(
        self,
        eligible: list,
        checklists: dict
    ) -> list[str]:
        """Генерация рекомендаций по заявкам"""
        recommendations = []
        
        if not eligible:
            return ["К сожалению, вы не соответствуете критериям доступных мер поддержки"]
        
        recommendations.append(
            f"Вы соответствуете {len(eligible)} мера(ам) поддержки"
        )
        
        for name, checklist in checklists.items():
            docs_count = len(checklist.get("documents", []))
            recommendations.append(
                f"Для '{name}' подготовьте {docs_count} документов"
            )
        
        return recommendations
    
    # ========== Универсальный поиск ==========
    
    def search(self, query: str) -> dict[str, Any]:
        """
        Универсальный поиск по базе знаний.
        
        Args:
            query: Поисковый запрос
        
        Returns:
            Результаты поиска по всем категориям
        """
        results = search_knowledge_base(query, limit=5)
        return {
            "task": "Поиск по базе знаний",
            "generated_at": datetime.utcnow().isoformat(),
            "query": query,
            **results
        }
    
    # ========== Демонстрация ==========
    
    def run_demo(self) -> None:
        """
        Запустить демонстрацию всех трёх задач агента.
        """
        print("=" * 70)
        print(f"🤖 {self.name} v{self.version}")
        print(f"📅 Сессия: {self.session_id}")
        print("=" * 70)
        
        # Задача 1: Анализ лучших практик
        print("\n📊 ЗАДАЧА 1: Анализ лучших практик")
        print("-" * 50)
        
        report1 = self.analyze_best_practices()
        self._print_practice_report(report1)
        
        # Задача 2: Поиск инвестиционного потенциала
        print("\n🗺️  ЗАДАЧА 2: Поиск инвестиционного потенциала")
        print("-" * 50)
        
        report2 = self.find_investment_opportunities(industry="IT")
        self._print_territory_report(report2)
        
        # Задача 3: Подготовка документов
        print("\n📋 ЗАДАЧА 3: Подготовка и верификация документов")
        print("-" * 50)
        
        applicant_data = {
            "industry": "производство",
            "investment_amount": 150,
            "location": "Екатеринбург",
            "jobs_created": 50
        }
        report3 = self.prepare_support_application(applicant_data)
        self._print_document_report(report3)
        
        # Итоги
        print("\n" + "=" * 70)
        print("✅ Демонстрация завершена!")
        print("=" * 70)
    
    def _print_practice_report(self, report: dict) -> None:
        """Вывод отчёта по лучшим практикам"""
        summary = report.get("summary", {})
        
        print(f"\n📈 Общая статистика:")
        print(f"   • Проектов: {summary.get('total_projects', 0)}")
        print(f"   • Инвестиций: {summary.get('total_investment_mlrd', 0)} млрд руб.")
        print(f"   • Рабочих мест: {summary.get('total_jobs_created', 0)}")
        
        print(f"\n🏆 Топ факторов успеха:")
        for factor in summary.get("top_success_factors", [])[:3]:
            print(f"   • {factor['factor']} ({factor['count']} проектов)")
        
        print(f"\n💡 Рекомендации:")
        for rec in report.get("recommendations", []):
            print(f"   → {rec}")
    
    def _print_territory_report(self, report: dict) -> None:
        """Вывод отчёта по территориям"""
        print(f"\n🔍 Найдено территорий: {report.get('found_territories', 0)}")
        
        print(f"\n📍 Подходящие территории:")
        for t in report.get("territories", [])[:3]:
            print(f"\n   {t['territory_name']} ({t['territory_type']})")
            print(f"      • Инфраструктура: {t['infrastructure_score']}/10")
            print(f"      • Участков: {t['available_lots']}")
            print(f"      • Отрасли: {', '.join(t['key_industries'][:3])}")
            print(f"      • Льготы: {t['tax_benefits'][:60]}...")
        
        print(f"\n💡 Рекомендации:")
        for rec in report.get("recommendations", []):
            print(f"   → {rec}")
    
    def _print_document_report(self, report: dict) -> None:
        """Вывод отчёта по документам"""
        print(f"\n📊 Рассмотрено мер: {report.get('total_measures_reviewed', 0)}")
        print(f"✅ Подходящих мер: {report.get('eligible_measures', 0)}")
        
        print(f"\n📋 Чек-листы документов:")
        for measure_name, checklist in report.get("document_checklists", {}).items():
            print(f"\n   {measure_name}:")
            for doc in checklist.get("documents", []):
                print(f"      □ {doc['name']}")
                print(f"        {doc['description']}")
        
        print(f"\n💡 Рекомендации:")
        for rec in report.get("recommendations", []):
            print(f"   → {rec}")


def create_agent() -> InvestorAssistantAgent:
    """Фабрика для создания агента"""
    return InvestorAssistantAgent()
