
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from db import get_all_orders, get_all_customers #  Предполагаем, что эти функции есть в db.py

def top_customers_by_orders(n=5):
    """
    Определяет топ-N клиентов по количеству заказов.Returns
    -------
    pandas.DataFrame
        DataFrame с информацией о топ-N клиентах и количестве их заказов.
    """
    orders = pd.DataFrame([(order.customer_id, order.order_date) for order in get_all_orders()], columns=['customer_id', 'order_date'])
    customers = pd.DataFrame([(customer.customer_id, customer.first_name, customer.last_name) for customer in get_all_customers()], columns=['customer_id', 'first_name', 'last_name'])
    
    order_counts = orders['customer_id'].value_counts().nlargest(n)
    top_customers = pd.DataFrame({'customer_id': order_counts.index, 'order_count': order_counts.values})
    
    #  Объединяем с таблицей клиентов для получения имен
    top_customers = pd.merge(top_customers, customers, on='customer_id')
    
    return top_customers


def plot_order_dynamics():
    """
    Строит график динамики количества заказов по датам.
    """
    orders = pd.DataFrame([(order.order_id, order.order_date) for order in get_all_orders()], columns=['order_id', 'order_date'])
    # Преобразуем столбец order_date в datetime
    orders['order_date'] = pd.to_datetime(orders['order_date'])# Группируем по дате и считаем количество заказов
    order_counts = orders.groupby('order_date')['order_id'].count()

    # Строим график
    plt.figure(figsize=(10, 6))
    order_counts.plot(kind='line')
    plt.title('Order Dynamics Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Orders')
    plt.grid(True)
    plt.show()
    
def create_customer_network():
    """
    Создает граф связей клиентов на основе общих товаров в заказах.
    """
    #  !!!  Здесь нужна более сложная логика анализа заказов и товаров для построения графа
    #  Это упрощенный пример, его нужно доработать
    G = nx.Graph()
    #  Пример добавления нескольких узлов и ребер
    G.add_node("Customer A")
    G.add_node("Customer B")
    G.add_edge("Customer A", "Customer B")nx.draw(G, with_labels=True)
plt.show()
