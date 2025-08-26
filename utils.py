
import re

def validate_email(email):
    """Проверяет email на соответствие формату."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Проверяет номер телефона на соответствие формату."""
    pattern = r"^\+?[0-9]{10,12}$"  # Пример: +79123456789 или 89123456789
    return re.match(pattern, phone) is not None

def sort_orders(orders, key="date", reverse=False):
    """Сортирует список заказов по дате или стоимости."""
    if key == "date":
        return sorted(orders, key=lambda order: order.order_date, reverse=reverse)
    elif key == "amount":
        return sorted(orders, key=lambda order: order.total_amount, reverse=reverse)
    else:
        return orders  # Возвращаем исходный список, если ключ невалиден
