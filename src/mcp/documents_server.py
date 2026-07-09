"""
MCP Server для работы с документами

Предоставляет инструменты для:
- Валидации документов
- Проверки полноты пакета документов
- Генерации документов по шаблонам
- Верификации соответствия требованиям
"""

import re
from datetime import datetime
from typing import Any
from mcp.server.fastmcp import FastMCP

from src.database.models import SupportMeasure, DocumentTemplate
from src.mcp.database_server import get_db_session

# Создаём MCP сервер
mcp = FastMCP("Investor Documents MCP")


def get_session():
    """Получить сессию (использует подменённую если есть)"""
    return get_db_session()


# Правила валидации для различных типов документов
DOCUMENT_RULES = {
    "заявление": {
        "required_fields": ["заявитель", "инн", "дата"],
        "inn_pattern": r"^\d{10}$|^\d{12}$",
        "max_length": 5000
    },
    "бизнес-план": {
        "required_sections": ["резюме", "описание проекта", "финансовый план", "оценка рисков"],
        "min_pages": 10,
        "requires_financials": True
    },
    "финансовая_отчетность": {
        "required_forms": ["баланс", "отчет_о_прибылях_и_убытках"],
        "max_age_months": 12,
        "requires_audit": False
    },
    "договор_поставки": {
        "required_fields": ["поставщик", "покупатель", "предмет", "сумма", "сроки"],
        "requires_signatures": True
    },
    "технические_условия": {
        "required_fields": ["объект", "вид_ресурса", "мощность", "сроки_подключения"],
        "requires_approval": True
    }
}


@mcp.tool()
def validate_document(
    document_type: str,
    content: dict[str, Any],
    support_measure_id: int | None = None
) -> dict[str, Any]:
    """
    Валидировать документ по правилам.
    
    Args:
        document_type: Тип документа (заявление, бизнес-план, финансовая_отчетность, etc.)
        content: Содержимое документа (словарь полей)
        support_measure_id: ID меры поддержки (для специфичных правил)
    
    Returns:
        Результат валидации с ошибками и рекомендациями
    """
    result = {
        "document_type": document_type,
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "recommendations": [],
        "validated_at": datetime.utcnow().isoformat()
    }
    
    rules = DOCUMENT_RULES.get(document_type)
    
    if not rules:
        result["warnings"].append(f"Нет правил валидации для типа '{document_type}'")
        return result
    
    # Проверка обязательных полей
    required_fields = rules.get("required_fields", [])
    for field in required_fields:
        if field not in content or not content[field]:
            result["errors"].append(f"Отсутствует обязательное поле: {field}")
            result["is_valid"] = False
    
    # Валидация ИНН
    if "инн" in content:
        inn = str(content["инн"]).replace(" ", "").replace("-", "")
        inn_pattern = rules.get("inn_pattern", r"^\d{10}$|^\d{12}$")
        if not re.match(inn_pattern, inn):
            result["errors"].append("Некорректный формат ИНН (должно быть 10 или 12 цифр)")
            result["is_valid"] = False
    
    # Проверка длины документа
    if "content" in content and len(str(content["content"])) > rules.get("max_length", 100000):
        result["warnings"].append("Документ превышает рекомендуемый размер")
    
    # Специфичные проверки для бизнес-плана
    if document_type == "бизнес-план":
        required_sections = rules.get("required_sections", [])
        content_text = str(content.get("content", "")).lower()
        
        for section in required_sections:
            if section not in content_text:
                result["warnings"].append(f"Рекомендуется добавить раздел: {section}")
        
        # Проверка финансовых показателей
        if rules.get("requires_financials"):
            financial_keywords = ["инвестиции", "окупаемость", "выручка", "расходы"]
            has_financials = any(kw in content_text for kw in financial_keywords)
            if not has_financials:
                result["warnings"].append("В бизнес-плане отсутствуют финансовые показатели")
    
    # Генерация рекомендаций
    if result["is_valid"] and not result["warnings"]:
        result["recommendations"].append("Документ полностью соответствует требованиям")
    
    return result


@mcp.tool()
def check_documents_completeness(
    support_measure_id: int,
    submitted_documents: list[str]
) -> dict[str, Any]:
    """
    Проверить полноту пакета документов для меры поддержки.
    
    Args:
        support_measure_id: ID меры поддержки
        submitted_documents: Список предоставленных документов (названия)
    
    Returns:
        Статус полноты пакета с недостающими документами
    """
    session = get_session()
    try:
        measure = session.query(SupportMeasure).get(support_measure_id)
        
        if not measure:
            return {
                "error": f"Мера поддержки с ID {support_measure_id} не найдена",
                "is_complete": False
            }
        
        required_docs = []
        if measure.required_documents:
            import json
            required_docs = json.loads(measure.required_documents)
        
        # Нормализуем названия для сравнения
        submitted_normalized = [d.lower().strip() for d in submitted_documents]
        required_normalized = [d.lower().strip() for d in required_docs]
        
        missing = []
        for req in required_docs:
            req_norm = req.lower().strip()
            if not any(req_norm in sub for sub in submitted_normalized):
                missing.append(req)
        
        is_complete = len(missing) == 0
        
        return {
            "support_measure": measure.name,
            "is_complete": is_complete,
            "required_documents": required_docs,
            "submitted_documents": submitted_documents,
            "missing_documents": missing,
            "completeness_percent": round(
                (len(required_docs) - len(missing)) / len(required_docs) * 100
            ) if required_docs else 100,
            "next_steps": [] if is_complete else [
                f"Подготовьте недостающие документы: {', '.join(missing)}"
            ]
        }
    finally:
        session.close()


@mcp.tool()
def generate_document_from_template(
    template_id: int,
    field_values: dict[str, str]
) -> dict[str, Any]:
    """
    Сгенерировать документ из шаблона.
    
    Args:
        template_id: ID шаблона документа
        field_values: Значения для подстановки в шаблон
    
    Returns:
        Сгенерированный документ
    """
    session = get_session()
    try:
        template = session.query(DocumentTemplate).get(template_id)
        
        if not template:
            return {
                "error": f"Шаблон с ID {template_id} не найден"
            }
        
        # Проверка обязательных полей
        import json
        required_fields = json.loads(template.required_fields) if template.required_fields else []
        missing_fields = [f for f in required_fields if f not in field_values]
        
        if missing_fields:
            return {
                "error": f"Не заполнены обязательные поля: {', '.join(missing_fields)}",
                "required_fields": required_fields
            }
        
        # Подстановка значений в шаблон
        content = template.template_content
        for field, value in field_values.items():
            placeholder = "{{" + field + "}}"
            content = content.replace(placeholder, str(value))
        
        return {
            "template_id": template_id,
            "document_type": template.document_type,
            "document_name": template.template_name,
            "generated_content": content,
            "generated_at": datetime.utcnow().isoformat(),
            "status": "ready"
        }
    finally:
        session.close()


@mcp.tool()
def verify_support_measure_eligibility(
    measure_id: int,
    applicant_data: dict[str, Any]
) -> dict[str, Any]:
    """
    Проверить соответствие заявителя критериям меры поддержки.
    
    Args:
        measure_id: ID меры поддержки
        applicant_data: Данные заявителя для проверки
    
    Returns:
        Результат проверки соответствия критериям
    """
    session = get_session()
    try:
        measure = session.query(SupportMeasure).get(measure_id)
        
        if not measure:
            return {
                "error": f"Мера поддержки с ID {measure_id} не найдена",
                "is_eligible": False
            }
        
        import json
        criteria = json.loads(measure.eligibility_criteria) if measure.eligibility_criteria else {}
        
        result = {
            "measure_name": measure.name,
            "is_eligible": True,
            "criteria_checks": [],
            "recommendations": []
        }
        
        # Проверка минимальных инвестиций
        if "min_investment" in criteria:
            min_inv = criteria["min_investment"]
            applicant_inv = applicant_data.get("investment_amount", 0)
            passed = applicant_inv >= min_inv
            result["criteria_checks"].append({
                "criterion": f"Минимальные инвестиции >= {min_inv} млн руб.",
                "passed": passed,
                "applicant_value": applicant_inv
            })
            if not passed:
                result["is_eligible"] = False
        
        # Проверка отрасли
        if "industry" in criteria:
            allowed_industries = criteria["industry"]
            applicant_ind = applicant_data.get("industry", "").lower()
            passed = any(ind.lower() in applicant_ind for ind in allowed_industries)
            result["criteria_checks"].append({
                "criterion": f"Отрасль в {allowed_industries}",
                "passed": passed,
                "applicant_value": applicant_data.get("industry")
            })
            if not passed:
                result["is_eligible"] = False
        
        # Проверка локации
        if "location" in criteria:
            allowed_locations = criteria["location"]
            applicant_loc = applicant_data.get("location", "").lower()
            passed = any(loc.lower() in applicant_loc for loc in allowed_locations)
            result["criteria_checks"].append({
                "criterion": f"Локация в {allowed_locations}",
                "passed": passed,
                "applicant_value": applicant_data.get("location")
            })
            if not passed:
                result["is_eligible"] = False
        
        # Проверка количества рабочих мест
        if "jobs_min" in criteria:
            min_jobs = criteria["jobs_min"]
            applicant_jobs = applicant_data.get("jobs_created", 0)
            passed = applicant_jobs >= min_jobs
            result["criteria_checks"].append({
                "criterion": f"Рабочих мест >= {min_jobs}",
                "passed": passed,
                "applicant_value": applicant_jobs
            })
            if not passed:
                result["is_eligible"] = False
        
        # Рекомендации
        if result["is_eligible"]:
            result["recommendations"].append(
                f"Вы соответствуете критериям меры '{measure.name}'. Рекомендуется подать заявку."
            )
        else:
            failed_criteria = [c["criterion"] for c in result["criteria_checks"] if not c["passed"]]
            result["recommendations"].append(
                f"Не выполнены критерии: {', '.join(failed_criteria)}. "
                "Рассмотрите другие меры поддержки."
            )
        
        return result
    finally:
        session.close()


@mcp.tool()
def get_document_checklist(support_measure_id: int) -> dict[str, Any]:
    """
    Получить чек-лист документов для меры поддержки.
    
    Args:
        support_measure_id: ID меры поддержки
    
    Returns:
        Чек-лист с описанием каждого документа
    """
    session = get_session()
    try:
        measure = session.query(SupportMeasure).get(support_measure_id)
        
        if not measure:
            return {"error": f"Мера поддержки с ID {support_measure_id} не найдена"}
        
        import json
        required_docs = json.loads(measure.required_documents) if measure.required_documents else []
        
        checklist = {
            "measure_name": measure.name,
            "documents": []
        }
        
        # Описание требований к каждому типу документа
        doc_descriptions = {
            "заявление": "Официальное заявление установленной формы с подписью руководителя",
            "бизнес-план": "Детальный план проекта с финансовыми расчётами (10+ страниц)",
            "финансовая отчетность": "Бухгалтерский баланс и отчёт о прибылях/убытках за последний год",
            "договоры поставки": "Копии договоров с поставщиками оборудования/материалов",
            "технические условия": "ТУ на подключение к инженерным сетям от ресурсоснабжающих организаций",
            "подтверждение локации": "Документы на земельный участок или договор аренды"
        }
        
        for doc in required_docs:
            doc_lower = doc.lower()
            description = next(
                (desc for key, desc in doc_descriptions.items() if key in doc_lower),
                "Документ согласно требованиям"
            )
            
            checklist["documents"].append({
                "name": doc,
                "description": description,
                "status": "pending"
            })
        
        return checklist
    finally:
        session.close()


if __name__ == "__main__":
    mcp.run()
