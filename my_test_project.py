from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Dict, List

DATE_FORMAT = '%Y-%m-%d'

# Словарь для хранения товаров
goods: Dict[str, List[Dict[str, Optional[Decimal]]]] = {}


def add(items, title, amount, expiration_date=None):
    """
    Добавляет товар в словарь items.
    """
    if title not in items:
        items[title] = []
    record = {'amount': Decimal(amount), 'expiration_date': None}
    # Проверяем, является ли expiration_date строкой
    if isinstance(expiration_date, str):
        record['expiration_date'] = datetime.strptime(expiration_date,
                                                      DATE_FORMAT).date()
    else:
        record['expiration_date'] = expiration_date
        # Если это объект date, добавляем напрямую

    items[title].append(record)


def add_by_note(items, note):
    """
    Добавляет товар в словарь items на основе текстовой записи.
    Формат записи: "<Название> <Количество> [Срок_годности]"
    """
    parts = note.split()
    expiration_date = None

    # Определяем, есть ли срок годности
    if len(parts) > 2:
        expiration_date = datetime.strptime(parts[-1], DATE_FORMAT).date()
        parts = parts[:-1]  # Убираем срок годности из списка
    else:
        expiration_date = None

    amount = Decimal(parts[-1])  # Последнее значение — это количество
    title = ' '.join(parts[:-1])  # Остальное — название
    add(items, title, amount, expiration_date)


def find(items, needle):
    """
    Ищет товары в словаре items, которые содержат needle в названии.
    """
    needle = needle.lower()
    found = []
    for title in items:
        if needle in title.lower():
            found.append(title)
    return found


def amount(items, needle):
    """
    Возвращает общее количество товаров, подходящих под поиск needle.
    """
    matching_items = find(items, needle)
    total_amount = Decimal(0)
    for title in matching_items:
        for record in items[title]:
            total_amount += record['amount']
    return total_amount


def expire(items, in_advance_days=0):
    """
    Возвращает список кортежей (название товара, количество),
    срок годности которых истёк, истекает сегодня или истекает
    через in_advance_days дней.
    Если in_advance_days не указан, возвращаются товары, срок
    годности которых истёк или истекает сегодня.
    """
    today = datetime.today().date()
    expiration_threshold = today + timedelta(days=in_advance_days)
    expiring_items = []

    for title, records in items.items():
        total_amount = Decimal(0)
        for record in records:
            expiration_date = record['expiration_date']
            # Проверяем: срок годности истёк, истекает сегодня
            # или в будущем в пределах in_advance_days
            if expiration_date and expiration_date <= expiration_threshold:
                total_amount += record['amount']
        if total_amount > 0:
            expiring_items.append((title, total_amount))
    return expiring_items


# Тестирование
add(goods, 'Яблоки', 10, '2024-12-30')
add(goods, 'Молоко', 5, '2024-12-25')
add_by_note(goods, 'Хлеб 2 2024-12-24')
add_by_note(goods, 'Сахар 15')

print("Товары:", goods)
print("Найденные товары:", find(goods, 'мо'))
print("Общее количество 'молока':", amount(goods, 'молоко'))
print("Товары, срок годности которых истекает через 5 дней:", expire(goods, 5))
