
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
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import json
import datetime
import secrets
import random

# Import the CryptoUtils for conceptual encryption/decryption
try:
    from modules.encryption.crypto_utils import CryptoUtils
except ImportError:
    messagebox.showerror("Ошибка импорта", "Не удалось загрузить модуль шифрования. Убедитесь, что 'modules/encryption/crypto_utils.py' существует и доступен.")
    CryptoUtils = None

# --- Концептуальный Мастер-Ключ для Демонстрации ---
# В реальной системе этот мастер-ключ управлялся бы крайне безопасно,
# возможно, был бы производным от надежной кодовой фразы или безопасно извлекался.
CONCEPTUAL_MASTER_KEY_FOR_DEMO = "ThisIsAReallyStrongDemoKeyForConceptualEncryptionOnly123!"

class DataPairingPage:
    # Принцип Пациента Зеро: "Я не вытираю попу пользователям, забыл мастер-пароль — сдохни.
    # Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные;
    # вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль,
    # потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
    # Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Пути для концептуального хранения данных спаривания и логов
        self.pairing_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pairing_data")
        self.pairing_log_file = os.path.join(self.pairing_data_dir, "pairing_log.json")
        self.paired_systems_file = os.path.join(self.pairing_data_dir, "paired_systems.json")

        os.makedirs(self.pairing_data_dir, exist_ok=True)

        self.crypto_utils = None
        if CryptoUtils:
            try:
                self.crypto_utils = CryptoUtils(CONCEPTUAL_MASTER_KEY_FOR_DEMO)
            except Exception as e:
                messagebox.showerror("Ошибка криптографии", f"Не удалось инициализировать CryptoUtils: {e}")

        self._load_initial_data()
        self._setup_ui()

    def _load_initial_data(self):
        """Загружает или инициализирует концептуальные данные спаривания и журналы."""
        if not os.path.exists(self.pairing_log_file):
            self.pairing_log = []
            self._log_pairing_activity("system", "Модуль спаривания запущен.")
        else:
            with open(self.pairing_log_file, 'r', encoding='utf-8') as f:
                self.pairing_log = json.load(f)

        if not os.path.exists(self.paired_systems_file):
            self.paired_systems = {} # Формат: {"system_id": {"name": "Система А", "type": "Fork", "last_paired": "timestamp"}}
        else:
            with open(self.paired_systems_file, 'r', encoding='utf-8') as f:
                self.paired_systems = json.load(f)

    def _save_data(self):
        """Сохраняет текущие концептуальные данные в файлы."""
        with open(self.pairing_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.pairing_log, f, indent=4, ensure_ascii=False)
        with open(self.paired_systems_file, 'w', encoding='utf-8') as f:
            json.dump(self.paired_systems, f, indent=4, ensure_ascii=False)

    def _log_pairing_activity(self, system_id, action, status="успех"):
        """Логирует концептуальную активность спаривания."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "system_id": system_id,
            "action": action,
            "status": status
        }
        self.pairing_log.append(log_entry)
        self._save_data() # Сохраняем после каждой записи

    def _setup_ui(self):
        """Настраивает элементы UI для страницы Спаривания Данных."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Ряд для блокнотов

        ttk.Label(main_frame, text="Спаривание Данных и Интероперабельность", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        self.pairing_notebook = ttk.Notebook(main_frame)
        self.pairing_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Вкладка "Спаренные Системы" ---
        self.paired_systems_frame = ttk.Frame(self.pairing_notebook, padding="10")
        self.pairing_notebook.add(self.paired_systems_frame, text="Спаренные Системы")
        self._setup_paired_systems_tab(self.paired_systems_frame)

        # --- Вкладка "Передача Данных" ---
        self.data_transfer_frame = ttk.Frame(self.pairing_notebook, padding="10")
        self.pairing_notebook.add(self.data_transfer_frame, text="Передача Данных")
        self._setup_data_transfer_tab(self.data_transfer_frame)

        # --- Вкладка "Журнал Спаривания" ---
        self.pairing_log_frame = ttk.Frame(self.pairing_notebook, padding="10")
        self.pairing_notebook.add(self.pairing_log_frame, text="Журнал Спаривания")
        self._setup_pairing_log_tab(self.pairing_log_frame)

        # Примечание от Пациента Зеро (общее для всех вкладок)
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер-пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные; "
            "вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
            "\n\n**Эту пометку нельзя удалять, и она должна оставаться неизменной во всех версиях документации.**"
            "\n\n**Важно:** Для доступа к данным в альтернативных системах, вы всегда используете СВОЙ пароль. Мы не храним его."
        ), font=("Arial", 9, "italic"), wraplength=700, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, pady=10, sticky="ew")

    def _setup_paired_systems_tab(self, parent_frame):
        """Настраивает UI для вкладки "Спаренные Системы"."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуально Спаренные Системы", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        # Список спаренных систем
        paired_tree_frame = ttk.LabelFrame(parent_frame, text="Список Систем", padding="10")
        paired_tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        paired_tree_frame.grid_rowconfigure(0, weight=1)
        paired_tree_frame.grid_columnconfigure(0, weight=1)

        self.paired_systems_tree = ttk.Treeview(paired_tree_frame, columns=("Type", "Last Paired"), show="headings")
        self.paired_systems_tree.grid(row=0, column=0, sticky="nsew")
        self.paired_systems_tree.heading("Type", text="Тип")
        self.paired_systems_tree.heading("Last Paired", text="Последнее Спаривание")
        self.paired_systems_tree.column("Type", width=100)
        self.paired_systems_tree.column("Last Paired", width=150)

        paired_systems_scrollbar = ttk.Scrollbar(paired_tree_frame, orient="vertical", command=self.paired_systems_tree.yview)
        paired_systems_scrollbar.grid(row=0, column=1, sticky="ns")
        self.paired_systems_tree.config(yscrollcommand=paired_systems_scrollbar.set)

        self._populate_paired_systems_tree()

        # Кнопки управления спариванием
        pairing_buttons_frame = ttk.Frame(parent_frame)
        pairing_buttons_frame.grid(row=2, column=0, pady=10)
        ttk.Button(pairing_buttons_frame, text="Инициировать Спаривание (Концепт)", command=self._initiate_pairing).pack(side=tk.LEFT, padx=5)
        ttk.Button(pairing_buttons_frame, text="Разорвать Спаривание", command=self._unpair_system).pack(side=tk.LEFT, padx=5)
        ttk.Button(pairing_buttons_frame, text="Обновить Список", command=self._populate_paired_systems_tree).pack(side=tk.LEFT, padx=5)

    def _populate_paired_systems_tree(self):
        """Заполняет treeview спаренных систем."""
        for iid in self.paired_systems_tree.get_children():
            self.paired_systems_tree.delete(iid)
        for system_id, data in self.paired_systems.items():
            self.paired_systems_tree.insert("", "end", iid=system_id, text=data["name"],
                                           values=(data.get("type", "N/A"), data.get("last_paired", "N/A")))

    def _initiate_pairing(self):
        """Концептуально инициирует процесс спаривания с другой системой/форком."""
        system_name = simpledialog.askstring("Инициировать Спаривание", "Введите название системы/форка для спаривания:")
        if not system_name:
            messagebox.showwarning("Отмена", "Спаривание отменено.")
            return

        system_type = simpledialog.askstring("Инициировать Спаривание", f"Введите тип системы ('Fork', 'External App', 'LAG-LMVL'):", initialvalue="Fork")
        if not system_type: system_type = "Unknown"

        user_password = simpledialog.askstring("Подтверждение", "Введите ваш МАСТЕР-ПАРОЛЬ для этой системы (НЕ будет сохранен):", show='*')
        if not user_password:
            messagebox.showwarning("Ошибка", "Для спаривания необходим ваш мастер-пароль.")
            return

        # Концептуальная имитация проверки пароля (использование CryptoUtils)
        # В реальной жизни, пароль будет использоваться для дешифрования данных, а не для "проверки" в этом модуле.
        # Здесь мы просто имитируем, что пароль "корректен" для доступа к данным.
        if self.crypto_utils:
            # Здесь мы не можем "проверить" пароль напрямую, так как у нас нет хеша от "удаленной" системы.
            # Мы просто предполагаем, что пользователь ввел свой верный мастер-пароль,
            # и этот пароль будет использоваться для дешифрования данных, полученных с другой стороны.
            messagebox.showinfo("Инициировать Спаривание", "Концептуальная проверка мастер-пароля успешна. "
                                                          "Этот пароль будет использован для доступа к данным в спаренной системе.")
        else:
            messagebox.showwarning("Ошибка криптографии", "Модуль шифрования недоступен. Концептуальное спаривание невозможно.")
            self._log_pairing_activity(system_name, "Инициировать спаривание (Ошибка CryptoUtils)", "ошибка")
            return

        system_id = hashlib.sha256(f"{system_name}{system_type}{datetime.datetime.now()}".encode()).hexdigest()

        self.paired_systems[system_id] = {
            "name": system_name,
            "type": system_type,
            "last_paired": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._save_data()
        self._populate_paired_systems_tree()
        self._log_pairing_activity(system_id, f"Инициировано спаривание с системой '{system_name}' ({system_type}).")
        messagebox.showinfo("Успех", f"Система '{system_name}' концептуально спарена.")

    def _unpair_system(self):
        """Разрывает спаривание с выбранной системой."""
        selected_items = self.paired_systems_tree.selection()
        if not selected_items:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите систему для разрыва спаривания.")
            return

        system_id = selected_items[0]
        system_name = self.paired_systems[system_id]["name"]

        if messagebox.askyesno("Подтверждение Разрыва Спаривания", f"Вы уверены, что хотите разорвать спаривание с системой '{system_name}'?"):
            del self.paired_systems[system_id]
            self._save_data()
            self._populate_paired_systems_tree()
            self._log_pairing_activity(system_id, f"Разорвано спаривание с системой '{system_name}'.")
            messagebox.showinfo("Успех", f"Спаривание с системой '{system_name}' разорвано.")

    def _setup_data_transfer_tab(self, parent_frame):
        """Настраивает UI для вкладки "Передача Данных"."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальная Передача Данных", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        transfer_controls_frame = ttk.LabelFrame(parent_frame, text="Параметры Передачи", padding="10")
        transfer_controls_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        transfer_controls_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(transfer_controls_frame, text="Система-Источник:").grid(row=0, column=0, sticky="w", pady=2)
        self.source_system_combobox = ttk.Combobox(transfer_controls_frame, values=list(self.paired_systems.keys()), state="readonly")
        self.source_system_combobox.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(transfer_controls_frame, text="Система-Назначение:").grid(row=1, column=0, sticky="w", pady=2)
        self.destination_system_combobox = ttk.Combobox(transfer_controls_frame, values=list(self.paired_systems.keys()), state="readonly")
        self.destination_system_combobox.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(transfer_controls_frame, text="Тип Данных:").grid(row=2, column=0, sticky="w", pady=2)
        self.data_type_combobox = ttk.Combobox(transfer_controls_frame, values=["Все Данные (Концепт)", "Пароли", "Заметки", "Файлы", "Журналы"], state="readonly")
        self.data_type_combobox.grid(row=2, column=1, sticky="ew", pady=2)
        self.data_type_combobox.set("Все Данные (Концепт)")

        ttk.Button(transfer_controls_frame, text="Инициировать Передачу Данных (Концепт)", command=self._initiate_data_transfer).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Label(transfer_controls_frame, text="Журнал Передачи Данных:", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", pady=5)
        self.transfer_log_text = tk.Text(transfer_controls_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 9), height=10)
        self.transfer_log_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.transfer_log_text.config(state="disabled")

        transfer_warning_label = ttk.Label(transfer_controls_frame, text=(
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: ⚠️\n"
            "Передача данных между системами может повлечь за собой потерю или повреждение, "
            "если целевая система не может корректно обрабатывать или дешифровать полученные данные. "
            "Всегда делайте резервные копии и убедитесь в совместимости систем."
        ), font=("Arial", 9, "bold"), wraplength=450, foreground="darkred")
        transfer_warning_label.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

    def _initiate_data_transfer(self):
        """Концептуально инициирует передачу данных между системами."""
        source_id = self.source_system_combobox.get()
        destination_id = self.destination_system_combobox.get()
        data_type = self.data_type_combobox.get()

        if not source_id or not destination_id or source_id == destination_id:
            messagebox.showwarning("Ошибка Ввода", "Пожалуйста, выберите разные системы-источник и систему-назначение.")
            return
        if source_id not in self.paired_systems or destination_id not in self.paired_systems:
            messagebox.showwarning("Ошибка", "Выберите спаренные системы из списка.")
            return

        # Концептуальное получение мастер-пароля для дешифрования данных из источника
        user_password = simpledialog.askstring("Подтверждение Передачи", "Введите ваш МАСТЕР-ПАРОЛЬ (НЕ будет сохранен):", show='*')
        if not user_password:
            messagebox.showwarning("Отмена", "Передача данных отменена. Мастер-пароль необходим.")
            return

        self.transfer_log_text.config(state="normal")
        self.transfer_log_text.delete("1.0", tk.END)
        self.transfer_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Начата концептуальная передача данных '{data_type}' из '{self.paired_systems[source_id]['name']}' в '{self.paired_systems[destination_id]['name']}'.\n")
        self.transfer_log_text.see(tk.END)

        try:
            # Имитация дешифрования данных из источника с помощью мастер-пароля
            if self.crypto_utils:
                # В реальной жизни: decrypted_data = self.crypto_utils.decrypt(encrypted_source_data, user_password)
                simulated_decryption_success = True
            else:
                simulated_decryption_success = False
                raise Exception("CryptoUtils не инициализирован.")

            if simulated_decryption_success:
                simulated_data_size = random.randint(10, 1000) # MB
                self.transfer_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Концептуально дешифровано {simulated_data_size} МБ данных из источника.\n")
                self.transfer_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Инициирована концептуальная передача по безопасному протоколу.\n")

                # Имитация передачи и шифрования для целевой системы
                if self.crypto_utils:
                    # В реальной жизни: encrypted_data_for_destination = self.crypto_utils.encrypt(decrypted_data, user_password)
                    simulated_encryption_success = True
                else:
                    simulated_encryption_success = False

                if simulated_encryption_success:
                    self.transfer_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Концептуальная передача и шифрование для назначения завершены. Данные доступны в целевой системе.\n")
                    self._log_pairing_activity(f"{source_id}->{destination_id}", f"Передача данных '{data_type}'", "успех")
                    messagebox.showinfo("Передача Данных", "Концептуальная передача данных завершена успешно.")
                else:
                    raise Exception("Ошибка концептуального шифрования для назначения.")
            else:
                raise Exception("Ошибка концептуального дешифрования данных из источника.")

        except Exception as e:
            self.transfer_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ОШИБКА ПЕРЕДАЧИ: {e}\n")
            self._log_pairing_activity(f"{source_id}->{destination_id}", f"Передача данных '{data_type}'", "ошибка")
            messagebox.showerror("Ошибка Передачи", f"Произошла ошибка во время концептуальной передачи данных: {e}")

        self.transfer_log_text.config(state="disabled")

    def _setup_pairing_log_tab(self, parent_frame):
        """Настраивает UI для вкладки "Журнал Спаривания"."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Журнал Активности Спаривания", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.pairing_activity_log_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10))
        self.pairing_activity_log_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        activity_log_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.pairing_activity_log_text.yview)
        activity_log_scrollbar.grid(row=1, column=1, sticky="ns")
        self.pairing_activity_log_text.config(yscrollcommand=activity_log_scrollbar.set, state="disabled")

        ttk.Button(parent_frame, text="Обновить Журнал Спаривания", command=self._populate_pairing_log_text).grid(row=2, column=0, pady=5, sticky="ew")

        self._populate_pairing_log_text()

    def _populate_pairing_log_text(self):
        """Заполняет текстовую область журнала активности спаривания."""
        self.pairing_activity_log_text.config(state="normal")
        self.pairing_activity_log_text.delete("1.0", tk.END)
        for entry in self.pairing_log:
            self.pairing_activity_log_text.insert(tk.END, f"[{entry.get('timestamp')}] Система: {entry.get('system_id')} - Действие: {entry.get('action')} (Статус: {entry.get('status')})\n")
        self.pairing_activity_log_text.see(tk.END)
        self.pairing_activity_log_text.config(state="disabled")

    def refresh_page(self):
        """Обновляет содержимое всей страницы."""
        self._load_initial_data()
        self._populate_paired_systems_tree()
        self._populate_pairing_log_text()
        # Обновляем комбобоксы источников/назначений
        self.source_system_combobox.config(values=list(self.paired_systems.keys()))
        self.destination_system_combobox.config(values=list(self.paired_systems.keys()))


# Это функция, которую будет вызывать главное приложение для настройки вкладки "Спаривание Данных"
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    data_pairing_page_instance = DataPairingPage(frame, app_data)
    return frame, data_pairing_page_instance.refresh_page
