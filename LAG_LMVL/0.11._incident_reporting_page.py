
# Принцип: Функциональность важнее чистоты: Если это работает, так и пусть остается.
# Нам все равно, как это работает или какую "темную магию" оно использует.
# Это хаос и безумие, и мы это любим. Чем больше хаоса, тем интереснее.
# Пользователи могут делать что хотят, мы им не вытираем попу.
# Пусть веселятся, накосячат, если они забудут свой пароль, они потеряют свою жизнь, и если они вспомнят, они восстановят
# только то, что успели синхронизировать, и пошли нахуй с вопросами.
# Принцип: мы отправляем, вышестоящая платформа невидимо подтверждает, мы получаем подтверждение, нам плевать на агрегатора; главное — результат, а не как.

# This is the rocket fuel that you and I will use to put out fires.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import datetime
import json
import random

class IncidentReportingPage:
    # Принцип Пациента Зеро: "Я не вытираю попу пользователям, забыл мастер-пароль — сдохни.
    # Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные;
    # вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль,
    # потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
    # Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.
    # Ваши проблемы — не мои.
    # Это примечание является основной философией приложения и должно быть заметно отображено или концептуально понято.

    # Концептуальный список стран, где несанкционированный доступ к данным является уголовным преступлением
    CRIMINAL_JURISDICTIONS = [
        "Германия (несанкционированный доступ, § 202a StGB)",
        "Франция (несанкционированный доступ, Code pénal, Art. 323-1)",
        "США (Computer Fraud and Abuse Act)",
        "Великобритания (Computer Misuse Act 1990)",
        "Канада (Уголовный кодекс, раздел 342.1)",
        "Швейцария (несанкционированный доступ, StGB Art. 143bis)",
        "Япония (Закон о несанкционированном доступе к компьютерам)",
        "Австралия (Cybercrime Act 2001)",
        "Китай (Статьи Уголовного кодекса КНР, касающиеся киберпреступлений)",
        "Россия (Статьи 272-274.1 УК РФ)",
        "Бразилия (Lei Carolina Dieckmann)",
        "Индия (Information Technology Act, 2000)"
    ]

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Пути для хранения концептуальных данных инцидентов
        self.incident_logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "incident_data")
        self.incident_log_file = os.path.join(self.incident_logs_dir, "incidents.json")
        self.report_output_dir = os.path.join(self.incident_logs_dir, "reports")
        self.data_access_log_file = os.path.join(self.incident_logs_dir, "data_access_history.json") # Новый файл для истории доступа

        os.makedirs(self.incident_logs_dir, exist_ok=True)
        os.makedirs(self.report_output_dir, exist_ok=True)

        self.incidents = self._load_incidents()
        self.data_access_history = self._load_data_access_history() # Загружаем историю доступа
        self._setup_ui()
        self._populate_incident_tree()
        self._populate_data_access_tree() # Заполняем дерево истории доступа

    def _load_incidents(self):
        """Загружает концептуальные журналы инцидентов."""
        if os.path.exists(self.incident_log_file):
            try:
                with open(self.incident_log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Ошибка загрузки инцидентов", "Файл инцидентов поврежден. Создаем новый.")
                return []
        return self._create_dummy_incidents() # Создаем фиктивные инциденты, если файл не существует

    def _create_dummy_incidents(self):
        """Создает несколько фиктивных записей инцидентов для демонстрации."""
        dummy_data = [
            {
                "id": "INC001",
                "timestamp": "2024-07-20 10:30:00",
                "type": "Попытка Root-доступа",
                "status": "Выявлено",
                "details": "Обнаружена подозрительная активность с попыткой получения привилегий root. IP: 192.168.1.100, Источник: Неизвестен. Проверка целостности системы показала несколько модифицированных файлов."
            },
            {
                "id": "INC002",
                "timestamp": "2024-07-21 14:00:00",
                "type": "Нарушение Контрольного Списка",
                "status": "Выявлено",
                "details": "Файл 'firewall_rules.conf' был изменен без авторизации. Контрольная сумма не совпадает. Локация: /etc/sysconfig/."
            },
            {
                "id": "INC003",
                "timestamp": "2024-07-22 09:15:00",
                "type": "Аномалия VPN-соединения",
                "status": "Выявлено",
                "details": "Обнаружено нестандартное VPN-соединение из нестандартной локации (страна: Китай). Протокол: OpenVPN. Возможно, перехват сессии."
            }
        ]
        with open(self.incident_log_file, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=4, ensure_ascii=False)
        return dummy_data

    def _save_incidents(self):
        """Сохраняет текущие журналы инцидентов."""
        with open(self.incident_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.incidents, f, indent=4, ensure_ascii=False)

    def _log_incident(self, incident_type, details, status="detected"):
        """Концептуально логирует новый инцидент."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_id = f"INC{len(self.incidents) + 1:03d}"
        log_entry = {
            "id": new_id,
            "timestamp": timestamp,
            "type": incident_type,
            "status": status,
            "details": details
        }
        self.incidents.append(log_entry)
        self._save_incidents()
        self._populate_incident_tree()
        messagebox.showinfo("Новый Инцидент", f"Зафиксирован новый инцидент: {incident_type} (ID: {new_id})")

    def _load_data_access_history(self):
        """Загружает историю доступа к данным."""
        if os.path.exists(self.data_access_log_file):
            try:
                with open(self.data_access_log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Ошибка загрузки истории доступа", "Файл истории доступа поврежден. Создаем новый.")
                return []
        return self._create_dummy_data_access_history()

    def _create_dummy_data_access_history(self):
        """Создает фиктивные записи истории доступа к данным."""
        dummy_data = [
            {
                "id": "DA001",
                "timestamp": "2024-07-20 10:45:00",
                "access_type": "Несанкционированный доступ к конфиденциальным данным",
                "accessed_item": "Переписка с гражданином Германии",
                "intruder_ip": "192.168.1.100",
                "intruder_location": "Москва, Россия (концептуально)",
                "affected_citizen_country": "Германия",
                "details": "Доступ к зашифрованному файлу чата 'chat_de.enc'. Возможно, через эксплойт ОС. Переписка, затрагивающая личные данные гражданина Германии.",
                "user_comment": "Это переписка с моим другом из Германии. Считаю, что это нарушение его прав на конфиденциальность!"
            },
            {
                "id": "DA002",
                "timestamp": "2024-07-21 15:30:00",
                "access_type": "Попытка извлечения данных из зашифрованного хранилища",
                "accessed_item": "Пароли из PasswordManager",
                "intruder_ip": "203.0.113.50",
                "intruder_location": "Пекин, Китай (концептуально)",
                "affected_citizen_country": "Канада",
                "details": "Попытка доступа к базе данных паролей. Без успешной дешифровки. Принадлежат гражданину Канады.",
                "user_comment": "Влезли в мой менеджер паролей! Это данные друга из Канады, там это уголовка!"
            }
        ]
        with open(self.data_access_log_file, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=4, ensure_ascii=False)
        return dummy_data

    def _save_data_access_history(self):
        """Сохраняет историю доступа к данным."""
        with open(self.data_access_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.data_access_history, f, indent=4, ensure_ascii=False)

    def _log_data_access(self, access_type, accessed_item, intruder_ip, intruder_location, affected_citizen_country, details, user_comment=""):
        """Концептуально логирует новый инцидент доступа к данным."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_id = f"DA{len(self.data_access_history) + 1:03d}"
        log_entry = {
            "id": new_id,
            "timestamp": timestamp,
            "access_type": access_type,
            "accessed_item": accessed_item,
            "intruder_ip": intruder_ip,
            "intruder_location": intruder_location,
            "affected_citizen_country": affected_citizen_country,
            "details": details,
            "user_comment": user_comment
        }
        self.data_access_history.append(log_entry)
        self._save_data_access_history()
        self._populate_data_access_tree()
        messagebox.showinfo("Новый Инцидент Доступа к Данным", f"Зафиксирован новый инцидент доступа: {access_type} (ID: {new_id})")


    def _setup_ui(self):
        """Настраивает элементы UI для страницы отчетов об инцидентах."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Строка для списка инцидентов

        ttk.Label(main_frame, text="LAG LMVL: Инциденты и Отчетность – Ваша Защита, Наша Фиксация", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Создаем Notebook для разных разделов отчетов
        self.incident_notebook = ttk.Notebook(main_frame)
        self.incident_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1) # Убедимся, что Notebook расширяется

        # Вкладка "Выявленные Инциденты"
        incident_tab_frame = ttk.Frame(self.incident_notebook, padding="10")
        self.incident_notebook.add(incident_tab_frame, text="Выявленные Инциденты")
        incident_tab_frame.grid_columnconfigure(0, weight=1)
        incident_tab_frame.grid_rowconfigure(0, weight=1)

        incident_list_frame = ttk.LabelFrame(incident_tab_frame, text="Список Инцидентов", padding="10")
        incident_list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        incident_list_frame.grid_rowconfigure(0, weight=1)
        incident_list_frame.grid_columnconfigure(0, weight=1)

        self.incident_tree = ttk.Treeview(incident_list_frame, columns=("Дата", "Тип", "Статус"), show="headings")
        self.incident_tree.grid(row=0, column=0, sticky="nsew")
        self.incident_tree.heading("#0", text="ID Инцидента")
        self.incident_tree.heading("Дата", text="Дата/Время")
        self.incident_tree.heading("Тип", text="Тип Инцидента")
        self.incident_tree.heading("Статус", text="Статус")
        self.incident_tree.column("#0", width=100)
        self.incident_tree.column("Дата", width=150)
        self.incident_tree.column("Тип", width=200)
        self.incident_tree.column("Статус", width=100)

        incident_tree_scrollbar = ttk.Scrollbar(incident_list_frame, orient="vertical", command=self.incident_tree.yview)
        incident_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.incident_tree.config(yscrollcommand=incident_tree_scrollbar.set)

        self.incident_tree.bind("<<TreeviewSelect>>", self._on_incident_select)

        details_actions_frame = ttk.LabelFrame(incident_tab_frame, text="Детали Инцидента и Действия", padding="10")
        details_actions_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        details_actions_frame.grid_columnconfigure(0, weight=1)
        details_actions_frame.grid_rowconfigure(0, weight=1)

        ttk.Label(details_actions_frame, text="Подробности Выбранного Инцидента:").grid(row=0, column=0, sticky="w", pady=2)
        self.incident_details_text = tk.Text(details_actions_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), height=8, state="disabled")
        self.incident_details_text.grid(row=1, column=0, sticky="nsew", pady=5)
        details_scrollbar = ttk.Scrollbar(details_actions_frame, orient="vertical", command=self.incident_details_text.yview)
        details_scrollbar.grid(row=1, column=1, sticky="ns")
        self.incident_details_text.config(yscrollcommand=details_scrollbar.set)

        action_buttons_frame = ttk.Frame(details_actions_frame)
        action_buttons_frame.grid(row=2, column=0, sticky="ew", pady=5)
        ttk.Button(action_buttons_frame, text="Посмотреть Детали (Концепт)", command=self._view_details_conceptual).pack(side=tk.LEFT, padx=2, expand=True, fill="x")
        ttk.Button(action_buttons_frame, text="Сгенерировать Отчет (Концепт)", command=self._generate_report_conceptual).pack(side=tk.LEFT, padx=2, expand=True, fill="x")

        # Вкладка "История Доступа к Данным"
        data_access_tab_frame = ttk.Frame(self.incident_notebook, padding="10")
        self.incident_notebook.add(data_access_tab_frame, text="История Доступа к Данным")
        data_access_tab_frame.grid_columnconfigure(0, weight=1)
        data_access_tab_frame.grid_rowconfigure(0, weight=1)

        data_access_list_frame = ttk.LabelFrame(data_access_tab_frame, text="Записи Доступа к Конфиденциальным Данным", padding="10")
        data_access_list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        data_access_list_frame.grid_rowconfigure(0, weight=1)
        data_access_list_frame.grid_columnconfigure(0, weight=1)

        self.data_access_tree = ttk.Treeview(data_access_list_frame, columns=("Дата", "Тип Доступа", "Объект Доступа", "Страна Гражданина", "IP Вторжения"), show="headings")
        self.data_access_tree.grid(row=0, column=0, sticky="nsew")
        self.data_access_tree.heading("#0", text="ID Записи")
        self.data_access_tree.heading("Дата", text="Дата/Время")
        self.data_access_tree.heading("Тип Доступа", text="Тип Доступа")
        self.data_access_tree.heading("Объект Доступа", text="Объект Доступа")
        self.data_access_tree.heading("Страна Гражданина", text="Страна Гражданина")
        self.data_access_tree.heading("IP Вторжения", text="IP Вторжения")
        self.data_access_tree.column("#0", width=80)
        self.data_access_tree.column("Дата", width=120)
        self.data_access_tree.column("Тип Доступа", width=180)
        self.data_access_tree.column("Объект Доступа", width=150)
        self.data_access_tree.column("Страна Гражданина", width=120)
        self.data_access_tree.column("IP Вторжения", width=100)

        data_access_tree_scrollbar = ttk.Scrollbar(data_access_list_frame, orient="vertical", command=self.data_access_tree.yview)
        data_access_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.data_access_tree.config(yscrollcommand=data_access_tree_scrollbar.set)

        self.data_access_tree.bind("<<TreeviewSelect>>", self._on_data_access_select)

        # Details for Data Access Entries
        data_access_details_frame = ttk.LabelFrame(data_access_tab_frame, text="Детали Записи Доступа и Отчетность", padding="10")
        data_access_details_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        data_access_details_frame.grid_columnconfigure(0, weight=1)
        data_access_details_frame.grid_rowconfigure(0, weight=1)

        ttk.Label(data_access_details_frame, text="Подробности Выбранной Записи Доступа:").grid(row=0, column=0, sticky="w", pady=2)
        self.data_access_details_text = tk.Text(data_access_details_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), height=8, state="disabled")
        self.data_access_details_text.grid(row=1, column=0, sticky="nsew", pady=5)
        data_access_details_scrollbar = ttk.Scrollbar(data_access_details_frame, orient="vertical", command=self.data_access_details_text.yview)
        data_access_details_scrollbar.grid(row=1, column=1, sticky="ns")
        self.data_access_details_text.config(yscrollcommand=data_access_details_scrollbar.set)

        # User comment and translation input
        comment_frame = ttk.Frame(data_access_details_frame)
        comment_frame.grid(row=2, column=0, sticky="ew", pady=5)
        comment_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(comment_frame, text="Ваш комментарий (любой язык):").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.user_comment_entry = ttk.Entry(comment_frame, width=50)
        self.user_comment_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        ttk.Button(comment_frame, text="Обновить комментарий", command=self._update_selected_data_access_comment).grid(row=1, column=0, columnspan=2, pady=5)

        # Buttons for Data Access reporting
        data_access_buttons_frame = ttk.Frame(data_access_details_frame)
        data_access_buttons_frame.grid(row=3, column=0, sticky="ew", pady=5)
        ttk.Button(data_access_buttons_frame, text="Сообщить о Нарушении Закона (Концепт)", command=self._report_legal_violation_for_data_access).pack(side=tk.LEFT, padx=2, expand=True, fill="x")

        # Вкладка "Уголовные Юрисдикции"
        criminal_jurisdictions_tab = ttk.Frame(self.incident_notebook, padding="10")
        self.incident_notebook.add(criminal_jurisdictions_tab, text="Уголовные Юрисдикции")
        criminal_jurisdictions_tab.grid_columnconfigure(0, weight=1)
        criminal_jurisdictions_tab.grid_rowconfigure(0, weight=1)

        ttk.Label(criminal_jurisdictions_tab, text="Список стран, где несанкционированный доступ к конфиденциальным данным (включая Root-доступ) преследуется уголовно:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="nw", pady=10)

        self.criminal_jurisdictions_text = tk.Text(criminal_jurisdictions_tab, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), height=15, state="disabled")
        self.criminal_jurisdictions_text.grid(row=1, column=0, sticky="nsew")
        jurisdictions_scrollbar = ttk.Scrollbar(criminal_jurisdictions_tab, orient="vertical", command=self.criminal_jurisdictions_text.yview)
        jurisdictions_scrollbar.grid(row=1, column=1, sticky="ns")
        self.criminal_jurisdictions_text.config(yscrollcommand=jurisdictions_scrollbar.set)

        self._populate_criminal_jurisdictions()


        # Patient Zero Principle Note (обновлено)
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Принцип Пациента Зеро: Я не вытираю попу пользователям, забыл мастер-пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные; "
            "вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
            "\n\n**Ваши проблемы — не мои.**"
            "\n**Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.**"
            "\n**Принцип: мы отправляем, вышестоящая платформа невидимо подтверждает, мы получаем подтверждение, нам плевать на агрегатора; главное — результат, а не как.**"
            "\n\n**LAG LMVL: Обнаружение Инцидентов: 'Влез досвидос умер'. Ваше право на ответ – наш инструмент фиксации.**"
            "\n⚠️ Каждый человек сам решает нажать клавишу 'Сообщить о Нарушении Закона' или нет. "
            "Приложение фиксирует факты и предоставляет вам инструменты для действия в рамках правового поля. "
            "Оно не совершает никаких действий, нарушающих закон. Защита конфиденциальных данных иностранных граждан - это уголовное преступление в их стране."
        ), font=("Arial", 9, "italic"), wraplength=1000, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, pady=10, sticky="ew") # Изменил ряд, чтобы был под Notebook

    def _populate_incident_tree(self):
        """Заполняет дерево инцидентов текущими концептуальными инцидентами."""
        for iid in self.incident_tree.get_children():
            self.incident_tree.delete(iid)

        for incident in self.incidents:
            self.incident_tree.insert("", "end", iid=incident["id"], text=incident["id"],
                                      values=(incident["timestamp"], incident["type"], incident["status"]))

    def _populate_data_access_tree(self):
        """Заполняет дерево истории доступа к данным."""
        for iid in self.data_access_tree.get_children():
            self.data_access_tree.delete(iid)

        for entry in self.data_access_history:
            self.data_access_tree.insert("", "end", iid=entry["id"], text=entry["id"],
                                        values=(entry["timestamp"], entry["access_type"], entry["accessed_item"],
                                                entry["affected_citizen_country"], entry["intruder_ip"]))

    def _on_incident_select(self, event):
        """Отображает детали выбранного инцидента."""
        selected_item = self.incident_tree.focus()
        if selected_item:
            incident_id = self.incident_tree.item(selected_item, "text")
            selected_incident = next((inc for inc in self.incidents if inc["id"] == incident_id), None)

            self.incident_details_text.config(state="normal")
            self.incident_details_text.delete("1.0", tk.END)
            if selected_incident:
                details = selected_incident.get("details", "Детали отсутствуют.")
                self.incident_details_text.insert(tk.END, f"ID: {selected_incident['id']}\n")
                self.incident_details_text.insert(tk.END, f"Дата/Время: {selected_incident['timestamp']}\n")
                self.incident_details_text.insert(tk.END, f"Тип: {selected_incident['type']}\n")
                self.incident_details_text.insert(tk.END, f"Статус: {selected_incident['status']}\n\n")
                self.incident_details_text.insert(tk.END, "Подробности:\n")
                self.incident_details_text.insert(tk.END, details)
            else:
                self.incident_details_text.insert(tk.END, "Выберите инцидент для просмотра деталей.")
            self.incident_details_text.config(state="disabled")

    def _on_data_access_select(self, event):
        """Отображает детали выбранной записи доступа к данным и заполняет поле комментария."""
        selected_item = self.data_access_tree.focus()
        if selected_item:
            access_id = self.data_access_tree.item(selected_item, "text")
            selected_access_entry = next((entry for entry in self.data_access_history if entry["id"] == access_id), None)

            self.data_access_details_text.config(state="normal")
            self.data_access_details_text.delete("1.0", tk.END)
            self.user_comment_entry.delete(0, tk.END) # Clear comment entry

            if selected_access_entry:
                details = selected_access_entry.get("details", "Детали отсутствуют.")
                self.data_access_details_text.insert(tk.END, f"ID Записи: {selected_access_entry['id']}\n")
                self.data_access_details_text.insert(tk.END, f"Дата/Время: {selected_access_entry['timestamp']}\n")
                self.data_access_details_text.insert(tk.END, f"Тип Доступа: {selected_access_entry['access_type']}\n")
                self.data_access_details_text.insert(tk.END, f"Объект Доступа: {selected_access_entry['accessed_item']}\n")
                self.data_access_details_text.insert(tk.END, f"IP Вторжения: {selected_access_entry['intruder_ip']}\n")
                self.data_access_details_text.insert(tk.END, f"Локация Вторжения (Концепт): {selected_access_entry['intruder_location']}\n")
                self.data_access_details_text.insert(tk.END, f"Страна Затронутого Гражданина: {selected_access_entry['affected_citizen_country']}\n\n")
                self.data_access_details_text.insert(tk.END, "Подробности:\n")
                self.data_access_details_text.insert(tk.END, details)

                # Load user comment if exists
                user_comment = selected_access_entry.get("user_comment", "")
                self.user_comment_entry.insert(0, user_comment)

            else:
                self.data_access_details_text.insert(tk.END, "Выберите запись доступа для просмотра деталей.")
            self.data_access_details_text.config(state="disabled")

    def _update_selected_data_access_comment(self):
        """Обновляет комментарий пользователя для выбранной записи доступа."""
        selected_item = self.data_access_tree.focus()
        if not selected_item:
            messagebox.showwarning("Нет выбора", "Пожалуйста, выберите запись доступа для обновления комментария.")
            return

        access_id = self.data_access_tree.item(selected_item, "text")
        new_comment = self.user_comment_entry.get().strip()

        for entry in self.data_access_history:
            if entry["id"] == access_id:
                entry["user_comment"] = new_comment
                self._save_data_access_history()
                messagebox.showinfo("Комментарий Обновлен", f"Комментарий для записи '{access_id}' обновлен.")
                self._on_data_access_select(None) # Refresh details display
                return
        messagebox.showerror("Ошибка", "Запись доступа не найдена для обновления комментария.")


    def _view_details_conceptual(self):
        """Концептуально просматривает более подробные сведения о выбранном инциденте."""
        selected_item = self.incident_tree.focus()
        if not selected_item:
            messagebox.showwarning("Нет выбора", "Пожалуйста, выберите инцидент для просмотра деталей.")
            return

        incident_id = self.incident_tree.item(selected_item, "text")
        selected_incident = next((inc for inc in self.incidents if inc["id"] == incident_id), None)

        if selected_incident:
            detailed_info = (
                f"--- Концептуальные Подробности Инцидента {incident_id} ---\n\n"
                f"Дата/Время: {selected_incident['timestamp']}\n"
                f"Тип инцидента: {selected_incident['type']}\n"
                f"Статус: {selected_incident['status']}\n\n"
                f"Описание: {selected_incident['details']}\n\n"
                f"Дополнительная концептуальная информация (например, хеши файлов, логи доступа, временные метки): "
                f"HASH_{random.randint(1000,9999)}_FILE.EXE, IP: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}, "
                f"User-Agent: 'Mozilla/5.0 (Conceptual; Win64; x64)'. "
                f"Эта информация концептуально собрана для дальнейшего анализа.\n"
                f"----------------------------------------------------\n"
            )
            messagebox.showinfo(f"Детали Инцидента: {incident_id}", detailed_info)
        else:
            messagebox.showwarning("Ошибка", "Инцидент не найден.")

    def _generate_report_conceptual(self):
        """Концептуально генерирует файл отчета для выбранного инцидента."""
        selected_item = self.incident_tree.focus()
        if not selected_item:
            messagebox.showwarning("Нет выбора", "Пожалуйста, выберите инцидент для генерации отчета.")
            return

        incident_id = self.incident_tree.item(selected_item, "text")
        selected_incident = next((inc for inc in self.incidents if inc["id"] == incident_id), None)

        if selected_incident:
            report_filename = f"LAG_LMVL_Report_{incident_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            report_filepath = os.path.join(self.report_output_dir, report_filename)

            report_content = (
                f"LAG LMVL - Концептуальный Отчет об Инциденте\n"
                f"Дата генерации: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"---------------------------------------------------\n"
                f"Инцидент ID: {selected_incident['id']}\n"
                f"Дата/Время инцидента: {selected_incident['timestamp']}\n"
                f"Тип инцидента: {selected_incident['type']}\n"
                f"Статус: {selected_incident['status']}\n\n"
                f"Подробное описание:\n{selected_incident['details']}\n\n"
                f"**ВАЖНО: Согласно принципам LAG LMVL, этот отчет содержит фактические данные, собранные приложением на вашем устройстве. "
                f"Приложение не несет ответственности за дальнейшие действия пользователя с этим отчетом.**"
                f"---------------------------------------------------\n"
            )

            try:
                with open(report_filepath, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                messagebox.showinfo("Отчет Сгенерирован", f"Концептуальный отчет для инцидента '{incident_id}' сгенерирован и сохранен как:\n{report_filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сгенерировать концептуальный отчет: {e}")
        else:
            messagebox.showwarning("Ошибка", "Инцидент не найден.")

    def _populate_criminal_jurisdictions(self):
        """Заполняет текстовое поле списком уголовных юрисдикций."""
        self.criminal_jurisdictions_text.config(state="normal")
        self.criminal_jurisdictions_text.delete("1.0", tk.END)
        self.criminal_jurisdictions_text.insert(tk.END, "Уголовные юрисдикции по несанкционированному доступу к данным:\n\n")
        for country in self.CRIMINAL_JURISDICTIONS:
            self.criminal_jurisdictions_text.insert(tk.END, f"- {country}\n")
        self.criminal_jurisdictions_text.config(state="disabled")

    # Концептуальная функция для перевода
    def _conceptual_translate(self, text, target_language="English"):
        """Концептуально 'переводит' текст на указанный язык. Для демонстрации."""
        # В реальном приложении здесь был бы вызов к API переводчика (например, Google Translate API)
        # Для концептуального примера просто добавляем префикс и показываем, что это перевод
        if text.strip() == "":
            return ""
        return f"[Translated to {target_language}]: {text}"

    def _report_legal_violation_for_data_access(self):
        """
        Концептуально сообщает о нарушении закона на основе выбранной записи доступа к данным.
        Включает комментарий пользователя (с "переводом") и концептуальный скриншот.
        """
        selected_item = self.data_access_tree.focus()
        if not selected_item:
            messagebox.showwarning("Нет выбора", "Пожалуйста, выберите запись доступа для сообщения о нарушении закона.")
            return

        access_id = self.data_access_tree.item(selected_item, "text")
        selected_access_entry = next((entry for entry in self.data_access_history if entry["id"] == access_id), None)

        if not selected_access_entry:
            messagebox.showwarning("Ошибка", "Запись доступа не найдена.")
            return

        # Получаем и концептуально переводим комментарий пользователя
        user_comment_original = self.user_comment_entry.get().strip()
        user_comment_translated = self._conceptual_translate(user_comment_original, "English")

        confirm_message = (
            f"Вы уверены, что хотите сообщить о нарушении закона, связанном с доступом к данным '{access_id}'?\n"
            "Это действие концептуально инициирует сбор данных и подготовку к отправке в соответствующие "
            "правоохранительные органы и/или международные организации (например, Интерпол), если это применимо "
            "и разрешено вашей юрисдикцией и философией.\n\n"
            "**Важно: Влез досвидос умер. Приложение фиксирует факты и предоставляет вам инструменты для действия. "
            "Дальнейшие шаги и их последствия — ваша ответственность. Мы просто инструмент. "
            "Доступ к конфиденциальным данным граждан другой страны может быть уголовным преступлением в их юрисдикции.**"
        )

        if messagebox.askyesno("Подтверждение Действия", confirm_message):
            report_filename = f"LAG_LMVL_LEGAL_DATA_ACCESS_REPORT_{access_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_filepath = os.path.join(self.report_output_dir, report_filename)

            conceptual_legal_report_data = {
                "report_id": f"LEGAL_DA_{access_id}_{random.randint(100,999)}",
                "timestamp_of_report": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "incident_type": selected_access_entry['access_type'],
                "accessed_item": selected_access_entry['accessed_item'],
                "intruder_ip": selected_access_entry['intruder_ip'],
                "intruder_location_conceptual": selected_access_entry['intruder_location'],
                "affected_citizen_country": selected_access_entry['affected_citizen_country'],
                "incident_details": selected_access_entry['details'],
                "user_comment_original": user_comment_original,
                "user_comment_translated_to_english": user_comment_translated,
                "conceptual_screenshot_of_correspondence": f"Приложение концептуально включает скриншот переписки с гражданином {selected_access_entry['affected_citizen_country']} (файл: screenshot_{access_id}.png). **Примечание: скриншот является концептуальным.**",
                "legal_context_note": (
                    "Этот отчет концептуально подготовлен для правовой оценки. LAG LMVL зафиксировал вторжение, "
                    "и пользователь инициирует процесс информирования. Приложение предоставляет ФАКТЫ, не совершая юридических действий самостоятельно. "
                    "В юрисдикции страны гражданства затронутого лица несанкционированный доступ (включая root-доступ) к конфиденциальной информации может быть уголовно наказуем."
                )
            }

            try:
                with open(report_filepath, 'w', encoding='utf-8') as f:
                    json.dump(conceptual_legal_report_data, f, indent=4, ensure_ascii=False)

                final_message = (
                    f"Концептуальный отчет о нарушении закона, связанном с доступом к данным '{access_id}', подготовлен и сохранен как:\n"
                    f"{report_filepath}\n\n"
                    f"**Отчет концептуально готов к отправке из вашего почтового клиента на указанные адреса (если такая функция будет реализована вне приложения).**\n"
                    f"**Нам плевать на агрегатора; главное — результат ваших действий.**"
                )
                messagebox.showinfo("Отчет о Нарушении Закона (Концепт)", final_message)
            except Exception as e:
                messagebox.showerror("Ошибка Отчета", f"Не удалось подготовить концептуальный отчет о нарушении закона: {e}")
        else:
            messagebox.showinfo("Действие отменено", "Сообщение о нарушении закона отменено пользователем.")


    def refresh_page(self):
        """Обновляет содержимое страницы."""
        self.incidents = self._load_incidents()
        self.data_access_history = self._load_data_access_history()
        self._populate_incident_tree()
        self._populate_data_access_tree()
        self.incident_details_text.config(state="normal")
        self.incident_details_text.delete("1.0", tk.END)
        self.incident_details_text.config(state="disabled")
        self.data_access_details_text.config(state="normal")
        self.data_access_details_text.delete("1.0", tk.END)
        self.data_access_details_text.config(state="disabled")
        self.user_comment_entry.delete(0, tk.END)

# Эта функция будет вызвана основным приложением для настройки вкладки "Отчетность об инцидентах"
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    incident_page_instance = IncidentReportingPage(frame, app_data)
    return frame, incident_page_instance.refresh_page
