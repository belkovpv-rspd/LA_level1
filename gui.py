import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import List

from db import (
    add_client, get_all_clients, delete_client, update_client, search_clients,
    export_to_csv, import_from_csv,
    add_product, get_all_products, delete_product
)
from models import Client, Product


class MainApplication(tk.Tk) :
    """
    Главное приложение с вкладками.
    """

    def __init__(self) :
        super().__init__()
        self.title("GIU Inet-shop")
        self.geometry("1000x700")

        # Создаем вкладки
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Создаем фреймы для вкладок
        self.clients_frame = ttk.Frame(self.notebook)
        self.products_frame = ttk.Frame(self.notebook)
        self.data_frame = ttk.Frame(self.notebook)

        # Добавляем вкладки
        self.notebook.add(self.clients_frame, text="Клиенты")
        self.notebook.add(self.products_frame, text="Товары")
        self.notebook.add(self.data_frame, text="Данные")

        # Инициализируем вкладки
        self.init_clients_tab()
        self.init_products_tab()
        self.init_data_tab()

    def init_clients_tab(self) :
        """Инициализация вкладки клиентов."""
        # Панель управления
        control_frame = ttk.Frame(self.clients_frame)
        control_frame.pack(pady=10)

        # Кнопки управления
        self.import_csv_btn = tk.Button(control_frame, text="Импорт из CSV", command=self.import_csv)
        self.import_csv_btn.pack(side=tk.LEFT, padx=5)

        self.export_csv_btn = tk.Button(control_frame, text="Экспорт в CSV", command=self.export_csv)
        self.export_csv_btn.pack(side=tk.LEFT, padx=5)

        # Поля ввода для клиента
        input_frame = ttk.Frame(self.clients_frame)
        input_frame.pack(pady=10)

        labels = ["Имя:", "Фамилия:", "Email:", "Телефон:", "Адрес:"]
        entries = []

        for i, label_text in enumerate(labels) :
            label = tk.Label(input_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=2, sticky=tk.E)
            entry = tk.Entry(input_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries.append(entry)

        self.first_name_entry, self.last_name_entry, self.email_entry, self.phone_entry, self.address_entry = entries

        # Кнопка сохранения
        self.save_client_btn = tk.Button(input_frame, text="Сохранить клиента", command=self.add_client)
        self.save_client_btn.grid(row=5, column=1, pady=10)

        # Поиск
        search_frame = ttk.Frame(self.clients_frame)
        search_frame.pack(pady=10)

        self.search_label = tk.Label(search_frame, text="Поиск:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_btn = tk.Button(search_frame, text="Найти", command=self.search_clients)
        self.search_btn.pack(side=tk.LEFT)

        self.clear_search_btn = tk.Button(search_frame, text="Очистить", command=self.load_clients)
        self.clear_search_btn.pack(side=tk.LEFT, padx=5)

        # Таблица клиентов
        tree_frame = ttk.Frame(self.clients_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("ID", "Имя", "Фамилия", "Email", "Телефон", "Адрес", "Дата регистрации"),
                                 show='headings', height=15)

        columns = ["ID", "Имя", "Фамилия", "Email", "Телефон", "Адрес", "Дата регистрации"]
        for col in columns :
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Scrollbar для таблицы
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Кнопки редактирования/удаления
        edit_frame = ttk.Frame(self.clients_frame)
        edit_frame.pack(pady=5)

        self.edit_btn = tk.Button(edit_frame, text="Редактировать", command=self.edit_client, state=tk.DISABLED)
        self.edit_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(edit_frame, text="Удалить", command=self.delete_client, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # Статус бар
        self.status_bar = tk.Label(self.clients_frame, text="Статус: Готов", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Привязка событий
        self.tree.bind("<ButtonRelease-1>", self.on_client_select)

        # Загружаем клиентов
        self.load_clients()

    def init_products_tab(self) :
        """Инициализация вкладки товаров."""
        # Панель управления
        control_frame = ttk.Frame(self.products_frame)
        control_frame.pack(pady=10)

        # Поля ввода для товара
        input_frame = ttk.Frame(self.products_frame)
        input_frame.pack(pady=10)

        labels = ["Название:", "Описание:", "Цена:"]
        entries = []

        for i, label_text in enumerate(labels) :
            label = tk.Label(input_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=2, sticky=tk.E)
            entry = tk.Entry(input_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries.append(entry)

        self.product_name_entry, self.product_desc_entry, self.product_price_entry = entries

        # Кнопка сохранения товара
        self.save_product_btn = tk.Button(input_frame, text="Сохранить товар", command=self.add_product)
        self.save_product_btn.grid(row=3, column=1, pady=10)

        # Таблица товаров
        tree_frame = ttk.Frame(self.products_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.products_tree = ttk.Treeview(tree_frame, columns=("ID", "Название", "Описание", "Цена"), show='headings',
                                          height=15)

        columns = ["ID", "Название", "Описание", "Цена"]
        for col in columns :
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Кнопки редактирования/удаления
        edit_frame = ttk.Frame(self.products_frame)
        edit_frame.pack(pady=5)

        self.edit_product_btn = tk.Button(edit_frame, text="Редактировать", command=self.edit_product,
                                          state=tk.DISABLED)
        self.edit_product_btn.pack(side=tk.LEFT, padx=5)

        self.delete_product_btn = tk.Button(edit_frame, text="Удалить", command=self.delete_product, state=tk.DISABLED)
        self.delete_product_btn.pack(side=tk.LEFT, padx=5)

        # Загружаем товары
        self.load_products()

        # Привязка событий
        self.products_tree.bind("<ButtonRelease-1>", self.on_product_select)

    def init_data_tab(self) :
        """Инициализация вкладки данных."""
        info_frame = ttk.Frame(self.data_frame)
        info_frame.pack(pady=20)

        info_text = """
        Система управления интернет-магазином

        Функциональность:
        - Управление клиентами
        - Управление товарами
        - Импорт/экспорт данных
        - Поиск и фильтрация

        Версия: a0.1
        """

        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()

    def load_clients(self) :
        """Загрузка клиентов из базы данных."""
        try :
            for item in self.tree.get_children() :
                self.tree.delete(item)

            clients = get_all_clients()
            for client in clients :
                self.tree.insert("", tk.END, values=(
                    client.client_id,
                    client.first_name,
                    client.last_name,
                    client.email,
                    client.phone,
                    client.address,
                    client.registration_date.strftime("%Y-%m-%d")
                ))

            self.status_bar.config(text=f"Статус: Загружено {len(clients)} клиентов ✅")
        except Exception as e :
            messagebox.showerror("Ошибка", f"Не удалось загрузить клиентов: {str(e)}")
            self.status_bar.config(text="Статус: Ошибка загрузки клиентов ❌")

    def add_client(self) :
        """Добавляет нового клиента."""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        if not all([first_name, last_name, email, phone, address]) :
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            self.status_bar.config(text="Статус: Ошибка - не все поля заполнены ❌")
            return

        try :
            client = Client(first_name, last_name, email, phone, address)
            client.registration_date = datetime.now()
            add_client(client)

            # Очищаем поля
            for entry in [self.first_name_entry, self.last_name_entry, self.email_entry, self.phone_entry,
                          self.address_entry] :
                entry.delete(0, tk.END)

            self.load_clients()
            self.status_bar.config(text="Статус: Клиент успешно добавлен ✅")
        except Exception as e :
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {str(e)}")
            self.status_bar.config(text="Статус: Ошибка добавления клиента ❌")

    def on_client_select(self, event) :
        """Обработка выбора клиента в таблице."""
        selection = self.tree.selection()
        if selection :
            self.edit_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else :
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)

    def edit_client(self) :
        """Редактирование выбранного клиента."""
        selection = self.tree.selection()
        if not selection :
            return

        item = self.tree.item(selection[0])
        client_id = item['values'][0]

        # Здесь можно реализовать диалог редактирования
        messagebox.showinfo("Информация", f"Редактирование клиента ID {client_id}")

    def delete_client(self) :
        """Удаление выбранного клиента."""
        selection = self.tree.selection()
        if not selection :
            return

        item = self.tree.item(selection[0])
        client_id = item['values'][0]

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого клиента?") :
            try :
                delete_client(client_id)
                self.load_clients()
                self.status_bar.config(text="Статус: Клиент успешно удален ✅")
            except Exception as e :
                messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {str(e)}")
                self.status_bar.config(text="Статус: Ошибка удаления клиента ❌")

    def search_clients(self) :
        """Поиск клиентов."""
        search_text = self.search_entry.get().strip()
        if not search_text :
            self.load_clients()
            return

        try :
            for item in self.tree.get_children() :
                self.tree.delete(item)

            clients = search_clients(search_text)
            for client in clients :
                self.tree.insert("", tk.END, values=(
                    client.client_id,
                    client.first_name,
                    client.last_name,
                    client.email,
                    client.phone,
                    client.address,
                    client.registration_date.strftime("%Y-%m-%d")
                ))

            self.status_bar.config(text=f"Статус: Найдено {len(clients)} клиентов по запросу '{search_text}' ✅")
        except Exception as e :
            messagebox.showerror("Ошибка", f"Ошибка поиска: {str(e)}")
            self.status_bar.config(text="Статус: Ошибка поиска ❌")

    def import_csv(self) :
        """Импорт данных из CSV."""
        filename = filedialog.askopenfilename(
            title="Выберите базовое имя для CSV файлов",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename :
            try :
                # Убираем расширение .csv если есть
                if filename.endswith('.csv') :
                    filename = filename[:-4]

                import_from_csv(filename)
                self.load_clients()
                self.load_products()
                messagebox.showinfo("Успех", "Данные успешно импортированы из CSV файлов")
                self.status_bar.config(text="Статус: Импорт завершен успешно ✅")
            except Exception as e :
                messagebox.showerror("Ошибка", f"Ошибка импорта: {str(e)}")
                self.status_bar.config(text="Статус: Ошибка импорта ❌")

    def export_csv(self) :
        """Экспорт данных в CSV."""
        filename = filedialog.asksaveasfilename(
            title="Сохранить как базовое имя для CSV файлов",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename :
            try :
                # Убираем расширение .csv если есть
                if filename.endswith('.csv') :
                    filename = filename[:-4]

                export_to_csv(filename)
                messagebox.showinfo("Успех", f"Данные успешно экспортированы в CSV файлы с базовым именем {filename}")
                self.status_bar.config(text="Статус: Экспорт завершен успешно ✅")
            except Exception as e :
                messagebox.showerror("Ошибка", f"Ошибка экспорта: {str(e)}")
                self.status_bar.config(text="Статус: Ошибка экспорта ❌")

    def load_products(self) :
        """Загрузка товаров из базы данных."""
        try :
            for item in self.products_tree.get_children() :
                self.products_tree.delete(item)

            products = get_all_products()
            for product in products :
                self.products_tree.insert("", tk.END, values=(
                    product.product_id,
                    product.name,
                    product.description,
                    product.price
                ))
        except Exception as e :
            messagebox.showerror("Ошибка", f"Не удалось загрузить товары: {str(e)}")

    def add_product(self) :
        """Добавляет новый товар."""
        name = self.product_name_entry.get().strip()
        description = self.product_desc_entry.get().strip()

        try :
            price = float(self.product_price_entry.get().strip())
        except ValueError :
            messagebox.showerror("Ошибка", "Цена должна быть числом")
            return

        if not name :
            messagebox.showerror("Ошибка", "Пожалуйста, заполните название товара")
            return

        try :
            product = Product(name, description, price)
            add_product(product)

            # Очищаем поля
            for entry in [self.product_name_entry, self.product_desc_entry, self.product_price_entry] :
                entry.delete(0, tk.END)

            self.load_products()
            messagebox.showinfo("Успех", "Товар успешно добавлен")
        except Exception as e :
            messagebox.showerror("Ошибка", f"Не удалось добавить товар: {str(e)}")

    def on_product_select(self, event) :
        """Обработка выбора товара в таблице."""
        selection = self.products_tree.selection()
        if selection :
            self.edit_product_btn.config(state=tk.NORMAL)
            self.delete_product_btn.config(state=tk.NORMAL)
        else :
            self.edit_product_btn.config(state=tk.DISABLED)
            self.delete_product_btn.config(state=tk.DISABLED)

    def edit_product(self) :
        """Редактирование выбранного товара."""
        selection = self.products_tree.selection()
        if not selection :
            return

        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]

        messagebox.showinfo("Информация", f"Редактирование товара ID {product_id}")

    def delete_product(self) :
        """Удаление выбранного товара."""
        selection = self.products_tree.selection()
        if not selection :
            return

        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот товар?") :
            try :
                delete_product(product_id)
                self.load_products()
                messagebox.showinfo("Успех", "Товар успешно удален")
            except Exception as e :
                messagebox.showerror("Ошибка", f"Не удалось удалить товар: {str(e)}")


