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
import secrets
from collections import defaultdict
import random
import time

# Импорты для шифрования
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode


class AIAssistantPage:
    # Принцип Пациента Зеро: "Я не вытираю попу пользователям, забыл мастер пароль сдохни.
    # Когда не получишь доступ обратно и никто не получит. Я не храню никакие данные,
    # только вы сами должны позаботиться, как и куда их сохранить и как запомнить пароль,
    # потому что пароль — это ключ к шифрованию всего на вашем профиле. Без этого нет доступа никому."
    # Эту пометку нельзя удалять.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths specific to AI Assistant Page and Log Monitoring
        self.ai_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai_data")
        self.conversation_logs_dir = os.path.join(self.ai_data_dir, "conversation_logs")
        self.ai_keys_dir = os.path.join(self.ai_data_dir, "keys")

        self.assistant_settings_file = os.path.join(self.ai_data_dir, "assistant_settings.json")
        self.submission_endpoints_file = os.path.join(self.ai_data_dir, "submission_endpoints.json")

        os.makedirs(self.conversation_logs_dir, exist_ok=True)
        os.makedirs(self.ai_keys_dir, exist_ok=True)
        os.makedirs(self.ai_data_dir, exist_ok=True) # Ensure base AI data dir exists

        self.ai_encryption_key = self._generate_or_load_encryption_key(os.path.join(self.ai_keys_dir, "ai_encryption_key.txt"), self.ai_keys_dir, "AI Assistant")

        self.conversation_history = defaultdict(list) # Stores history for each contact
        self.current_contact = "AI_General" # Default contact for demonstration

        self._load_settings()
        self._load_submission_endpoints()
        self._load_conversation_history() # Load previous history on startup

        self._setup_ui()
        self._update_conversation_display()


    def _generate_or_load_encryption_key(self, key_file_path, keys_dir, module_name):
        """
        Generates a new Fernet key or loads an existing one.
        In a real application, this key should be managed securely,
        e.g., derived from a user's master password, not stored directly.
        """
        if os.path.exists(key_file_path):
            with open(key_file_path, 'rb') as f:
                key = f.read()
            messagebox.showinfo("Загрузка Ключа", f"Ключ шифрования для модуля '{module_name}' загружен.")
        else:
            key = Fernet.generate_key()
            with open(key_file_path, 'wb') as f:
                f.write(key)
            messagebox.showinfo("Генерация Ключа", f"Новый ключ шифрования для модуля '{module_name}' сгенерирован и сохранен в '{keys_dir}'.")
        return Fernet(key)

    def _encrypt_message(self, message):
        """Encrypts a message using the generated key."""
        try:
            return self.ai_encryption_key.encrypt(message.encode()).decode()
        except Exception as e:
            messagebox.showerror("Ошибка Шифрования", f"Не удалось зашифровать сообщение: {e}")
            return message # Return unencrypted on error (for demo, not production)

    def _decrypt_message(self, encrypted_message):
        """Decrypts a message using the generated key."""
        try:
            return self.ai_encryption_key.decrypt(encrypted_message.encode()).decode()
        except Exception as e:
            messagebox.showerror("Ошибка Дешифрования", f"Не удалось расшифровать сообщение: {e}")
            return encrypted_message # Return encrypted on error (for demo, not production)

    def _load_settings(self):
        """Loads assistant settings from file."""
        if os.path.exists(self.assistant_settings_file):
            with open(self.assistant_settings_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "response_mode": "creative",
                "api_key_concept": "YOUR_CONCEPTUAL_API_KEY_HERE" # Conceptual API key
            }
            self._save_settings()

    def _save_settings(self):
        """Saves current assistant settings to file."""
        with open(self.assistant_settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    def _load_submission_endpoints(self):
        """Loads conceptual submission endpoints."""
        if os.path.exists(self.submission_endpoints_file):
            with open(self.submission_endpoints_file, 'r', encoding='utf-8') as f:
                self.submission_endpoints = json.load(f)
        else:
            self.submission_endpoints = [
                {"name": "General AI API (Концепт)", "url": "https://conceptual.ai/api/general", "method": "POST"},
                {"name": "Security AI API (Концепт)", "url": "https://conceptual.ai/api/security", "method": "POST"},
            ]
            self._save_submission_endpoints()

    def _save_submission_endpoints(self):
        """Saves conceptual submission endpoints."""
        with open(self.submission_endpoints_file, 'w', encoding='utf-8') as f:
            json.dump(self.submission_endpoints, f, indent=4, ensure_ascii=False)

    def _load_conversation_history(self):
        """Loads encrypted conversation history for all contacts."""
        self.conversation_history = defaultdict(list)
        for filename in os.listdir(self.conversation_logs_dir):
            if filename.endswith(".json"):
                contact_id = filename.replace(".json", "")
                filepath = os.path.join(self.conversation_logs_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                        self.conversation_history[contact_id] = logs
                except json.JSONDecodeError:
                    messagebox.showwarning("Ошибка Загрузки Истории", f"Поврежден файл истории для {contact_id}.")
                    self.conversation_history[contact_id] = [] # Reset corrupted history


    def _save_conversation_history(self, contact_id):
        """Saves encrypted conversation history for a specific contact."""
        filepath = os.path.join(self.conversation_logs_dir, f"{contact_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history[contact_id], f, indent=4, ensure_ascii=False)

    def _setup_ui(self):
        """Sets up the UI elements for the AI Assistant page."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1) # Row for conversation display

        ttk.Label(main_frame, text="LAG LMVL: ИИ-Ассистент – Ваш Хаос, Наша Автоматизация", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Input and Controls Frame
        input_controls_frame = ttk.LabelFrame(main_frame, text="Ввод и Настройки", padding="10")
        input_controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        input_controls_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_controls_frame, text="Ваш Запрос:").grid(row=0, column=0, sticky="w", pady=2)
        self.query_entry = ttk.Entry(input_controls_frame, width=60)
        self.query_entry.grid(row=0, column=1, sticky="ew", pady=2)
        self.query_entry.bind("<Return>", lambda e: self._send_query_conceptual()) # Send on Enter

        ttk.Button(input_controls_frame, text="Отправить Запрос (Концепт)", command=self._send_query_conceptual).grid(row=0, column=2, padx=5)

        ttk.Label(input_controls_frame, text="Режим Ответа:").grid(row=1, column=0, sticky="w", pady=2)
        self.response_mode_combobox = ttk.Combobox(input_controls_frame, values=["creative", "factual", "technical"], state="readonly")
        self.response_mode_combobox.grid(row=1, column=1, sticky="ew", pady=2)
        self.response_mode_combobox.set(self.settings.get("response_mode", "creative"))
        self.response_mode_combobox.bind("<<ComboboxSelected>>", self._update_settings)

        ttk.Button(input_controls_frame, text="Управление Точками Входа API (Концепт)", command=self._manage_endpoints).grid(row=2, column=0, columnspan=3, pady=5, sticky="ew")

        # Conversation Display Frame
        conversation_display_frame = ttk.LabelFrame(main_frame, text="История Разговоров", padding="10")
        conversation_display_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        conversation_display_frame.grid_columnconfigure(0, weight=1)
        conversation_display_frame.grid_rowconfigure(0, weight=1)

        self.conversation_text = tk.Text(conversation_display_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), state="disabled")
        self.conversation_text.grid(row=0, column=0, sticky="nsew")
        conversation_scrollbar = ttk.Scrollbar(conversation_display_frame, orient="vertical", command=self.conversation_text.yview)
        conversation_scrollbar.grid(row=0, column=1, sticky="ns")
        self.conversation_text.config(yscrollcommand=conversation_scrollbar.set)

        # Conceptual Contacts for AI
        ttk.Label(conversation_display_frame, text="Выбрать Концептуального AI-Контакта:").grid(row=1, column=0, sticky="w", pady=2)
        self.contact_combobox = ttk.Combobox(conversation_display_frame, values=["AI_General", "AI_Security", "AI_Financial"], state="readonly")
        self.contact_combobox.grid(row=2, column=0, sticky="ew", pady=2)
        self.contact_combobox.set(self.current_contact)
        self.contact_combobox.bind("<<ComboboxSelected>>", self._change_contact)

        ttk.Button(conversation_display_frame, text="Очистить Историю для Контакта", command=self._clear_conversation_history).grid(row=3, column=0, sticky="ew", pady=5)


        # Patient Zero and AI Philosophy Note
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ (Пациент Зеро): ⚠️\n"
            "AI-Ассистент — это лишь инструмент. Он может галлюцинировать, ошибаться и быть бесполезным. "
            "LAG LMVL не несет ответственности за любой бред, который он сгенерирует. "
            "Мне похуй. Используйте на свой страх и риск. Ваши запросы и ответы "
            "концептуально шифруются, но безопасность ваших ключей — ваша забота. "
            "Помните: 'если это работает, так и пусть остается'. Если это приведет к хаосу, "
            "тем лучше. Чем больше хаоса, тем интереснее. "
            "Пользователи идут нахуй и делают что хотят, мы им не вытираем попу."
        ), font=("Arial", 9, "bold"), wraplength=700, foreground="darkred")
        patient_zero_note_label.grid(row=3, column=0, pady=10, sticky="ew")


    def _update_settings(self, event=None):
        """Updates and saves assistant settings."""
        self.settings["response_mode"] = self.response_mode_combobox.get()
        self._save_settings()
        messagebox.showinfo("Настройки Обновлены", f"Режим ответа изменен на: {self.settings['response_mode']}.")

    def _change_contact(self, event=None):
        """Changes the current AI contact and loads its history."""
        self.current_contact = self.contact_combobox.get()
        self._update_conversation_display()
        messagebox.showinfo("Контакт Изменен", f"Теперь вы общаетесь с: {self.current_contact}.")

    def _send_query_conceptual(self):
        """Conceptually sends a query to the AI assistant and gets a response."""
        user_query = self.query_entry.get().strip()
        if not user_query:
            messagebox.showwarning("Пустой Запрос", "Пожалуйста, введите ваш запрос.")
            return

        # Encrypt user query conceptually
        encrypted_query = self._encrypt_message(user_query)

        # Simulate sending to an endpoint based on current_contact
        endpoint_url = "N/A"
        for ep in self.submission_endpoints:
            if self.current_contact.lower() in ep["name"].lower():
                endpoint_url = ep["url"]
                break
        if endpoint_url == "N/A": # Fallback
            endpoint_url = self.submission_endpoints[0]["url"] if self.submission_endpoints else "https://conceptual.ai/default"

        self._add_message_to_display("You", user_query)
        self.query_entry.delete(0, tk.END)

        # Simulate AI thinking and response
        self._add_message_to_display("AI Assistant", "Думаю...", is_ai=True)
        self.conversation_text.update_idletasks() # Refresh display
        time.sleep(random.uniform(0.5, 2.0)) # Simulate delay

        conceptual_response_prefix = ""
        if self.settings["response_mode"] == "creative":
            conceptual_response_prefix = "Творческий ответ: "
        elif self.settings["response_mode"] == "factual":
            conceptual_response_prefix = "Фактический ответ: "
        elif self.settings["response_mode"] == "technical":
            conceptual_response_prefix = "Технический ответ: "

        simulated_ai_response = f"{conceptual_response_prefix}Концептуальный ответ ИИ на ваш запрос: '{user_query}'. (Через {endpoint_url})."

        # Encrypt AI response conceptually
        encrypted_ai_response = self._encrypt_message(simulated_ai_response)

        self._add_message_to_display("AI Assistant", simulated_ai_response, is_ai=True, replace_last=True)

        # Save both encrypted query and response to history
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history[self.current_contact].append({
            "timestamp": timestamp,
            "sender": "You",
            "encrypted_message": encrypted_query
        })
        self.conversation_history[self.current_contact].append({
            "timestamp": timestamp,
            "sender": "AI Assistant",
            "encrypted_message": encrypted_ai_response
        })
        self._save_conversation_history(self.current_contact)

    def _add_message_to_display(self, sender, message, is_ai=False, replace_last=False):
        """Adds a message to the conversation display."""
        self.conversation_text.config(state="normal")
        if replace_last:
            # Remove "Думаю..." message
            last_line_index = self.conversation_text.index("end-2c linestart") # Go to start of second to last line
            self.conversation_text.delete(last_line_index, "end-1c")

        tag = "user"
        if is_ai:
            tag = "ai"

        self.conversation_text.insert(tk.END, f"{sender}: ", tag)
        self.conversation_text.insert(tk.END, f"{message}\n\n", tag)
        self.conversation_text.see(tk.END)
        self.conversation_text.config(state="disabled")

        self.conversation_text.tag_config("user", foreground="blue")
        self.conversation_text.tag_config("ai", foreground="green")

    def _clear_conversation_history(self):
        """Clears the conversation history for the current contact."""
        if messagebox.askyesno("Очистить Историю", f"Вы уверены, что хотите очистить историю разговоров с '{self.current_contact}'? "
                                                "Это действие необратимо. Помните: ваша попа — ваша, а не наша."):
            self.conversation_history[self.current_contact] = []
            self._save_conversation_history(self.current_contact)
            self._update_conversation_display()
            messagebox.showinfo("История Очищена", f"История разговоров с '{self.current_contact}' очищена.")

    def _update_conversation_display(self):
        """Refreshes the conversation display from loaded history."""
        self.conversation_text.config(state="normal")
        self.conversation_text.delete("1.0", tk.END)
        if self.current_contact in self.conversation_history:
            for entry in self.conversation_history[self.current_contact]:
                # Decrypt messages before displaying
                decrypted_message = self._decrypt_message(entry.get("encrypted_message", ""))
                sender = entry.get("sender", "Unknown")
                tag = "user" if sender == "You" else "ai"
                self.conversation_text.insert(tk.END, f"{sender}: ", tag)
                self.conversation_text.insert(tk.END, f"{decrypted_message}\n\n", tag)
        else:
            self.conversation_text.insert(tk.END, f"Начните новый разговор с {self.current_contact}.\n")
        self.conversation_text.see(tk.END)
        self.conversation_text.config(state="disabled")

        self.conversation_text.tag_config("user", foreground="blue")
        self.conversation_text.tag_config("ai", foreground="green")


    def _manage_endpoints(self):
        """Opens a dialog to manage conceptual API submission endpoints."""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Управление Точками Входа API")
        dialog.transient(self.parent_frame)
        dialog.grab_set()

        dialog_frame = ttk.Frame(dialog, padding="10")
        dialog_frame.pack(fill="both", expand=True)

        # Treeview for endpoints
        self.endpoints_tree = ttk.Treeview(dialog_frame, columns=("Name", "URL", "Method"), show="headings")
        self.endpoints_tree.pack(fill="both", expand=True, pady=5)
        self.endpoints_tree.heading("Name", text="Имя")
        self.endpoints_tree.heading("URL", text="URL")
        self.endpoints_tree.heading("Method", text="Метод")

        self.endpoints_tree.column("Name", width=150)
        self.endpoints_tree.column("URL", width=250)
        self.endpoints_tree.column("Method", width=80)

        endpoints_scrollbar = ttk.Scrollbar(dialog_frame, orient="vertical", command=self.endpoints_tree.yview)
        endpoints_scrollbar.pack(side="right", fill="y")
        self.endpoints_tree.config(yscrollcommand=endpoints_scrollbar.set)

        self._populate_endpoints_treeview()

        # Buttons for managing endpoints
        button_frame = ttk.Frame(dialog_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Добавить", command=lambda: self._show_endpoint_form_dialog()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self._delete_endpoint).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Закрыть", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()

    def _populate_endpoints_treeview(self):
        """Populates the treeview with current conceptual endpoints."""
        for iid in self.endpoints_tree.get_children():
            self.endpoints_tree.delete(iid)
        for endpoint in self.submission_endpoints:
            self.endpoints_tree.insert("", "end", values=(endpoint.get("name"), endpoint.get("url"), endpoint.get("method")))

    def _show_endpoint_form_dialog(self, endpoint_data=None):
        """Shows a dialog to add or edit an endpoint."""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Добавить/Редактировать Точку Входа API")
        dialog.transient(self.parent_frame)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill="both", expand=True)
        form_frame.grid_columnconfigure(1, weight=1)

        labels = ["Имя:", "URL:", "Метод:"]
        entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=2)
            if label_text == "Метод:":
                entry = ttk.Combobox(form_frame, values=["GET", "POST", "PUT", "DELETE"], state="readonly")
                entry.set("POST") # Default method
            else:
                entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            entries[label_text.replace(":", "")] = entry

        # If editing existing endpoint
        if endpoint_data:
            entries["Имя"].insert(0, endpoint_data.get("name", ""))
            entries["URL"].insert(0, endpoint_data.get("url", ""))
            entries["Метод"].set(endpoint_data.get("method", "POST"))

        def save_endpoint():
            name = entries["Имя"].get().strip()
            url = entries["URL"].get().strip()
            method = entries["Метод"].get().strip()

            if not name or not url or not method:
                messagebox.showwarning("Ошибка Ввода", "Все поля должны быть заполнены.")
                return

            new_endpoint = {"name": name, "url": url, "method": method}

            # Check if endpoint already exists (by name)
            found = False
            for i, ep in enumerate(self.submission_endpoints):
                if ep.get("name") == name:
                    self.submission_endpoints[i] = new_endpoint
                    found = True
                    break
            if not found:
                self.submission_endpoints.append(new_endpoint)

            self._save_submission_endpoints()
            self._populate_endpoints_treeview() # Refresh treeview
            dialog.destroy()

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Сохранить", command=save_endpoint).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        dialog.wait_window() # Keep dialog open until closed

    def _delete_endpoint(self):
        """Deletes selected endpoint from the list."""
        selected_items = self.endpoints_tree.selection()
        if not selected_items:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите адрес для удаления.")
            return

        selected_name = self.endpoints_tree.item(selected_items[0], "values")[0]
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить адрес '{selected_name}'?"):
            self.submission_endpoints = [ep for ep in self.submission_endpoints if ep.get("name") != selected_name]
            self._save_submission_endpoints()
            self._populate_endpoints_treeview() # Refresh treeview


# This is the function the main App will call to set up the AI Assistant tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    ai_assistant_page_instance = AIAssistantPage(frame, app_data)
    return frame, ai_assistant_page_instance.refresh_page
