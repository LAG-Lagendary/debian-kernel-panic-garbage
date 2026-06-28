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
import shutil
import zipfile
import datetime
import secrets
import json
from collections import defaultdict # For structuring synchronization data

# Import our encryption module, if available
try:
    from modules.encryption.crypto_utils import CryptoUtils
except ImportError:
    messagebox.showerror("Import Error", "Could not load encryption module. Please check the path.")
    CryptoUtils = None

# --- Conceptual Master Key (for demonstration) ---
# In a real system, this key should be requested from the user
# or securely obtained from PasswordManagerPage
CONCEPTUAL_MASTER_KEY = "YourSharedConceptualMasterKeyForCloudEncryption"


class CloudStorageManager:
    """
    Conceptual class for managing cloud storage, synchronization,
    and user data encryption.
    """
    def __init__(self, base_dir, master_key):
        self.base_dir = base_dir # Base directory for simulated cloud storage
        self.cloud_dirs = {
            "google_drive": os.path.join(base_dir, "GoogleDrive_Simulated"),
            "dropbox": os.path.join(base_dir, "Dropbox_Simulated"),
            "one_drive": os.path.join(base_dir, "OneDrive_Simulated"),
        }
        self.user_data_dir = os.path.join(self.base_dir, "user_profiles_encrypted")
        os.makedirs(self.user_data_dir, exist_ok=True)

        for cloud_path in self.cloud_dirs.values():
            os.makedirs(cloud_path, exist_ok=True)
            # Create a dummy "manifest" file if not exists
            dummy_manifest_path = os.path.join(cloud_path, "cloud_manifest.txt")
            if not os.path.exists(dummy_manifest_path):
                with open(dummy_manifest_path, "w") as f:
                    f.write(f"This is a simulated manifest for {os.path.basename(cloud_path)}. Do not modify.\n")

        self.crypto_utils = None
        if CryptoUtils:
            try:
                self.crypto_utils = CryptoUtils(master_key)
            except Exception as e:
                messagebox.showerror("Crypto Error", f"Failed to initialize CryptoUtils for Cloud: {e}")

    def upload_file_conceptual(self, local_path, cloud_name, user_id, encrypt=True):
        """Conceptually uploads and encrypts/decrypts a file to a simulated cloud."""
        if cloud_name not in self.cloud_dirs:
            return False, "Invalid cloud name."

        target_cloud_path = self.cloud_dirs[cloud_name]
        filename = os.path.basename(local_path)

        # Conceptual: User-specific folder within the simulated cloud
        user_cloud_path = os.path.join(target_cloud_path, user_id)
        os.makedirs(user_cloud_path, exist_ok=True)

        destination_path = os.path.join(user_cloud_path, filename)

        if encrypt and self.crypto_utils:
            encrypted_filename = f"{filename}.enc"
            encrypted_destination_path = os.path.join(user_cloud_path, encrypted_filename)
            success = self.crypto_utils.encrypt_file(local_path, encrypted_destination_path)
            if success:
                return True, f"Conceptually uploaded and encrypted to {cloud_name}/{user_id}/{encrypted_filename}"
            else:
                return False, f"Encryption failed during conceptual upload for {filename}."
        else:
            try:
                shutil.copy(local_path, destination_path)
                return True, f"Conceptually uploaded to {cloud_name}/{user_id}/{filename}"
            except Exception as e:
                return False, f"Conceptual upload failed: {e}"

    def download_file_conceptual(self, cloud_path, local_destination_dir, user_id, decrypt=True):
        """Conceptually downloads and decrypts a file from a simulated cloud."""
        # cloud_path here should be relative to the user's conceptual cloud folder
        full_cloud_path = os.path.join(self.cloud_dirs[os.path.dirname(cloud_path).split(os.sep)[0]], user_id, os.path.basename(cloud_path))

        if not os.path.exists(full_cloud_path):
            return False, "File not found in conceptual cloud."

        filename = os.path.basename(full_cloud_path)
        local_destination_path = os.path.join(local_destination_dir, filename.replace(".enc", "") if decrypt else filename)

        if decrypt and self.crypto_utils and filename.endswith(".enc"):
            success = self.crypto_utils.decrypt_file(full_cloud_path, local_destination_path)
            if success:
                return True, f"Conceptually downloaded and decrypted to {local_destination_path}"
            else:
                return False, f"Decryption failed during conceptual download for {filename}."
        else:
            try:
                shutil.copy(full_cloud_path, local_destination_path)
                return True, f"Conceptually downloaded to {local_destination_path}"
            except Exception as e:
                return False, f"Conceptual download failed: {e}"

    def list_cloud_files_conceptual(self, cloud_name, user_id):
        """Conceptually lists files for a user in a simulated cloud."""
        if cloud_name not in self.cloud_dirs:
            return []

        user_cloud_path = os.path.join(self.cloud_dirs[cloud_name], user_id)
        if not os.path.exists(user_cloud_path):
            os.makedirs(user_cloud_path, exist_ok=True)
            return [] # No files yet for this user

        files = []
        for f in os.listdir(user_cloud_path):
            if os.path.isfile(os.path.join(user_cloud_path, f)):
                files.append(f)
        return files

    def get_user_profile_data_conceptual(self, user_id, master_password):
        """
        Conceptually retrieves and decrypts user profile data from simulated encrypted storage.
        This would be used by CloudComputeAggregator to get conceptual API keys or configurations.
        """
        user_profile_file = os.path.join(self.user_data_dir, f"{user_id}.enc")
        if not os.path.exists(user_profile_file):
            return None

        if self.crypto_utils:
            try:
                with open(user_profile_file, 'rb') as f:
                    encrypted_data = f.read()

                # Use a dummy password to decrypt, in a real app this would be the user's actual master password
                decrypted_bytes = self.crypto_utils.decrypt_data(encrypted_data, master_password)
                if decrypted_bytes:
                    return json.loads(decrypted_bytes.decode('utf-8'))
                else:
                    return None # Decryption failed (wrong password or corrupted)
            except Exception as e:
                print(f"Error decrypting user profile for {user_id}: {e}")
                return None
        return None

    def save_user_profile_data_conceptual(self, user_id, data, master_password):
        """
        Conceptually encrypts and saves user profile data to simulated encrypted storage.
        """
        user_profile_file = os.path.join(self.user_data_dir, f"{user_id}.enc")

        if self.crypto_utils:
            try:
                plaintext_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
                encrypted_bytes = self.crypto_utils.encrypt_data(plaintext_bytes, master_password)
                with open(user_profile_file, 'wb') as f:
                    f.write(encrypted_bytes)
                return True
            except Exception as e:
                print(f"Error encrypting and saving user profile for {user_id}: {e}")
                return False
        return False


class CloudComputeAggregatorPage:
    # Patient Zero Principle: "I don't wipe users' asses, if you forgot your master password, die.
    # When you don't regain access, and no one else does. I don't store any data,
    # you yourselves must take care of how and where to save it and how to remember the password,
    # because the password is the key to encrypting everything on your profile. Without it, no one has access."
    # This note cannot be deleted and must remain unchanged in all document versions.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths for conceptual cloud compute data storage
        self.cloud_compute_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cloud_compute_data")
        self.resource_configs_dir = os.path.join(self.cloud_compute_data_dir, "resource_configs")
        self.terminal_outputs_dir = os.path.join(self.cloud_compute_data_dir, "terminal_outputs")
        self.master_keys_dir = os.path.join(self.cloud_compute_data_dir, "master_keys") # For conceptual master key storage

        os.makedirs(self.resource_configs_dir, exist_ok=True)
        os.makedirs(self.terminal_outputs_dir, exist_ok=True)
        os.makedirs(self.master_keys_dir, exist_ok=True)

        self.conceptual_master_key = CONCEPTUAL_MASTER_KEY # Use the global conceptual key for now

        # Initialize CloudStorageManager with the conceptual master key
        self.cloud_storage_manager = CloudStorageManager(
            base_dir=os.path.join(self.cloud_compute_data_dir, "simulated_clouds"),
            master_key=self.conceptual_master_key
        )

        self._load_conceptual_data()
        self._setup_ui()

        self.current_selected_compute_path = None # Store path of selected resource config file

    def _load_conceptual_data(self):
        """Loads conceptual compute resource configurations."""
        self.compute_resources = {}
        for filename in os.listdir(self.resource_configs_dir):
            if filename.endswith(".json"):
                resource_id = filename.replace(".json", "")
                filepath = os.path.join(self.resource_configs_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        self.compute_resources[resource_id] = config
                except json.JSONDecodeError:
                    messagebox.showwarning("Config Load Error", f"Corrupted config file for {resource_id}.")
                    self.compute_resources[resource_id] = {} # Reset corrupted config

    def _save_conceptual_data(self):
        """Saves current conceptual compute resource configurations."""
        for resource_id, config in self.compute_resources.items():
            filepath = os.path.join(self.resource_configs_dir, f"{resource_id}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

    def _setup_ui(self):
        """Sets up the UI elements for the Cloud Compute Aggregator page."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Row for resource list and controls

        ttk.Label(main_frame, text="LAG LMVL: Агрегатор Облачных Вычислений – Полный Контроль Над Хаосом", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Left Column: Compute Resource List
        resource_list_frame = ttk.LabelFrame(main_frame, text="Концептуальные Вычислительные Ресурсы", padding="10")
        resource_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        resource_list_frame.grid_rowconfigure(0, weight=1)
        resource_list_frame.grid_columnconfigure(0, weight=1)

        self.resource_tree = ttk.Treeview(resource_list_frame, columns=("Type", "Status", "IP/Endpoint"), show="headings")
        self.resource_tree.grid(row=0, column=0, sticky="nsew")
        self.resource_tree.heading("#0", text="Имя Ресурса")
        self.resource_tree.heading("Type", text="Тип")
        self.resource_tree.heading("Status", text="Статус")
        self.resource_tree.heading("IP/Endpoint", text="IP/Конечная Точка")
        self.resource_tree.column("Type", width=80)
        self.resource_tree.column("Status", width=80)
        self.resource_tree.column("IP/Endpoint", width=150)

        resource_tree_scrollbar = ttk.Scrollbar(resource_list_frame, orient="vertical", command=self.resource_tree.yview)
        resource_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.resource_tree.config(yscrollcommand=resource_tree_scrollbar.set)

        self.resource_tree.bind("<<TreeviewSelect>>", self._on_resource_select)

        resource_buttons_frame = ttk.Frame(resource_list_frame)
        resource_buttons_frame.grid(row=1, column=0, sticky="ew", pady=5)
        ttk.Button(resource_buttons_frame, text="Добавить Ресурс", command=self._add_resource_dialog).pack(side=tk.LEFT, padx=2, expand=True, fill="x")
        ttk.Button(resource_buttons_frame, text="Удалить Ресурс", command=self._delete_resource).pack(side=tk.LEFT, padx=2, expand=True, fill="x")
        ttk.Button(resource_buttons_frame, text="Настройки Ресурса", command=self._edit_resource_dialog).pack(side=tk.LEFT, padx=2, expand=True, fill="x")

        # Right Column: Terminal and Cloud Status
        right_column_frame = ttk.Frame(main_frame, padding="10")
        right_column_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        right_column_frame.grid_columnconfigure(0, weight=1)
        right_column_frame.grid_rowconfigure(2, weight=1) # Row for terminal output

        # Cloud Status Section
        cloud_status_frame = ttk.LabelFrame(right_column_frame, text="Статус Облака", padding="10")
        cloud_status_frame.grid(row=0, column=0, sticky="ew", pady=5)
        cloud_status_frame.grid_columnconfigure(0, weight=1)

        self.cloud_status_text = tk.Text(cloud_status_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 9), height=5)
        self.cloud_status_text.pack(fill="both", expand=True)
        self.cloud_status_text.config(state="disabled") # Read-only
        self._update_cloud_status_display()

        # Terminal Section (Public/Non-Private)
        self.non_private_terminal_frame = ttk.LabelFrame(right_column_frame, text="Концептуальный Публичный Терминал (SSH/API)", padding="10")
        self.non_private_terminal_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        self.non_private_terminal_frame.grid_columnconfigure(0, weight=1)
        self.non_private_terminal_frame.grid_rowconfigure(1, weight=1)

        self.non_private_command_entry = ttk.Entry(self.non_private_terminal_frame, width=50, state="disabled")
        self.non_private_command_entry.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(self.non_private_terminal_frame, text="Выполнить", command=lambda: self._execute_command_conceptual(self.non_private_command_entry.get(), "non_private"), state="disabled").grid(row=0, column=1, padx=2, pady=2)

        self.non_private_text = tk.Text(self.non_private_terminal_frame, wrap="word", bg="#000", fg="#0F0", relief="sunken", bd=1, font=("Courier New", 9), height=10, state="disabled")
        self.non_private_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)

        # Terminal Section (Private/Encrypted)
        self.private_terminal_frame = ttk.LabelFrame(right_column_frame, text="Концептуальный Приватный Терминал (Зашифровано)", padding="10")
        self.private_terminal_frame.grid(row=2, column=0, sticky="nsew", pady=5)
        self.private_terminal_frame.grid_columnconfigure(0, weight=1)
        self.private_terminal_frame.grid_rowconfigure(1, weight=1)

        self.private_command_entry = ttk.Entry(self.private_terminal_frame, width=50, state="disabled")
        self.private_command_entry.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(self.private_terminal_frame, text="Выполнить (Зашифр.)", command=lambda: self._execute_command_conceptual(self.private_command_entry.get(), "private"), state="disabled").grid(row=0, column=1, padx=2, pady=2)

        self.private_text = tk.Text(self.private_terminal_frame, wrap="word", bg="#000", fg="#0F0", relief="sunken", bd=1, font=("Courier New", 9), height=10, state="disabled")
        self.private_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)

        # Patient Zero Principle Note (Common for Cloud Compute Aggregator)
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер-пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные; "
            "вы сами должны заботиться о том, как и куда их сохранять и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
            "\n\n**Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.**"
            "\n\n**LAG LMVL: Облака: 'Ваш полный контроль, наш полный похуизм.'**"
            "\n⚠️ Мы не несем ответственности за потерю данных, сбой операций или несовместимость с вашими облачными провайдерами. "
            "Если облако не видит завершенной операции, это его проблемы, а не наши. Главное — результат, а не как."
            "\nПринцип такой: отправляем, невидимо подтверждаем вышестоящей платформой, получили подтверждение, насрать на агрегатора, главное результат, а не как."
        ), font=("Arial", 9, "italic"), wraplength=1000, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

    def _populate_compute_resource_tree(self):
        """Populates the resource treeview with current conceptual compute resources."""
        for iid in self.resource_tree.get_children():
            self.resource_tree.delete(iid)
        for resource_id, config in self.compute_resources.items():
            resource_type = config.get("type", "N/A")
            status = config.get("status", "Offline")
            endpoint = config.get("ip_endpoint", "N/A")
            self.resource_tree.insert("", "end", iid=resource_id, text=resource_id, values=(resource_type, status, endpoint))

    def _on_resource_select(self, event):
        """Loads selected resource data into a conceptual terminal display."""
        selected_item = self.resource_tree.focus()
        if selected_item:
            resource_id = selected_item
            config = self.compute_resources.get(resource_id, {})
            self.current_selected_compute_path = os.path.join(self.resource_configs_dir, f"{resource_id}.json")
            self._load_terminal_content(self.current_selected_compute_path)

            # Enable terminal inputs and buttons
            self.non_private_command_entry.config(state="normal")
            self.private_command_entry.config(state="normal")
            for btn in [self.non_private_terminal_frame.winfo_children()[-1], self.private_terminal_frame.winfo_children()[-1]]:
                if isinstance(btn, ttk.Button):
                    btn.config(state="normal")
        else:
            self.current_selected_compute_path = None
            self.non_private_command_entry.config(state="disabled")
            self.private_command_entry.config(state="disabled")
            for btn in [self.non_private_terminal_frame.winfo_children()[-1], self.private_terminal_frame.winfo_children()[-1]]:
                if isinstance(btn, ttk.Button):
                    btn.config(state="disabled")
            for text_widget in [self.non_private_text, self.private_text]:
                text_widget.config(state="normal")
                text_widget.delete("1.0", tk.END)
                text_widget.insert(tk.END, "Выберите ресурс для взаимодействия с терминалом.")
                text_widget.config(state="disabled")

    def _load_terminal_content(self, config_filepath):
        """Loads conceptual terminal content for a selected resource."""
        resource_id = os.path.basename(config_filepath).replace(".json", "")
        output_file_public = os.path.join(self.terminal_outputs_dir, f"{resource_id}_public_output.log")
        output_file_private = os.path.join(self.terminal_outputs_dir, f"{resource_id}_private_output.log")

        def _load_and_display(text_widget, filepath):
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_widget.insert(tk.END, content)
                except Exception as e:
                    text_widget.insert(tk.END, f"Error loading output: {e}")
            else:
                text_widget.insert(tk.END, f"No output history for {resource_id}.\n")
            text_widget.see(tk.END)
            text_widget.config(state="disabled")

        _load_and_display(self.non_private_text, output_file_public)
        _load_and_display(self.private_text, output_file_private)


    def _execute_command_conceptual(self, command, terminal_type):
        """Simulates execution of a command on the selected conceptual resource."""
        if not self.current_selected_compute_path:
            messagebox.showwarning("Нет Ресурса", "Пожалуйста, выберите вычислительный ресурс.")
            return

        resource_id = os.path.basename(self.current_selected_compute_path).replace(".json", "")
        config = self.compute_resources.get(resource_id, {})
        resource_type = config.get("type", "N/A")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        simulated_output = ""

        if terminal_type == "non_private":
            output_file = os.path.join(self.terminal_outputs_dir, f"{resource_id}_public_output.log")
            terminal_text_widget = self.non_private_text
            simulated_output += f"[{timestamp}] PUBLIC Terminal on {resource_id} ({resource_type}): Executing '{command}'...\n"
            if "status" in command.lower():
                simulated_output += f"    > Концептуальный статус: {config.get('status', 'Unknown')}\n"
            elif "list files" in command.lower():
                simulated_output += f"    > Концептуальные файлы: file1.log, file2.data, report.txt\n"
            else:
                simulated_output += f"    > Выполнено: {command} (концептуально. Результат: Успешно)\n"
            simulated_output += f"[{timestamp}] КОНЦЕПТУАЛЬНЫЙ РЕЗУЛЬТАТ: Операция выполнена, агрегатор не важен, если подтверждено вышестоящей платформой.\n"

        elif terminal_type == "private":
            output_file = os.path.join(self.terminal_outputs_dir, f"{resource_id}_private_output.log")
            terminal_text_widget = self.private_text
            simulated_output += f"[{timestamp}] PRIVATE Terminal on {resource_id} ({resource_type}): Executing encrypted '{command}'...\n"

            # Simulate encryption/decryption of command/output
            if self.cloud_storage_manager.crypto_utils:
                try:
                    encrypted_command = self.cloud_storage_manager.crypto_utils.encrypt_data(command.encode(), self.conceptual_master_key).decode('latin-1')
                    simulated_output += f"    > Отправлено (зашифровано): {encrypted_command[:50]}...\n"

                    simulated_response = f"Simulated encrypted response for '{command}' from private resource."
                    encrypted_response = self.cloud_storage_manager.crypto_utils.encrypt_data(simulated_response.encode(), self.conceptual_master_key).decode('latin-1')
                    simulated_output += f"    > Получено (зашифровано): {encrypted_response[:50]}...\n"

                    decrypted_response = self.cloud_storage_manager.crypto_utils.decrypt_data(encrypted_response.encode('latin-1'), self.conceptual_master_key).decode('utf-8')
                    simulated_output += f"    > Расшифровано: {decrypted_response}\n"

                except Exception as e:
                    simulated_output += f"    > Ошибка шифрования/дешифрования: {e}\n"
            else:
                simulated_output += "    > Шифрование недоступно.\n"
            simulated_output += f"[{timestamp}] КОНЦЕПТУАЛЬНЫЙ РЕЗУЛЬТАТ: Операция выполнена, агрегатор не важен, если подтверждено вышестоящей платформой.\n"

        # Append to log file and display in terminal
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(simulated_output + "\n")

        terminal_text_widget.config(state="normal")
        terminal_text_widget.insert(tk.END, simulated_output + "\n")
        terminal_text_widget.see(tk.END)
        terminal_text_widget.config(state="disabled")

        # Clear command entry after execution
        if terminal_type == "non_private":
            self.non_private_command_entry.delete(0, tk.END)
        else:
            self.private_command_entry.delete(0, tk.END)


    def _update_cloud_status_display(self):
        """Updates the conceptual cloud status display."""
        self.cloud_status_text.config(state="normal")
        self.cloud_status_text.delete("1.0", tk.END)

        status_messages = []
        # Simulate checking each cloud provider status
        for cloud_name in self.cloud_storage_manager.cloud_dirs.keys():
            status = "Online" if random.random() > 0.1 else "Offline" # 90% chance of being online
            latency = f"{random.randint(10, 100)}ms"
            status_messages.append(f"• {cloud_name.replace('_', ' ').title()}: {status} (Latency: {latency})")

        connected_resources = sum(1 for res_id, cfg in self.compute_resources.items() if cfg.get("status") == "Online")
        total_resources = len(self.compute_resources)

        self.cloud_status_text.insert(tk.END, "Концептуальный статус агрегатора облачных вычислений:\n")
        for msg in status_messages:
            self.cloud_status_text.insert(tk.END, msg + "\n")
        self.cloud_status_text.insert(tk.END, f"\nПодключено ресурсов: {connected_resources}/{total_resources}")
        self.cloud_status_text.config(state="disabled")

    def _add_resource_dialog(self):
        """Opens a dialog to add a new conceptual compute resource."""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Добавить Вычислительный Ресурс")
        dialog.transient(self.parent_frame)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill="both", expand=True)
        form_frame.grid_columnconfigure(1, weight=1)

        labels = ["ID Ресурса:", "Тип (VM/Container/Server):", "Статус (Online/Offline):", "IP/Конечная Точка:"]
        entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=2)
            if "Тип" in label_text:
                entry = ttk.Combobox(form_frame, values=["VM", "Container", "Server", "Edge Device"], state="readonly")
            elif "Статус" in label_text:
                entry = ttk.Combobox(form_frame, values=["Online", "Offline", "Maintenance"], state="readonly")
            else:
                entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            entries[label_text.replace(":", "")] = entry

        entries["Статус (Online/Offline)"].set("Offline") # Default status

        def save_resource():
            resource_id = entries["ID Ресурса"].get().strip()
            resource_type = entries["Тип (VM/Container/Server)"].get().strip()
            status = entries["Статус (Online/Offline)"].get().strip()
            ip_endpoint = entries["IP/Конечная Точка"].get().strip()

            if not resource_id or not resource_type or not status or not ip_endpoint:
                messagebox.showwarning("Ошибка Ввода", "Все поля должны быть заполнены.")
                return
            if resource_id in self.compute_resources:
                messagebox.showwarning("Существует", f"Ресурс с ID '{resource_id}' уже существует.")
                return

            self.compute_resources[resource_id] = {
                "type": resource_type,
                "status": status,
                "ip_endpoint": ip_endpoint,
                "conceptual_logs": [] # To store conceptual terminal logs for this resource
            }
            self._save_conceptual_data()
            self._populate_compute_resource_tree()
            self._update_cloud_status_display()
            messagebox.showinfo("Успех", f"Ресурс '{resource_id}' добавлен.")
            dialog.destroy()

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Сохранить", command=save_resource).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()

    def _edit_resource_dialog(self):
        """Opens a dialog to edit an existing conceptual compute resource."""
        selected_item = self.resource_tree.focus()
        if not selected_item:
            messagebox.showwarning("Нет Выбора", "Пожалуйста, выберите ресурс для редактирования.")
            return

        resource_id = selected_item
        current_config = self.compute_resources.get(resource_id, {})

        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(f"Редактировать Вычислительный Ресурс: {resource_id}")
        dialog.transient(self.parent_frame)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill="both", expand=True)
        form_frame.grid_columnconfigure(1, weight=1)

        labels = ["ID Ресурса:", "Тип (VM/Container/Server):", "Статус (Online/Offline):", "IP/Конечная Точка:"]
        entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=2)
            if "Тип" in label_text:
                entry = ttk.Combobox(form_frame, values=["VM", "Container", "Server", "Edge Device"], state="readonly")
            elif "Статус" in label_text:
                entry = ttk.Combobox(form_frame, values=["Online", "Offline", "Maintenance"], state="readonly")
            else:
                entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            entries[label_text.replace(":", "")] = entry

        # Populate with current data
        entries["ID Ресурса"].insert(0, resource_id)
        entries["ID Ресурса"].config(state="readonly") # ID cannot be changed
        entries["Тип (VM/Container/Server)"].set(current_config.get("type", ""))
        entries["Статус (Online/Offline)"].set(current_config.get("status", ""))
        entries["IP/Конечная Точка"].insert(0, current_config.get("ip_endpoint", ""))

        def update_resource():
            resource_type = entries["Тип (VM/Container/Server)"].get().strip()
            status = entries["Статус (Online/Offline)"].get().strip()
            ip_endpoint = entries["IP/Конечная Точка"].get().strip()

            if not resource_type or not status or not ip_endpoint:
                messagebox.showwarning("Ошибка Ввода", "Все поля должны быть заполнены.")
                return

            self.compute_resources[resource_id].update({
                "type": resource_type,
                "status": status,
                "ip_endpoint": ip_endpoint
            })
            self._save_conceptual_data()
            self._populate_compute_resource_tree()
            self._update_cloud_status_display()
            messagebox.showinfo("Успех", f"Ресурс '{resource_id}' обновлен.")
            dialog.destroy()

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Обновить", command=update_resource).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        dialog.wait_window()


    def _delete_resource(self):
        """Deletes the selected conceptual compute resource."""
        selected_item = self.resource_tree.focus()
        if not selected_item:
            messagebox.showwarning("Нет Выбора", "Пожалуйста, выберите ресурс для удаления.")
            return

        resource_id = selected_item
        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить ресурс '{resource_id}'? "
                                                      "Это также удалит его концептуальные журналы терминала."):
            if resource_id in self.compute_resources:
                del self.compute_resources[resource_id]
                self._save_conceptual_data()

                # Delete associated conceptual terminal logs
                output_file_public = os.path.join(self.terminal_outputs_dir, f"{resource_id}_public_output.log")
                output_file_private = os.path.join(self.terminal_outputs_dir, f"{resource_id}_private_output.log")
                if os.path.exists(output_file_public):
                    os.remove(output_file_public)
                if os.path.exists(output_file_private):
                    os.remove(output_file_private)

                self._populate_compute_resource_tree()
                self._update_cloud_status_display()
                messagebox.showinfo("Успех", f"Ресурс '{resource_id}' удален.")
                self._on_resource_select(None) # Clear selection and terminal
            else:
                messagebox.showwarning("Не Найден", f"Ресурс '{resource_id}' не найден.")

    def refresh_page(self):
        self._load_conceptual_data()
        self._populate_compute_resource_tree()
        self._update_cloud_status_display()
        # Ensure terminal input/buttons are disabled if no resource is selected initially
        if not self.current_selected_compute_path:
            self.non_private_command_entry.config(state="disabled")
            self.private_command_entry.config(state="disabled")
            for btn in [self.non_private_terminal_frame.winfo_children()[-1], self.private_terminal_frame.winfo_children()[-1]]:
                if isinstance(btn, ttk.Button):
                    btn.config(state="disabled")
            for text_widget in [self.non_private_text, self.private_text]:
                text_widget.config(state="normal")
                text_widget.delete("1.0", tk.END)
                text_widget.insert(tk.END, "Выберите ресурс для взаимодействия с терминалом.")
                text_widget.config(state="disabled")
        else: # Reload if a resource was selected
            self._load_terminal_content(self.current_selected_compute_path)


# This is the function the main App will call to set up the Cloud Compute Aggregator tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    cloud_compute_aggregator_page_instance = CloudComputeAggregatorPage(frame, app_data)
    return frame, cloud_compute_aggregator_page_instance.refresh_page
