# Principle: Functionality over purity: If it works, keep it.
# We don't care how it works or what "dark magic" it uses.
# It's chaos and madness, and we love it. The more chaos, the more fun.
# Users can fuck off and do whatever they want, we don't wipe their asses.
# Let them have fun, screw up, if they forget their password, they'll lose their life, and if they remember, they'll restore
# only what they managed to sync, and fuck off with questions.
# This file marks the 'modules' directory as a Python package.
# It can be left empty for simple package initialization.
# For more complex packages, it might contain imports,
# package-level variables, or functions to be exposed.
# i don't care what you think just use the biggest dildos you know to make everyone happy
# I don't care how they work as long as they work

# This is the rocket fuel that you and I will use to put out fires.

iimport tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime

class AboutPage:
    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data # Potentially useful for paths etc.

        # Paths for new documentation/contact folders (relative to project root)
        self.project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.instructions_for_dev_dir = os.path.join(self.project_root_dir, "Instructions_for_dev")
        self.instructions_for_users_dir = os.path.join(self.project_root_dir, "Instructions_for_users")
        self.contacts_dir = os.path.join(self.project_root_dir, "Contacts")

        # Ensure directories exist
        os.makedirs(self.instructions_for_dev_dir, exist_ok=True)
        os.makedirs(self.instructions_for_users_dir, exist_ok=True)
        os.makedirs(self.contacts_dir, exist_ok=True)

        # Create dummy instruction files (English, Russian)
        self._create_dummy_instruction_file(self.instructions_for_dev_dir, "FOLLOW_ME_PLEASE_en.txt", "Developer Instructions (English)")
        self._create_dummy_instruction_file(self.instructions_for_dev_dir, "FOLLOW_ME_PLEASE_ru.txt", "Инструкции для разработчика (Русский)")
        self._create_dummy_instruction_file(self.instructions_for_dev_dir, "Instructions_en.md", "# Developer Instructions\nThis is a Markdown file for developers.")
        self._create_dummy_instruction_file(self.instructions_for_dev_dir, "Instructions_ru.md", "# Инструкции для разработчиков\nЭто Markdown файл для разработчиков.")

        self._create_dummy_instruction_file(self.instructions_for_users_dir, "FOLLOW_ME_PLEASE_en.txt", "User Instructions (English)")
        self._create_dummy_instruction_file(self.instructions_for_users_dir, "FOLLOW_ME_PLEASE_ru.txt", "Инструкции для пользователей (Русский)")
        self._create_dummy_instruction_file(self.instructions_for_users_dir, "Instructions_en.md", "# User Instructions\nThis is a Markdown file for users.")
        self._create_dummy_instruction_file(self.instructions_for_users_dir, "Instructions_ru.md", "# Инструкции для пользователей\nЭто Markdown файл для пользователей.")

        # Create dummy contact files
        self._create_dummy_contact_file(self.contacts_dir, "0_LAG_author_of_the_idea.txt", "LAG Author: conceptual author of the LAG-LMV idea.")
        self._create_dummy_contact_file(self.contacts_dir, "1_next_follower.txt", "Next Follower: conceptual contributor 1.")
        self._create_dummy_contact_file(self.contacts_dir, "2_another_follower.txt", "Another Follower: conceptual contributor 2.")

        self._setup_ui()

    def _setup_ui(self):
        """Sets up the UI elements for the About page."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Row for main content

        ttk.Label(main_frame, text="О Программе LAG-LMVL", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        info_text_content = (
            "Версия: 1.0.0 (Концептуальная Демонстрация)\n"
            "Дата разработки: Август 2025\n"
            "Разработчик: LAG (Концептуальный)\n"
            "Назначение: LAG-LMVL (Log Monitoring Viewer) - это многофункциональное "
            "демонстрационное приложение, разработанное для исследования и иллюстрации "
            "концепций безопасного мониторинга, управления данными, конфиденциальности и "
            "интеграции ИИ в единый интерфейс. Оно создано для демонстрации "
            "принципов модульности, аудита и контроля доступа в контексте "
            "конфиденциальности и безопасности.\n\n"
            "Все функции, связанные с шифрованием, платежами, VPN, облачными вычислениями, "
            "социальными сетями и ИИ-ассистентом, являются КОНЦЕПТУАЛЬНЫМИ и НЕ "
            "предназначены для использования с реальными конфиденциальными данными или в производственной "
            "среде без соответствующей разработки и реализации надежных "
            "криптографических решений."
        )

        self.about_text = tk.Text(main_frame, wrap="word", bg="#f8f8f8", fg="#333", relief="flat", bd=0, font=("Arial", 11))
        self.about_text.insert(tk.END, info_text_content)
        self.about_text.config(state="disabled")
        self.about_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Documentation and Contacts Section
        doc_contact_frame = ttk.LabelFrame(main_frame, text="Документация и Контакты", padding="10 10 10 10")
        doc_contact_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        doc_contact_frame.grid_columnconfigure(0, weight=1)
        doc_contact_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(doc_contact_frame, text="Инструкции для Разработчиков", command=self._open_dev_instructions_folder).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(doc_contact_frame, text="Инструкции для Пользователей", command=self._open_user_instructions_folder).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(doc_contact_frame, text="Контакты", command=self._open_contacts_folder).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def _create_dummy_instruction_file(self, folder, filename, content):
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _create_dummy_contact_file(self, folder, filename, content):
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _open_folder(self, path, folder_name):
        if os.path.exists(path):
            try:
                os.startfile(path) if os.name == 'nt' else os.system(f'xdg-open "{path}"')
                messagebox.showinfo("Открыть Папку", f"Папка открыта: {folder_name}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть папку '{folder_name}': {e}")
        else:
            messagebox.showwarning("Не Найдено", f"Папка '{folder_name}' не найдена по пути: {path}")

    def _open_dev_instructions_folder(self):
        self._open_folder(self.instructions_for_dev_dir, "Инструкции для Разработчиков")

    def _open_user_instructions_folder(self):
        self._open_folder(self.instructions_for_users_dir, "Инструкции для Пользователей")

    def _open_contacts_folder(self):
        self._open_folder(self.contacts_dir, "Контакты")

    def refresh_page(self):
        # Nothing to dynamically refresh on this page, content is static
        pass

# This is the function the main App will call to set up the About tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    about_page_instance = AboutPage(frame, app_data)
    return frame, about_page_instance.refresh_page
