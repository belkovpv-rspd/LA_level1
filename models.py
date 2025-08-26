"""
Данный модуль содержит

описание классов данных:

-клиент
-продукт
-заказ
"""

import re
from datetime import datetime
from typing import List, Optional

class Person:

    def __init__(self, first_name: str, last_name: str, email: str, phone: str):
        """
        :param first_name:  Имя
        :param last_name:   Фамилия
        :param email:       адрес электронной почты клиента
        :param phone:       телефон клиента
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"{self.__class__.__name__}(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', phone='{self.phone}')"

    def validate_email(self):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, self.email) is not None

    def validate_phone(self):
        phone_pattern = r"^\+?[0-9]{10,12}$"
        return re.match(phone_pattern, self.phone) is not None


class Client(Person):
    """
    наследуется от класса Person

    client_id = уникальный идентификатор клиента  int
    address = адрес клиента str
    registration_date = дата регистрации клиента datetime
    orders = список заказов клиента list[order]
    """

    def __init__(self, first_name: str, last_name: str, email: str, phone: str, address: str):
        super().__init__(first_name, last_name, email, phone)
        self.client_id: Optional[int] = None  # ID устанавливаются как Optional[int] = None и будут заполняться базой данных при сохранении
        self.address = address
        self.registration_date = datetime.now()
        self.orders: List['Order'] = []

    def __repr__(self):
        return f"Client(client_id={self.client_id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', phone='{self.phone}', address='{self.address}', registration_date={self.registration_date})"

    def add_order(self, order: 'Order'):
        # добавление заказа в список заказов
        self.orders.append(order)


class Product:
    def __init__(self, name: str, description: str, price: float):
        self.product_id: Optional[int] = None  # ID устанавливаются как Optional[int] = None и будут заполняться базой данных при сохранении
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return f"Product(product_id={self.product_id}, name='{self.name}', description='{self.description}', price={self.price})"


class Order:
    def __init__(self, client: Client, products: List[Product], status: str = "Создан!"):
        self.order_id: Optional[int] = None  # ID устанавливаются как Optional[int] = None и будут заполняться базой данных при сохранении
        self.client = client
        self.products = products
        self.order_date = datetime.now()
        self.status = status

    def __repr__(self):
        product_names = [product.name for product in self.products]
        return f"Order(order_id={self.order_id}, client={self.client.first_name}, products={product_names}, order_date={self.order_date}, status='{self.status}')"

    def calc_total(self) -> float:
        return sum(product.price for product in self.products)

    def add_product(self, product: Product):
        self.products.append(product)
