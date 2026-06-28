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
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import json
import datetime
import random # Potentially used for dummy data/simulations

class SystemAndSelfManagementPage:
    # Patient Zero Principle: "I don't wipe users' asses, if you forgot your master password, die.
    # When you don't regain access, and no one else does. I don't store any data,
    # you yourselves must take care of how and where to save it and how to remember the password,
    # because the password is the key to encrypting everything on your profile. Without it, no one has access."
    # This note cannot be deleted and must remain unchanged in all document versions.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # --- Paths and Data for System Monitoring ---
        self.log_base_dir = app_data.get("LOG_BASE_DIR", "/var/log/monitoring_script") # Fallback
        self.current_run_details_log = app_data.get("CURRENT_RUN_DETAILS_LOG", os.path.join(self.log_base_dir, "current_run_details.log"))
        self.latest_intrusion_log_path_file = app_data.get("LATEST_INTRUSION_LOG_PATH_FILE", os.path.join(self.log_base_dir, "latest_intrusion_log_path.txt"))
        self.latest_checklist_report_path_file = app_data.get("LATEST_CHECKLIST_REPORT_PATH_FILE", os.path.join(self.log_base_dir, "latest_checklist_report_path.txt"))

        # --- Paths and Data for Personal Growth & Wellness ---
        self.wellness_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wellness_data")
        self.goals_file = os.path.join(self.wellness_data_dir, "user_goals.json")
        self.meditation_logs_file = os.path.join(self.wellness_data_dir, "meditation_logs.json")
        os.makedirs(self.wellness_data_dir, exist_ok=True)

        # Initialize data holders for wellness part
        self.user_goals = {}
        self.meditation_logs = []

        # --- Paths and Data for Documents & Automated Reports ---
        self.documents_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "documents_data")
        self.notes_file = os.path.join(self.documents_data_dir, "my_notes.json")
        self.dummy_pdf_path = os.path.join(self.documents_data_dir, "conceptual_document.pdf")
        self.dummy_table_path = os.path.join(self.documents_data_dir, "conceptual_table.csv")
        self.dummy_word_path = os.path.join(self.documents_data_dir, "conceptual_report.docx")
        self.zero_archive_path = os.path.join(self.documents_data_dir, "zero_archive_manifest.json") # New: ZERO Archive path

        os.makedirs(self.documents_data_dir, exist_ok=True)
        self._create_dummy_document_files() # Create dummy files for documents and ZERO Archive


        # Initialize data holders for notes
        self.notes = {}
        self.current_note_name = ""


        self._load_initial_data() # Load data for wellness and documents part
        self._setup_ui()

    def _create_dummy_document_files(self):
        """Создает фиктивные файлы для демонстрации, если они не существуют."""
        if not os.path.exists(self.dummy_pdf_path):
            with open(self.dummy_pdf_path, 'w', encoding='utf-8') as f:
                f.write("Это концептуальный PDF-документ.\n\n"
                        "В реальном приложении здесь будет отображаться содержимое PDF-файла.")
        if not os.path.exists(self.dummy_table_path):
            with open(self.dummy_table_path, 'w', encoding='utf-8') as f:
                f.write("Header1,Header2,Header3\n")
                f.write("Row1Col1,Row1Col2,Row1Col3\n")
                f.write("Row2Col1,Row2Col2,Row2Col3\n")
                f.write("Row3Col1,Row3Col2,Row3Col3\n")
        if not os.path.exists(self.dummy_word_path):
            with open(self.dummy_word_path, 'w', encoding='utf-8') as f:
                f.write("Это концептуальный Word-документ.\n\n"
                        "В реальном приложении здесь будет отображаться содержимое DOCX-файла.\n"
                        "Может включать текст, изображения и форматирование.")
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump({"default_note": "Это ваша первая заметка. Вы можете редактировать ее и сохранять."}, f, indent=4, ensure_ascii=False)
        # Create a dummy ZERO Archive manifest
        if not os.path.exists(self.zero_archive_path):
            dummy_manifest = {
                "archive_id": "ZEROARCHIVE_" + "".join(random.choices("0123456789abcdef", k=12)),
                "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": "Концептуальный манифест синхронизации облачных ресурсов.",
                "cloud_services_metadata": [
                    {"service_name": "Google Drive", "last_sync": "2023-01-15", "checksum_algo": "SHA256", "data_point_count": 120, "sync_status": "OK"},
                    {"service_name": "Dropbox", "last_sync": "2023-01-10", "checksum_algo": "MD5", "data_point_count": 80, "sync_status": "Issues"},
                    {"service_name": "OneDrive", "last_sync": "2023-01-20", "checksum_algo": "SHA256", "data_point_count": 200, "sync_status": "OK"}
                ],
                "local_data_references": [
                    {"type": "notes", "path_segment": "documents_data/my_notes.json", "checksum": "abc123def456"},
                    {"type": "goals", "path_segment": "wellness_data/user_goals.json", "checksum": "ghi789jkl012"}
                ],
                "recovery_instructions_conceptual": "Если этот манифест найден, используйте ваш мастер-пароль для концептуальной 'расшифровки' и 'поиска' по децентрализованным сетям для восстановления полной структуры данных."
            }
            with open(self.zero_archive_path, 'w', encoding='utf-8') as f:
                json.dump(dummy_manifest, f, indent=4, ensure_ascii=False)


    def _load_initial_data(self):
        """Загружает или инициализирует концептуальные данные для целей, сессий медитации и заметок."""
        # Load Goals
        if not os.path.exists(self.goals_file):
            self.user_goals = {
                "Научиться Python": {"status": "В процессе", "progress": 50, "last_update": datetime.datetime.now().strftime("%Y-%m-%d")},
                "Заниматься спортом 3 раза в неделю": {"status": "Активно", "progress": 80, "last_update": datetime.datetime.now().strftime("%Y-%m-%d")}
            }
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_goals, f, indent=4, ensure_ascii=False)
        else:
            try:
                with open(self.goals_file, 'r', encoding='utf-8') as f:
                    self.user_goals = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка загрузки", "Файл целей поврежден. Загружены цели по умолчанию.")
                self.user_goals = {} # Reset to empty or default if corrupted

        # Load Meditation Logs
        if not os.path.exists(self.meditation_logs_file):
            self.meditation_logs = []
            with open(self.meditation_logs_file, 'w', encoding='utf-8') as f:
                json.dump(self.meditation_logs, f, indent=4, ensure_ascii=False)
        else:
            try:
                with open(self.meditation_logs_file, 'r', encoding='utf-8') as f:
                    self.meditation_logs = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка загрузки", "Файл журнала медитаций поврежден. Загружен пустой журнал.")
                self.meditation_logs = [] # Reset to empty if corrupted

        # Load Notes
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка загрузки", "Файл заметок поврежден. Загружена пустая заметка.")
                self.notes = {"default_note": "Ошибка: файл заметок поврежден. Эта заметка по умолчанию."}
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить заметки: {e}")
                self.notes = {"default_note": "Ошибка загрузки заметок. Эта заметка по умолчанию."}
        else:
            self.notes = {"default_note": "Начните писать свою заметку здесь."}
        self.current_note_name = list(self.notes.keys())[0] if self.notes else "default_note" # Set first note as current


    def _save_wellness_data(self):
        """Сохраняет текущие концептуальные данные для здоровья и обучения в файлы."""
        try:
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_goals, f, indent=4, ensure_ascii=False)
            with open(self.meditation_logs_file, 'w', encoding='utf-8') as f:
                json.dump(self.meditation_logs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные для здоровья и обучения: {e}")

    def _save_notes(self):
        """Сохраняет заметки в файл."""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Сохранение", "Заметки успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить заметки: {e}")

    def _setup_ui(self):
        """Настраивает элементы пользовательского интерфейса для объединенной страницы."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="Управление Системой и Личным Развитием", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        self.combined_notebook = ttk.Notebook(main_frame)
        self.combined_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Tab 1: System Monitoring & Reports ---
        self.system_monitoring_frame = ttk.Frame(self.combined_notebook, padding="10")
        self.combined_notebook.add(self.system_monitoring_frame, text="Мониторинг Системы и Отчеты")
        self._setup_system_monitoring_tab(self.system_monitoring_frame)

        # --- Tab 2: Personal Growth & Wellness ---
        self.personal_growth_frame = ttk.Frame(self.combined_notebook, padding="10")
        self.combined_notebook.add(self.personal_growth_frame, text="Личное Развитие и Благополучие")
        self._setup_personal_growth_tab(self.personal_growth_frame)

        # --- Tab 3: Documents & Automated Reports ---
        self.documents_reports_frame = ttk.Frame(self.combined_notebook, padding="10")
        self.combined_notebook.add(self.documents_reports_frame, text="Расширенное Управление Документами и Отчеты")
        self._setup_documents_reports_tab(self.documents_reports_frame)


        # Patient Zero Principle Note (Main application level)
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные, "
            "только вы сами должны позаботиться, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без этого нет доступа никому."
            "\n\n**Эту пометку нельзя удалять, и она должна оставаться неизменной во всех версиях документа.**"
        ), font=("Arial", 9, "italic"), wraplength=700, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, pady=10, sticky="ew")

        # Initial populate for personal growth part
        self._populate_goals_tree()
        self._populate_notes_listbox() # Initial population for notes


    # --- System Monitoring Tab Methods (Adapted from old IncidentsPage / learning_page.py) ---
    def _setup_system_monitoring_tab(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)

        reports_notebook = ttk.Notebook(parent_frame)
        reports_notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Intrusion Log Tab
        intrusion_frame = ttk.Frame(reports_notebook)
        reports_notebook.add(intrusion_frame, text="Журнал Вторжений/Аномалий")
        self.intrusion_text = tk.Text(intrusion_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1)
        self.intrusion_text.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.intrusion_text, orient="vertical", command=self.intrusion_text.yview).pack(side="right", fill="y")
        self.intrusion_text.config(yscrollcommand=self.intrusion_text.set)

        # Checklist Report Tab
        checklist_frame = ttk.Frame(reports_notebook)
        reports_notebook.add(checklist_frame, text="Отчет по Чек-листу")
        self.checklist_text = tk.Text(checklist_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1)
        self.checklist_text.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.checklist_text, orient="vertical", command=self.checklist_text.yview).pack(side="right", fill="y")
        self.checklist_text.config(yscrollcommand=self.checklist_text.set)

        # Controls for refresh and info
        controls_frame = ttk.Frame(parent_frame)
        controls_frame.grid(row=1, column=0, pady=10)
        ttk.Button(controls_frame, text="Обновить Отчеты", command=self._refresh_system_reports).pack(side=tk.LEFT, padx=10)
        ttk.Button(controls_frame, text="Показать Детали Последнего Запуска", command=self._show_current_run_details).pack(side=tk.LEFT, padx=10)

        self._refresh_system_reports() # Load on startup

    def _show_current_run_details(self):
        """Отображает содержимое журнала деталей текущего запуска."""
        if os.path.exists(self.current_run_details_log):
            try:
                with open(self.current_run_details_log, 'r', encoding='utf-8') as f:
                    content = f.read()
                messagebox.showinfo("Детали Текущего Запуска Скрипта", content)
            except Exception as e:
                messagebox.showerror("Ошибка чтения лога", f"Не удалось прочитать детали текущего запуска: {e}")
        else:
            messagebox.showinfo("Детали Текущего Запуска Скрипта", "Файл деталей текущего запуска не найден.")

    def _refresh_system_reports(self):
        """Обновляет отображение журналов вторжений и отчетов по чек-листам."""
        def load_report_content(file_path_file_var, text_widget):
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            file_path_file = file_path_file_var # This is the full path already
            if os.path.exists(file_path_file):
                try:
                    with open(file_path_file, 'r', encoding='utf-8') as f_path:
                        latest_report_path = f_path.read().strip()
                        if os.path.exists(latest_report_path):
                            with open(latest_report_path, 'r', encoding='utf-8') as f_report:
                                text_widget.insert(tk.END, f_report.read())
                        else:
                            text_widget.insert(tk.END, f"Файл отчета не найден: {latest_report_path}")
                except Exception as e:
                    text_widget.insert(tk.END, f"Ошибка загрузки отчета: {e}")
            else:
                text_widget.insert(tk.END, "Путь к последнему отчету не найден.")
            text_widget.config(state="disabled")

        load_report_content(self.latest_intrusion_log_path_file, self.intrusion_text)
        load_report_content(self.latest_checklist_report_path_file, self.checklist_text)


    # --- Personal Growth & Wellness Tab Methods (Adapted from learning_wellness_page.py) ---
    def _setup_personal_growth_tab(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)

        personal_notebook = ttk.Notebook(parent_frame)
        personal_notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Learning Resources Tab
        self.learning_frame = ttk.Frame(personal_notebook, padding="10")
        personal_notebook.add(self.learning_frame, text="Ресурсы для Обучения")
        self._setup_learning_resources_subtab(self.learning_frame)

        # Goal Tracker Tab
        self.goals_frame = ttk.Frame(personal_notebook, padding="10")
        personal_notebook.add(self.goals_frame, text="Отслеживание Целей")
        self._setup_goals_subtab(self.goals_frame)

        # Mindfulness Tools Tab
        self.mindfulness_frame = ttk.Frame(personal_notebook, padding="10")
        personal_notebook.add(self.mindfulness_frame, text="Инструменты для Осознанности")
        self._setup_mindfulness_subtab(self.mindfulness_frame)

    def _setup_learning_resources_subtab(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Кураторские Обучающие Ресурсы", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.learning_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10))
        self.learning_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.learning_text.config(state="normal")
        self.learning_text.insert(tk.END,
            "Добро пожаловать в хаб обучения! Здесь вы можете найти концептуальные ресурсы для развития.\n\n"
            "• Статья: 'Основы Кибербезопасности для Домашних Пользователей'\n"
            "• Видеокурс: 'Введение в Python для Начинающих'\n"
            "• Книга: 'Искусство Мышления вне Коробки'\n\n"
            "Используйте это пространство для самообразования и открытия новых знаний. "
            "В реальном приложении здесь были бы ссылки на внешние ресурсы или интегрированные обучающие модули."
        )
        self.learning_text.config(state="disabled")

        ttk.Button(parent_frame, text="Найти Больше Ресурсов (Концепт)", command=self._find_more_resources).grid(row=2, column=0, pady=5)

    def _find_more_resources(self):
        messagebox.showinfo("Поиск Ресурсов (Концепт)",
                            "В реальном приложении здесь будет реализован поиск и рекомендации "
                            "обучающих материалов на основе ваших интересов или прогресса.")

    def _setup_goals_subtab(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Мои Цели и Прогресс", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Left: Goals list
        goals_list_frame = ttk.LabelFrame(parent_frame, text="Список Целей", padding="10")
        goals_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        goals_list_frame.grid_rowconfigure(0, weight=1)
        goals_list_frame.grid_columnconfigure(0, weight=1)

        self.goals_tree = ttk.Treeview(goals_list_frame, columns=("Status", "Progress", "Last Update"), show="headings")
        self.goals_tree.grid(row=0, column=0, sticky="nsew")
        self.goals_tree.heading("Status", text="Статус")
        self.goals_tree.heading("Progress", text="Прогресс (%)")
        self.goals_tree.heading("Last Update", text="Последнее Обновление")
        self.goals_tree.column("Status", width=100)
        self.goals_tree.column("Progress", width=80)
        self.goals_tree.column("Last Update", width=120)

        goals_tree_scrollbar = ttk.Scrollbar(goals_list_frame, orient="vertical", command=self.goals_tree.yview)
        goals_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.goals_tree.config(yscrollcommand=goals_tree_scrollbar.set)

        self.goals_tree.bind("<<TreeviewSelect>>", self._on_goal_select)

        # Right: Goal details and management
        goal_management_frame = ttk.LabelFrame(parent_frame, text="Управление Целью", padding="10")
        goal_management_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        goal_management_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(goal_management_frame, text="Название Цели:").grid(row=0, column=0, sticky="w", pady=2)
        self.goal_name_entry = ttk.Entry(goal_management_frame, width=30)
        self.goal_name_entry.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(goal_management_frame, text="Статус:").grid(row=1, column=0, sticky="w", pady=2)
        self.goal_status_combobox = ttk.Combobox(goal_management_frame, values=["Активно", "В процессе", "Завершено", "Отложено"], state="readonly")
        self.goal_status_combobox.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(goal_management_frame, text="Прогресс (%):").grid(row=2, column=0, sticky="w", pady=2)
        self.goal_progress_scale = ttk.Scale(goal_management_frame, from_=0, to=100, orient="horizontal")
        self.goal_progress_scale.grid(row=2, column=1, sticky="ew", pady=2)
        self.goal_progress_value_label = ttk.Label(goal_management_frame, text="0%")
        self.goal_progress_value_label.grid(row=2, column=2, sticky="w", padx=5)
        self.goal_progress_scale.config(command=lambda val: self.goal_progress_value_label.config(text=f"{int(float(val))}%"))


        ttk.Button(goal_management_frame, text="Добавить Цель", command=self._add_goal).grid(row=3, column=0, columnspan=3, pady=5, sticky="ew")
        ttk.Button(goal_management_frame, text="Обновить Цель", command=self._update_goal).grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")
        ttk.Button(goal_management_frame, text="Удалить Цель", command=self._delete_goal).grid(row=5, column=0, columnspan=3, pady=5, sticky="ew")

    def _populate_goals_tree(self):
        """Заполняет дерево целей текущими данными."""
        for iid in self.goals_tree.get_children():
            self.goals_tree.delete(iid)
        for goal_name, data in self.user_goals.items():
            self.goals_tree.insert("", "end", iid=goal_name, text=goal_name, values=(data["status"], data["progress"], data["last_update"]))

    def _on_goal_select(self, event):
        """Загружает данные выбранной цели в поля ввода."""
        selected_item = self.goals_tree.focus()
        if selected_item:
            goal_name = selected_item
            data = self.user_goals[goal_name]
            self.goal_name_entry.delete(0, tk.END)
            self.goal_name_entry.insert(0, goal_name)
            self.goal_status_combobox.set(data["status"])
            self.goal_progress_scale.set(data["progress"])
            self.goal_progress_value_label.config(text=f"{data['progress']}%")

    def _add_goal(self):
        goal_name = self.goal_name_entry.get().strip()
        status = self.goal_status_combobox.get()
        progress = int(self.goal_progress_scale.get())
        if not goal_name or not status:
            messagebox.showwarning("Ошибка ввода", "Название цели и статус не могут быть пустыми.")
            return
        if goal_name in self.user_goals:
            messagebox.showwarning("Предупреждение", "Цель с таким именем уже существует. Используйте 'Обновить Цель'.")
            return

        self.user_goals[goal_name] = {
            "status": status,
            "progress": progress,
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self._save_wellness_data()
        self._populate_goals_tree()
        messagebox.showinfo("Успех", f"Цель '{goal_name}' добавлена.")

    def _update_goal(self):
        goal_name = self.goal_name_entry.get().strip()
        status = self.goal_status_combobox.get()
        progress = int(self.goal_progress_scale.get())
        if not goal_name or not status:
            messagebox.showwarning("Ошибка ввода", "Название цели и статус не могут быть пустыми.")
            return
        if goal_name not in self.user_goals:
            messagebox.showwarning("Не найдено", "Цель не найдена. Используйте 'Добавить Цель'.")
            return

        self.user_goals[goal_name]["status"] = status
        self.user_goals[goal_name]["progress"] = progress
        self.user_goals[goal_name]["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d")
        self._save_wellness_data()
        self._populate_goals_tree()
        messagebox.showinfo("Успех", f"Цель '{goal_name}' обновлена.")

    def _delete_goal(self):
        goal_name = self.goal_name_entry.get().strip()
        if not goal_name:
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, выберите цель для удаления.")
            return
        if goal_name not in self.user_goals:
            messagebox.showwarning("Не найдено", "Цель не найдена.")
            return
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить цель '{goal_name}'?"):
            del self.user_goals[goal_name]
            self._save_wellness_data()
            self._populate_goals_tree()
            messagebox.showinfo("Успех", f"Цель '{goal_name}' удалена.")
            self.goal_name_entry.delete(0, tk.END)
            self.goal_status_combobox.set('')
            self.goal_progress_scale.set(0)
            self.goal_progress_value_label.config(text="0%")


    def _setup_mindfulness_subtab(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Инструменты для Расслабления и Медитации", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.mindfulness_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10))
        self.mindfulness_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.mindfulness_text.config(state="normal")
        self.mindfulness_text.insert(tk.END,
            "Добро пожаловать в раздел осознанности. Здесь вы можете найти инструменты для расслабления.\n\n"
            "• **Концептуальная Управляемая Медитация:** Нажмите кнопку, чтобы начать сессию.\n"
            "• **Дыхательные Упражнения:** Следуйте инструкциям для расслабления.\n"
            "• **Звуки Природы:** Имитация успокаивающих звуков.\n\n"
            "Регулярная практика осознанности помогает снизить стресс и улучшить концентрацию."
        )
        self.mindfulness_text.config(state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Начать Медитацию (Концепт)", command=self._start_meditation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Журнал Медитаций", command=self._show_meditation_log).pack(side=tk.LEFT, padx=5)

    def _start_meditation(self):
        duration_str = simpledialog.askstring("Начать Медитацию", "Введите продолжительность медитации в минутах (концептуально):")
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
            self.meditation_logs.append({
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration_minutes": duration,
                "note": "Концептуальная медитация завершена."
            })
            self._save_wellness_data()
            messagebox.showinfo("Медитация (Концепт)", f"Вы начали {duration}-минутную концептуальную медитацию. Наслаждайтесь моментом. ✨")
        except (ValueError, TypeError):
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, введите корректное число для продолжительности.")

    def _show_meditation_log(self):
        log_content = "--- Журнал Концептуальных Медитаций ---\n\n"
        if not self.meditation_logs:
            log_content += "Журнал пуст. Начните медитацию, чтобы добавить записи."
        else:
            for entry in self.meditation_logs:
                log_content += f"Дата: {entry['date']}, Продолжительность: {entry['duration_minutes']} мин, Примечание: {entry['note']}\n"

        messagebox.showinfo("Журнал Медитаций", log_content)


    # --- Documents & Automated Reports Tab Methods ---
    def _setup_documents_reports_tab(self, parent_frame):
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)

        documents_reports_notebook = ttk.Notebook(parent_frame)
        documents_reports_notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Notes Tab
        self.notes_tab_frame = ttk.Frame(documents_reports_notebook, padding="10")
        documents_reports_notebook.add(self.notes_tab_frame, text="Заметки (Текст)")
        self._setup_notes_subtab(self.notes_tab_frame)

        # PDF Viewer Tab
        self.pdf_viewer_frame = ttk.Frame(documents_reports_notebook, padding="10")
        documents_reports_notebook.add(self.pdf_viewer_frame, text="Просмотр PDF (Концепт)")
        self._setup_pdf_viewer_subtab(self.pdf_viewer_frame)

        # Table Viewer Tab
        self.table_viewer_frame = ttk.Frame(documents_reports_notebook, padding="10")
        documents_reports_notebook.add(self.table_viewer_frame, text="Просмотр Таблиц (Концепт)")
        self._setup_table_viewer_subtab(self.table_viewer_frame)

        # Word Analog Tab
        self.word_analog_frame = ttk.Frame(documents_reports_notebook, padding="10")
        documents_reports_notebook.add(self.word_analog_frame, text="Аналог Word (Концепт)")
        self._setup_word_analog_subtab(self.word_analog_frame)

        # Automated Reports with Charts Tab
        self.automated_reports_frame = ttk.Frame(documents_reports_notebook, padding="10")
        documents_reports_notebook.add(self.automated_reports_frame, text="Автоматизированные Отчеты с Графиками (Концепт)")
        self._setup_automated_reports_subtab(self.automated_reports_frame)

        # NEW: ZERO Archive Management Tab
        self.zero_archive_frame = ttk.Frame(documents_reports_notebook, padding="10")
        documents_reports_notebook.add(self.zero_archive_frame, text="Управление Архивом ЗЕРО")
        self._setup_zero_archive_subtab(self.zero_archive_frame)


    def _setup_notes_subtab(self, parent_frame):
        """Настраивает UI для подвкладки Заметки."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=3)
        parent_frame.grid_rowconfigure(1, weight=1)

        # Left: Note list and controls
        notes_controls_frame = ttk.Frame(parent_frame, padding="5")
        notes_controls_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        notes_controls_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(notes_controls_frame, text="Мои Заметки", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, sticky="w")

        self.notes_listbox = tk.Listbox(notes_controls_frame, height=15, font=("Arial", 10))
        self.notes_listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.notes_listbox.bind("<<ListboxSelect>>", self._on_note_select)

        notes_listbox_scrollbar = ttk.Scrollbar(notes_controls_frame, orient="vertical", command=self.notes_listbox.yview)
        notes_listbox_scrollbar.grid(row=1, column=1, sticky="ns")
        self.notes_listbox.config(yscrollcommand=notes_listbox_scrollbar.set)

        button_frame = ttk.Frame(notes_controls_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Новая Заметка", command=self._new_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Удалить Заметку", command=self._delete_note).pack(side=tk.LEFT, padx=2)

        # Right: Note content editor
        note_editor_frame = ttk.Frame(parent_frame, padding="5")
        note_editor_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        note_editor_frame.grid_rowconfigure(1, weight=1)
        note_editor_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(note_editor_frame, text="Название Заметки:").grid(row=0, column=0, sticky="w", pady=2)
        self.note_name_entry = ttk.Entry(note_editor_frame, font=("Arial", 12))
        self.note_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        self.note_text_editor = tk.Text(note_editor_frame, wrap="word", font=("Arial", 10))
        self.note_text_editor.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        note_editor_scrollbar = ttk.Scrollbar(note_editor_frame, orient="vertical", command=self.note_text_editor.yview)
        note_editor_scrollbar.grid(row=1, column=2, sticky="ns")
        self.note_text_editor.config(yscrollcommand=note_editor_scrollbar.set)

        ttk.Button(note_editor_frame, text="Сохранить Текущую Заметку", command=self._save_current_note).grid(row=2, column=0, columnspan=3, pady=5)

    def _populate_notes_listbox(self):
        """Заполняет список заметок."""
        self.notes_listbox.delete(0, tk.END)
        for name in self.notes.keys():
            self.notes_listbox.insert(tk.END, name)

        if self.current_note_name in self.notes:
            try: # Use try-except for robustness if note not found in listbox
                index = list(self.notes.keys()).index(self.current_note_name)
                self.notes_listbox.selection_set(index)
                self.notes_listbox.see(index)
            except ValueError:
                pass # Note not found in listbox (e.g., if it was just deleted)

    def _display_current_note(self):
        """Отображает содержимое текущей выбранной заметки."""
        self.note_name_entry.delete(0, tk.END)
        self.note_text_editor.delete("1.0", tk.END)
        if self.current_note_name in self.notes:
            self.note_name_entry.insert(0, self.current_note_name)
            self.note_text_editor.insert(tk.END, self.notes[self.current_note_name])
        else:
            self.note_name_entry.insert(0, "Новая заметка")
            self.note_text_editor.insert(tk.END, "")


    def _on_note_select(self, event):
        """Обрабатывает выбор заметки из списка."""
        selected_indices = self.notes_listbox.curselection()
        if selected_indices:
            new_note_name = self.notes_listbox.get(selected_indices[0])
            if new_note_name != self.current_note_name:
                self._save_current_note(silent=True) # Silently save changes to previous note
                self.current_note_name = new_note_name
                self._display_current_note()

    def _new_note(self):
        """Создает новую пустую заметку."""
        self._save_current_note(silent=True) # Save current note before creating new
        new_name = simpledialog.askstring("Новая Заметка", "Введите название для новой заметки:")
        if new_name and new_name.strip() != "":
            if new_name in self.notes:
                messagebox.showwarning("Предупреждение", "Заметка с таким именем уже существует.")
                return
            self.notes[new_name] = ""
            self.current_note_name = new_name
            self._save_notes() # Save immediately to update file
            self._populate_notes_listbox()
            self._display_current_note()
        else:
            messagebox.showwarning("Ошибка ввода", "Название заметки не может быть пустым.")

    def _delete_note(self):
        """Удаляет выбранную заметку."""
        selected_indices = self.notes_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите заметку для удаления.")
            return

        note_to_delete = self.notes_listbox.get(selected_indices[0])
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить заметку '{note_to_delete}'?"):
            del self.notes[note_to_delete]
            if note_to_delete == self.current_note_name:
                self.current_note_name = list(self.notes.keys())[0] if self.notes else "default_note"
                if not self.notes: # If no notes left, add a default one
                    self.notes["default_note"] = "Начните писать свою заметку здесь."
                    self.current_note_name = "default_note"

            self._save_notes()
            self._populate_notes_listbox()
            self._display_current_note()


    def _save_current_note(self, silent=False):
        """Сохраняет содержимое текущей заметки."""
        current_name_in_entry = self.note_name_entry.get().strip()
        current_content_in_editor = self.note_text_editor.get("1.0", tk.END).strip()

        if self.current_note_name not in self.notes: # Should not happen if logic is correct
            self.notes[self.current_note_name] = current_content_in_editor
            if not silent: messagebox.showinfo("Сохранение", "Новая заметка сохранена.")
        else:
            if current_name_in_entry != self.current_note_name:
                # If name was changed, create new entry and delete old
                if current_name_in_entry in self.notes and current_name_in_entry != self.current_note_name:
                    if not silent: messagebox.showwarning("Ошибка сохранения", "Новое название заметки уже существует.")
                    return
                self.notes[current_name_in_entry] = current_content_in_editor
                del self.notes[self.current_note_name]
                self.current_note_name = current_name_in_entry
                self._populate_notes_listbox() # Refresh list to reflect name change
                if not silent: messagebox.showinfo("Сохранение", f"Заметка переименована и сохранена как '{self.current_note_name}'.")
            else:
                self.notes[self.current_note_name] = current_content_in_editor
                if not silent: messagebox.showinfo("Сохранение", "Текущая заметка сохранена.")

        self._save_notes() # Always save to disk
        self._populate_notes_listbox() # Ensure listbox is up-to-date


    def _setup_pdf_viewer_subtab(self, parent_frame):
        """Настраивает UI для подвкладки Просмотр PDF."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальный Просмотр PDF", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.pdf_display_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), height=20)
        self.pdf_display_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.pdf_display_text.config(state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Загрузить PDF (Концепт)", command=self._load_pdf_concept).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Открыть PDF в Программе по Умолчанию (Концепт)", command=self._open_pdf_external_concept).pack(side=tk.LEFT, padx=5)

        self._load_pdf_concept(initial_load=True) # Load dummy content on startup


    def _load_pdf_concept(self, initial_load=False):
        """Концептуальная загрузка PDF-файла."""
        file_path = self.dummy_pdf_path
        if not initial_load:
            file_path = filedialog.askopenfilename(
                title="Выберите PDF-файл (Концепт)",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if not file_path:
                return

        self.pdf_display_text.config(state="normal")
        self.pdf_display_text.delete("1.0", tk.END)
        if os.path.exists(file_path):
            try:
                # In a real app, you'd use a PDF rendering library here (e.g., PyMuPDF)
                with open(file_path, 'r', encoding='utf-8') as f: # Reading as text for conceptual demo
                    content = f.read()
                    self.pdf_display_text.insert(tk.END, f"--- Содержимое концептуального PDF-файла: {os.path.basename(file_path)} ---\n\n")
                    self.pdf_display_text.insert(tk.END, content)
                messagebox.showinfo("Загрузка PDF", f"Концептуальный PDF '{os.path.basename(file_path)}' загружен.")
            except Exception as e:
                self.pdf_display_text.insert(tk.END, f"Ошибка загрузки концептуального PDF: {e}")
                messagebox.showerror("Ошибка", f"Не удалось загрузить концептуальный PDF: {e}")
        else:
            self.pdf_display_text.insert(tk.END, "Файл PDF не найден для отображения концептуального содержимого.")
            if not initial_load:
                messagebox.showwarning("Файл не найден", "Выбранный PDF-файл не найден.")
        self.pdf_display_text.config(state="disabled")

    def _open_pdf_external_concept(self):
        """Концептуальное открытие PDF во внешней программе."""
        file_path = self.dummy_pdf_path # Use dummy for concept
        messagebox.showinfo("Открыть PDF (Концепт)",
                            f"В реальном приложении файл '{os.path.basename(file_path)}' "
                            "был бы открыт в программе для просмотра PDF по умолчанию на вашей системе.")

    def _setup_table_viewer_subtab(self, parent_frame):
        """Настраивает UI для подвкладки Просмотр Таблиц."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальный Просмотр Таблиц", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.table_display_text = tk.Text(parent_frame, wrap="none", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Courier New", 10), height=20)
        self.table_display_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        table_xscrollbar = ttk.Scrollbar(parent_frame, orient="horizontal", command=self.table_display_text.xview)
        table_xscrollbar.grid(row=2, column=0, sticky="ew")
        self.table_display_text.config(xscrollcommand=table_xscrollbar.set)

        table_yscrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.table_display_text.yview)
        table_yscrollbar.grid(row=1, column=1, sticky="ns")
        self.table_display_text.config(yscrollcommand=table_yscrollbar.set, state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=3, column=0, pady=5)
        ttk.Button(button_frame, text="Загрузить Таблицу (Концепт)", command=self._load_table_concept).pack(side=tk.LEFT, padx=5)

        self._load_table_concept(initial_load=True) # Load dummy content on startup


    def _load_table_concept(self, initial_load=False):
        """Концептуальная загрузка табличного файла (например, CSV)."""
        file_path = self.dummy_table_path
        if not initial_load:
            file_path = filedialog.askopenfilename(
                title="Выберите Табличный файл (Концепт)",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return

        self.table_display_text.config(state="normal")
        self.table_display_text.delete("1.0", tk.END)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.table_display_text.insert(tk.END, f"--- Содержимое концептуальной таблицы: {os.path.basename(file_path)} ---\n\n")
                    self.table_display_text.insert(tk.END, content)
                messagebox.showinfo("Загрузка Таблицы", f"Концептуальная таблица '{os.path.basename(file_path)}' загружена.")
            except Exception as e:
                self.table_display_text.insert(tk.END, f"Ошибка загрузки концептуальной таблицы: {e}")
                messagebox.showerror("Ошибка", f"Не удалось загрузить концептуальную таблицу: {e}")
        else:
            self.table_display_text.insert(tk.END, "Файл таблицы не найден для отображения концептуального содержимого.")
            if not initial_load:
                messagebox.showwarning("Файл не найден", "Выбранный табличный файл не найден.")
        self.table_display_text.config(state="disabled")

    def _setup_word_analog_subtab(self, parent_frame):
        """Настраивает UI для подвкладки Аналог Word."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальный Аналог Word-Документа", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.word_analog_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 11), height=20)
        self.word_analog_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        word_analog_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.word_analog_text.yview)
        word_analog_scrollbar.grid(row=1, column=1, sticky="ns")
        self.word_analog_text.config(yscrollcommand=word_analog_scrollbar.set, state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Загрузить Документ (Концепт)", command=self._load_word_analog_concept).pack(side=tk.LEFT, padx=5)

        self._load_word_analog_concept(initial_load=True) # Load dummy content on startup


    def _load_word_analog_concept(self, initial_load=False):
        """Концептуальная загрузка Word-аналога (например, DOCX)."""
        file_path = self.dummy_word_path
        if not initial_load:
            file_path = filedialog.askopenfilename(
                title="Выберите Документ (Концепт)",
                filetypes=[("Word documents", "*.docx"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return

        self.word_analog_text.config(state="normal")
        self.word_analog_text.delete("1.0", tk.END)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f: # Reading as text for conceptual demo
                    content = f.read()
                    self.word_analog_text.insert(tk.END, f"--- Содержимое концептуального Word-документа: {os.path.basename(file_path)} ---\n\n")
                    self.word_analog_text.insert(tk.END, content)
                messagebox.showinfo("Загрузка Документа", f"Концептуальный документ '{os.path.basename(file_path)}' загружен.")
            except Exception as e:
                self.word_analog_text.insert(tk.END, f"Ошибка загрузки концептуального документа: {e}")
                messagebox.showerror("Ошибка", f"Не удалось загрузить концептуальный документ: {e}")
        else:
            self.word_analog_text.insert(tk.END, "Файл документа не найден для отображения концептуального содержимого.")
            if not initial_load:
                messagebox.showwarning("Файл не найден", "Выбранный документ не найден.")
        self.word_analog_text.config(state="disabled")

    def _setup_automated_reports_subtab(self, parent_frame):
        """Настраивает UI для подвкладки Автоматизированные Отчеты с Графиками."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Автоматизированные Отчеты с Графиками (Концепт)", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.report_output_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Courier New", 10))
        self.report_output_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.report_output_text.config(state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Сгенерировать Отчет (Концепт)", command=self._generate_automated_report).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Экспортировать в Word (Концепт)", command=lambda: self._export_report_concept("Word")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Экспортировать в PDF (Концепт)", command=lambda: self._export_report_concept("PDF")).pack(side=tk.LEFT, padx=5)

    def _generate_automated_report(self):
        """Концептуально генерирует автоматизированный отчет с графиками."""
        self.report_output_text.config(state="normal")
        self.report_output_text.delete("1.0", tk.END)

        report_title = "Сводный Отчет LAG-LMV (Концепт)"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_content = [
            f"--- {report_title} ({timestamp}) ---\n",
            "## 1. Обзор Системного Мониторинга",
            "**Последний Отчет по Чек-листу:**",
            self._get_latest_checklist_summary(),
            "\n**Обнаруженные Аномалии (Последний Запуск):**",
            self._get_latest_intrusion_summary(),
            "\n**Концептуальный График Аномалий за Последние 7 Дней (Линейный):**",
            self._generate_conceptual_line_chart("Аномалии", [random.randint(0, 5) for _ in range(7)]),
            "\n------------------------------------------------\n",

            "## 2. Прогресс в Личном Развитии",
            "**Ваши Активные Цели:**",
            self._get_active_goals_summary(),
            "\n**Концептуальный График Прогресса Целей (Столбчатая Диаграмма):**",
            self._generate_conceptual_bar_chart("Прогресс Целей", {goal: self.user_goals[goal]['progress'] for goal in self.user_goals if self.user_goals[goal]['status'] == 'Активно'}),
            "\n------------------------------------------------\n",

            "## 3. Резюме Медитаций",
            "**Последние Сессии Медитации:**",
            self._get_latest_meditation_summary(),
            "\n**Концептуальный График Продолжительности Медитаций (Круговая Диаграмма):**",
            self._generate_conceptual_pie_chart("Распределение Продолжительности Медитаций", {f"{entry['duration_minutes']} мин": 1 for entry in self.meditation_logs[-5:]}), # Last 5
            "\n------------------------------------------------\n",
            "Этот отчет является концептуальным. В реальном приложении он бы генерировался с использованием "
            "библиотек для визуализации данных (например, Matplotlib для Python) и экспорта в полноценные форматы документов."
        ]
        self.report_output_text.insert(tk.END, "\n".join(report_content))
        self.report_output_text.config(state="disabled")
        messagebox.showinfo("Генерация Отчета", "Концептуальный отчет с графиками сгенерирован.")

    def _get_latest_checklist_summary(self):
        if os.path.exists(self.latest_checklist_report_path_file):
            try:
                with open(self.latest_checklist_report_path_file, 'r', encoding='utf-8') as f_path:
                    latest_report_path = f_path.read().strip()
                    if os.path.exists(latest_report_path):
                        with open(latest_report_path, 'r', encoding='utf-8') as f_report:
                            content = f_report.read().splitlines()
                            return "\n".join(content[:5]) + "..." # Get first few lines
            except Exception:
                return "Нет данных или ошибка чтения."
        return "Нет данных."

    def _get_latest_intrusion_summary(self):
        if os.path.exists(self.latest_intrusion_log_path_file):
            try:
                with open(self.latest_intrusion_log_path_file, 'r', encoding='utf-8') as f_path:
                    latest_report_path = f_path.read().strip()
                    if os.path.exists(latest_report_path):
                        with open(latest_report_path, 'r', encoding='utf-8') as f_report:
                            content = f_report.read().splitlines()
                            return "\n".join(content[:5]) + "..." # Get first few lines
            except Exception:
                return "Нет данных или ошибка чтения."
        return "Нет данных."

    def _get_active_goals_summary(self):
        active_goals = [f"- {name} ({data['progress']}%)" for name, data in self.user_goals.items() if data['status'] == 'Активно']
        return "\n".join(active_goals) if active_goals else "Нет активных целей."

    def _get_latest_meditation_summary(self):
        if self.meditation_logs:
            latest = self.meditation_logs[-3:] # Last 3 entries
            summary = [f"- {entry['date']}: {entry['duration_minutes']} мин" for entry in latest]
            return "\n".join(summary)
        return "Нет записей медитаций."

    def _generate_conceptual_line_chart(self, title, data_points):
        """Генерирует концептуальный линейный график в текстовом формате."""
        chart = [f"График: {title}"]
        max_val = max(data_points) if data_points else 0
        if max_val == 0:
            return "\n(Нет данных для графика)\n"

        # Scale for ASCII art
        scale_factor = 10.0 / max_val if max_val > 0 else 1

        for i, val in enumerate(data_points):
            bar = "#" * int(val * scale_factor)
            chart.append(f"День {i+1}: {bar} ({val})")
        return "\n".join(chart) + "\n"

    def _generate_conceptual_bar_chart(self, title, data_dict):
        """Генерирует концептуальную столбчатую диаграмму в текстовом формате."""
        chart = [f"Диаграмма: {title}"]
        if not data_dict:
            return "\n(Нет данных для диаграммы)\n"

        max_label_len = max(len(label) for label in data_dict.keys())
        max_val = max(data_dict.values())
        if max_val == 0:
            return "\n(Нет данных для диаграммы)\n"

        scale_factor = 20.0 / max_val

        for label, value in data_dict.items():
            bar = "█" * int(value * scale_factor)
            chart.append(f"{label.ljust(max_label_len)} | {bar} {value}%")
        return "\n".join(chart) + "\n"

    def _generate_conceptual_pie_chart(self, title, data_dict):
        """Генерирует концептуальную круговую диаграмму в текстовом формате."""
        chart = [f"Круговая Диаграмма: {title}"]
        if not data_dict:
            return "\n(Нет данных для диаграммы)\n"

        total = sum(data_dict.values())
        if total == 0:
            return "\n(Нет данных для диаграммы)\n"

        for label, value in data_dict.items():
            percentage = (value / total) * 100
            chart.append(f"- {label}: {percentage:.1f}%")
        chart.append("\n(Представление круговой диаграммы ограничено текстовым форматом)")
        return "\n".join(chart) + "\n"

    def _export_report_concept(self, export_type):
        """Концептуальный экспорт отчета в Word или PDF."""
        content = self.report_output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Экспорт Отчета", "Сначала сгенерируйте отчет для экспорта.")
            return

        messagebox.showinfo("Экспорт Отчета (Концепт)",
                            f"В реальном приложении сгенерированный отчет будет экспортирован в формат {export_type}. "
                            "Это может включать встроенные графики и форматирование, используя соответствующие библиотеки (например, python-docx, reportlab).")

    def _setup_zero_archive_subtab(self, parent_frame):
        """Настраивает UI для подвкладки Управление Архивом ЗЕРО."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Управление Архивом ЗЕРО (Концепт)", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        zero_archive_info_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), height=15)
        zero_archive_info_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        zero_archive_info_text.config(state="normal")
        zero_archive_info_text.insert(tk.END,
            "**Архив ЗЕРО:** Это концептуальный архив, который хранит *структуру и метаданные* ваших синхронизаций с облачными сервисами (Google Drive, Spotify и т.д.), а не сами данные. "
            "Он действует как 'манифест' для восстановления, если вы потеряете локальный доступ, но помните свой пароль.\n\n"
            "**Структура:**\n"
            "Архив --> КЛЮЧ ПОЛЬЗОВАТЕЛЯ (ваш пароль-дешифратор) --> Манифест --> Что/Куда (описание данных и их контрольные суммы).\n\n"
            "**Принцип Пациента Зеро:** Если вы вспомните свой пароль и найдете хотя бы один 'Архив ЗЕРО', приложение концептуально сможет начать автоматическое восстановление, "
            "используя ваш пароль для расшифровки манифеста и поиска остальных частей данных через все доступные "
            "децентрализованные способы связи (торренты, Tor, Google, Telegram и т.д.), которые держат сервера (концептуально).\n\n"
            "**ВАЖНО:** Ваши проблемы не мои. Этот архив предназначен для вашей самостоятельной помощи. Приложение не хранит ваш пароль и не несет ответственности за потерю данных."
        )
        zero_archive_info_text.config(state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Создать Архив ЗЕРО (Концепт)", command=self._create_zero_archive_manifest).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Загрузить Архив ЗЕРО (Концепт)", command=self._load_zero_archive_manifest).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Инициировать Восстановление (Концепт)", command=self._initiate_decentralized_recovery).pack(side=tk.LEFT, padx=5)

    def _create_zero_archive_manifest(self):
        """Концептуально создает новый манифест Архива ЗЕРО."""
        new_manifest = {
            "archive_id": "ZEROARCHIVE_" + "".join(random.choices("0123456789abcdef", k=16)),
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": "Концептуальный манифест синхронизации облачных ресурсов, сгенерированный пользователем.",
            "cloud_services_metadata": [
                {"service_name": "Google Drive", "last_sync": datetime.datetime.now().strftime("%Y-%m-%d"), "checksum_algo": "SHA256", "data_point_count": random.randint(50, 500), "sync_status": random.choice(["OK", "Warning"])},
                {"service_name": "Spotify", "last_sync": datetime.datetime.now().strftime("%Y-%m-%d"), "checksum_algo": "MD5", "data_point_count": random.randint(20, 300), "sync_status": random.choice(["OK", "Warning"])},
                {"service_name": "Telegram Cloud", "last_sync": datetime.datetime.now().strftime("%Y-%m-%d"), "checksum_algo": "SHA256", "data_point_count": random.randint(100, 1000), "sync_status": random.choice(["OK", "Warning"])},
                {"service_name": "Other Cloud Service", "last_sync": datetime.datetime.now().strftime("%Y-%m-%d"), "checksum_algo": "SHA256", "data_point_count": random.randint(10, 150), "sync_status": random.choice(["OK", "Warning", "Error"])}
            ],
            "local_data_references": [
                {"type": "notes", "path_segment": "documents_data/my_notes.json", "checksum": "".join(random.choices("0123456789abcdef", k=32))},
                {"type": "goals", "path_segment": "wellness_data/user_goals.json", "checksum": "".join(random.choices("0123456789abcdef", k=32))}
            ],
            "recovery_instructions_conceptual": "Этот манифест является ключом. Используйте свой пароль для дешифровки и поиска других частей ваших данных в децентрализованных сетях. Ваши проблемы не мои."
        }
        try:
            with open(self.zero_archive_path, 'w', encoding='utf-8') as f:
                json.dump(new_manifest, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Создание Архива ЗЕРО", f"Концептуальный 'Архив ЗЕРО' создан по пути: {self.zero_archive_path}\n"
                                                      "Помните: это манифест, а не сами данные. Для восстановления вам понадобится ваш пароль и доступ к децентрализованным сетям (концептуально).")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать 'Архив ЗЕРО': {e}")

    def _load_zero_archive_manifest(self):
        """Концептуально загружает и отображает манифест Архива ЗЕРО."""
        if os.path.exists(self.zero_archive_path):
            try:
                with open(self.zero_archive_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)

                display_content = [
                    "--- Концептуальный Архив ЗЕРО (Манифест) ---\n",
                    f"ID Архива: {manifest.get('archive_id', 'N/A')}",
                    f"Дата создания: {manifest.get('creation_date', 'N/A')}",
                    f"Описание: {manifest.get('description', 'N/A')}\n",
                    "## Метаданные облачных сервисов:",
                ]
                for service in manifest.get('cloud_services_metadata', []):
                    display_content.append(f"- Сервис: {service.get('service_name', 'N/A')}, Последняя синхронизация: {service.get('last_sync', 'N/A')}, Статус: {service.get('sync_status', 'N/A')}, Элементов: {service.get('data_point_count', 'N/A')}")

                display_content.append("\n## Ссылки на локальные данные:")
                for ref in manifest.get('local_data_references', []):
                    display_content.append(f"- Тип: {ref.get('type', 'N/A')}, Путь: {ref.get('path_segment', 'N/A')}, Контрольная сумма: {ref.get('checksum', 'N/A')}")

                display_content.append(f"\n## Инструкции по восстановлению (концептуально):")
                display_content.append(manifest.get('recovery_instructions_conceptual', 'N/A'))

                messagebox.showinfo("Загрузка Архива ЗЕРО", "\n".join(display_content) + "\n\n(Восстановление начнется, только если вы предоставите свой мастер-пароль. Приложение не хранит его.)")

            except json.JSONDecodeError:
                messagebox.showerror("Ошибка загрузки", "Файл 'Архива ЗЕРО' поврежден или имеет неверный формат.")
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить 'Архив ЗЕРО': {e}")
        else:
            messagebox.showwarning("Архив не найден", "Файл 'Архива ЗЕРО' не найден. Пожалуйста, создайте его сначала.")

    def _initiate_decentralized_recovery(self):
        """Концептуально инициирует процесс децентрализованного восстановления."""
        password = simpledialog.askstring("Инициировать Восстановление", "Введите ваш мастер-пароль для дешифровки манифеста и начала восстановления (концептуально):", show='*')

        if password:
            if not os.path.exists(self.zero_archive_path):
                messagebox.showwarning("Ошибка", "Файл 'Архива ЗЕРО' не найден. Сначала создайте или загрузите его.")
                return

            try:
                with open(self.zero_archive_path, 'r', encoding='utf-8') as f:
                    manifest_content = json.load(f) # Read for conceptual processing

                # Conceptual decryption (password is used as a conceptual key)
                # In a real system, 'password' would be used with a crypto library to decrypt the manifest.
                # For this demo, we just simulate success if password is provided.
                if len(password) < 5: # Simple conceptual check
                     messagebox.showwarning("Ошибка", "Пароль слишком короткий для концептуального восстановления. Попробуйте еще раз.")
                     return

                recovery_log = [
                    f"--- Концептуальное Восстановление Инициировано ({datetime.datetime.now().strftime('%H:%M:%S')}) ---\n",
                    f"Использование пароля для концептуальной дешифровки манифеста ID: {manifest_content.get('archive_id', 'N/A')}",
                    "Манифест дешифрован (концептуально). Идет поиск данных по каналам:\n",
                    "- Поиск через концептуальную сеть торрентов... (найдено 10% метаданных)",
                    "- Поиск через концептуальный Google Drive API... (найдено 30% метаданных)",
                    "- Поиск через концептуальный Telegram Cloud... (найдено 20% метаданных)",
                    "- Поиск через концептуальную Tor-сеть... (найдено 5% метаданных)",
                    "\n**Концептуально:** Приложение ищет ваши данные, используя контрольные суммы из манифеста и различные каналы связи. "
                    "Это сложный и длительный процесс, зависящий от доступности ваших резервных копий в децентрализованных и облачных источниках.",
                    "\n**Ваши проблемы не мои.** Восстановление возможно только при наличии архива и вашего пароля. Приложение не восстанавливает сами данные, а лишь помогает найти их расположение."
                ]
                messagebox.showinfo("Инициирование Восстановления (Концепт)", "\n".join(recovery_log))

            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Файл 'Архива ЗЕРО' поврежден или имеет неверный формат. Невозможно инициировать восстановление.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при инициировании восстановления: {e}")
        else:
            messagebox.showwarning("Отмена", "Восстановление отменено. Пароль не был введен.")


    def refresh_page(self):
        """Обновляет содержимое всей страницы (системные отчеты, личное развитие, документы и отчеты)."""
        self._refresh_system_reports() # Refresh system monitoring part
        self._load_initial_data() # Reload data for wellness and documents part
        self._populate_goals_tree()
        self._populate_notes_listbox()
        self._display_current_note() # Refresh current note display
        self._load_pdf_concept(initial_load=True) # Reload dummy PDF
        self._load_table_concept(initial_load=True) # Reload dummy Table
        self._load_word_analog_concept(initial_load=True) # Reload dummy Word
        # No specific refresh needed for ZERO Archive, as it's static informational text initially


# This is the function the main App will call to set up the new combined tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    system_and_self_management_page_instance = SystemAndSelfManagementPage(frame, app_data)
    # Store instance for potential external access if needed, though for this specific page it might not be strictly necessary
    app_data["system_and_self_management_page_instance"] = system_and_self_management_page_instance
    return frame, system_and_self_management_page_instance.refresh_page
