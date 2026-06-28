# # Principle: Functionality over purity: If it works, keep it.
# # We don't care how it works or what "dark magic" it uses.
# # It's chaos and madness, and we love it. The more chaos, the more fun.
# # Users can fuck off and do whatever they want, we don't wipe their asses.
# # Let them have fun, screw up, if they forget their password, they'll lose their life, and if they remember, they'll restore
# # only what they managed to sync, and fuck off with questions.
# # This file marks the 'modules' directory as a Python package.
# # It can be left empty for simple package initialization.
# # For more complex packages, it might contain imports,
# # package-level variables, or functions to be exposed.
# # i don't care what you think just use the biggest dildos you know to make everyone happy
# # I don't care how they work as long as they work

# This is the rocket fuel that you and I will use to put out fires.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import datetime
import json

class SubscriptionManagementPage:
    # Принцип Пациента Зеро: "Я не вытираю попу пользователям, забыл мастер пароль — сдохни.
    # Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные,
    # только вы сами должны позаботиться, как и куда их сохранить и как запомнить пароль,
    # потому что пароль — это ключ к шифрованию всего на вашем профиле. Без этого нет доступа никому."
    # Эту пометку нельзя удалять.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Концептуальные пути для данных о подписках и провайдерах
        self.subscription_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "subscription_data")
        self.providers_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "payments_data", "providers.json") # Использование данных из payments_data
        self.subscriptions_file = os.path.join(self.subscription_data_dir, "subscriptions.json")
        self.subscription_log_file = os.path.join(self.subscription_data_dir, "subscription_activity.log")

        os.makedirs(self.subscription_data_dir, exist_ok=True)

        self._load_initial_data()
        self._setup_ui()
        self.refresh_page() # Инициализация UI

    def _load_initial_data(self):
        """Загружает или инициализирует концептуальные данные о провайдерах и подписках."""
        # Загружаем провайдеров из payments_data/providers.json
        if os.path.exists(self.providers_file):
            with open(self.providers_file, 'r', encoding='utf-8') as f:
                self.providers = json.load(f)
        else:
            self.providers = [] # Если файл не найден, список провайдеров пуст
            messagebox.showwarning("Ошибка загрузки", f"Файл провайдеров '{self.providers_file}' не найден. Пожалуйста, убедитесь, что страница платежей инициализирована.")

        # Загружаем текущие подписки пользователя
        if not os.path.exists(self.subscriptions_file):
            self.subscriptions = []
            with open(self.subscriptions_file, 'w', encoding='utf-8') as f:
                json.dump(self.subscriptions, f, indent=4, ensure_ascii=False)
        else:
            with open(self.subscriptions_file, 'r', encoding='utf-8') as f:
                self.subscriptions = json.load(f)

        if not os.path.exists(self.subscription_log_file):
            with open(self.subscription_log_file, 'w', encoding='utf-8') as f:
                f.write(f"[{self._get_timestamp()}] Журнал активности подписок инициализирован.\n")

    def _save_subscriptions(self):
        """Сохраняет текущие данные о подписках."""
        with open(self.subscriptions_file, 'w', encoding='utf-8') as f:
            json.dump(self.subscriptions, f, indent=4, ensure_ascii=False)

    def _log_subscription_activity(self, service_name, action, status, details=""):
        """Логирует активность подписок."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "service": service_name,
            "action": action, # e.g., "subscribe", "unsubscribe", "update_preferences"
            "status": status,
            "details": details
        }
        try:
            with open(self.subscription_log_file, 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"Ошибка записи в журнал подписок: {e}")

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс для страницы управления подписками."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="LAG-LMVL: Управление Подписками и Сервисами", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Список доступных сервисов и их статус подписки
        services_frame = ttk.LabelFrame(main_frame, text="Доступные Сервисы и Подписки", padding="10")
        services_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        services_frame.grid_columnconfigure(0, weight=1)
        services_frame.grid_rowconfigure(0, weight=1)

        self.services_tree = ttk.Treeview(services_frame, columns=("Description", "Status", "Payment Method"), show="headings")
        self.services_tree.grid(row=0, column=0, sticky="nsew")
        self.services_tree.heading("Description", text="Описание")
        self.services_tree.heading("Status", text="Статус Подписки")
        self.services_tree.heading("Payment Method", text="Предпочитаемая Оплата")
        self.services_tree.column("Description", width=250)
        self.services_tree.column("Status", width=120, anchor="center")
        self.services_tree.column("Payment Method", width=150, anchor="center")

        services_tree_scrollbar_y = ttk.Scrollbar(services_frame, orient="vertical", command=self.services_tree.yview)
        services_tree_scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.services_tree.config(yscrollcommand=services_tree_scrollbar_y.set)
        self.services_tree.bind("<<TreeviewSelect>>", self._on_service_select)

        # Кнопки управления подписками
        action_buttons_frame = ttk.Frame(services_frame)
        action_buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.subscribe_button = ttk.Button(action_buttons_frame, text="Подписаться", command=self._subscribe_service)
        self.subscribe_button.pack(side=tk.LEFT, padx=5)

        self.unsubscribe_button = ttk.Button(action_buttons_frame, text="Отписаться", command=self._unsubscribe_service)
        self.unsubscribe_button.pack(side=tk.LEFT, padx=5)

        self.manage_payment_button = ttk.Button(action_buttons_frame, text="Настроить Оплату Подписки", command=self._manage_subscription_payment_preferences)
        self.manage_payment_button.pack(side=tk.LEFT, padx=5)

        # Журнал активности подписок
        ttk.Label(main_frame, text="Журнал Активности Подписок:", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(15, 5))
        self.subscription_log_text = tk.Text(main_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, height=10)
        self.subscription_log_text.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        ttk.Scrollbar(self.subscription_log_text, orient="vertical", command=self.subscription_log_text.yview).grid(row=3, column=1, sticky="ns")
        self.subscription_log_text.config(yscrollcommand=self.subscription_log_text.set, state="disabled")

        ttk.Button(main_frame, text="Обновить страницу", command=self.refresh_page).grid(row=4, column=0, pady=10)

        # Примечание "Пациент Зеро"
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ (Пациент Зеро): ⚠️\n"
            "Это демонстрация концепции управления подписками. Настоящие подписки и финансовые операции НЕ выполняются. "
            "LAG-LMVL не несет ответственности за любые финансовые риски. "
            "Ваши проблемы - не наши. Используйте на свой страх и риск."
        ), font=("Arial", 9, "bold"), wraplength=700, foreground="darkred")
        patient_zero_note_label.grid(row=5, column=0, pady=10, sticky="ew")

        self._populate_services_tree()
        self._on_service_select() # Инициализация состояния кнопок

    def _populate_services_tree(self):
        """Заполняет дерево сервисов и их статусов подписки."""
        for iid in self.services_tree.get_children():
            self.services_tree.delete(iid)

        for provider in self.providers:
            service_name = provider["name"]
            # Проверяем, подписан ли пользователь на этот сервис
            subscription_status = "Не подписан"
            preferred_method = "Н/Д"
            for sub in self.subscriptions:
                if sub["service_name"] == service_name:
                    subscription_status = "Подписан"
                    preferred_method = sub.get("preferred_method", "Н/Д")
                    break

            self.services_tree.insert("", "end", iid=service_name, text=service_name,
                                      values=(provider.get("description", ""), subscription_status, preferred_method))

            # Настраиваем теги для цвета статуса
            if subscription_status == "Подписан":
                self.services_tree.tag_configure(service_name, foreground="green")
            else:
                self.services_tree.tag_configure(service_name, foreground="red")


    def _on_service_select(self, event=None):
        """Обновляет состояние кнопок при выборе сервиса."""
        selected_item = self.services_tree.focus()
        if not selected_item:
            self.subscribe_button.config(state="disabled")
            self.unsubscribe_button.config(state="disabled")
            self.manage_payment_button.config(state="disabled")
            return

        service_name = selected_item
        is_subscribed = any(sub["service_name"] == service_name for sub in self.subscriptions)

        self.subscribe_button.config(state="disabled" if is_subscribed else "normal")
        self.unsubscribe_button.config(state="normal" if is_subscribed else "disabled")
        self.manage_payment_button.config(state="normal" if is_subscribed else "disabled")

    def _subscribe_service(self):
        """Концептуально подписывает пользователя на выбранный сервис."""
        selected_item = self.services_tree.focus()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите сервис для подписки.")
            return

        service_name = selected_item
        if any(sub["service_name"] == service_name for sub in self.subscriptions):
            messagebox.showinfo("Подписка", f"Вы уже подписаны на сервис '{service_name}'.")
            return

        # Имитация подписки
        self.subscriptions.append({
            "service_name": service_name,
            "status": "active",
            "subscription_date": self._get_timestamp(),
            "preferred_method": "Не установлено" # Устанавливается через "Настроить Оплату"
        })
        self._save_subscriptions()
        self._log_subscription_activity(service_name, "subscribe", "success", "Пользователь подписался на сервис.")
        messagebox.showinfo("Подписка", f"Вы успешно подписались на сервис '{service_name}' (концептуально).")
        self.refresh_page()

    def _unsubscribe_service(self):
        """Концептуально отписывает пользователя от выбранного сервиса."""
        selected_item = self.services_tree.focus()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите сервис для отписки.")
            return

        service_name = selected_item
        if not any(sub["service_name"] == service_name for sub in self.subscriptions):
            messagebox.showinfo("Отписка", f"Вы не подписаны на сервис '{service_name}'.")
            return

        if messagebox.askyesno("Подтверждение отписки", f"Вы уверены, что хотите отписаться от сервиса '{service_name}'?"):
            self.subscriptions = [sub for sub in self.subscriptions if sub["service_name"] != service_name]
            self._save_subscriptions()
            self._log_subscription_activity(service_name, "unsubscribe", "success", "Пользователь отписался от сервиса.")
            messagebox.showinfo("Отписка", f"Вы успешно отписались от сервиса '{service_name}' (концептуально).")
            self.refresh_page()

    def _manage_subscription_payment_preferences(self):
        """Открывает диалог для настройки предпочтений оплаты для выбранной подписки."""
        selected_item = self.services_tree.focus()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите сервис для настройки оплаты.")
            return

        service_name = selected_item
        current_subscription = next((sub for sub in self.subscriptions if sub["service_name"] == service_name), None)

        if not current_subscription:
            messagebox.showwarning("Ошибка", "Сервис не подписан. Пожалуйста, сначала подпишитесь.")
            return

        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(f"Настройка Оплаты для '{service_name}'")
        dialog.transient(self.parent_frame)
        dialog.grab_set()

        dialog_frame = ttk.Frame(dialog, padding="15")
        dialog_frame.pack(fill="both", expand=True)

        ttk.Label(dialog_frame, text="Предпочитаемый Метод Оплаты:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        payment_methods = ["currency", "crypto", "stocks"] # Все доступные концептуальные методы
        self.dialog_method_combobox = ttk.Combobox(dialog_frame, values=payment_methods, state="readonly")
        self.dialog_method_combobox.grid(row=0, column=1, sticky="ew", pady=5)

        # Установить текущее предпочтение, если оно есть
        if "preferred_method" in current_subscription:
            self.dialog_method_combobox.set(current_subscription["preferred_method"])
        else:
            self.dialog_method_combobox.set("currency") # Дефолтное значение

        ttk.Label(dialog_frame, text="Дополнительные Детали (Концепт):", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", pady=(15,5))
        self.dialog_details_text = tk.Text(dialog_frame, wrap="word", height=5, width=40)
        self.dialog_details_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Загрузить существующие детали
        if "payment_details" in current_subscription:
            self.dialog_details_text.insert(tk.END, current_subscription["payment_details"])

        def save_preferences():
            preferred_method = self.dialog_method_combobox.get()
            payment_details = self.dialog_details_text.get("1.0", tk.END).strip()

            if not preferred_method:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите предпочитаемый метод оплаты.")
                return

            # Обновляем подписку
            for sub in self.subscriptions:
                if sub["service_name"] == service_name:
                    sub["preferred_method"] = preferred_method
                    sub["payment_details"] = payment_details
                    break
            self._save_subscriptions()
            self._log_subscription_activity(service_name, "update_preferences", "success", f"Обновлены предпочтения оплаты на: {preferred_method}.")
            messagebox.showinfo("Успех", f"Настройки оплаты для '{service_name}' сохранены (концептуально).")
            dialog.destroy()
            self.refresh_page() # Обновить дерево

        button_frame = ttk.Frame(dialog_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Сохранить", command=save_preferences).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()

    def refresh_page(self):
        """Обновляет содержимое страницы управления подписками."""
        self._load_initial_data() # Перезагрузить данные на случай изменений
        self._populate_services_tree() # Обновить дерево сервисов
        self._on_service_select() # Обновить состояние кнопок

        self.subscription_log_text.config(state="normal")
        self.subscription_log_text.delete("1.0", tk.END)
        try:
            if os.path.exists(self.subscription_log_file):
                with open(self.subscription_log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            self.subscription_log_text.insert(tk.END, f"[{entry.get('timestamp', 'N/A')}] Сервис: {entry.get('service', 'N/A')}, Действие: {entry.get('action', 'N/A')}, Статус: {entry.get('status', 'N/A')}. Детали: {entry.get('details', '')}\n")
                        except json.JSONDecodeError:
                            self.subscription_log_text.insert(tk.END, f"Ошибка чтения строки лога: {line}\n")
            else:
                self.subscription_log_text.insert(tk.END, "Журнал активности подписок не найден.\n")
        except Exception as e:
            self.subscription_log_text.insert(tk.END, f"Ошибка при загрузке журнала подписок: {e}\n")
        finally:
            self.subscription_log_text.see(tk.END)
            self.subscription_log_text.config(state="disabled")

# Эта функция будет вызвана основным приложением для настройки вкладки Управление Подписками
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    subscription_page_instance = SubscriptionManagementPage(frame, app_data)
    return frame, subscription_page_instance.refresh_page


