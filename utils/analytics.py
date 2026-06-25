from collections import defaultdict

RECOMMENDATIONS = {
    "Еда": "Попробуй готовить дома — экономия до 40%.",
    "Кафе": "Ограничь кафе до 2 раз в неделю.",
    "Развлечения": "Ищи бесплатные мероприятия в городе.",
    "Такси": "Используй общественный транспорт.",
    "Одежда": "Покупай в сезон распродаж.",
    "Подписки": "Проверь, какими подписками не пользуешься.",
    "Транспорт": "Рассмотри проездной — выгоднее разовых поездок.",
    "Здоровье": "Проверь полис ОМС — многое покрывается бесплатно.",
    "Коммунальные": "Установи счётчики воды, если ещё нет.",
    "Другое": "Веди учёт мелких трат — они незаметно накапливаются.",
}

def analyze(expenses):
    if not expenses:
        return {}

    total = sum(e.amount for e in expenses)
    by_category = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.amount

    dates = set(e.date for e in expenses)
    avg_per_day = total / len(dates) if dates else 0

    sorted_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    top_category = sorted_categories[0][0] if sorted_categories else None

    recommendation = RECOMMENDATIONS.get(
        top_category,
        f"Категория «{top_category}» самая затратная. Постарайся снизить расходы на 20%."
    ) if top_category else "Добавь расходы для анализа."

    return {
        "total": total,
        "by_category": dict(sorted_categories),
        "avg_per_day": avg_per_day,
        "top_category": top_category,
        "recommendation": recommendation,
    }
