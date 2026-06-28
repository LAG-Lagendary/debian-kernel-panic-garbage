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
import secrets # For dummy key generation
import time # For simulated delays

# Импорт CryptoUtils из корневого каталога modules, если нужно
# from .crypto_utils import CryptoUtils # В реальном приложении, чтобы избежать круговых зависимостей

class PaymentsPage:
    # Принцип Пациента Зеро: "Я не вытираю попу пользователям, забыл мастер пароль — сдохни.
    # Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные,
    # только вы сами должны позаботиться, как и куда их сохранить и как запомнить пароль,
    # потому что пароль — это ключ к шифрованию всего на вашем профиле. Без этого нет доступа никому."
    # Эту пометку нельзя удалять.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Концептуальные пути для данных о платежах
        self.payments_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "payments_data")
        self.providers_file = os.path.join(self.payments_data_dir, "providers.json")
        self.payment_log_file = os.path.join(self.payments_data_dir, "payment_activity.log")
        self.brokerage_accounts_file = os.path.join(self.payments_data_dir, "brokerage_accounts.json")

        os.makedirs(self.payments_data_dir, exist_ok=True)

        self._load_initial_data()
        self._setup_ui()
        self.refresh_page() # Инициализация UI

    def _load_initial_data(self):
        """Загружает или инициализирует концептуальные данные о провайдерах и их методах оплаты."""
        if not os.path.exists(self.providers_file):
            self.providers = [
                {
                    "name": "Основной Сервис LAG-LMVL",
                    "description": "Базовые функции и премиум-возможности LAG-LMVL.",
                    "available_methods": ["currency", "crypto", "stocks"],
                    "fee_currency": 0.05, # 5% комиссия за валюту
                    "fee_crypto": 0.01,   # 1% комиссия за крипту
                    "fee_stocks": 0.02,   # 2% комиссия за акции
                    "preferred_currency": "USD",
                    "preferred_crypto": "BTC"
                },
                {
                    "name": "Модуль AI Ассистента (Премиум)",
                    "description": "Дополнительные модели и более быстрые ответы.",
                    "available_methods": ["currency", "crypto"], # Не принимает акции
                    "fee_currency": 0.03,
                    "fee_crypto": 0.005,
                    "preferred_currency": "EUR",
                    "preferred_crypto": "ETH"
                },
                {
                    "name": "VPN Автоматизация (Pro)",
                    "description": "Расширенные возможности VPN и индивидуальные сервера.",
                    "available_methods": ["currency", "stocks"], # Не принимает крипту
                    "fee_currency": 0.10,
                    "fee_stocks": 0.03,
                    "preferred_currency": "USD"
                }
            ]
            with open(self.providers_file, 'w', encoding='utf-8') as f:
                json.dump(self.providers, f, indent=4, ensure_ascii=False)
        else:
            with open(self.providers_file, 'r', encoding='utf-8') as f:
                self.providers = json.load(f)

        if not os.path.exists(self.payment_log_file):
            with open(self.payment_log_file, 'w', encoding='utf-8') as f:
                f.write(f"[{self._get_timestamp()}] Журнал платежной активности инициализирован.\n")

        # Концептуальные брокерские счета (dummy data)
        if not os.path.exists(self.brokerage_accounts_file):
            self.brokerage_accounts = [
                {"name": "Brokerage_Account_A", "balance_usd": 10000, "holdings": {"AAPL": 50, "GOOG": 20}},
                {"name": "Brokerage_Account_B", "balance_usd": 5000, "holdings": {"MSFT": 30}}
            ]
            with open(self.brokerage_accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.brokerage_accounts, f, indent=4, ensure_ascii=False)
        else:
            with open(self.brokerage_accounts_file, 'r', encoding='utf-8') as f:
                self.brokerage_accounts = json.load(f)


    def _save_providers(self):
        """Сохраняет текущие данные о провайдерах."""
        with open(self.providers_file, 'w', encoding='utf-8') as f:
            json.dump(self.providers, f, indent=4, ensure_ascii=False)

    def _log_payment_activity(self, provider, method, amount, status, details=""):
        """Логирует платежную активность."""
        log_entry = {
            "timestamp": self._get_timestamp(),
            "provider": provider,
            "method": method,
            "amount": amount,
            "status": status,
            "details": details
        }
        try:
            with open(self.payment_log_file, 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"Ошибка записи в журнал платежей: {e}")

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс для страницы платежей."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        ttk.Label(main_frame, text="LAG-LMVL: Гибкие Платежи и Подписки", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Выбор провайдера
        provider_selection_frame = ttk.LabelFrame(main_frame, text="Выберите Услугу/Провайдера", padding="10")
        provider_selection_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        provider_selection_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(provider_selection_frame, text="Провайдер:").grid(row=0, column=0, sticky="w", pady=2)
        self.provider_combobox = ttk.Combobox(provider_selection_frame, values=[p["name"] for p in self.providers], state="readonly")
        self.provider_combobox.grid(row=0, column=1, sticky="ew", pady=2)
        self.provider_combobox.bind("<<ComboboxSelected>>", self._on_provider_select)
        if self.providers:
            self.provider_combobox.set(self.providers[0]["name"]) # Установить первого провайдера по умолчанию

        ttk.Label(provider_selection_frame, text="Описание:").grid(row=1, column=0, sticky="w", pady=2)
        self.provider_description_label = ttk.Label(provider_selection_frame, text="", wraplength=400)
        self.provider_description_label.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(provider_selection_frame, text="Предлагаемая цена (Концепт):").grid(row=2, column=0, sticky="w", pady=2)
        self.price_label = ttk.Label(provider_selection_frame, text="0.00 USD (Без комиссий)")
        self.price_label.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Label(provider_selection_frame, text="Сумма к оплате (Концепт):").grid(row=3, column=0, sticky="w", pady=2)
        self.amount_entry = ttk.Entry(provider_selection_frame, width=15)
        self.amount_entry.grid(row=3, column=1, sticky="w", pady=2)
        self.amount_entry.insert(0, "10.00") # Дефолтная сумма

        # Панель методов оплаты
        payment_methods_frame = ttk.LabelFrame(main_frame, text="Выберите Способ Оплаты", padding="10")
        payment_methods_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        payment_methods_frame.grid_columnconfigure(0, weight=1)
        payment_methods_frame.grid_columnconfigure(1, weight=1)
        payment_methods_frame.grid_columnconfigure(2, weight=1)

        self.currency_button = ttk.Button(payment_methods_frame, text="Оплатить Валютой", command=lambda: self._process_payment("currency"))
        self.currency_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.crypto_button = ttk.Button(payment_methods_frame, text="Оплатить Криптовалютой", command=lambda: self._process_payment("crypto"))
        self.crypto_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.stocks_button = ttk.Button(payment_methods_frame, text="Оплатить Акциями", command=lambda: self._process_payment("stocks"))
        self.stocks_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Дополнительные элементы для акций/брокерских счетов
        ttk.Label(payment_methods_frame, text="Брокерский счет (для акций):").grid(row=1, column=0, columnspan=3, sticky="w", pady=(10,2))
        self.brokerage_account_combobox = ttk.Combobox(payment_methods_frame, values=[acc["name"] for acc in self.brokerage_accounts], state="readonly")
        self.brokerage_account_combobox.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        if self.brokerage_accounts:
            self.brokerage_account_combobox.set(self.brokerage_accounts[0]["name"])

        ttk.Label(payment_methods_frame, text="Тикер акции (например, AAPL):").grid(row=3, column=0, sticky="w", pady=2)
        self.stock_ticker_entry = ttk.Entry(payment_methods_frame, width=10)
        self.stock_ticker_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(payment_methods_frame, text="Количество акций:").grid(row=3, column=2, sticky="w", pady=2)
        self.stock_quantity_entry = ttk.Entry(payment_methods_frame, width=10)
        self.stock_quantity_entry.grid(row=3, column=3, sticky="ew", padx=5, pady=2)


        # Журнал платежной активности
        ttk.Label(main_frame, text="Журнал Платежной Активности:", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=(15, 5))
        self.payment_log_text = tk.Text(main_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, height=10)
        self.payment_log_text.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        ttk.Scrollbar(self.payment_log_text, orient="vertical", command=self.payment_log_text.yview).grid(row=4, column=1, sticky="ns")
        self.payment_log_text.config(yscrollcommand=self.payment_log_text.set, state="disabled")

        ttk.Button(main_frame, text="Обновить страницу", command=self.refresh_page).grid(row=5, column=0, pady=10)

        self._on_provider_select() # Инициализация для выбранного по умолчанию провайдера

        # Примечание "Пациент Зеро"
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ (Пациент Зеро): ⚠️\n"
            "Это демонстрация концепции оплаты. Настоящие финансовые операции НЕ выполняются. "
            "LAG-LMVL не несет ответственности за любые финансовые риски. "
            "Ваши проблемы - не наши. Используйте на свой страх и риск."
        ), font=("Arial", 9, "bold"), wraplength=700, foreground="darkred")
        patient_zero_note_label.grid(row=6, column=0, pady=10, sticky="ew")


    def _on_provider_select(self, event=None):
        """Обновляет UI при выборе нового провайдера."""
        selected_provider_name = self.provider_combobox.get()
        current_provider = next((p for p in self.providers if p["name"] == selected_provider_name), None)

        if current_provider:
            self.provider_description_label.config(text=current_provider.get("description", "Нет описания."))

            # Обновление доступных методов оплаты
            self.currency_button.config(state="normal" if "currency" in current_provider["available_methods"] else "disabled")
            self.crypto_button.config(state="normal" if "crypto" in current_provider["available_methods"] else "disabled")
            self.stocks_button.config(state="normal" if "stocks" in current_provider["available_methods"] else "disabled")

            # Обновление предполагаемой цены (концептуально)
            # Примем базовую цену 100 для расчета комиссий
            base_price = 100.00
            currency_fee = current_provider.get("fee_currency", 0) * base_price
            crypto_fee = current_provider.get("fee_crypto", 0) * base_price
            stocks_fee = current_provider.get("fee_stocks", 0) * base_price

            price_info = f"{base_price:.2f} {current_provider.get('preferred_currency', 'USD')} (Концепт)"
            fees_info = []
            if "currency" in current_provider["available_methods"]:
                fees_info.append(f"Валюта: +{currency_fee:.2f}{current_provider.get('preferred_currency', 'USD')}")
            if "crypto" in current_provider["available_methods"]:
                fees_info.append(f"Крипта: +{crypto_fee:.2f}{current_provider.get('preferred_crypto', 'BTC')}")
            if "stocks" in current_provider["available_methods"]:
                fees_info.append(f"Акции: +{stocks_fee:.2f} USD")

            if fees_info:
                self.price_label.config(text=f"{price_info}\n(Примерные комиссии: {', '.join(fees_info)})")
            else:
                self.price_label.config(text=f"{price_info}\n(Нет доступных методов оплаты)")

        else:
            self.provider_description_label.config(text="Выберите провайдера из списка.")
            self.currency_button.config(state="disabled")
            self.crypto_button.config(state="disabled")
            self.stocks_button.config(state="disabled")
            self.price_label.config(text="0.00 USD (Выберите провайдера)")


    def _process_payment(self, method):
        """Концептуально обрабатывает платеж выбранным методом."""
        selected_provider_name = self.provider_combobox.get()
        current_provider = next((p for p in self.providers if p["name"] == selected_provider_name), None)

        if not current_provider:
            messagebox.showwarning("Ошибка оплаты", "Пожалуйста, выберите провайдера.")
            return

        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной.")
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, введите корректную сумму для оплаты.")
            return

        # Проверка доступности метода для данного провайдера
        if method not in current_provider["available_methods"]:
            messagebox.showerror("Метод не поддерживается", f"Провайдер '{current_provider['name']}' не поддерживает оплату через '{method}'.")
            self._log_payment_activity(selected_provider_name, method, amount, "failed", f"Метод '{method}' не поддерживается провайдером.")
            return

        # Имитация платежа
        status_message = ""
        log_status = "initiated"
        details = ""

        if method == "currency":
            status_message = (f"Концептуальная оплата {amount:.2f} {current_provider.get('preferred_currency', 'USD')} "
                              f"через валютный счет для '{selected_provider_name}'.\n"
                              "В реальном приложении это потребовало бы интеграции с платежной системой.")
            details = f"Валюта: {current_provider.get('preferred_currency', 'USD')}"
            messagebox.showinfo("Оплата Валютой", status_message)
            log_status = "success_currency"

        elif method == "crypto":
            status_message = (f"Концептуальная оплата {amount:.2f} {current_provider.get('preferred_crypto', 'BTC')} "
                              f"через криптовалютный кошелек для '{selected_provider_name}'.\n"
                              "В реальном приложении это потребовало бы генерации адреса кошелька и мониторинга блокчейна.")
            details = f"Криптовалюта: {current_provider.get('preferred_crypto', 'BTC')}"
            messagebox.showinfo("Оплата Криптовалютой", status_message)
            log_status = "success_crypto"

        elif method == "stocks":
            selected_brokerage_account = self.brokerage_account_combobox.get()
            stock_ticker = self.stock_ticker_entry.get().strip().upper()
            try:
                stock_quantity = int(self.stock_quantity_entry.get())
                if stock_quantity <= 0:
                    raise ValueError("Количество акций должно быть положительным.")
            except ValueError:
                messagebox.showwarning("Ошибка ввода", "Пожалуйста, введите корректное количество акций.")
                self.stock_quantity_entry.delete(0, tk.END)
                return

            # Проверка наличия акций на счете (концептуально)
            account_data = next((acc for acc in self.brokerage_accounts if acc["name"] == selected_brokerage_account), None)
            if not account_data or account_data.get("holdings", {}).get(stock_ticker, 0) < stock_quantity:
                messagebox.showwarning("Недостаточно акций", f"На счету '{selected_brokerage_account}' недостаточно акций '{stock_ticker}'.")
                self._log_payment_activity(selected_provider_name, method, amount, "failed", "Недостаточно акций.")
                return

            status_message = (f"Концептуальная оплата {stock_quantity} акциями '{stock_ticker}' "
                              f"с брокерского счета '{selected_brokerage_account}' для '{selected_provider_name}'.\n"
                              "Уведомляем пользователя: оплата акциями по расчету Т+2. "
                              "Ждите два дня, и сервис будет подключен.\n"
                              "В реальном приложении это потребовало бы интеграции с брокерским API.")
            details = f"Акции: {stock_quantity} {stock_ticker} с {selected_brokerage_account}. Расчет Т+2."
            messagebox.showinfo("Оплата Акциями (T+2)", status_message)
            log_status = "success_stocks_T+2"

            # Имитация обновления баланса акций (концептуально)
            account_data["holdings"][stock_ticker] -= stock_quantity
            if account_data["holdings"][stock_ticker] == 0:
                del account_data["holdings"][stock_ticker]
            with open(self.brokerage_accounts_file, 'w', encoding='utf-8') as f:
                json.dump(self.brokerage_accounts, f, indent=4, ensure_ascii=False)


        # Добавляем запись в журнал активности
        self._log_payment_activity(selected_provider_name, method, amount, log_status, details)
        self.refresh_page() # Обновить журнал и состояние

    def refresh_page(self):
        """Обновляет содержимое страницы платежей."""
        self._load_initial_data() # Перезагрузить данные на случай изменений
        self._on_provider_select() # Обновить UI в соответствии с выбранным провайдером

        self.payment_log_text.config(state="normal")
        self.payment_log_text.delete("1.0", tk.END)
        try:
            if os.path.exists(self.payment_log_file):
                with open(self.payment_log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            self.payment_log_text.insert(tk.END, f"[{entry.get('timestamp', 'N/A')}] Провайдер: {entry.get('provider', 'N/A')}, Метод: {entry.get('method', 'N/A')}, Сумма: {entry.get('amount', 'N/A')}, Статус: {entry.get('status', 'N/A')}. Детали: {entry.get('details', '')}\n")
                        except json.JSONDecodeError:
                            self.payment_log_text.insert(tk.END, f"Ошибка чтения строки лога: {line}\n")
            else:
                self.payment_log_text.insert(tk.END, "Журнал платежной активности не найден.\n")
        except Exception as e:
            self.payment_log_text.insert(tk.END, f"Ошибка при загрузке журнала платежей: {e}\n")
        finally:
            self.payment_log_text.see(tk.END)
            self.payment_log_text.config(state="disabled")

# Эта функция будет вызвана основным приложением для настройки вкладки Платежи
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    payments_page_instance = PaymentsPage(frame, app_data)
    return frame, payments_page_instance.refresh_page

