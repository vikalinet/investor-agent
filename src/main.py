"""
Точка входа для демонстрации работы агента

Запуск:
    python -m src.main              — полная демонстрация
    python -m src.main --task 1     — только анализ практик
    python -m src.main --task 2     — только поиск потенциала
    python -m src.main --task 3     — только документы
    python -m src.main --search "металлургия" — поиск
"""

import sys
import json
import argparse

from src.agent.core import create_agent


def main():
    parser = argparse.ArgumentParser(
        description="Помощник инвестора в Свердловской области"
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=[1, 2, 3],
        help="Запустить конкретную задачу (1, 2 или 3)"
    )
    parser.add_argument(
        "--search",
        type=str,
        help="Поиск по базе знаний"
    )
    parser.add_argument(
        "--industry",
        type=str,
        help="Отрасль для фильтрации"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод в JSON формате"
    )
    
    args = parser.parse_args()
    
    agent = create_agent()
    
    if args.search:
        # Режим поиска
        result = agent.search(args.search)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 Поиск: \"{args.search}\"")
            print(f"Найдено: {result['total_found']} результатов\n")
            
            for category, items in [("Лучшие практики", result["best_practices"]),
                                   ("Территории", result["territories"]),
                                   ("Меры поддержки", result["support_measures"])]:
                if items:
                    print(f"📂 {category}:")
                    for item in items:
                        print(f"   • [{item['type']}] {item['title']}")
                        print(f"     {item['snippet']}")
                        print()
        return
    
    if args.task == 1:
        # Анализ лучших практик
        result = agent.analyze_best_practices(industry=args.industry)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            agent._print_practice_report(result)
        return
    
    if args.task == 2:
        # Поиск инвестиционного потенциала
        result = agent.find_investment_opportunities(industry=args.industry)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            agent._print_territory_report(result)
        return
    
    if args.task == 3:
        # Подготовка документов
        applicant_data = {
            "industry": args.industry or "производство",
            "investment_amount": 150,
            "location": "Екатеринбург",
            "jobs_created": 50
        }
        result = agent.prepare_support_application(applicant_data)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        else:
            agent._print_document_report(result)
        return
    
    # Полная демонстрация
    agent.run_demo()


if __name__ == "__main__":
    main()
