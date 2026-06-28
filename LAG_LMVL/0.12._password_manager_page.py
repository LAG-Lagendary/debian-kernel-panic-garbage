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

# LAG-LMV/modules/password_manager_page.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

# Импортируем наш модуль шифрования
# Путь относительно того, как Python ищет модули (modules.encryption)
try:
    from modules.encryption.crypto_utils import CryptoUtils
except ImportError:
    # Обработка ситуации, если модуль шифрования не найден
    messagebox.showerror("Ошибка импорта", "Не удалось загрузить модуль шифрования. Проверьте путь.")
    CryptoUtils = None # Устанавливаем None, чтобы избежать ошибок при создании экземпляра

# --- Конфигурация для менеджера паролей ---
# Путь к файлу для хранения паролей (концептуально)
# В реальной системе это должно быть что-то более безопасное (например, база данных)
PASSWORDS_FILE = os.path.expanduser("~/LAG-LMV_passwords.encrypted")
MASTER_KEY = "YourReallyStrongMasterKeyHere" # !!! ВАЖНО: Никогда не храните ключ так в продакшне !!!
                                            # Он должен быть запрошен у пользователя или безопасно загружен.

class PasswordManagerPage:
    def __init__(self, parent_notebook, app_data):
        self.frame = ttk.Frame(parent_notebook)
        self.app_data = app_data
        self.crypto_utils = None

        # Инициализируем CryptoUtils, если он был успешно импортирован
        if CryptoUtils:
            try:
                self.crypto_utils = CryptoUtils(MASTER_KEY)
            except Exception as e:
                messagebox.showerror("Ошибка шифрования", f"Не удалось инициализировать CryptoUtils: {e}")
                self.crypto_utils = None # Отключаем шифрование при ошибке

        self.setup_ui()
        self.load_passwords() # Загружаем и дешифруем пароли при старте

    def setup_ui(self):
        """Настраивает пользовательский интерфейс для страницы менеджера паролей."""
        title_label = ttk.Label(self.frame, text="Менеджер Паролей", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Поле для ввода имени сервиса
        ttk.Label(self.frame, text="Сервис:").pack(pady=5)
        self.service_entry = ttk.Entry(self.frame, width=50)
        self.service_entry.pack(pady=5)

        # Поле для ввода имени пользователя
        ttk.Label(self.frame, text="Имя пользователя:").pack(pady=5)
        self.username_entry = ttk.Entry(self.frame, width=50)
        self.username_entry.pack(pady=5)

        # Поле для ввода пароля
        ttk.Label(self.frame, text="Пароль:").pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*", width=50) # Скрываем пароль
        self.password_entry.pack(pady=5)

        # Кнопки
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Сохранить Пароль", command=self.save_password).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Загрузить Пароли", command=self.load_passwords).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Очистить Поля", command=self.clear_entries).pack(side=tk.LEFT, padx=10)

        # Список для отображения паролей
        self.passwords_listbox = tk.Listbox(self.frame, width=70, height=10, font=("Arial", 10))
        self.passwords_listbox.pack(pady=10)
        self.passwords_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def save_password(self):
        """
        Сохраняет введенные данные о пароле, предварительно их зашифровав.
        """
        service = self.service_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not all([service, username, password]):
            messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля.")
            return

        if not self.crypto_utils:
            messagebox.showerror("Ошибка", "Функции шифрования недоступны.")
            return

        # Шифруем чувствительные данные
        try:
            encrypted_username = self.crypto_utils.encrypt(username)
            encrypted_password = self.crypto_utils.encrypt(password)
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", f"Не удалось зашифровать данные: {e}")
            return

        new_entry = {
            "service": service,
            "username": encrypted_username,
            "password": encrypted_password
        }

        all_passwords = self._read_encrypted_passwords() # Читаем существующие зашифрованные данные
        # Обновляем или добавляем новую запись
        updated = False
        for i, entry in enumerate(all_passwords):
            if entry.get("service") == service:
                all_passwords[i] = new_entry
                updated = True
                break
        if not updated:
            all_passwords.append(new_entry)

        self._write_encrypted_passwords(all_passwords) # Записываем зашифрованные данные обратно
        messagebox.showinfo("Сохранено", "Пароль успешно сохранен (зашифрован).")
        self.load_passwords() # Обновляем список

    def load_passwords(self):
        """
        Загружает зашифрованные данные о паролях и дешифрует их для отображения.
        """
        self.passwords_listbox.delete(0, tk.END) # Очищаем список

        if not self.crypto_utils:
            messagebox.showerror("Ошибка", "Функции дешифрования недоступны.")
            return

        all_passwords = self._read_encrypted_passwords()

        if not all_passwords:
            self.passwords_listbox.insert(tk.END, "Нет сохраненных паролей.")
            return

        for entry in all_passwords:
            # Дешифруем данные для отображения
            try:
                decrypted_username = self.crypto_utils.decrypt(entry.get("username", ""))
                # Пароль не отображаем напрямую в списке, только сервис и имя пользователя
                self.passwords_listbox.insert(tk.END, f"Сервис: {entry.get('service')}, Пользователь: {decrypted_username}")
            except Exception as e:
                self.passwords_listbox.insert(tk.END, f"Ошибка дешифрования записи для сервиса: {entry.get('service')} - {e}")

    def on_listbox_select(self, event):
        """
        Обрабатывает выбор элемента в списке, заполняя поля для редактирования/просмотра.
        """
        selected_indices = self.passwords_listbox.curselection()
        if not selected_indices:
            return

        index = selected_indices[0]
        selected_text = self.passwords_listbox.get(index)

        all_passwords = self._read_encrypted_passwords()
        if index < len(all_passwords):
            entry = all_passwords[index]
            self.service_entry.delete(0, tk.END)
            self.service_entry.insert(0, entry.get("service", ""))

            if self.crypto_utils:
                try:
                    self.username_entry.delete(0, tk.END)
                    self.username_entry.insert(0, self.crypto_utils.decrypt(entry.get("username", "")))
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, self.crypto_utils.decrypt(entry.get("password", "")))
                except Exception as e:
                    messagebox.showerror("Ошибка дешифрования", f"Не удалось дешифровать выбранную запись: {e}")
            else:
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, "Шифрование недоступно")
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, "Шифрование недоступно")


    def clear_entries(self):
        """Очищает поля ввода."""
        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def _read_encrypted_passwords(self):
        """Вспомогательная функция для чтения зашифрованных данных из файла."""
        if not os.path.exists(PASSWORDS_FILE):
            return []
        try:
            with open(PASSWORDS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    return []
                # Файл уже содержит зашифрованный JSON, его не нужно дешифровать здесь.
                # Дешифровка отдельных полей происходит в load_passwords.
                return json.loads(content)
        except json.JSONDecodeError as e:
            messagebox.showerror("Ошибка чтения файла", f"Файл паролей поврежден или имеет неверный формат JSON: {e}")
            return []
        except Exception as e:
            messagebox.showerror("Ошибка чтения файла", f"Не удалось прочитать файл паролей: {e}")
            return []

    def _write_encrypted_passwords(self, data):
        """Вспомогательная функция для записи зашифрованных данных в файл."""
        try:
            with open(PASSWORDS_FILE, 'w', encoding='utf-8') as f:
                # Записываем данные как JSON
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка записи файла", f"Не удалось записать пароли в файл: {e}")

    def refresh_method(self):
        """Метод для обновления содержимого страницы, вызываемый из основного приложения."""
        self.load_passwords()
        self.clear_entries()

# Функция setup_page, которая вызывается из LAG-LMVL.py для создания страницы
def setup_page(notebook, app_data):
    page = PasswordManagerPage(notebook, app_data)
    return page.frame, page.refresh_method

# Запуск для тестирования страницы отдельно (опционально)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Тест Менеджера Паролей")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Имитация app_data
    mock_app_data = {
        "LOG_BASE_DIR": "/tmp",
        "LATEST_INTRUSION_LOG_PATH_FILE": "/tmp/intrusion.log",
        "LATEST_CHECKLIST_REPORT_PATH_FILE": "/tmp/checklist.log",
        "status_callback": lambda s: print(f"Статус: {s}"),
        "master": root
    }

    frame, refresh = setup_page(notebook, mock_app_data)
    notebook.add(frame, text="Менеджер Паролей")

    root.mainloop()
