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
import json
import datetime
import secrets

class MusicAggregatorPage:
    # Patient Zero Principle: "I don't wipe users' asses, if you forgot your master password, die.
    # When you don't regain access, and no one else does. I don't store any data,
    # you yourselves must take care of how and where to save it and how to remember the password,
    # because the password is the key to encrypting everything on your profile. Without it, no one has access."
    # This note cannot be deleted and must remain unchanged in all document versions.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths for conceptual music data storage
        self.music_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "music_data")
        self.connected_services_file = os.path.join(self.music_data_dir, "connected_services.json")
        self.synced_playlists_file = os.path.join(self.music_data_dir, "synced_playlists.json")

        os.makedirs(self.music_data_dir, exist_ok=True)

        self._load_initial_data()
        self._setup_ui()

    def _load_initial_data(self):
        """Загружает или инициализирует концептуальные данные о подключенных сервисах и плейлистах."""
        if not os.path.exists(self.connected_services_file):
            self.connected_services = {
                "Google Music (Concept)": {"status": "Disconnected", "api_key": None},
                "Spotify (Concept)": {"status": "Disconnected", "api_key": None},
                "Open Source Music (Concept)": {"status": "Disconnected", "api_key": None}
            }
            with open(self.connected_services_file, 'w', encoding='utf-8') as f:
                json.dump(self.connected_services, f, indent=4, ensure_ascii=False)
        else:
            with open(self.connected_services_file, 'r', encoding='utf-8') as f:
                self.connected_services = json.load(f)

        if not os.path.exists(self.synced_playlists_file):
            self.synced_playlists = []
            with open(self.synced_playlists_file, 'w', encoding='utf-8') as f:
                json.dump(self.synced_playlists, f, indent=4, ensure_ascii=False)
        else:
            with open(self.synced_playlists_file, 'r', encoding='utf-8') as f:
                self.synced_playlists = json.load(f)

    def _save_data(self):
        """Сохраняет текущие концептуальные данные в файлы."""
        with open(self.connected_services_file, 'w', encoding='utf-8') as f:
            json.dump(self.connected_services, f, indent=4, ensure_ascii=False)
        with open(self.synced_playlists_file, 'w', encoding='utf-8') as f:
            json.dump(self.synced_playlists, f, indent=4, ensure_ascii=False)

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс для страницы агрегатора музыки."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="Музыкальный Агрегатор и Синхронизация", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        self.music_notebook = ttk.Notebook(main_frame)
        self.music_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Connected Services Tab ---
        self.services_frame = ttk.Frame(self.music_notebook, padding="10")
        self.music_notebook.add(self.services_frame, text="Подключенные Сервисы")
        self._setup_services_tab(self.services_frame)

        # --- Synced Playlists Tab ---
        self.playlists_frame = ttk.Frame(self.music_notebook, padding="10")
        self.music_notebook.add(self.playlists_frame, text="Синхронизированные Плейлисты")
        self._setup_playlists_tab(self.playlists_frame)

        # --- Now Playing / Player Controls Tab ---
        self.player_frame = ttk.Frame(self.music_notebook, padding="10")
        self.music_notebook.add(self.player_frame, text="Сейчас Играет / Управление")
        self._setup_player_tab(self.player_frame)

        # Patient Zero Principle Note
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные, "
            "только вы сами должны позаботиться, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без этого нет доступа никому."
            "\n\n**Эту пометку нельзя удалять, и она должна оставаться неизменной во всех версиях документа.**"
        ), font=("Arial", 9, "italic"), wraplength=700, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, pady=10, sticky="ew")

        self._populate_services_tree()
        self._populate_playlists_tree()

    def _setup_services_tab(self, parent_frame):
        """Настраивает UI для вкладки Подключенные Сервисы."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Управление Музыкальными Сервисами", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Left: Services list
        services_list_frame = ttk.LabelFrame(parent_frame, text="Доступные Сервисы", padding="10")
        services_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        services_list_frame.grid_rowconfigure(0, weight=1)
        services_list_frame.grid_columnconfigure(0, weight=1)

        self.services_tree = ttk.Treeview(services_list_frame, columns=("Status",), show="headings")
        self.services_tree.grid(row=0, column=0, sticky="nsew")
        self.services_tree.heading("Status", text="Статус")
        self.services_tree.column("Status", width=100)

        services_tree_scrollbar = ttk.Scrollbar(services_list_frame, orient="vertical", command=self.services_tree.yview)
        services_tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.services_tree.config(yscrollcommand=services_tree_scrollbar.set)

        self._populate_services_tree()
        self.services_tree.bind("<<TreeviewSelect>>", self._on_service_select)

        # Right: Service connection management
        service_management_frame = ttk.LabelFrame(parent_frame, text="Подключить/Отключить Сервис", padding="10")
        service_management_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        service_management_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(service_management_frame, text="Выбранный Сервис:").grid(row=0, column=0, sticky="w", pady=2)
        self.selected_service_label = ttk.Label(service_management_frame, text="N/A", font=("Arial", 10, "bold"))
        self.selected_service_label.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(service_management_frame, text="API Key / Token (Концепт):").grid(row=1, column=0, sticky="w", pady=2)
        self.api_key_entry = ttk.Entry(service_management_frame, width=30, show="*")
        self.api_key_entry.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Button(service_management_frame, text="Подключить (Концепт)", command=self._connect_service).grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(service_management_frame, text="Отключить (Концепт)", command=self._disconnect_service).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        # Connection status feedback
        self.connection_status_label = ttk.Label(service_management_frame, text="", foreground="blue")
        self.connection_status_label.grid(row=4, column=0, columnspan=2, pady=5)

    def _populate_services_tree(self):
        """Заполняет дерево сервисов текущими статусами."""
        for iid in self.services_tree.get_children():
            self.services_tree.delete(iid)
        for service_name, data in self.connected_services.items():
            self.services_tree.insert("", "end", iid=service_name, text=service_name, values=(data["status"],))

    def _on_service_select(self, event):
        """Обрабатывает выбор сервиса из списка, обновляет поля ввода."""
        selected_item = self.services_tree.focus()
        if selected_item:
            service_name = selected_item
            self.selected_service_label.config(text=service_name)
            self.api_key_entry.delete(0, tk.END)
            # In a real app, you wouldn't display stored API keys directly
            # self.api_key_entry.insert(0, self.connected_services[service_name].get("api_key", ""))

            # Update connection status label
            status = self.connected_services[service_name]["status"]
            self.connection_status_label.config(text=f"Статус: {status}", foreground="green" if status == "Connected" else "red")


    def _connect_service(self):
        """Концептуально подключается к выбранному сервису."""
        service_name = self.selected_service_label.cget("text")
        api_key = self.api_key_entry.get().strip()
        if service_name == "N/A" or not api_key:
            messagebox.showwarning("Ошибка подключения", "Пожалуйста, выберите сервис и введите API-ключ/токен.")
            return

        # Simulate connection
        self.connected_services[service_name]["status"] = "Connected"
        self.connected_services[service_name]["api_key"] = api_key # Store conceptually
        self._save_data()
        self._populate_services_tree()
        self.connection_status_label.config(text="Статус: Подключено", foreground="green")
        messagebox.showinfo("Подключение", f"Сервис '{service_name}' концептуально подключен.")

    def _disconnect_service(self):
        """Концептуально отключается от выбранного сервиса."""
        service_name = self.selected_service_label.cget("text")
        if service_name == "N/A" or self.connected_services[service_name]["status"] == "Disconnected":
            messagebox.showwarning("Ошибка отключения", "Пожалуйста, выберите подключенный сервис.")
            return

        if messagebox.askyesno("Отключение", f"Вы уверены, что хотите отключить сервис '{service_name}'?"):
            self.connected_services[service_name]["status"] = "Disconnected"
            self.connected_services[service_name]["api_key"] = None # Clear key
            self._save_data()
            self._populate_services_tree()
            self.connection_status_label.config(text="Статус: Отключено", foreground="red")
            messagebox.showinfo("Отключение", f"Сервис '{service_name}' концептуально отключен.")

    def _setup_playlists_tab(self, parent_frame):
        """Настраивает UI для вкладки Синхронизированные Плейлисты."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Синхронизация Плейлистов и Библиотеки", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        # Playlist/Library Treeview
        self.playlists_tree = ttk.Treeview(parent_frame, columns=("Source", "Items"), show="headings")
        self.playlists_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.playlists_tree.heading("Source", text="Источник")
        self.playlists_tree.heading("Items", text="Элементов")
        self.playlists_tree.column("Source", width=150)
        self.playlists_tree.column("Items", width=80)

        playlists_tree_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.playlists_tree.yview)
        playlists_tree_scrollbar.grid(row=1, column=1, sticky="ns")
        self.playlists_tree.config(yscrollcommand=playlists_tree_scrollbar.set)

        self._populate_playlists_tree()

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Синхронизировать Плейлисты (Концепт)", command=self._sync_playlists).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить Плейлист (Концепт)", command=self._delete_playlist).pack(side=tk.LEFT, padx=5)

        ttk.Label(button_frame, text="Журнал Синхронизации:", font=("Arial", 10, "bold")).pack(pady=5, anchor="w")
        self.sync_log_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 9), height=5)
        self.sync_log_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.sync_log_text.config(state="disabled")

    def _populate_playlists_tree(self):
        """Заполняет дерево плейлистов."""
        for iid in self.playlists_tree.get_children():
            self.playlists_tree.delete(iid)
        for playlist in self.synced_playlists:
            self.playlists_tree.insert("", "end", iid=playlist["name"], text=playlist["name"], values=(playlist["source"], playlist["items"]))

    def _sync_playlists(self):
        """Концептуально синхронизирует плейлисты с подключенных сервисов."""
        self.sync_log_text.config(state="normal")
        self.sync_log_text.delete("1.0", tk.END)
        self.sync_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Запуск синхронизации...\n")

        any_connected = False
        for service_name, data in self.connected_services.items():
            if data["status"] == "Connected":
                any_connected = True
                self.sync_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Синхронизация с '{service_name}'...\n")
                # Simulate fetching playlists
                dummy_playlist_name = f"Мой Плейлист от {service_name.split(' ')[0]}"
                dummy_items = random.randint(10, 100)

                # Check if playlist already exists to avoid duplicates in demo
                existing_playlist = next((p for p in self.synced_playlists if p["name"] == dummy_playlist_name), None)
                if existing_playlist:
                    existing_playlist["items"] = dummy_items # Update item count
                    self.sync_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Плейлист '{dummy_playlist_name}' обновлен. Элементов: {dummy_items}\n")
                else:
                    self.synced_playlists.append({
                        "name": dummy_playlist_name,
                        "source": service_name,
                        "items": dummy_items
                    })
                    self.sync_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Найден и добавлен плейлист: '{dummy_playlist_name}'. Элементов: {dummy_items}\n")

                self._save_data()
                self._populate_playlists_tree()

        if not any_connected:
            self.sync_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Нет подключенных сервисов для синхронизации.\n")
            messagebox.showwarning("Синхронизация", "Пожалуйста, подключите музыкальные сервисы в соответствующей вкладке.")
        else:
            self.sync_log_text.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Синхронизация завершена.\n")
            messagebox.showinfo("Синхронизация", "Концептуальная синхронизация плейлистов завершена.")

        self.sync_log_text.config(state="disabled")

    def _delete_playlist(self):
        """Концептуально удаляет выбранный плейлист из списка синхронизированных."""
        selected_item = self.playlists_tree.focus()
        if not selected_item:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите плейлист для удаления.")
            return

        playlist_name = selected_item
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить плейлист '{playlist_name}' из синхронизированных? Это не удалит его из исходного сервиса."):
            self.synced_playlists = [p for p in self.synced_playlists if p["name"] != playlist_name]
            self._save_data()
            self._populate_playlists_tree()
            messagebox.showinfo("Удаление", f"Плейлист '{playlist_name}' удален из синхронизированных.")


    def _setup_player_tab(self, parent_frame):
        """Настраивает UI для вкладки Сейчас Играет / Управление."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Управление Воспроизведением (Концепт)", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.now_playing_label = ttk.Label(parent_frame, text="Сейчас не играет ни один трек.", font=("Arial", 14, "italic"), wraplength=400)
        self.now_playing_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=20)

        # Player controls
        player_controls_frame = ttk.Frame(parent_frame)
        player_controls_frame.grid(row=2, column=0, pady=10)

        ttk.Button(player_controls_frame, text="Предыдущий", command=self._play_previous_concept).pack(side=tk.LEFT, padx=5)
        ttk.Button(player_controls_frame, text="Воспроизвести / Пауза", command=self._toggle_play_pause_concept).pack(side=tk.LEFT, padx=5)
        ttk.Button(player_controls_frame, text="Следующий", command=self._play_next_concept).pack(side=tk.LEFT, padx=5)

        ttk.Button(player_controls_frame, text="Выбрать Трек (Концепт)", command=self._select_track_concept).pack(side=tk.LEFT, padx=15)

    def _toggle_play_pause_concept(self):
        """Концептуальное переключение воспроизведения/паузы."""
        current_text = self.now_playing_label.cget("text")
        if "Играет:" in current_text:
            self.now_playing_label.config(text=current_text.replace("Играет:", "Пауза:"))
            messagebox.showinfo("Плеер", "Воспроизведение приостановлено (концептуально).")
        elif "Пауза:" in current_text:
            self.now_playing_label.config(text=current_text.replace("Пауза:", "Играет:"))
            messagebox.showinfo("Плеер", "Воспроизведение возобновлено (концептуально).")
        else:
            self.now_playing_label.config(text="Играет: Концептуальный трек - Артист (Концепт)")
            messagebox.showinfo("Плеер", "Начато воспроизведение (концептуально).")

    def _play_previous_concept(self):
        """Концептуальное воспроизведение предыдущего трека."""
        messagebox.showinfo("Плеер", "Воспроизводится предыдущий трек (концептуально).")
        self.now_playing_label.config(text="Играет: Предыдущий концептуальный трек - Артист (Концепт)")

    def _play_next_concept(self):
        """Концептуальное воспроизведение следующего трека."""
        messagebox.showinfo("Плеер", "Воспроизводится следующий трек (концептуально).")
        self.now_playing_label.config(text="Играет: Следующий концептуальный трек - Артист (Концепт)")

    def _select_track_concept(self):
        """Концептуальный выбор трека из синхронизированных плейлистов."""
        if not self.synced_playlists:
            messagebox.showwarning("Выбор Трека", "Нет синхронизированных плейлистов для выбора трека.")
            return

        # Simple dialog to select a conceptual track
        selected_track = simpledialog.askstring("Выбрать Трек", "Введите название трека для воспроизведения (концептуально):")
        if selected_track:
            self.now_playing_label.config(text=f"Играет: {selected_track} - Выбранный Артист (Концепт)")
            messagebox.showinfo("Плеер", f"Трек '{selected_track}' выбран и воспроизводится (концептуально).")
        else:
            messagebox.showinfo("Плеер", "Выбор трека отменен.")


    def refresh_page(self):
        """Обновляет содержимое страницы агрегатора музыки."""
        self._load_initial_data()
        self._populate_services_tree()
        self._populate_playlists_tree()
        self.now_playing_label.config(text="Сейчас не играет ни один трек.") # Reset player status on refresh


# This is the function the main App will call to set up the Music Aggregator tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    music_aggregator_page_instance = MusicAggregatorPage(frame, app_data)
    app_data["music_aggregator_page_instance"] = music_aggregator_page_instance # Store instance for potential external access
    return frame, music_aggregator_page_instance.refresh_page

