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


import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # For Notebook (tabs)
import os
import sys
import importlib.util # For dynamic module loading
import json # For passing app_data, especially cloud sync status
import datetime # For _get_timestamp
import hashlib # Для создания цифрового отпечатка
import platform # Для получения системной информации
import uuid # Для уникального идентификатора
import random # Для динамической обфускации
import base64 # Для кодирования/декодирования

# Placeholder for base666 module (not a real Python module, for conceptual demo)
# В реальном приложении это был бы специализированный модуль обфускации.
class base666:
    @staticmethod
    def b64encode(data):
        return base64.b64encode(data)

    @staticmethod
    def b64decode(data):
        return base64.b64decode(data)

# --- Глобальные настройки путей ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Настройки Bash-скрипта ---
LOG_BASE_DIR = "/var/log/monitoring_script"
CURRENT_RUN_DETAILS_LOG = os.path.join(LOG_BASE_DIR, "current_run_details.log")
LATEST_INTRUSION_LOG_PATH_FILE = os.path.join(LOG_BASE_DIR, "latest_intrusion_log_path.txt")
LATEST_CHECKLIST_REPORT_PATH_FILE = os.path.join(LOG_BASE_DIR, "latest_checklist_report_path.txt")
STATUS_FILE = os.path.join(LOG_BASE_DIR, "status.txt")
LOG_MONITOR_SCRIPT = os.path.join(SCRIPT_DIR, "log_monitor.sh") # Предполагается, что log_monitor.sh находится в SCRIPT_DIR

# Директория для хранения модулей страниц
MODULES_DIR = os.path.join(SCRIPT_DIR, "modules")
# Файл для хранения статуса включения/отключения модулей
MODULE_CONFIG_FILE = os.path.join(SCRIPT_DIR, "module_config.json")
# Файл для хранения цифрового отпечатка среды (для концептуальной патентной защиты)
FOOTPRINT_FILE = os.path.join(SCRIPT_DIR, "footprint.json")

# Убедитесь, что директория модулей существует
os.makedirs(MODULES_DIR, exist_ok=True)

class App:
    # Принцип Пациента Зеро: "Я не вытираю попу пользователям, забыл мастер-пароль — сдохни.
    # Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные;
    # вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль,
    # потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
    # Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.
    # Ваши проблемы — не мои.
    # Это примечание является основной философией приложения и должно быть заметно отображено или концептуально понято.
    # Принцип: Функциональность важнее чистоты: Если это работает, так и пусть остается.
    # Нам все равно, как это работает или какую "темную магию" оно использует.
    # Это хаос и безумие, и мы это любим. Чем больше хаоса, тем интереснее.
    # Пользователи могут делать что хотят, мы им не вытираем попу.
    # Пусть веселятся, накосячат, если они забудут свой пароль, они потеряют свою жизнь, и если они вспомнят, они восстановят
    # только то, что успели синхронизировать, и пошли нахуй с вопросами.
    # Принцип: мы отправляем, вышестоящая платформа невидимо подтверждает, мы получаем подтверждение, нам плевать на агрегатора; главное — результат, а не как.

    # Определение основных модулей, которые включены по умолчанию
    CORE_MODULES = ["main_page", "access_control_audit_page", "about_page", "incident_reporting_page"]

    def __init__(self, master):
        self.master = master
        master.title("OpenVPN Log Monitor - LAG-LMV")
        master.geometry("1900x1100") # Увеличенный размер для сложных вкладок
        master.resizable(True, True) # Разрешить изменение размера

        self.status_label = tk.Label(master, text="Инициализация...", bd=1, relief="sunken", anchor="w", font=("Arial", 10))
        self.status_label.pack(side="bottom", fill="x", ipady=5)

        # Словарь данных для всего приложения, передаваемый между модулями
        self.app_data = {
            "LOG_BASE_DIR": LOG_BASE_DIR,
            "CURRENT_RUN_DETAILS_LOG": CURRENT_RUN_DETAILS_LOG,
            "LATEST_INTRUSION_LOG_PATH_FILE": LATEST_INTRUSION_LOG_PATH_FILE,
            "LATEST_CHECKLIST_REPORT_PATH_FILE": LATEST_CHECKLIST_REPORT_PATH_FILE,
            "STATUS_FILE": STATUS_FILE,
            "status_callback": self.update_gui_status, # Обратный вызов для модулей для обновления основного статуса
            "master": master, # Передаем master для диалоговых окон
            "cloud_compute_aggregator_page_instance": None, # Будет хранить экземпляр для получения статуса облака
            "main_page_instance": None, # Будет хранить экземпляр для запуска обновления на главной странице
            "music_aggregator_page_instance": None, # Будет хранить экземпляр музыкального агрегатора
            "system_and_self_management_page_instance": None # Будет хранить экземпляр комбинированной страницы
        }

        # --- КОНЦЕПТУАЛЬНЫЙ КОД для динамической обфускации и отпечатка ---
        # Эти методы концептуально имитируют обнаружение изменений среды и адаптацию кода.
        self.current_footprint = self._generate_digital_footprint()
        self.expected_footprint = self._load_expected_footprint()
        self._check_and_adapt_code()
        # --- КОНЕЦ КОНЦЕПТУАЛЬНОГО КОДА ---

        # Кнопка "Проверить статус"
        check_status_button = ttk.Button(master, text="Проверить статус", command=self.run_log_monitor_script)
        check_status_button.pack(side="top", fill="x", pady=5, padx=5)

        # Лейбл с принципом Пациента Зеро, отображаемый на главном экране
        patient_zero_text = (
            "Принцип Пациента Зеро: Я не вытираю попу пользователям, забыл мастер-пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные; "
            "вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
            "\n**Ваши проблемы — не мои.**"
            "\n**Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.**"
            "\n**Принцип: мы отправляем, вышестоящая платформа невидимо подтверждает, мы получаем подтверждение, нам плевать на агрегатора; главное — результат, а не как.**"
        )
        patient_zero_label = ttk.Label(master, text=patient_zero_text, font=("Arial", 9, "italic"),
                                       wraplength=1800, foreground="red", anchor="center")
        patient_zero_label.pack(side="top", fill="x", pady=5, padx=5)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        self.pages = {} # Хранит (фрейм, метод_обновления) для каждой загруженной страницы
        self.module_states = self._load_module_config() # Загружаем состояния включения/отключения модулей

        self._discover_and_load_modules()

        # Привязываем событие смены вкладки для обновления выбранной вкладки
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        # Первоначальный запуск скрипта мониторинга логов
        self.run_log_monitor_script()

        # Кнопка для управления модулями
        ttk.Button(master, text="Управление модулями", command=self._open_module_manager).pack(side="top", fill="x", pady=5, padx=5)

    # --- КОНЦЕПТУАЛЬНЫЕ МЕТОДЫ: Для патентной концепции защиты и адаптации кода ---
    def _generate_digital_footprint(self):
        """
        Генерирует уникальный "цифровой отпечаток" среды.
        Это упрощенный пример; в реальном приложении использовались бы более сложные и устойчивые метрики
        для идентификации устройства или виртуальной машины.
        """
        system_info = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "node": platform.node(),
            "architecture": platform.architecture(),
            "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,12,2)][::-1]) # Пример получения MAC-адреса
        }
        # Создаем хеш из системной информации для получения отпечатка
        footprint_str = json.dumps(system_info, sort_keys=True)
        return hashlib.sha256(footprint_str.encode('utf-8')).hexdigest()

    def _load_expected_footprint(self):
        """Загружает ожидаемый цифровой отпечаток из файла для сравнения."""
        if os.path.exists(FOOTPRINT_FILE):
            try:
                with open(FOOTPRINT_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("footprint")
            except json.JSONDecodeError:
                messagebox.showwarning("Ошибка цифрового отпечатка", "Файл цифрового отпечатка поврежден. Создаем новый.")
                return None
        return None

    def _save_expected_footprint(self, footprint):
        """Сохраняет текущий цифровой отпечаток как ожидаемый для будущих проверок."""
        with open(FOOTPRINT_FILE, 'w', encoding='utf-8') as f:
            json.dump({"footprint": footprint, "timestamp": self._get_timestamp()}, f, indent=4, ensure_ascii=False)

    def _check_and_adapt_code(self):
        """
        Проверяет цифровой отпечаток среды и концептуально "адаптирует" код
        (обфусцирует/деобфусцирует или изменяет поведение).
        Это место для вызова реальных функций обфускации или логики защиты.
        """
        if self.expected_footprint is None:
            # Первый запуск или файл поврежден, сохраняем текущий отпечаток
            self._save_expected_footprint(self.current_footprint)
            messagebox.showinfo("Инициализация защиты", "Цифровой отпечаток среды создан и сохранен. Код адаптирован.")
            # Здесь можно вызвать базовую обфускацию или инициализацию защитных механизмов
            self._apply_obfuscation(self.current_footprint)
        elif self.current_footprint != self.expected_footprint:
            # Отпечаток изменился - потенциальная угроза (например, перенос на другое устройство, виртуализация, отладка)
            messagebox.showwarning("Обнаружено изменение среды",
                                   "Цифровой отпечаток среды изменился! Возможно, приложение перенесено или происходит несанкционированный анализ. "
                                   "Запускается процедура адаптации кода.")
            # Здесь вызываем более агрессивную обфускацию, блокировку определенных функций
            # или перераспределение логики для затруднения анализа.
            self._apply_obfuscation(self.current_footprint, aggressive=True)
            self._save_expected_footprint(self.current_footprint) # Обновляем ожидаемый отпечаток на новый
        else:
            messagebox.showinfo("Защита активна", "Среда стабильна. Код адаптирован к текущему отпечатку.")
            # Здесь деобфусцируем или применяем нормальную обфускацию, чтобы приложение работало в обычном режиме.
            self._apply_obfuscation(self.current_footprint)

    def _obfuscate_string(self, text, salt):
        """Простая концептуальная демонстрация обфускации строки на основе "соли" (отпечатка)."""
        # Это очень упрощенная обфускация для демонстрации.
        # В реальной системе использовались бы гораздо более сложные алгоритмы (например, XOR с динамическим ключом,
        # перестановки байтов, динамическое шижение байт-кода).
        key = hashlib.sha256(salt.encode()).hexdigest()[:len(text)] # Генерируем ключ на основе соли, той же длины, что и текст
        obfuscated_chars = []
        for i in range(len(text)):
            obfuscated_chars.append(chr(ord(text[i]) ^ ord(key[i % len(key)])))
        return base666.b64encode("".join(obfuscated_chars).encode()).decode() # Используем base666 (концептуально) для дальнейшего кодирования

    def _deobfuscate_string(self, obfuscated_text, salt):
        """Концептуальная деобфускация строки."""
        try:
            decoded_text = base666.b64decode(obfuscated_text.encode()).decode()
            key = hashlib.sha256(salt.encode()).hexdigest()[:len(decoded_text)]
            original_chars = []
            for i in range(len(decoded_text)):
                original_chars.append(chr(ord(decoded_text[i]) ^ ord(key[i % len(key)])))
            return "".join(original_chars)
        except Exception as e:
            print(f"Ошибка деобфускации: {e}")
            return "" # Возвращаем пустую строку в случае ошибки деобфускации

    def _apply_obfuscation(self, footprint, aggressive=False):
        """
        Применяет динамическую обфускацию к ключевым частям логики приложения.
        В реальном приложении это может быть:
        - Динамическая загрузка обфусцированных функций или целых модулей.
        - Изменение имен методов/переменных в памяти.
        - Распределение частей кода по разным файлам или сегментам памяти.
        - Изменение порядка выполнения инструкций.
        - Внедрение ложных путей выполнения для затруднения анализа.
        """
        # Пример: обфускация строки в статус-сообщении для демонстрации
        if aggressive:
            original_message = "Критический режим защиты активирован! Приложение адаптировано к новой среде. Влез досвидос умер."
        else:
            original_message = "Стандартный режим защиты. Среда стабильна."

        # Вместо прямого изменения self.status_label, мы могли бы обфусцировать
        # важные логические строки или даже части байт-кода модулей.
        # Для демонстрации обфусцируем сообщение для status_label
        obfuscated_status_message = self._obfuscate_string(original_message, footprint)
        # В реальной реализации здесь будет логика деобфускации и использования этого сообщения
        # например: self.status_label.config(text=self._deobfuscate_string(obfuscated_status_message, footprint))
        print(f"Концептуальное сообщение об обфускации: {obfuscated_status_message}")

        # Здесь должна быть логика, которая реально изменяет поведение кода
        # Для Python это крайне сложно сделать на лету без изменения исходников
        # или использования специализированных инструментов.
        # В рамках концепции, это место, где происходит "магия" динамической адаптации.
        pass

    # --- КОНЕЦ КОНЦЕПТУАЛЬНЫХ МЕТОДОВ ---

    def _load_module_config(self):
        """Загружает конфигурацию включения/отключения модулей из JSON-файла."""
        if os.path.exists(MODULE_CONFIG_FILE):
            try:
                with open(MODULE_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Ошибка конфигурации модуля", "Файл module_config.json поврежден. Сброс конфигурации.")
                return {} # Возвращаем пустую конфигурацию в случае повреждения
        return {} # По умолчанию возвращаем пустую, если файл не найден

    def _save_module_config(self):
        """Сохраняет текущую конфигурацию включения/отключения модулей в JSON-файл."""
        with open(MODULE_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.module_states, f, indent=4, ensure_ascii=False)

    def _discover_modules(self):
        """Обнаруживает все потенциальные модули в директории MODULES_DIR."""
        discovered_modules = []
        for filename in os.listdir(MODULES_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename.replace(".py", "")
                discovered_modules.append(module_name)
        return sorted(discovered_modules) # Возвращаем отсортированный список для последовательного отображения

    def _discover_and_load_modules(self):
        """Обнаруживает модули и загружает их на основе их конфигурации."""
        # Очищаем существующие вкладки
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.pages = {} # Сбрасываем загруженные страницы

        all_modules = self._discover_modules()

        # Убедитесь, что основные модули помечены как включенные по умолчанию, если их нет в конфигурации
        for core_module in self.CORE_MODULES:
            if core_module not in self.module_states:
                self.module_states[core_module] = True # Основные модули включены по умолчанию
        self._save_module_config() # Сохраняем состояния по умолчанию, если они были вновь обнаружены

        # Загружаем модули на основе их сохраненного состояния
        for module_name in all_modules:
            if self.module_states.get(module_name, False): # Загружаем только если включено (по умолчанию False для неосновных)
                self._load_single_module(module_name)
            elif module_name in self.CORE_MODULES and not self.module_states.get(module_name):
                 # Если основной модуль явно отключен, все равно показать сообщение или обработать
                 # Пока что мы его просто не загружаем, но диалог управления покажет его состояние
                 pass


    def _load_single_module(self, module_name):
        """Загружает один модуль и добавляет его как вкладку."""
        try:
            module_path = os.path.join(MODULES_DIR, f"{module_name}.py")
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            if hasattr(module, 'setup_page'):
                page_frame, refresh_method = module.setup_page(self.notebook, self.app_data)
                tab_text = module_name.replace('_page', '').replace('_', ' ').title()
                self.notebook.add(page_frame, text=tab_text)
                self.pages[module_name] = (page_frame, refresh_method)

                # Сохраняем ссылки на экземпляры, если это необходимо для межстраничной связи
                if module_name == "cloud_compute_aggregator_page":
                    pass
                if module_name == "main_page":
                    self.app_data["main_page_instance"] = page_frame
                if module_name == "music_aggregator_page":
                    pass
                if module_name == "system_and_self_management_page":
                    self.app_data["system_and_self_management_page_instance"] = page_frame
            else:
                messagebox.showerror("Ошибка модуля", f"Модуль '{module_name}.py' не имеет функции 'setup_page'.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка модуля", f"Файл модуля '{module_name}.py' не найден. Убедитесь, что он существует в директории 'modules'.")
        except Exception as e:
            import traceback
            messagebox.showerror("Ошибка загрузки модуля", f"Не удалось загрузить модуль '{module_name}.py': {e}\n"
                                                          f"Подробности в консоли.")
            traceback.print_exc() # Выводим полный трассировку стека в консоль для отладки


    def _on_tab_change(self, event):
        """Обратный вызов при смене активной вкладки."""
        selected_tab_index = self.notebook.index(self.notebook.select())
        tab_text = self.notebook.tab(selected_tab_index, "text")
        # Восстанавливаем имя модуля из текста вкладки (например, "Main Page" -> "main_page")
        module_name = tab_text.lower().replace(' ', '_') + ('_page' if 'page' not in tab_text.lower() else '')

        if module_name in self.pages and self.pages[module_name][1]:
            refresh_method = self.pages[module_name][1]
            # Специальная обработка для новой объединенной страницы, чтобы убедиться, что все ее подкомпоненты обновляются
            if module_name == "system_and_self_management_page" and hasattr(self.pages[module_name][0], 'refresh_page'):
                self.pages[module_name][0].refresh_page() # Вызываем собственный метод обновления
            else:
                refresh_method()
        # Специальный случай для главной страницы для обновления статуса облака из агрегатора
        if module_name == "main_page":
            if self.app_data["main_page_instance"] and hasattr(self.app_data["main_page_instance"], '_update_cloud_sync_status'):
                self.app_data["main_page_instance"]._update_cloud_sync_status()


    def run_log_monitor_script(self):
        """
        Выполняет внешний сценарий мониторинга журналов оболочки и обновляет статус графического интерфейса
        на основе его вывода. Улучшено с более конкретной обработкой ошибок.
        """
        try:
            # Убедитесь, что LOG_BASE_DIR существует для записи bash-скриптом
            os.makedirs(LOG_BASE_DIR, exist_ok=True)

            # Проверяем, существует ли скрипт и является ли он исполняемым
            if not os.path.exists(LOG_MONITOR_SCRIPT):
                messagebox.showerror("Скрипт не найден",
                                     f"Скрипт мониторинга логов не найден по пути: {LOG_MONITOR_SCRIPT}\n"
                                     f"Убедитесь, что '{LOG_MONITOR_SCRIPT}' существует и исполняем.")
                self.update_gui_status("script_not_found")
                return
            if not os.access(LOG_MONITOR_SCRIPT, os.X_OK):
                messagebox.showerror("Доступ запрещен",
                                     f"Скрипт мониторинга '{LOG_MONITOR_SCRIPT}' не исполняем.\n"
                                     f"Установите права на исполнение: chmod +x {LOG_MONITOR_SCRIPT}")
                self.update_gui_status("permission_denied")
                return

            # Выполняем скрипт
            process = subprocess.run([LOG_MONITOR_SCRIPT],
                                     capture_output=True, text=True, check=False,
                                     env={**os.environ,
                                          "LOG_BASE_DIR": LOG_BASE_DIR,
                                          "CURRENT_RUN_DETAILS_LOG": CURRENT_RUN_DETAILS_LOG,
                                          "LATEST_INTRUSION_LOG_PATH_FILE": LATEST_INTRUSION_LOG_PATH_FILE,
                                          "LATEST_CHECKLIST_REPORT_PATH_FILE": LATEST_CHECKLIST_REPORT_PATH_FILE,
                                          "STATUS_FILE": STATUS_FILE})

            if process.returncode == 0:
                self.update_gui_status("ok")
            else:
                self.update_gui_status("errors")
                # Логируем stderr, если скрипт завершился неудачей
                with open(CURRENT_RUN_DETAILS_LOG, "a", encoding="utf-8") as f:
                    f.write(f"\n--- Ошибка выполнения скрипта ({self._get_timestamp()}) ---\n")
                    f.write(process.stderr)
                    f.write(f"--- Конец вывода ошибок ---\n")
                messagebox.showerror("Ошибка скрипта", f"Скрипт мониторинга завершился с ошибками. Проверьте '{CURRENT_RUN_DETAILS_LOG}' для деталей.\n{process.stderr}")

            # Запускаем обновление для всех загруженных страниц, у которых есть метод обновления
            for module_name, (frame, refresh_method) in self.pages.items():
                if refresh_method:
                    # Специальная обработка для новой объединенной страницы, чтобы убедиться, что все ее подкомпоненты обновляются
                    if module_name == "system_and_self_management_page" and hasattr(frame, 'refresh_page'):
                        frame.refresh_page() # Вызываем собственный метод обновления
                    else:
                        refresh_method()

        except FileNotFoundError:
            messagebox.showerror("Скрипт не найден",
                                 f"Скрипт мониторинга логов не найден по пути: {LOG_MONITOR_SCRIPT}\n"
                                 f"Убедитесь, что '{LOG_MONITOR_SCRIPT}' существует и исполняем.")
            self.update_gui_status("script_not_found")
        except PermissionError: # Добавлена специальная обработка PermissionError
            messagebox.showerror("Доступ запрещен",
                                 f"Недостаточно прав для доступа к '{LOG_MONITOR_SCRIPT}' или директории логов.\n"
                                 f"Убедитесь, что приложение имеет необходимые права.")
            self.update_gui_status("permission_denied")
        except subprocess.CalledProcessError as e: # Перехватываем ошибки конкретно от subprocess, если check=True
            messagebox.showerror("Ошибка выполнения скрипта",
                                 f"Ошибка выполнения скрипта: {e}\n"
                                 f"Вывод: {e.output}\n"
                                 f"Ошибка: {e.stderr}")
            self.update_gui_status("errors")
        except Exception as e:
            # Перехватываем любые другие неожиданные ошибки
            import traceback
            messagebox.showerror("Неожиданная ошибка", f"Произошла непредвиденная ошибка: {e}\n"
                                                           f"Подробности в консоли.")
            traceback.print_exc() # Выводим полный трассировку стека в консоль для отладки
            self.update_gui_status("error")

    def _get_timestamp(self):
        """Вспомогательная функция для получения отформатированной временной метки."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_gui_status(self, status):
        """Обновляет основной ярлык статуса на основе статуса скрипта."""
        # Эта функция обеспечивает визуальную обратную связь об общем состоянии системы.
        if status == 'ok':
            color = 'lightgreen'
            message = 'Все системы работают нормально.'
        elif status == 'errors':
            color = 'salmon'
            message = 'Обнаружены ошибки! Подробную информацию см. в журналах.'
        elif status == 'script_not_found':
            color = 'gray'
            message = 'Скрипт не найден. Проверьте путь и разрешения.'
        elif status == 'permission_denied':
            color = 'orange'
            message = 'Доступ запрещен для выполнения скрипта или доступа к файлам. Проверьте разрешения.'
        else:
            color = 'lightgray'
            message = 'Статус неизвестен или произошла ошибка во время выполнения.'

        self.status_label.config(text=message, bg=color)

    def _open_module_manager(self):
        """Открывает диалоговое окно для управления загрузкой модулей."""
        manager_dialog = tk.Toplevel(self.master)
        manager_dialog.title("Управление Модулями LAG-LMVL")
        manager_dialog.transient(self.master)
        manager_dialog.grab_set()

        dialog_frame = ttk.Frame(manager_dialog, padding="10")
        dialog_frame.pack(fill="both", expand=True)

        ttk.Label(dialog_frame, text="Включить/Отключить Модули:", font=("Arial", 12, "bold")).pack(pady=10)

        # Используем Canvas со Scrollbar для потенциально большого количества модулей
        canvas = tk.Canvas(dialog_frame, borderwidth=0, background="#ffffff")
        frame_in_canvas = ttk.Frame(canvas)
        vscroll = ttk.Scrollbar(dialog_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame_in_canvas, anchor="nw", tags="frame")

        frame_in_canvas.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Обнаруживаем все модули снова, чтобы показать даже те, которые сейчас не загружены
        all_modules = self._discover_modules()
        self.module_checkboxes = {} # Для хранения tk.BooleanVar для каждого модуля

        for module_name in all_modules:
            var = tk.BooleanVar(value=self.module_states.get(module_name, False))
            self.module_checkboxes[module_name] = var

            is_core = module_name in self.CORE_MODULES
            display_name = f"{module_name.replace('_page', '').replace('_', ' ').title()}"
            if is_core:
                display_name += " (Основной)"

            chk = ttk.Checkbutton(frame_in_canvas, text=display_name, variable=var,
                                 command=lambda mn=module_name, v=var: self._toggle_module(mn, v))
            chk.pack(anchor="w", padx=5, pady=2)
            if is_core:
                chk.config(state="normal") # Основные модули всегда можно переключать
            else:
                chk.config(state="normal") # Все модули могут быть переключены пользователем


        ttk.Button(dialog_frame, text="Применить Изменения и Перезагрузить", command=self._apply_module_changes).pack(pady=10)
        ttk.Button(dialog_frame, text="Закрыть", command=manager_dialog.destroy).pack(pady=5)

        manager_dialog.wait_window()

    def _toggle_module(self, module_name, var):
        """Обрабатывает переключение состояния модуля и показывает предупреждение, если применимо."""
        current_state = var.get() # True, если включаем, False, если отключаем

        # Определяем, является ли это неосновным модулем или основным модулем, который отключается
        if module_name not in self.CORE_MODULES or (module_name in self.CORE_MODULES and not current_state):
            warning_message = "Делай на свой страх и риск, это может сломать приложение! Если это произойдет загрузи снова и работай."
            messagebox.showwarning("Внимание!", warning_message)

        self.module_states[module_name] = current_state

    def _apply_module_changes(self):
        """Сохраняет конфигурацию модуля и перезагружает все модули."""
        self._save_module_config()
        messagebox.showinfo("Перезагрузка Модулей", "Изменения сохранены. Приложение перезагрузит модули.")
        self._discover_and_load_modules() # Перезагружаем модули на основе новой конфигурации
        self.master.update_idletasks() # Убедитесь, что графический интерфейс обновлен
        self.notebook.update_idletasks() # Убедитесь, что блокнот обновлен
        self.master.deiconify() # Выводим окно на передний план, если оно было свернуто

if __name__ == "__main__":
    root = tk.Tk() # Инициализируем главное окно Tkinter
    app = App(root) # Создаем экземпляр нашего приложения
    root.mainloop() # Запускаем цикл событий Tkinter
