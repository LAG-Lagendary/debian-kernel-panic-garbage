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

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json
import datetime
import secrets
import random # For simulated NN operations
import hashlib # For conceptual password hashing
import shutil # For conceptual deletion of user company data

# Import the CryptoUtils for conceptual encryption/decryption
try:
    from modules.encryption.crypto_utils import CryptoUtils
except ImportError:
    messagebox.showerror("Import Error", "Could not load encryption module. Please ensure 'modules/encryption/crypto_utils.py' exists and is accessible.")
    CryptoUtils = None

# --- Conceptual Master Key for Demo ---
# In a real system, this master key would be managed extremely securely,
# potentially derived from a strong passphrase or securely retrieved.
CONCEPTUAL_MASTER_KEY_FOR_DEMO = "ThisIsAReallyStrongDemoKeyForConceptualEncryptionOnly123!"

class AccessControlAuditPage:
    # Patient Zero Principle: "I don't wipe users' asses, if you forgot your master password, die.
    # When you don't regain access, and no one else does. I don't store any data,
    # you yourselves must take care of how and where to save it and how to remember the password,
    # because the password is the key to encrypting everything on your profile. Without it, no one has access."
    # This note cannot be deleted and must remain unchanged in all document versions.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths for conceptual data storage
        self.audit_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audit_data")
        self.user_roles_file = os.path.join(self.audit_data_dir, "user_roles.json")
        self.activity_log_file = os.path.join(self.audit_data_dir, "activity_log.json")
        self.mfa_config_file = os.path.join(self.audit_data_dir, "mfa_config.json")
        self.user_nns_file = os.path.join(self.audit_data_dir, "user_neural_networks.json") # New file for user NNs
        self.companies_file = os.path.join(self.audit_data_dir, "companies.json") # NEW: File for company data
        self.company_user_data_base_dir = os.path.join(self.audit_data_dir, "company_user_data") # NEW: Base dir for conceptual company-specific user files

        os.makedirs(self.audit_data_dir, exist_ok=True)
        os.makedirs(self.company_user_data_base_dir, exist_ok=True) # Ensure company user data directory exists

        self.crypto_utils = None
        if CryptoUtils:
            try:
                self.crypto_utils = CryptoUtils(CONCEPTUAL_MASTER_KEY_FOR_DEMO)
            except Exception as e:
                messagebox.showerror("Crypto Error", f"Failed to initialize CryptoUtils: {e}")

        self._load_initial_data()
        self._setup_ui()

    def _load_initial_data(self):
        """Loads or initializes conceptual user roles, activity log, MFA config, user NNs, and company data."""
        # Conceptual user roles (now includes company_id and password_hash)
        if not os.path.exists(self.user_roles_file):
            self.user_roles = {
                "admin_user": {"role": "Admin", "permissions": ["all"], "company_id": None, "password_hash": self._conceptual_hash_password("admin_pass")},
                "auditor_user": {"role": "Auditor", "permissions": ["view_logs", "view_reports"], "company_id": None, "password_hash": self._conceptual_hash_password("auditor_pass")},
                "guest_user": {"role": "Guest", "permissions": ["view_main_page"], "company_id": None, "password_hash": self._conceptual_hash_password("guest_pass")},
            }
            with open(self.user_roles_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_roles, f, indent=4, ensure_ascii=False)
        else:
            with open(self.user_roles_file, 'r', encoding='utf-8') as f:
                self.user_roles = json.load(f)

        # Conceptual activity log
        if not os.path.exists(self.activity_log_file):
            self.activity_log = []
            self._log_activity("system", "Application started.", "info")
        else:
            with open(self.activity_log_file, 'r', encoding='utf-8') as f:
                self.activity_log = json.load(f)

        # Conceptual MFA config
        if not os.path.exists(self.mfa_config_file):
            self.mfa_config = {
                "admin_user": {"enabled": False, "method": "TOTP"},
                "auditor_user": {"enabled": False, "method": "TOTP"},
                "guest_user": {"enabled": False, "method": "TOTP"},
            }
            with open(self.mfa_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.mfa_config, f, indent=4, ensure_ascii=False)
        else:
            with open(self.mfa_config_file, 'r', encoding='utf-8') as f:
                self.mfa_config = json.load(f)

        # Conceptual User Neural Networks
        if not os.path.exists(self.user_nns_file):
            self.user_neural_networks = {} # Format: {"user_id": {"nns": {"nn_name": {"status": "inactive", "cloud": "none", "path": "conceptual_path"}}, "active_nn": None}}
            with open(self.user_nns_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_neural_networks, f, indent=4, ensure_ascii=False)
        else:
            with open(self.user_nns_file, 'r', encoding='utf-8') as f:
                self.user_neural_networks = json.load(f)

        # NEW: Conceptual Companies
        if not os.path.exists(self.companies_file):
            self.companies = {
                "google_concept": {"name": "Google (Concept)", "admin_user_id": "admin_user", "internal_resources": ["GDrive_Access_Module", "GSuite_Policy_Docs"]},
                "kpmg_concept": {"name": "KPMG (Concept)", "admin_user_id": "auditor_user", "internal_resources": ["KPMG_Audit_Tools"]},
            }
            with open(self.companies_file, 'w', encoding='utf-8') as f:
                json.dump(self.companies, f, indent=4, ensure_ascii=False)
        else:
            with open(self.companies_file, 'r', encoding='utf-8') as f:
                self.companies = json.load(f)

        # Assign existing conceptual users to companies for demo
        if "google_concept" in self.companies and "admin_user" in self.user_roles:
            self.user_roles["admin_user"]["company_id"] = "google_concept"
        if "kpmg_concept" in self.companies and "auditor_user" in self.user_roles:
            self.user_roles["auditor_user"]["company_id"] = "kpmg_concept"
        self._save_data() # Save updated user roles with company_id

    def _save_data(self):
        """Saves current conceptual data to files."""
        with open(self.user_roles_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_roles, f, indent=4, ensure_ascii=False)
        with open(self.activity_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.activity_log, f, indent=4, ensure_ascii=False)
        with open(self.mfa_config_file, 'w', encoding='utf-8') as f:
            json.dump(self.mfa_config, f, indent=4, ensure_ascii=False)
        with open(self.user_nns_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_neural_networks, f, indent=4, ensure_ascii=False)
        with open(self.companies_file, 'w', encoding='utf-8') as f:
            json.dump(self.companies, f, indent=4, ensure_ascii=False)

    def _log_activity(self, user_id, action, status="success"):
        """Logs a conceptual user activity."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "user_id": user_id,
            "action": action,
            "status": status
        }
        self.activity_log.append(log_entry)
        self._save_data() # Save after each log

    def _conceptual_hash_password(self, password: str) -> str:
        """
        Концептуальное хеширование пароля.
        В реальном приложении использовались бы надежные, медленные алгоритмы хеширования (например, bcrypt, Argon2)
        с солью, чтобы предотвратить атаки по словарю и радужным таблицам.
        """
        if self.crypto_utils:
            return self.crypto_utils.hash_password(password)
        else:
            # Fallback if crypto_utils is not loaded (should not happen in production)
            return hashlib.sha256(password.encode()).hexdigest()

    def _conceptual_verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Концептуальная проверка пароля.
        """
        if self.crypto_utils:
            return self.crypto_utils.verify_password(password, hashed_password)
        else:
            return hashlib.sha256(password.encode()).hexdigest() == hashed_password


    def _setup_ui(self):
        """Sets up the UI elements for the Access Control and Audit page."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Row for notebooks

        ttk.Label(main_frame, text="Управление Доступом и Аудит", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        self.audit_notebook = ttk.Notebook(main_frame)
        self.audit_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- User Roles Tab (Existing, will be modified) ---
        self.user_roles_frame = ttk.Frame(self.audit_notebook, padding="10")
        self.audit_notebook.add(self.user_roles_frame, text="Пользователи и Роли")
        self._setup_user_roles_tab(self.user_roles_frame)

        # --- Activity Log Tab ---
        self.activity_log_frame = ttk.Frame(self.audit_notebook, padding="10")
        self.audit_notebook.add(self.activity_log_frame, text="Журнал Активности")
        self._setup_activity_log_tab(self.activity_log_frame)

        # --- MFA Configuration Tab ---
        self.mfa_config_frame = ttk.Frame(self.audit_notebook, padding="10")
        self.audit_notebook.add(self.mfa_config_frame, text="Настройка MFA")
        self._setup_mfa_config_tab(self.mfa_config_frame)

        # --- User AI & Automation Tab ---
        self.user_ai_automation_frame = ttk.Frame(self.audit_notebook, padding="10")
        self.audit_notebook.add(self.user_ai_automation_frame, text="ИИ и Автоматизация")
        self._setup_user_ai_automation_tab(self.user_ai_automation_frame)

        # --- NEW: Company Management Tab ---
        self.company_management_frame = ttk.Frame(self.audit_notebook, padding="10")
        self.audit_notebook.add(self.company_management_frame, text="Управление Компаниями")
        self._setup_company_management_tab(self.company_management_frame)


        # Patient Zero Principle Note (Common for all tabs)
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер-пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные; "
            "вы сами должны заботиться о том, как и куда их сохранять и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
            "\n\n**Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.**"
            "\n\n**Важно:** Компания может знать ваш логин, но не пароль. При удалении пользователя из компании, "
            "все файлы, которые не были сохранены на корпоративном источнике (сервере компании), удаляются. "
            "Ваш пароль — это ваша личная ответственность. Это не устройство или система, а просто набор символов, "
            "который вы запомнили. Если он никуда не привязан, то логин и пароль — это исключительно ответственность пользователя."
        ), font=("Arial", 9, "italic"), wraplength=700, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, pady=10, sticky="ew")

    def _setup_user_roles_tab(self, parent_frame):
        """Sets up the UI for the User Roles tab."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальные Пользователи и Роли", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # User List
        user_list_frame = ttk.LabelFrame(parent_frame, text="Пользователи", padding="10")
        user_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        user_list_frame.grid_rowconfigure(0, weight=1)
        user_list_frame.grid_columnconfigure(0, weight=1)

        self.user_tree = ttk.Treeview(user_list_frame, columns=("Role", "Company ID"), show="headings") # Added Company ID
        self.user_tree.grid(row=0, column=0, sticky="nsew")
        self.user_tree.heading("Role", text="Роль")
        self.user_tree.heading("Company ID", text="ID Компании") # New heading
        self.user_tree.column("Role", width=100)
        self.user_tree.column("Company ID", width=150) # Adjusted width

        user_tree_scrollbar = ttk.Scrollbar(user_list_frame, orient="vertical", command=self.user_tree.yview)
        user_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.user_tree.config(yscrollcommand=user_tree_scrollbar.set)

        self._populate_user_tree()

        # Role Management Section
        role_management_frame = ttk.LabelFrame(parent_frame, text="Управление Ролями", padding="10")
        role_management_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        role_management_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(role_management_frame, text="ID Пользователя:").grid(row=0, column=0, sticky="w", pady=2)
        self.user_id_entry = ttk.Entry(role_management_frame, width=30)
        self.user_id_entry.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(role_management_frame, text="Пароль (для нового пользователя):").grid(row=1, column=0, sticky="w", pady=2)
        self.user_password_entry = ttk.Entry(role_management_frame, width=30, show="*") # New password field
        self.user_password_entry.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(role_management_frame, text="Роль:").grid(row=2, column=0, sticky="w", pady=2) # Shifted row
        self.role_combobox = ttk.Combobox(role_management_frame, values=["Admin", "Auditor", "Guest"], state="readonly")
        self.role_combobox.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Label(role_management_frame, text="ID Компании (опционально):").grid(row=3, column=0, sticky="w", pady=2) # New company field
        self.company_id_combobox = ttk.Combobox(role_management_frame, values=list(self.companies.keys()) + [""], state="readonly")
        self.company_id_combobox.grid(row=3, column=1, sticky="ew", pady=2)
        self.company_id_combobox.set("") # Default to no company

        ttk.Button(role_management_frame, text="Добавить Пользователя", command=self._add_user).grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(role_management_frame, text="Обновить Роль/Компанию", command=self._update_user_role_and_company).grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(role_management_frame, text="Удалить Пользователя", command=self._delete_user).grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

        self.user_tree.bind("<<TreeviewSelect>>", self._on_user_select)

    def _populate_user_tree(self):
        """Populates the user treeview with current user roles."""
        for iid in self.user_tree.get_children():
            self.user_tree.delete(iid)
        for user_id, data in self.user_roles.items():
            # Permissions are conceptual and not directly displayed in this tree, but can be retrieved
            company_id = data.get("company_id", "N/A")
            self.user_tree.insert("", "end", iid=user_id, values=(data.get("role"), company_id))

    def _on_user_select(self, event):
        """Loads selected user's data into input fields."""
        selected_item = self.user_tree.focus()
        if selected_item:
            user_id = selected_item
            user_data = self.user_roles[user_id]
            self.user_id_entry.delete(0, tk.END)
            self.user_id_entry.insert(0, user_id)
            self.role_combobox.set(user_data["role"])
            self.company_id_combobox.set(user_data.get("company_id", ""))
            self.user_password_entry.delete(0, tk.END) # Clear password field on select for security

    def _add_user(self):
        user_id = self.user_id_entry.get().strip()
        password = self.user_password_entry.get()
        role = self.role_combobox.get()
        company_id = self.company_id_combobox.get().strip() if self.company_id_combobox.get() else None

        if not user_id or not role or not password:
            messagebox.showwarning("Ошибка Ввода", "ID пользователя, Пароль и Роль не могут быть пустыми.")
            return
        if user_id in self.user_roles:
            messagebox.showwarning("Существует", f"Пользователь '{user_id}' уже существует. Используйте 'Обновить Роль/Компанию'.")
            return
        if company_id and company_id not in self.companies:
            messagebox.showwarning("Ошибка Компании", f"Компания с ID '{company_id}' не найдена. Сначала добавьте компанию.")
            return

        permissions = []
        if role == "Admin": permissions = ["all"]
        elif role == "Auditor": permissions = ["view_logs", "view_reports"]
        elif role == "Guest": permissions = ["view_main_page"]

        hashed_password = self._conceptual_hash_password(password)

        self.user_roles[user_id] = {"role": role, "permissions": permissions, "company_id": company_id, "password_hash": hashed_password}
        # Also add to MFA config with default disabled
        if user_id not in self.mfa_config:
            self.mfa_config[user_id] = {"enabled": False, "method": "TOTP"}
        # Also add to User NN config with default inactive
        if user_id not in self.user_neural_networks:
            self.user_neural_networks[user_id] = {"nns": {}, "active_nn": None} # Each user has their own NN config


        self._save_data()
        self._populate_user_tree()
        self._populate_mfa_user_tree() # Refresh MFA tree as a new user might be added
        self._populate_company_user_tree() # Refresh company user tree
        self._log_activity("admin", f"Добавлен пользователь '{user_id}' с ролью '{role}' для компании '{company_id}'.")
        messagebox.showinfo("Успех", f"Пользователь '{user_id}' добавлен как '{role}'. Пароль установлен. (Пароль известен только пользователю).")
        self.user_password_entry.delete(0, tk.END) # Clear password after use

    def _update_user_role_and_company(self):
        user_id = self.user_id_entry.get().strip()
        role = self.role_combobox.get()
        company_id = self.company_id_combobox.get().strip() if self.company_id_combobox.get() else None
        new_password = self.user_password_entry.get() # Allow changing password

        if not user_id or not role:
            messagebox.showwarning("Ошибка Ввода", "ID пользователя и Роль не могут быть пустыми.")
            return
        if user_id not in self.user_roles:
            messagebox.showwarning("Не Найден", f"Пользователь '{user_id}' не найден. Используйте 'Добавить Пользователя'.")
            return
        if company_id and company_id not in self.companies:
            messagebox.showwarning("Ошибка Компании", f"Компания с ID '{company_id}' не найдена. Сначала добавьте компанию.")
            return

        permissions = []
        if role == "Admin": permissions = ["all"]
        elif role == "Auditor": permissions = ["view_logs", "view_reports"]
        elif role == "Guest": permissions = ["view_main_page"]

        self.user_roles[user_id]["role"] = role
        self.user_roles[user_id]["permissions"] = permissions
        self.user_roles[user_id]["company_id"] = company_id
        if new_password: # Update password only if provided
            self.user_roles[user_id]["password_hash"] = self._conceptual_hash_password(new_password)
            messagebox.showinfo("Пароль Обновлен", f"Пароль пользователя '{user_id}' был обновлен. (Новый пароль известен только пользователю).")

        self._save_data()
        self._populate_user_tree()
        self._populate_company_user_tree() # Refresh company user tree
        self._log_activity("admin", f"Обновлена роль пользователя '{user_id}' на '{role}', компания: '{company_id}'.")
        messagebox.showinfo("Успех", f"Роль для пользователя '{user_id}' обновлена на '{role}', компания: '{company_id}'.")
        self.user_password_entry.delete(0, tk.END) # Clear password after use

    def _delete_user(self):
        user_id = self.user_id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Ошибка Ввода", "ID пользователя не может быть пустым.")
            return
        if user_id not in self.user_roles:
            messagebox.showwarning("Не Найден", f"Пользователь '{user_id}' не найден.")
            return
        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить пользователя '{user_id}'? "
                                                        "Это действие необратимо и приведет к удалению всех связанных с ним концептуальных данных, "
                                                        "не сохраненных на источнике компании."):
            # Conceptual: Delete user-specific conceptual data files in company directory
            user_company_data_path = os.path.join(self.company_user_data_base_dir, user_id)
            if os.path.exists(user_company_data_path):
                # Simulate deletion of "unsaved" data
                for root, dirs, files in os.walk(user_company_data_path):
                    for file in files:
                        if "unsaved" in file.lower() or "temp" in file.lower(): # Conceptual check for unsaved files
                            os.remove(os.path.join(root, file))
                            self._log_activity("system", f"Удален несохраненный файл '{file}' пользователя '{user_id}' при его удалении.")
                # After cleaning unsaved, remove user's conceptual company data directory if empty
                if os.path.exists(user_company_data_path) and not os.listdir(user_company_data_path):
                    os.rmdir(user_company_data_path)
                    self._log_activity("system", f"Удалена директория данных пользователя '{user_id}' после удаления.")


            del self.user_roles[user_id]
            # Also remove MFA config if exists
            if user_id in self.mfa_config:
                del self.mfa_config[user_id]
            # Also remove NN config if exists
            if user_id in self.user_neural_networks:
                del self.user_neural_networks[user_id]

            self._save_data()
            self._populate_user_tree()
            self._populate_mfa_user_tree() # Refresh MFA tree
            self._populate_user_nn_tree() # Refresh NN tree
            self._populate_company_user_tree() # Refresh company user tree
            self._log_activity("admin", f"Пользователь '{user_id}' удален. Все несохраненные концептуальные данные пользователя удалены.")
            messagebox.showinfo("Успех", f"Пользователь '{user_id}' удален. (Помните, пароль — ваша ответственность).")
            self.user_id_entry.delete(0, tk.END)
            self.role_combobox.set('') # Clear role selection
            self.company_id_combobox.set('') # Clear company selection
            self.user_password_entry.delete(0, tk.END)

    def _setup_activity_log_tab(self, parent_frame):
        """Sets up the UI for the Activity Log tab."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Журнал Активности Приложения", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.activity_log_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10))
        self.activity_log_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        activity_log_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.activity_log_text.yview)
        activity_log_scrollbar.grid(row=1, column=1, sticky="ns")
        self.activity_log_text.config(yscrollcommand=activity_log_scrollbar.set, state="disabled")

        ttk.Button(parent_frame, text="Обновить Журнал", command=self._populate_activity_log_text).grid(row=2, column=0, pady=5, sticky="ew")

        self._populate_activity_log_text()

    def _populate_activity_log_text(self):
        """Populates the activity log text area."""
        self.activity_log_text.config(state="normal")
        self.activity_log_text.delete("1.0", tk.END)
        for entry in self.activity_log:
            self.activity_log_text.insert(tk.END, f"[{entry.get('timestamp')}] Пользователь: {entry.get('user_id')} - Действие: {entry.get('action')} (Статус: {entry.get('status')})\n")
        self.activity_log_text.see(tk.END)
        self.activity_log_text.config(state="disabled")

    def _setup_mfa_config_tab(self, parent_frame):
        """Sets up the UI for the MFA Configuration tab."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1) # List of users for MFA

        ttk.Label(parent_frame, text="Конфигурация Многофакторной Аутентификации (MFA)", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # MFA User List
        mfa_user_list_frame = ttk.LabelFrame(parent_frame, text="Пользователи для MFA", padding="10")
        mfa_user_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        mfa_user_list_frame.grid_rowconfigure(0, weight=1)
        mfa_user_list_frame.grid_columnconfigure(0, weight=1)

        self.mfa_user_tree = ttk.Treeview(mfa_user_list_frame, columns=("MFA Enabled", "Method"), show="headings")
        self.mfa_user_tree.grid(row=0, column=0, sticky="nsew")
        self.mfa_user_tree.heading("MFA Enabled", text="MFA Включено")
        self.mfa_user_tree.heading("Method", text="Метод")
        self.mfa_user_tree.column("MFA Enabled", width=100)
        self.mfa_user_tree.column("Method", width=100)

        mfa_user_tree_scrollbar = ttk.Scrollbar(mfa_user_list_frame, orient="vertical", command=self.mfa_user_tree.yview)
        mfa_user_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.mfa_user_tree.config(yscrollcommand=mfa_user_tree_scrollbar.set)

        self._populate_mfa_user_tree()

        # MFA Management Section
        mfa_management_frame = ttk.LabelFrame(parent_frame, text="Управление MFA", padding="10")
        mfa_management_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        mfa_management_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(mfa_management_frame, text="ID Пользователя:").grid(row=0, column=0, sticky="w", pady=2)
        self.mfa_user_id_entry = ttk.Entry(mfa_management_frame, width=30, state="readonly") # Readonly, set by selection
        self.mfa_user_id_entry.grid(row=0, column=1, sticky="ew", pady=2)

        self.mfa_enabled_var = tk.BooleanVar()
        self.mfa_checkbox = ttk.Checkbutton(mfa_management_frame, text="Включить MFA", variable=self.mfa_enabled_var, command=self._toggle_mfa_status)
        self.mfa_checkbox.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        ttk.Label(mfa_management_frame, text="Метод MFA:").grid(row=2, column=0, sticky="w", pady=2)
        self.mfa_method_combobox = ttk.Combobox(mfa_management_frame, values=["TOTP", "SMS (Концепт)", "Email (Концепт)"], state="readonly")
        self.mfa_method_combobox.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Button(mfa_management_frame, text="Обновить Настройки MFA", command=self._update_mfa_settings).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        # Conceptual MFA Setup (e.g., show QR code for TOTP)
        ttk.Button(mfa_management_frame, text="Концептуальная Настройка MFA", command=self._conceptual_mfa_setup).grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        self.mfa_user_tree.bind("<<TreeviewSelect>>", self._on_mfa_user_select)

    def _populate_mfa_user_tree(self):
        """Populates the MFA user treeview with current MFA configurations."""
        for iid in self.mfa_user_tree.get_children():
            self.mfa_user_tree.delete(iid)
        for user_id, config in self.mfa_config.items():
            enabled_str = "Да" if config.get("enabled", False) else "Нет"
            self.mfa_user_tree.insert("", "end", iid=user_id, values=(enabled_str, config.get("method", "N/A")))

    def _on_mfa_user_select(self, event):
        """Loads selected user's MFA data into input fields."""
        selected_item = self.mfa_user_tree.focus()
        if selected_item:
            user_id = selected_item
            self.mfa_user_id_entry.config(state="normal")
            self.mfa_user_id_entry.delete(0, tk.END)
            self.mfa_user_id_entry.insert(0, user_id)
            self.mfa_user_id_entry.config(state="readonly")

            self.mfa_enabled_var.set(self.mfa_config[user_id].get("enabled", False))
            self.mfa_method_combobox.set(self.mfa_config[user_id].get("method", "TOTP"))

    def _toggle_mfa_status(self):
        # This is primarily for visual feedback. Actual update happens in _update_mfa_settings
        pass

    def _update_mfa_settings(self):
        user_id = self.mfa_user_id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите пользователя.")
            return

        enabled = self.mfa_enabled_var.get()
        method = self.mfa_method_combobox.get()

        if user_id not in self.mfa_config:
            self.mfa_config[user_id] = {} # Initialize if new user

        self.mfa_config[user_id]["enabled"] = enabled
        self.mfa_config[user_id]["method"] = method
        self._save_data()
        self._populate_mfa_user_tree()
        self._log_activity("admin", f"Обновлен MFA для пользователя '{user_id}': Включено={enabled}, Метод='{method}'.")
        messagebox.showinfo("Успех", f"Настройки MFA обновлены для '{user_id}'.")

    def _conceptual_mfa_setup(self):
        user_id = self.mfa_user_id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите пользователя для концептуальной настройки MFA.")
            return

        method = self.mfa_method_combobox.get()
        if not self.mfa_enabled_var.get():
             messagebox.showinfo("Настройка MFA (Концепт)", f"MFA не включено для {user_id}. Включите его сначала.")
             return

        if method == "TOTP":
            secret_key = secrets.token_hex(16).upper()
            messagebox.showinfo("Настройка MFA (Концепт TOTP)",
                                f"Для пользователя '{user_id}' концептуально сгенерируйте QR-код TOTP или секретный ключ.\n\n"
                                f"Секретный ключ: {secret_key}\n\n"
                                "В реальном приложении вы бы отсканировали QR-код приложением-аутентификатором (например, Google Authenticator).")
        elif method == "SMS (Концепт)":
            messagebox.showinfo("Настройка MFA (Концепт SMS)",
                                f"Для пользователя '{user_id}' концептуально код верификации будет отправлен на его зарегистрированный номер телефона через SMS.")
        elif method == "Email (Концепт)":
            messagebox.showinfo("Настройка MFA (Концепт Email)",
                                f"Для пользователя '{user_id}' концептуально код верификации будет отправлен на его зарегистрированный адрес электронной почты.")

        self._log_activity(user_id, f"Инициирована концептуальная настройка MFA для метода '{method}'.", "info")

    def _setup_user_ai_automation_tab(self, parent_frame):
        """Sets up the UI for the User AI & Automation tab."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Управление Пользовательским ИИ и Автоматизацией для Облаков", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Left side: List of uploaded NNs
        nn_list_frame = ttk.LabelFrame(parent_frame, text="Загруженные Нейросети", padding="10")
        nn_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        nn_list_frame.grid_rowconfigure(0, weight=1)
        nn_list_frame.grid_columnconfigure(0, weight=1)

        self.nn_tree = ttk.Treeview(nn_list_frame, columns=("Status", "Cloud"), show="headings")
        self.nn_tree.grid(row=0, column=0, sticky="nsew")
        self.nn_tree.heading("Status", text="Статус")
        self.nn_tree.heading("Cloud", text="Облако")
        self.nn_tree.column("Status", width=80)
        self.nn_tree.column("Cloud", width=120)

        nn_tree_scrollbar = ttk.Scrollbar(nn_list_frame, orient="vertical", command=self.nn_tree.yview)
        nn_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.nn_tree.config(yscrollcommand=nn_tree_scrollbar.set)

        self._populate_user_nn_tree()

        # Right side: NN management and deep clean
        nn_management_frame = ttk.LabelFrame(parent_frame, text="Настройки Нейросети", padding="10")
        nn_management_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        nn_management_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(nn_management_frame, text="Пользователь (для НС):").grid(row=0, column=0, sticky="w", pady=2)
        self.nn_user_id_entry = ttk.Entry(nn_management_frame, width=30)
        self.nn_user_id_entry.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(nn_management_frame, text="Название НС:").grid(row=1, column=0, sticky="w", pady=2)
        self.nn_name_entry = ttk.Entry(nn_management_frame, width=30)
        self.nn_name_entry.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(nn_management_frame, text="Связать с облаком:").grid(row=2, column=0, sticky="w", pady=2)
        self.nn_cloud_combobox = ttk.Combobox(nn_management_frame,
                                              values=["GoogleDrive", "Dropbox", "OneDrive", "None"],
                                              state="readonly")
        self.nn_cloud_combobox.grid(row=2, column=1, sticky="ew", pady=2)
        self.nn_cloud_combobox.set("None") # Default to no cloud association

        ttk.Button(nn_management_frame, text="Загрузить Нейросеть (Концепт)", command=self._upload_neural_network).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(nn_management_frame, text="Активировать НС", command=lambda: self._toggle_nn_status(True)).grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(nn_management_frame, text="Деактивировать НС", command=lambda: self._toggle_nn_status(False)).grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(nn_management_frame, text="Удалить НС", command=self._delete_neural_network).grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

        # Deep Clean button and output
        ttk.Separator(nn_management_frame, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(nn_management_frame, text="Запустить Глубокую Очистку (Концепт)", command=self._run_deep_clean).grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

        ttk.Label(nn_management_frame, text="Журнал Автоматизации:", font=("Arial", 10, "bold")).grid(row=9, column=0, columnspan=2, sticky="w", pady=5)
        self.automation_log_text = tk.Text(nn_management_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 9), height=10)
        self.automation_log_text.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.automation_log_text.config(state="disabled")

        # Critical warning for user NNs
        nn_warning_label = ttk.Label(nn_management_frame, text=(
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ (Хаос и Безумие): ⚠️\n"
            "Загрузка пользовательских нейросетей предоставляет полный контроль над вашими файлами в облаке. "
            "Это может привести к необратимому удалению или изменению данных. "
            "Принцип Пациента Зеро: 'сломаешь - установишь заново программу и войдешь в профиль все просто. Все восстановится из облака что было сохранено'. "
            "Ответственность полностью на вас. Убедитесь, что у вас есть резервные копии в облаке."
        ), font=("Arial", 9, "bold"), wraplength=350, foreground="darkred")
        nn_warning_label.grid(row=11, column=0, columnspan=2, pady=10, sticky="ew")


    def _populate_user_nn_tree(self):
        """Populates the NN treeview with current user NN configurations for the active user."""
        for iid in self.nn_tree.get_children():
            self.nn_tree.delete(iid)

        # For demonstration, we'll use a hardcoded "admin_user" or the first available user.
        # In a real app, this would be the currently logged-in user.
        current_user_id = next(iter(self.user_roles.keys()), "default_user") # Get the first user or a dummy one
        if current_user_id == "default_user":
            return # No actual users to populate for

        if current_user_id not in self.user_neural_networks:
            self.user_neural_networks[current_user_id] = {"nns": {}, "active_nn": None}
            self._save_data()

        user_nns = self.user_neural_networks[current_user_id]["nns"]
        for nn_name, data in user_nns.items():
            status_str = data.get("status", "inactive").capitalize()
            cloud_str = data.get("cloud", "None")
            self.nn_tree.insert("", "end", iid=nn_name, values=(status_str, cloud_str))

    def _on_nn_select(self, event):
        """Loads selected NN's data into input fields."""
        selected_item = self.nn_tree.focus()
        if selected_item:
            nn_name = selected_item
            current_user_id = next(iter(self.user_roles.keys()), "default_user") # Demo user
            if current_user_id == "default_user": return # No user to select

            nn_data = self.user_neural_networks[current_user_id]["nns"].get(nn_name, {})

            self.nn_user_id_entry.delete(0, tk.END)
            self.nn_user_id_entry.insert(0, current_user_id) # Auto-fill current user

            self.nn_name_entry.delete(0, tk.END)
            self.nn_name_entry.insert(0, nn_name)

            self.nn_cloud_combobox.set(nn_data.get("cloud", "None"))

    def _upload_neural_network(self):
        user_id = self.nn_user_id_entry.get().strip()
        nn_name = self.nn_name_entry.get().strip()
        cloud = self.nn_cloud_combobox.get()

        if not user_id or not nn_name:
            messagebox.showwarning("Ошибка Ввода", "ID пользователя и Имя НС не могут быть пустыми.")
            return

        if user_id not in self.user_neural_networks:
            self.user_neural_networks[user_id] = {"nns": {}, "active_nn": None}

        if nn_name in self.user_neural_networks[user_id]["nns"]:
            messagebox.showwarning("Существует", f"Нейросеть '{nn_name}' уже существует для пользователя '{user_id}'.")
            return

        # Simulate file path or configuration storage
        conceptual_path = os.path.join(self.audit_data_dir, "user_nns", user_id, f"{nn_name}.config")
        os.makedirs(os.path.dirname(conceptual_path), exist_ok=True)
        with open(conceptual_path, 'w', encoding='utf-8') as f:
            f.write(f"Концептуальная конфигурация для НС: {nn_name}\nСвязанное облако: {cloud}\n")

        self.user_neural_networks[user_id]["nns"][nn_name] = {
            "status": "inactive",
            "cloud": cloud,
            "path": conceptual_path
        }
        self._save_data()
        self._populate_user_nn_tree()
        self._log_activity(user_id, f"Загружена концептуальная нейросеть '{nn_name}' для облака '{cloud}'.")
        messagebox.showinfo("Успех", f"Нейросеть '{nn_name}' загружена (концептуально) для '{user_id}'.")
        self.nn_name_entry.delete(0, tk.END) # Clear after upload

    def _toggle_nn_status(self, activate: bool):
        user_id = self.nn_user_id_entry.get().strip()
        nn_name = self.nn_name_entry.get().strip()
        if not user_id or not nn_name:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите пользователя и НС.")
            return

        if user_id not in self.user_neural_networks or nn_name not in self.user_neural_networks[user_id]["nns"]:
            messagebox.showwarning("Не Найден", f"Нейросеть '{nn_name}' не найдена для пользователя '{user_id}'.")
            return

        status = "active" if activate else "inactive"
        self.user_neural_networks[user_id]["nns"][nn_name]["status"] = status

        if activate:
            # Deactivate any other active NN for this user, only one can be active at a time
            for other_nn_name, other_nn_data in self.user_neural_networks[user_id]["nns"].items():
                if other_nn_name != nn_name and other_nn_data["status"] == "active":
                    other_nn_data["status"] = "inactive"
            self.user_neural_networks[user_id]["active_nn"] = nn_name
            message = f"Нейросеть '{nn_name}' активирована для пользователя '{user_id}' и связана с {self.user_neural_networks[user_id]['nns'][nn_name]['cloud']}."
        else:
            if self.user_neural_networks[user_id]["active_nn"] == nn_name:
                self.user_neural_networks[user_id]["active_nn"] = None
            message = f"Нейросеть '{nn_name}' деактивирована для пользователя '{user_id}'."

        self._save_data()
        self._populate_user_nn_tree()
        self._log_activity(user_id, message)
        messagebox.showinfo("Обновление Статуса", message)

    def _delete_neural_network(self):
        user_id = self.nn_user_id_entry.get().strip()
        nn_name = self.nn_name_entry.get().strip()
        if not user_id or not nn_name:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите пользователя и НС для удаления.")
            return
        if user_id not in self.user_neural_networks or nn_name not in self.user_neural_networks[user_id]["nns"]:
            messagebox.showwarning("Не Найден", f"Нейросеть '{nn_name}' не найдена для пользователя '{user_id}'.")
            return
        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить нейросеть '{nn_name}' для пользователя '{user_id}'?"):
            # Conceptual: remove the config file
            conceptual_path = self.user_neural_networks[user_id]["nns"][nn_name].get("path")
            if conceptual_path and os.path.exists(conceptual_path):
                os.remove(conceptual_path)

            del self.user_neural_networks[user_id]["nns"][nn_name]
            if self.user_neural_networks[user_id]["active_nn"] == nn_name:
                self.user_neural_networks[user_id]["active_nn"] = None
            self._save_data()
            self._populate_user_nn_tree()
            self._log_activity(user_id, f"Удалена нейросеть '{nn_name}'.")
            messagebox.showinfo("Успех", f"Нейросеть '{nn_name}' удалена (концептуально).")
            self.nn_name_entry.delete(0, tk.END)

    def _run_deep_clean(self):
        user_id = self.nn_user_id_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите пользователя для глубокой очистки.")
            return

        self.automation_log_text.config(state="normal")
        self.automation_log_text.delete("1.0", tk.END)
        self.automation_log_text.insert(tk.END, f"Инициирована глубокая очистка для пользователя: {user_id}...\n")
        self.automation_log_text.see(tk.END)

        if messagebox.askyesno("Подтверждение Глубокой Очистки",
                               f"Вы уверены, что хотите запустить глубокую очистку для пользователя '{user_id}'? "
                               "Это концептуально очистит все временные и кэшированные данные, "
                               "связанные с его активными нейросетями в облаках.\n"
                               "⚠️ Это действие НЕОБРАТИМО для концептуальных данных!"):
            self.automation_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Начало глубокой очистки...\n")
            # Simulate cleaning up temporary files and caches associated with user's NNs
            simulated_clean_files = random.randint(5, 20)
            self.automation_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Концептуально удалено {simulated_clean_files} временных файлов.\n")
            self.automation_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Концептуально очищен кэш облачных операций.\n")

            # This is where the "Patient Zero" rule about responsibility comes in for data *not* on corporate servers.
            self.automation_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Глубокая очистка завершена. "
                                                    "Помните: 'сломаешь - установишь заново программу и войдешь в профиль все просто. Все восстановится из облака что было сохранено'. "
                                                    "Ваша ответственность за личные данные.\n")
            self._log_activity(user_id, "Запущена концептуальная глубокая очистка.", "success")
            messagebox.showinfo("Глубокая Очистка", "Концептуальная глубокая очистка завершена. Проверьте журнал автоматизации.")
        else:
            self.automation_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Глубокая очистка отменена.\n")
            messagebox.showinfo("Глубокая Очистка", "Глубокая очистка отменена.")

        self.automation_log_text.config(state="disabled")

    # --- NEW: Company Management Tab ---
    def _setup_company_management_tab(self, parent_frame):
        """Sets up the UI for the Company Management tab."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Управление Концептуальными Компаниями и Пользователями", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Left side: Company list
        company_list_frame = ttk.LabelFrame(parent_frame, text="Компании", padding="10")
        company_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        company_list_frame.grid_rowconfigure(0, weight=1)
        company_list_frame.grid_columnconfigure(0, weight=1)

        self.company_tree = ttk.Treeview(company_list_frame, columns=("Company Name", "Admin User", "Resources"), show="headings")
        self.company_tree.grid(row=0, column=0, sticky="nsew")
        self.company_tree.heading("Company Name", text="Название Компании")
        self.company_tree.heading("Admin User", text="Админ Пользователь")
        self.company_tree.heading("Resources", text="Внутренние Ресурсы")
        self.company_tree.column("Company Name", width=150)
        self.company_tree.column("Admin User", width=100)
        self.company_tree.column("Resources", width=200)

        company_tree_scrollbar = ttk.Scrollbar(company_list_frame, orient="vertical", command=self.company_tree.yview)
        company_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.company_tree.config(yscrollcommand=company_tree_scrollbar.set)

        self._populate_company_tree()
        self.company_tree.bind("<<TreeviewSelect>>", self._on_company_select)

        # Right side: Company/User management within company
        company_management_controls_frame = ttk.LabelFrame(parent_frame, text="Управление Компанией / Пользователями", padding="10")
        company_management_controls_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        company_management_controls_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(company_management_controls_frame, text="ID Компании:").grid(row=0, column=0, sticky="w", pady=2)
        self.company_id_entry_mgmt = ttk.Entry(company_management_controls_frame, width=30)
        self.company_id_entry_mgmt.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(company_management_controls_frame, text="Название Компании:").grid(row=1, column=0, sticky="w", pady=2)
        self.company_name_entry_mgmt = ttk.Entry(company_management_controls_frame, width=30)
        self.company_name_entry_mgmt.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(company_management_controls_frame, text="Админ Пользователь Компании:").grid(row=2, column=0, sticky="w", pady=2)
        self.company_admin_user_entry_mgmt = ttk.Entry(company_management_controls_frame, width=30)
        self.company_admin_user_entry_mgmt.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Button(company_management_controls_frame, text="Добавить Компанию", command=self._add_company).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(company_management_controls_frame, text="Обновить Компанию", command=self._update_company).grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(company_management_controls_frame, text="Удалить Компанию", command=self._delete_company).grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

        ttk.Separator(company_management_controls_frame, orient="horizontal").grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

        # Conceptual User Management by Company Admin
        ttk.Label(company_management_controls_frame, text="Управление Пользователями Компании", font=("Arial", 11, "bold")).grid(row=7, column=0, columnspan=2, pady=5)

        ttk.Label(company_management_controls_frame, text="Пользователи этой Компании:").grid(row=8, column=0, sticky="w", pady=2)

        # Treeview for users within a selected company
        self.company_user_tree = ttk.Treeview(company_management_controls_frame, columns=("User ID", "Role", "Password Known (Company)"), show="headings")
        self.company_user_tree.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.company_user_tree.heading("User ID", text="ID Пользователя")
        self.company_user_tree.heading("Role", text="Роль")
        self.company_user_tree.heading("Password Known (Company)", text="Пароль Известен (Компания)") # Conceptual: company only knows login, not password
        self.company_user_tree.column("User ID", width=100)
        self.company_user_tree.column("Role", width=80)
        self.company_user_tree.column("Password Known (Company)", width=150)

        company_user_tree_scrollbar = ttk.Scrollbar(company_management_controls_frame, orient="vertical", command=self.company_user_tree.yview)
        company_user_tree_scrollbar.grid(row=9, column=2, sticky="ns")
        self.company_user_tree.config(yscrollcommand=company_user_tree_scrollbar.set)

        self.company_user_tree.bind("<<TreeviewSelect>>", self._on_company_user_select)

        ttk.Button(company_management_controls_frame, text="Добавить Пользователя в Компанию", command=self._add_user_to_company).grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(company_management_controls_frame, text="Удалить Пользователя из Компании", command=self._remove_user_from_company).grid(row=11, column=0, columnspan=2, pady=5, sticky="ew")

        # Conceptual Internal Resources Management
        ttk.Separator(company_management_controls_frame, orient="horizontal").grid(row=12, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(company_management_controls_frame, text="Управление Внутренними Ресурсами Компании", font=("Arial", 11, "bold")).grid(row=13, column=0, columnspan=2, pady=5)

        ttk.Label(company_management_controls_frame, text="Доступные Ресурсы:").grid(row=14, column=0, sticky="w", pady=2)
        self.company_resources_listbox = tk.Listbox(company_management_controls_frame, height=3)
        self.company_resources_listbox.grid(row=15, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Button(company_management_controls_frame, text="Добавить Ресурс", command=self._add_company_resource).grid(row=16, column=0, sticky="ew", pady=5, padx=2)
        ttk.Button(company_management_controls_frame, text="Удалить Ресурс", command=self._remove_company_resource).grid(row=16, column=1, sticky="ew", pady=5, padx=2)


    def _populate_company_tree(self):
        """Populates the company treeview with current conceptual companies."""
        for iid in self.company_tree.get_children():
            self.company_tree.delete(iid)
        for company_id, data in self.companies.items():
            resources_str = ", ".join(data.get("internal_resources", []))
            self.company_tree.insert("", "end", iid=company_id, values=(data.get("name"), data.get("admin_user_id"), resources_str))

    def _on_company_select(self, event):
        """Loads selected company's data into input fields and populates user tree."""
        selected_item = self.company_tree.focus()
        if selected_item:
            company_id = selected_item
            company_data = self.companies[company_id]
            self.company_id_entry_mgmt.delete(0, tk.END)
            self.company_id_entry_mgmt.insert(0, company_id)
            self.company_name_entry_mgmt.delete(0, tk.END)
            self.company_name_entry_mgmt.insert(0, company_data.get("name", ""))
            self.company_admin_user_entry_mgmt.delete(0, tk.END)
            self.company_admin_user_entry_mgmt.insert(0, company_data.get("admin_user_id", ""))
            self._populate_company_user_tree(company_id)
            self._populate_company_resources_listbox(company_id)
        else:
            self.company_id_entry_mgmt.delete(0, tk.END)
            self.company_name_entry_mgmt.delete(0, tk.END)
            self.company_admin_user_entry_mgmt.delete(0, tk.END)
            self._populate_company_user_tree(None) # Clear user tree
            self._populate_company_resources_listbox(None) # Clear resources

    def _add_company(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        company_name = self.company_name_entry_mgmt.get().strip()
        admin_user_id = self.company_admin_user_entry_mgmt.get().strip()

        if not company_id or not company_name or not admin_user_id:
            messagebox.showwarning("Ошибка Ввода", "ID, Название компании и ID Админа не могут быть пустыми.")
            return
        if company_id in self.companies:
            messagebox.showwarning("Существует", f"Компания с ID '{company_id}' уже существует.")
            return
        if admin_user_id not in self.user_roles or self.user_roles[admin_user_id]["role"] != "Admin":
            messagebox.showwarning("Ошибка Админа", f"Пользователь '{admin_user_id}' не найден или не имеет роли 'Admin'.")
            return

        self.companies[company_id] = {
            "name": company_name,
            "admin_user_id": admin_user_id,
            "internal_resources": [] # Initially empty
        }
        # Update admin user's company_id
        self.user_roles[admin_user_id]["company_id"] = company_id
        self._save_data()
        self._populate_company_tree()
        self._populate_user_tree() # Update user tree as admin's company might change
        self._log_activity(admin_user_id, f"Добавлена новая компания '{company_name}' (ID: {company_id}).")
        messagebox.showinfo("Успех", f"Компания '{company_id}' добавлена.")

    def _update_company(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        company_name = self.company_name_entry_mgmt.get().strip()
        admin_user_id = self.company_admin_user_entry_mgmt.get().strip()

        if not company_id or not company_name or not admin_user_id:
            messagebox.showwarning("Ошибка Ввода", "ID, Название компании и ID Админа не могут быть пустыми.")
            return
        if company_id not in self.companies:
            messagebox.showwarning("Не Найден", f"Компания с ID '{company_id}' не найдена.")
            return
        if admin_user_id not in self.user_roles or self.user_roles[admin_user_id]["role"] != "Admin":
            messagebox.showwarning("Ошибка Админа", f"Пользователь '{admin_user_id}' не найден или не имеет роли 'Admin'.")
            return

        old_admin_user_id = self.companies[company_id].get("admin_user_id")

        self.companies[company_id]["name"] = company_name
        self.companies[company_id]["admin_user_id"] = admin_user_id

        # Update user's company_id if admin user changed
        if old_admin_user_id and old_admin_user_id != admin_user_id:
            if old_admin_user_id in self.user_roles and self.user_roles[old_admin_user_id]["company_id"] == company_id:
                self.user_roles[old_admin_user_id]["company_id"] = None # Unassign from this company
            self.user_roles[admin_user_id]["company_id"] = company_id # Assign new admin to this company

        self._save_data()
        self._populate_company_tree()
        self._populate_user_tree() # Update user tree as admin's company might change
        self._log_activity(admin_user_id, f"Обновлена информация о компании '{company_id}'.")
        messagebox.showinfo("Успех", f"Компания '{company_id}' обновлена.")

    def _delete_company(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        if not company_id:
            messagebox.showwarning("Ошибка Ввода", "ID Компании не может быть пустым.")
            return
        if company_id not in self.companies:
            messagebox.showwarning("Не Найден", f"Компания с ID '{company_id}' не найдена.")
            return
        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить компанию '{company_id}'? "
                                                        "Это действие необратимо и приведет к удалению всех связанных с ней пользователей "
                                                        "и их данных, не сохраненных на локальных устройствах."):

            # Conceptual: Unassign all users from this company and delete their company-specific conceptual data
            users_to_unassign = [uid for uid, data in self.user_roles.items() if data.get("company_id") == company_id]
            for user_id in users_to_unassign:
                self.user_roles[user_id]["company_id"] = None
                # Simulate deletion of conceptual company-specific user data
                user_company_data_path = os.path.join(self.company_user_data_base_dir, user_id, company_id)
                if os.path.exists(user_company_data_path):
                    shutil.rmtree(user_company_data_path)
                    self._log_activity("system", f"Удалены концептуальные корпоративные данные пользователя '{user_id}' при удалении компании.")

            del self.companies[company_id]
            self._save_data()
            self._populate_company_tree()
            self._populate_user_tree() # Update user tree as users are unassigned
            self._populate_company_user_tree(None) # Clear company user tree
            self._log_activity("admin", f"Компания '{company_id}' удалена. Все связанные пользователи отвязаны.")
            messagebox.showinfo("Успех", f"Компания '{company_id}' удалена.")
            self.company_id_entry_mgmt.delete(0, tk.END)
            self.company_name_entry_mgmt.delete(0, tk.END)
            self.company_admin_user_entry_mgmt.delete(0, tk.END)

    def _populate_company_user_tree(self, company_id=None):
        """Populates the user treeview for the selected company."""
        for iid in self.company_user_tree.get_children():
            self.company_user_tree.delete(iid)

        if company_id is None:
            return # Clear the tree if no company selected

        for user_id, data in self.user_roles.items():
            if data.get("company_id") == company_id:
                # Conceptual: company only knows login, not actual password
                password_known_by_company = "Нет"
                self.company_user_tree.insert("", "end", iid=user_id, values=(user_id, data.get("role"), password_known_by_company))

    def _on_company_user_select(self, event):
        """Handle selection in the company's user tree (e.g., for showing details/actions)."""
        selected_item = self.company_user_tree.focus()
        if selected_item:
            user_id = selected_item
            messagebox.showinfo("Детали Пользователя Компании", f"Выбран пользователь: {user_id}\n"
                                                              f"(Концептуально, здесь могут отображаться более подробные данные о пользователе в рамках компании)")

    def _add_user_to_company(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        if not company_id or company_id not in self.companies:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите существующую компанию.")
            return

        user_id = simpledialog.askstring("Добавить Пользователя", "Введите ID пользователя для добавления в компанию:")
        if not user_id or user_id.strip() == "":
            messagebox.showwarning("Ошибка Ввода", "ID пользователя не может быть пустым.")
            return

        if user_id not in self.user_roles:
            messagebox.showwarning("Не Найден", f"Пользователь '{user_id}' не найден. Сначала создайте его через вкладку 'Пользователи и Роли'.")
            return

        if self.user_roles[user_id].get("company_id") == company_id:
            messagebox.showwarning("Уже в Компании", f"Пользователь '{user_id}' уже привязан к компании '{company_id}'.")
            return

        # Assign user to company
        self.user_roles[user_id]["company_id"] = company_id
        self._save_data()
        self._populate_company_user_tree(company_id)
        self._populate_user_tree() # Update main user tree
        self._log_activity(self.companies[company_id]["admin_user_id"], f"Пользователь '{user_id}' добавлен в компанию '{company_id}'.")
        messagebox.showinfo("Успех", f"Пользователь '{user_id}' добавлен в компанию '{company_id}'.")
        # Conceptual: Create conceptual private storage for user within the company if it doesn't exist
        company_user_private_data_path = os.path.join(self.company_user_data_base_dir, user_id, company_id)
        os.makedirs(company_user_private_data_path, exist_ok=True)
        with open(os.path.join(company_user_private_data_path, "company_private_document_unsaved.txt"), 'w', encoding='utf-8') as f:
            f.write(f"Концептуальный приватный документ пользователя {user_id} для компании {company_id} (несохраненный).\n")
        with open(os.path.join(company_user_private_data_path, "company_saved_document.txt"), 'w', encoding='utf-8') as f:
            f.write(f"Концептуальный приватный документ пользователя {user_id} для компании {company_id} (сохраненный).\n")


    def _remove_user_from_company(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        if not company_id or company_id not in self.companies:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите существующую компанию.")
            return

        selected_items = self.company_user_tree.selection()
        if not selected_items:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите пользователя для удаления из компании.")
            return
        user_id_to_remove = selected_items[0] # The iid is the user_id

        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить пользователя '{user_id_to_remove}' из компании '{company_id}'? "
                                                        "Это приведет к удалению всех его концептуальных данных, не сохраненных на локальных устройствах пользователя."):

            # Conceptual: Delete company-specific conceptual data files for this user
            user_company_data_path = os.path.join(self.company_user_data_base_dir, user_id_to_remove, company_id)
            if os.path.exists(user_company_data_path):
                # Simulate deletion of "unsaved" data
                for root, dirs, files in os.walk(user_company_data_path):
                    for file in files:
                        if "unsaved" in file.lower() or "temp" in file.lower(): # Conceptual check for unsaved files
                            os.remove(os.path.join(root, file))
                            self._log_activity("system", f"Удален несохраненный концептуальный корпоративный файл '{file}' пользователя '{user_id_to_remove}' при удалении из компании.")
                # After cleaning unsaved, remove user's conceptual company data directory if empty
                if os.path.exists(user_company_data_path) and not os.listdir(user_company_data_path):
                    os.rmdir(user_company_data_path)


            # Unassign user from company (keep user in system, just remove company link)
            if user_id_to_remove in self.user_roles:
                self.user_roles[user_id_to_remove]["company_id"] = None

            self._save_data()
            self._populate_company_user_tree(company_id)
            self._populate_user_tree() # Update main user tree
            self._log_activity(self.companies[company_id]["admin_user_id"], f"Пользователь '{user_id_to_remove}' удален из компании '{company_id}'.")
            messagebox.showinfo("Успех", f"Пользователь '{user_id_to_remove}' удален из компании '{company_id}'. "
                                        "Несохраненные корпоративные данные удалены. (Пароль — ваша ответственность).")


    def _populate_company_resources_listbox(self, company_id=None):
        self.company_resources_listbox.delete(0, tk.END)
        if company_id and company_id in self.companies:
            for resource in self.companies[company_id].get("internal_resources", []):
                self.company_resources_listbox.insert(tk.END, resource)

    def _add_company_resource(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        if not company_id or company_id not in self.companies:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите компанию для добавления ресурса.")
            return

        resource_name = simpledialog.askstring("Добавить Ресурс", "Введите название нового внутреннего ресурса:")
        if resource_name and resource_name.strip() != "":
            if resource_name in self.companies[company_id].get("internal_resources", []):
                messagebox.showwarning("Существует", "Этот ресурс уже добавлен в компанию.")
                return
            self.companies[company_id].setdefault("internal_resources", []).append(resource_name)
            self._save_data()
            self._populate_company_resources_listbox(company_id)
            self._populate_company_tree() # Refresh company tree to show updated resources
            self._log_activity(self.companies[company_id]["admin_user_id"], f"Ресурс '{resource_name}' добавлен в компанию '{company_id}'.")
            messagebox.showinfo("Успех", f"Ресурс '{resource_name}' добавлен.")
        else:
            messagebox.showwarning("Ошибка Ввода", "Название ресурса не может быть пустым.")

    def _remove_company_resource(self):
        company_id = self.company_id_entry_mgmt.get().strip()
        if not company_id or company_id not in self.companies:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите компанию для удаления ресурса.")
            return

        selected_indices = self.company_resources_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Ошибка Выбора", "Пожалуйста, выберите ресурс для удаления.")
            return

        resource_to_remove = self.company_resources_listbox.get(selected_indices[0])
        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить ресурс '{resource_to_remove}' из компании '{company_id}'?"):
            self.companies[company_id]["internal_resources"].remove(resource_to_remove)
            self._save_data()
            self._populate_company_resources_listbox(company_id)
            self._populate_company_tree() # Refresh company tree
            self._log_activity(self.companies[company_id]["admin_user_id"], f"Ресурс '{resource_to_remove}' удален из компании '{company_id}'.")
            messagebox.showinfo("Успех", f"Ресурс '{resource_to_remove}' удален.")


    def refresh_page(self):
        self._load_initial_data() # Reload all data to ensure consistency
        self._populate_user_tree()
        self._populate_mfa_user_tree()
        self._populate_user_nn_tree()
        self._populate_company_tree()
        # Ensure company user tree and resources list are cleared or re-populated if a company is selected
        selected_company_item = self.company_tree.focus()
        if selected_company_item:
            company_id = self.company_tree.item(selected_company_item, "iid")
            self._populate_company_user_tree(company_id)
            self._populate_company_resources_listbox(company_id)
        else:
            self._populate_company_user_tree(None)
            self._populate_company_resources_listbox(None)
        self._populate_activity_log_text()


# This is the function the main App will call to set up the Access Control & Audit tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    access_control_audit_page_instance = AccessControlAuditPage(frame, app_data)
    return frame, access_control_audit_page_instance.refresh_page

