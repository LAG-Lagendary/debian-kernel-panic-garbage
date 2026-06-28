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
from tkinter import ttk, messagebox, filedialog
import os
import datetime
import json
import secrets # For dummy key generation

class EmailPage:
    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths specific to Email Module (relative to project root)
        self.email_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "email_data")
        self.email_accounts_file = os.path.join(self.email_data_dir, "email_accounts.json")
        self.inbox_dir = os.path.join(self.email_data_dir, "inbox")
        self.sent_dir = os.path.join(self.email_data_dir, "sent")
        self.email_keys_dir = os.path.join(self.email_data_dir, "keys")
        self.email_activity_log = os.path.join(self.email_data_dir, "email_activity.log")

        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.sent_dir, exist_ok=True)
        os.makedirs(self.email_keys_dir, exist_ok=True)
        os.makedirs(self.email_data_dir, exist_ok=True)

        self.email_encryption_key = self._generate_or_load_encryption_key(os.path.join(self.email_keys_dir, "email_encryption_key.txt"), self.email_keys_dir, "Email")

        # Create dummy data if not exists
        self._initialize_dummy_data()

        self.current_selected_email_path = None # Stores path to the selected email file

        parent_frame.grid_columnconfigure(0, weight=1) # Left: Accounts and Folders
        parent_frame.grid_columnconfigure(1, weight=3) # Right: Email Viewer/Composer
        parent_frame.grid_rowconfigure(0, weight=1)

        # Left Section: Email Accounts and Folders
        sidebar_frame = ttk.LabelFrame(parent_frame, text="Учетные Записи и Папки", relief="groove", borderwidth=1)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        sidebar_frame.grid_rowconfigure(1, weight=1) # Treeview expands
        sidebar_frame.grid_columnconfigure(0, weight=1)

        self.email_tree = ttk.Treeview(sidebar_frame)
        self.email_tree.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.email_tree, orient="vertical", command=self.email_tree.yview).pack(side="right", fill="y")
        self.email_tree.config(yscrollcommand=self.email_tree.set)
        self.email_tree.bind("<<TreeviewSelect>>", self._on_email_tree_select)

        email_buttons_frame = ttk.Frame(sidebar_frame)
        email_buttons_frame.pack(pady=5)
        ttk.Button(email_buttons_frame, text="Добавить Учетную Запись (Концепт)", command=self._add_account_concept).pack(fill=tk.X, pady=2)
        ttk.Button(email_buttons_frame, text="Показать Лог Активности", command=self._show_email_activity_log).pack(fill=tk.X, pady=2)
        ttk.Button(email_buttons_frame, text="Показать Папку Ключей", command=self._show_email_keys_info).pack(fill=tk.X, pady=2)


        # Right Section: Email Viewer and Composer
        email_content_frame = ttk.LabelFrame(parent_frame, text="Просмотр и Составление Писем", relief="groove", borderwidth=1)
        email_content_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        email_content_frame.grid_columnconfigure(0, weight=1)
        email_content_frame.grid_rowconfigure(1, weight=1) # Message display expands

        # Notebook for Inbox/Sent/Compose
        self.email_notebook = ttk.Notebook(email_content_frame)
        self.email_notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.email_notebook.grid_columnconfigure(0, weight=1)
        self.email_notebook.grid_rowconfigure(0, weight=1)


        # Inbox Tab
        self.inbox_tab = ttk.Frame(self.email_notebook)
        self.email_notebook.add(self.inbox_tab, text="Входящие")
        self.inbox_display = tk.Text(self.inbox_tab, wrap="word", bg="#f8f8f8", fg="#333", relief="sunken", bd=1, font=("Arial", 11))
        self.inbox_display.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.inbox_display, orient="vertical", command=self.inbox_display.yview).pack(side="right", fill="y")
        self.inbox_display.config(yscrollcommand=self.inbox_display.set, state="disabled")

        # Sent Tab
        self.sent_tab = ttk.Frame(self.email_notebook)
        self.email_notebook.add(self.sent_tab, text="Отправленные")
        self.sent_display = tk.Text(self.sent_tab, wrap="word", bg="#f8f8f8", fg="#333", relief="sunken", bd=1, font=("Arial", 11))
        self.sent_display.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.sent_display, orient="vertical", command=self.sent_display.yview).pack(side="right", fill="y")
        self.sent_display.config(yscrollcommand=self.sent_display.set, state="disabled")

        # Compose Tab
        self.compose_tab = ttk.Frame(self.email_notebook)
        self.email_notebook.add(self.compose_tab, text="Написать")

        ttk.Label(self.compose_tab, text="От кого:").pack(pady=(5,0), padx=5, anchor="w")
        self.sender_email_entry = ttk.Entry(self.compose_tab)
        self.sender_email_entry.pack(fill=tk.X, padx=5)

        ttk.Label(self.compose_tab, text="Кому:").pack(pady=(5,0), padx=5, anchor="w")
        self.recipient_email_entry = ttk.Entry(self.compose_tab)
        self.recipient_email_entry.pack(fill=tk.X, padx=5)

        ttk.Label(self.compose_tab, text="Тема:").pack(pady=(5,0), padx=5, anchor="w")
        self.subject_entry = ttk.Entry(self.compose_tab)
        self.subject_entry.pack(fill=tk.X, padx=5)

        ttk.Label(self.compose_tab, text="Сообщение:").pack(pady=(5,0), padx=5, anchor="w")
        self.message_body_text = tk.Text(self.compose_tab, wrap="word", height=10)
        self.message_body_text.pack(expand=True, fill="both", padx=5)
        ttk.Scrollbar(self.message_body_text, orient="vertical", command=self.message_body_text.yview).pack(side="right", fill="y")
        self.message_body_text.config(yscrollcommand=self.message_body_text.set)

        self.encryption_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.compose_tab, text="Шифровать письмо (Концепт)", variable=self.encryption_var).pack(pady=(5,0), padx=5, anchor="w")

        ttk.Button(self.compose_tab, text="Отправить Письмо (Концепт)", command=self._send_email_concept).pack(pady=10)


        ttk.Button(email_content_frame, text="Обновить Почту", command=self.refresh_page).grid(row=1, column=0, pady=10)

        self.refresh_page() # Initial population

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _get_short_timestamp(self):
        return datetime.datetime.now().strftime("%H:%M")

    def _generate_or_load_encryption_key(self, key_file_path, key_dir, purpose_name):
        """Helper to generate/load encryption keys."""
        if os.path.exists(key_file_path):
            try:
                with open(key_file_path, 'r') as f:
                    key = f.read().strip()
                messagebox.showinfo("Информация о безопасности (Концептуально)", f"Загружен фиктивный ключ шифрования для {purpose_name} из:\n{key_file_path}\n"
                                                     "Это ТОЛЬКО для демонстрации и НЕ безопасно для реальных данных.")
                return key
            except Exception as e:
                messagebox.showerror("Ошибка загрузки ключа", f"Не удалось загрузить ключ шифрования для {purpose_name}: {e}")
                return None
        else:
            key = secrets.token_hex(64) # Longer key for better conceptual security (128 chars hex)
            try:
                os.makedirs(key_dir, exist_ok=True)
                with open(key_file_path, 'w', encoding='utf-8') as f:
                    f.write(key)
                messagebox.showinfo("Информация о безопасности (Концептуально)", f"Сгенерирован и сохранен новый фиктивный ключ шифрования для {purpose_name} в:\n{key_file_path}\n"
                                                     "Этот ключ ТОЛЬКО для демонстрации и НЕ безопасен для реальных данных.")
                return key
            except Exception as e:
                messagebox.showerror("Ошибка генерации ключа", f"Не удалось сохранить ключ шифрования для {purpose_name}: {e}\n"
                                                              f"Пожалуйста, убедитесь, что есть разрешения на запись в {key_dir}.")
                return None

    def _log_email_activity(self, email_type, sender, recipient, subject, status):
        """Logs email activity to a central log file."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "type": email_type, # e.g., "sent", "received"
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "status": status
        }
        try:
            with open(self.email_activity_log, 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n') # Newline for each JSON object
        except Exception as e:
            print(f"Error writing to email activity log: {e}") # Print to console, can't use messagebox

    def _initialize_dummy_data(self):
        # Dummy accounts
        if not os.path.exists(self.email_accounts_file):
            dummy_accounts = [
                {"address": "user@example.com", "provider": "ExampleMail", "type": "main"},
                {"address": "private.user@secure.com", "provider": "SecureMail", "type": "private"},
            ]
            with open(self.email_accounts_file, 'w', encoding='utf-8') as f:
                json.dump(dummy_accounts, f, indent=4, ensure_ascii=False)
            self._log_email_activity("System", "System", "N/A", "Dummy email accounts initialized.", "info")

        # Dummy inbox emails
        if not os.path.exists(os.path.join(self.inbox_dir, "Welcome_to_LAG-LMV.json")):
            welcome_email = {
                "sender": "LAG-LMV Support <support@laglmv.com>",
                "recipient": "user@example.com",
                "subject": "Добро пожаловать в LAG-LMV!",
                "timestamp": self._get_timestamp(),
                "body": "Привет! Спасибо, что используете LAG-LMV. Это демонстрация работы электронной почты."
            }
            with open(os.path.join(self.inbox_dir, "Welcome_to_LAG-LMV.json"), 'w', encoding='utf-8') as f:
                json.dump(welcome_email, f, indent=4, ensure_ascii=False)
            self._log_email_activity("received", "LAG-LMV Support", "user@example.com", "Welcome to LAG-LMV!", "success")

        # Dummy sent email
        if not os.path.exists(os.path.join(self.sent_dir, "Test_Email.json")):
            test_email = {
                "sender": "user@example.com",
                "recipient": "recipient@other.com",
                "subject": "Тестовое письмо",
                "timestamp": self._get_timestamp(),
                "body": "Это тестовое письмо, отправленное из концептуального модуля электронной почты."
            }
            with open(os.path.join(self.sent_dir, "Test_Email.json"), 'w', encoding='utf-8') as f:
                json.dump(test_email, f, indent=4, ensure_ascii=False)
            self._log_email_activity("sent", "user@example.com", "recipient@other.com", "Test Email", "success")

        if not os.path.exists(self.email_activity_log):
            with open(self.email_activity_log, 'w', encoding='utf-8') as f:
                f.write(f"[{self._get_timestamp()}] Лог активности электронной почты инициализирован.\n")


    def _populate_email_tree(self):
        for iid in self.email_tree.get_children():
            self.email_tree.delete(iid)

        # Load accounts
        accounts = []
        if os.path.exists(self.email_accounts_file):
            try:
                with open(self.email_accounts_file, 'r', encoding='utf-8') as f:
                    accounts = json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Ошибка", "Файл учетных записей почты поврежден или пуст.")
                return

        account_nodes = {}
        for account in accounts:
            acc_node = self.email_tree.insert("", "end", text=account["address"], open=True, tags=('account'))
            account_nodes[account["address"]] = acc_node

            # Inbox for this account (conceptual)
            inbox_node = self.email_tree.insert(acc_node, "end", text="Входящие", values=("inbox_folder", account["address"]))
            if os.path.exists(self.inbox_dir):
                for filename in os.listdir(self.inbox_dir):
                    if filename.endswith(".json"):
                        email_path = os.path.join(self.inbox_dir, filename)
                        try:
                            with open(email_path, 'r', encoding='utf-8') as f:
                                email_data = json.load(f)
                            # Only show emails relevant to this account (conceptual check)
                            if email_data.get("recipient") == account["address"] or account["type"] == "main": # "main" account gets all dummy inbox
                                self.email_tree.insert(inbox_node, "end", text=email_data.get("subject", "No Subject"), values=("email", "inbox", email_path))
                        except Exception as e:
                            print(f"Error loading email {filename}: {e}")

            # Sent for this account (conceptual)
            sent_node = self.email_tree.insert(acc_node, "end", text="Отправленные", values=("sent_folder", account["address"]))
            if os.path.exists(self.sent_dir):
                for filename in os.listdir(self.sent_dir):
                    if filename.endswith(".json"):
                        email_path = os.path.join(self.sent_dir, filename)
                        try:
                            with open(email_path, 'r', encoding='utf-8') as f:
                                email_data = json.load(f)
                            # Only show emails relevant to this account (conceptual check)
                            if email_data.get("sender") == account["address"] or account["type"] == "main": # "main" account gets all dummy sent
                                self.email_tree.insert(sent_node, "end", text=email_data.get("subject", "No Subject"), values=("email", "sent", email_path))
                        except Exception as e:
                            print(f"Error loading email {filename}: {e}")


        self.email_tree.tag_configure('account', font=('Arial', 10, 'bold'))

    def _on_email_tree_select(self, event):
        selected_item = self.email_tree.focus()
        if not selected_item:
            return

        item_values = self.email_tree.item(selected_item, "values")
        self.current_selected_email_path = None

        if item_values:
            item_type = item_values[0]
            if item_type == "email":
                folder_type = item_values[1] # "inbox" or "sent"
                email_path = item_values[2]
                self.current_selected_email_path = email_path
                self._display_email(folder_type, email_path)
            elif item_type.endswith("_folder"): # Inbox or Sent folder selected
                # Optionally display a summary of the folder
                self.inbox_display.config(state="normal")
                self.inbox_display.delete("1.0", tk.END)
                self.sent_display.config(state="normal")
                self.sent_display.delete("1.0", tk.END)

                folder_name = self.email_tree.item(selected_item, "text")
                self.inbox_display.insert(tk.END, f"Selected folder: {folder_name}.\nSelect an email to view its content.")
                self.sent_display.insert(tk.END, f"Selected folder: {folder_name}.\nSelect an email to view its content.")

                self.inbox_display.config(state="disabled")
                self.sent_display.config(state="disabled")

        else: # Account selected or invalid item
            self._clear_email_displays()


    def _display_email(self, folder_type, email_path):
        self._clear_email_displays()
        display_widget = self.inbox_display if folder_type == "inbox" else self.sent_display

        display_widget.config(state="normal")
        display_widget.delete("1.0", tk.END)

        try:
            with open(email_path, 'r', encoding='utf-8') as f:
                email_data = json.load(f)

            sender = email_data.get("sender", "N/A")
            recipient = email_data.get("recipient", "N/A")
            subject = email_data.get("subject", "N/A")
            timestamp = email_data.get("timestamp", "N/A")
            body = email_data.get("body", "No content.")

            # Check if email is conceptually encrypted and needs decryption
            is_encrypted = "Encrypted with " in body and self.email_encryption_key
            if is_encrypted and folder_type == "inbox":
                # Simulate decryption
                body = body.replace(f"Encrypted with {self.email_encryption_key[:5]}...: ", "")
                messagebox.showinfo("Расшифровка письма (Концепт)", "Письмо концептуально расшифровано для просмотра.")
                self._log_email_activity("decryption", "N/A", recipient, subject, "success")


            display_widget.insert(tk.END, f"От: {sender}\n")
            display_widget.insert(tk.END, f"Кому: {recipient}\n")
            display_widget.insert(tk.END, f"Тема: {subject}\n")
            display_widget.insert(tk.END, f"Дата: {timestamp}\n\n")
            display_widget.insert(tk.END, f"{body}\n")

            display_widget.see(tk.END)
            self.email_notebook.select(self.inbox_tab if folder_type == "inbox" else self.sent_tab)

        except json.JSONDecodeError:
            display_widget.insert(tk.END, "Ошибка: Файл письма поврежден или пуст.")
        except Exception as e:
            display_widget.insert(tk.END, f"Ошибка при загрузке письма: {e}")
        finally:
            display_widget.config(state="disabled")

    def _clear_email_displays(self):
        for widget in [self.inbox_display, self.sent_display, self.message_body_text]:
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            if isinstance(widget, tk.Text): # Only disable Text widgets, not Entry
                widget.config(state="disabled")

        self.sender_email_entry.delete(0, tk.END)
        self.recipient_email_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.encryption_var.set(False)

    def _send_email_concept(self):
        sender = self.sender_email_entry.get().strip()
        recipient = self.recipient_email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.message_body_text.get("1.0", tk.END).strip()
        encrypt = self.encryption_var.get()

        if not sender or not recipient or not subject or not body:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля (От кого, Кому, Тема, Сообщение).")
            return

        if encrypt and not self.email_encryption_key:
            messagebox.showerror("Ошибка", "Ключ шифрования электронной почты недоступен. Невозможно зашифровать письмо.")
            return

        messagebox.showinfo("Отправка письма (Концепт)",
                            "Инициирована концептуальная отправка письма.\n\n"
                            "В реальном приложении это потребовало бы интеграции с SMTP-сервером "
                            "и обработки отправки письма. Для шифрования потребовалась бы "
                            "реальная криптографическая реализация (например, PGP/GPG).")

        # Simulate sending/saving email
        timestamp = self._get_timestamp()

        email_body_to_save = body
        status = "sent"
        if encrypt:
            email_body_to_save = f"Encrypted with {self.email_encryption_key[:5]}...: {body}"
            status = "encrypted_sent"

        sent_email_data = {
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "timestamp": timestamp,
            "body": email_body_to_save
        }

        # Save to sent folder
        sent_filename = f"Sent_{subject}_{self._get_short_timestamp()}.json".replace(" ", "_").replace(":", "")
        sent_filepath = os.path.join(self.sent_dir, sent_filename)
        try:
            with open(sent_filepath, 'w', encoding='utf-8') as f:
                json.dump(sent_email_data, f, indent=4, ensure_ascii=False)
            self._log_email_activity("sent", sender, recipient, subject, status)
            messagebox.showinfo("Успех", "Письмо сохранено в отправленных (концептуально).")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить отправленное письмо: {e}")

        # Simulate receiving the same email in inbox (if it's to our dummy user)
        if recipient == "user@example.com":
            inbox_filename = f"Received_{subject}_{self._get_short_timestamp()}.json".replace(" ", "_").replace(":", "")
            inbox_filepath = os.path.join(self.inbox_dir, inbox_filename)
            inbox_email_data = {**sent_email_data, "sender": sender, "recipient": recipient} # Ensure sender/recipient roles are correct for inbox
            try:
                with open(inbox_filepath, 'w', encoding='utf-8') as f:
                    json.dump(inbox_email_data, f, indent=4, ensure_ascii=False)
                self._log_email_activity("received", sender, recipient, subject, "received")
            except Exception as e:
                print(f"Error simulating inbox reception: {e}") # Log to console, not critical for user

        self._clear_email_displays() # Clear composer after sending
        self.refresh_page() # Refresh treeview to show new sent/received email

    def _add_account_concept(self):
        messagebox.showinfo("Добавить Учетную Запись (Концепт)",
                            "Добавление новой учетной записи электронной почты - это концептуальная функция.\n\n"
                            "В реальном приложении это потребовало бы ввода учетных данных SMTP/IMAP, "
                            "проверки соединения и безопасного хранения этих учетных данных. "
                            "Для шифрованных аккаунтов также потребовались бы ключи PGP/GPG.")
        self._log_email_activity("Account Management", "N/A", "N/A", "Attempted conceptual account addition.", "info")

    def _show_email_activity_log(self):
        if os.path.exists(self.email_activity_log):
            try:
                with open(self.email_activity_log, 'r', encoding='utf-8') as f:
                    content = f.read()
                messagebox.showinfo("Лог Активности Электронной Почты", content)
            except Exception as e:
                messagebox.showerror("Ошибка чтения лога", f"Не удалось прочитать лог активности электронной почты: {e}")
        else:
            messagebox.showinfo("Лог Активности", "Лог активности электронной почты не найден.")
        self._log_email_activity("Log View", "N/A", "N/A", "Viewed email activity log.", "info")


    def _show_email_keys_info(self):
        messagebox.showinfo(
            "Папка Ключей (Электронная Почта)",
            f"Эта директория ({self.email_keys_dir}) концептуально предназначена для хранения "
            f"ключа шифрования, используемого для шифрования и дешифрования писем.\n\n"
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: ⚠️\n"
            "Хранение реальных ключей шифрования в файлах без надлежащей защиты "
            "и системы управления ключами ОЧЕНЬ ОПАСНО. Это приложение является "
            "лишь концептуальной демонстрацией."
        )
        self._log_email_activity("Security Info", "N/A", "N/A", "Viewed email keys folder info.", "info")

    def refresh_page(self):
        self._populate_email_tree()
        self._clear_email_displays() # Clear content areas on refresh
        # Set default sender if a dummy account exists
        accounts = []
        if os.path.exists(self.email_accounts_file):
            try:
                with open(self.email_accounts_file, 'r', encoding='utf-8') as f:
                    accounts = json.load(f)
            except json.JSONDecodeError:
                pass
        if accounts:
            self.sender_email_entry.delete(0, tk.END)
            self.sender_email_entry.insert(0, accounts[0]["address"]) # Set first dummy account as default sender


# This is the function the main App will call to set up the Email tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    email_page_instance = EmailPage(frame, app_data)
    return frame, email_page_instance.refresh_page
