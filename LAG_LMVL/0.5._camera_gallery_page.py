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
import shutil
import zipfile
import datetime
import secrets # For dummy key generation

class CameraGalleryPage:
    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths specific to Camera & Gallery Page (now relative to project root)
        self.camera_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "camera_data")
        self.public_storage_dir = os.path.join(self.camera_data_dir, "public_storage")
        self.private_storage_dir = os.path.join(self.camera_data_dir, "private_storage")
        self.cam_keys_dir = os.path.join(self.camera_data_dir, "keys")

        os.makedirs(self.public_storage_dir, exist_ok=True)
        os.makedirs(self.private_storage_dir, exist_ok=True)
        os.makedirs(self.cam_keys_dir, exist_ok=True)

        # In a real app, this key would be managed securely,
        # e.g., derived from a user's master password, not stored directly.
        from cryptography.fernet import Fernet
        self.cam_encryption_key = self._generate_or_load_encryption_key(os.path.join(self.cam_keys_dir, "camera_encryption_key.txt"), self.cam_keys_dir, "Camera")

        self.save_mode_var = tk.StringVar(value="public") # Default save mode
        self.current_selected_photo_path = None # Stores the path of the selected photo in gallery

        self._setup_ui()
        self._populate_gallery_trees()

    def _generate_or_load_encryption_key(self, key_file_path, keys_dir, module_name):
        """
        Generates a new Fernet key or loads an existing one.
        This is a conceptual key management for demo purposes.
        """
        from cryptography.fernet import Fernet
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

    def _setup_ui(self):
        """Sets up the UI elements for the Camera & Gallery page."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Row for gallery trees

        ttk.Label(main_frame, text="LAG LMVL: Камера и Галерея – Ваша Визуальная Территория", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Left Column: Camera Controls
        camera_frame = ttk.LabelFrame(main_frame, text="Управление Камерой (Концепт)", padding="10")
        camera_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        camera_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(camera_frame, text="Режим сохранения фото:").pack(pady=5)
        ttk.Radiobutton(camera_frame, text="Публичное хранилище", variable=self.save_mode_var, value="public").pack(anchor="w")
        ttk.Radiobutton(camera_frame, text="Приватное хранилище (Концептуально зашифровано)", variable=self.save_mode_var, value="private").pack(anchor="w")

        ttk.Button(camera_frame, text="Сделать Фото (Концепт)", command=self._take_photo_conceptual).pack(pady=10, fill="x")
        ttk.Button(camera_frame, text="Настройки Камеры (Концепт)", command=self._show_camera_settings).pack(pady=5, fill="x")
        ttk.Button(camera_frame, text="Информация об Open Source Камерах", command=self._show_open_source_cam_info).pack(pady=5, fill="x")
        ttk.Button(camera_frame, text="Управление Ключами Шифрования Камеры", command=self._show_cam_keys_info).pack(pady=5, fill="x")

        # Right Column: Gallery Display
        gallery_frame = ttk.LabelFrame(main_frame, text="Галерея Изображений", padding="10")
        gallery_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        gallery_frame.grid_columnconfigure(0, weight=1)
        gallery_frame.grid_rowconfigure(0, weight=1)

        # Notebook for Public/Private tabs
        self.gallery_notebook = ttk.Notebook(gallery_frame)
        self.gallery_notebook.pack(expand=True, fill="both")

        self.public_gallery_frame = ttk.Frame(self.gallery_notebook)
        self.gallery_notebook.add(self.public_gallery_frame, text="Публичные")
        self._setup_gallery_tree(self.public_gallery_frame, "public")

        self.private_gallery_frame = ttk.Frame(self.gallery_notebook)
        self.gallery_notebook.add(self.private_gallery_frame, text="Приватные (Расшифровка)")
        self._setup_gallery_tree(self.private_gallery_frame, "private")

        # Action buttons for gallery
        gallery_action_frame = ttk.Frame(gallery_frame)
        gallery_action_frame.pack(pady=5, fill="x")
        ttk.Button(gallery_action_frame, text="Показать Фото (Концепт)", command=self._show_photo_conceptual).pack(side=tk.LEFT, expand=True, fill="x", padx=2)
        ttk.Button(gallery_action_frame, text="Удалить Фото (Концепт)", command=self._delete_photo_conceptual).pack(side=tk.LEFT, expand=True, fill="x", padx=2)
        ttk.Button(gallery_action_frame, text="Извлечь Все в ZIP (Концепт)", command=self._extract_all_to_zip).pack(side=tk.LEFT, expand=True, fill="x", padx=2)

        # Patient Zero Principle Note
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер-пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные; "
            "вы сами должны заботиться о том, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без него доступа нет никому."
            "\n\n**Это примечание нельзя удалять, и оно должно оставаться неизменным во всех версиях документации.**"
            "\n\n**LAG LMVL Камера и Галерея: 'Ваши визуальные данные, ваш контроль. Мы просто инструмент.'**"
            "\n⚠️ Мы не несем ответственности за потерю незашифрованных или несинхронизированных данных. "
            "Если вы потеряете свои ключи шифрования, ваши приватные фото будут недоступны. Нам похуй."
            "\nПринцип такой: отправляем, невидимо подтверждаем вышестоящей платформой, получили подтверждение, насрать на агрегатора, главное результат, а не как."
        ), font=("Arial", 9, "italic"), wraplength=1000, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")


    def _setup_gallery_tree(self, parent_frame, storage_type):
        """Sets up a Treeview widget for displaying photos."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)

        tree = ttk.Treeview(parent_frame, columns=("Date", "Size"), show="headings")
        tree.grid(row=0, column=0, sticky="nsew")
        tree.heading("#0", text="Имя Файла")
        tree.heading("Date", text="Дата")
        tree.heading("Size", text="Размер")
        tree.column("#0", width=150)
        tree.column("Date", width=100)
        tree.column("Size", width=80)

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree.config(yscrollcommand=scrollbar.set)

        tree.bind("<<TreeviewSelect>>", self._on_photo_select)

        if storage_type == "public":
            self.public_tree = tree
        else:
            self.private_tree = tree

    def _populate_gallery_trees(self):
        """Populates both public and private gallery treeviews."""
        self._clear_gallery_trees()

        # Public Storage
        for filename in os.listdir(self.public_storage_dir):
            filepath = os.path.join(self.public_storage_dir, filename)
            if os.path.isfile(filepath):
                file_stat = os.stat(filepath)
                file_date = datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                file_size = f"{file_stat.st_size / 1024:.1f} KB"
                self.public_tree.insert("", "end", iid=filepath, text=filename, values=(file_date, file_size))

        # Private Storage (displaying encrypted names, actual content would need decryption)
        for filename in os.listdir(self.private_storage_dir):
            filepath = os.path.join(self.private_storage_dir, filename)
            if os.path.isfile(filepath):
                file_stat = os.stat(filepath)
                file_date = datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                file_size = f"{file_stat.st_size / 1024:.1f} KB"
                self.private_tree.insert("", "end", iid=filepath, text=filename, values=(file_date, file_size))

    def _clear_gallery_trees(self):
        """Clears all items from both gallery treeviews."""
        for iid in self.public_tree.get_children():
            self.public_tree.delete(iid)
        for iid in self.private_tree.get_children():
            self.private_tree.delete(iid)

    def _take_photo_conceptual(self):
        """Simulates taking a photo and saving it to the selected storage."""
        save_mode = self.save_mode_var.get()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dummy_filename = f"photo_{timestamp}.txt" # Using .txt for conceptual content

        if save_mode == "public":
            target_dir = self.public_storage_dir
            save_message = "публичное хранилище."
        else: # private
            target_dir = self.private_storage_dir
            dummy_filename = f"photo_{timestamp}.enc" # Use .enc for encrypted
            save_message = "приватное хранилище (концептуально зашифровано)."

        filepath = os.path.join(target_dir, dummy_filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                content = f"Это концептуальное фото, сделанное {timestamp}. Content will be encrypted if saved privately."
                if save_mode == "private":
                    content = self.cam_encryption_key.encrypt(content.encode()).decode('latin-1') # Simulate encryption
                f.write(content)

            messagebox.showinfo("Фото Сделано", f"Концептуальное фото сохранено в {save_message}")
            self._populate_gallery_trees() # Refresh gallery display
        except Exception as e:
            messagebox.showerror("Ошибка Сохранения Фото", f"Не удалось сохранить концептуальное фото: {e}")

    def _show_camera_settings(self):
        """Displays conceptual camera settings."""
        messagebox.showinfo("Настройки Камеры (Концепт)",
                            "Это концептуальные настройки камеры.\n"
                            "В реальном приложении здесь могли бы быть: \n"
                            "- Разрешение фото/видео\n"
                            "- Частота кадров\n"
                            "- Режим вспышки\n"
                            "- Выбор источника камеры (веб-камера, IP-камера, Raspberry Pi Camera и т.д.)\n"
                            "- Настройки приватности и шифрования по умолчанию")

    def _on_photo_select(self, event):
        """Stores the path of the selected photo."""
        selected_item = None
        if self.gallery_notebook.tab(self.gallery_notebook.select(), "text") == "Публичные":
            selected_item = self.public_tree.focus()
        else:
            selected_item = self.private_tree.focus()

        if selected_item:
            self.current_selected_photo_path = selected_item
        else:
            self.current_selected_photo_path = None


    def _show_photo_conceptual(self):
        """Displays the content of the selected photo, decrypting if private."""
        if not self.current_selected_photo_path:
            messagebox.showwarning("Выбор Фото", "Пожалуйста, выберите фото для просмотра.")
            return

        filepath = self.current_selected_photo_path

        try:
            with open(filepath, 'r', encoding='latin-1') as f: # Use latin-1 for encrypted content
                content = f.read()

            # Check if it's an encrypted file and attempt decryption
            if filepath.endswith(".enc"):
                try:
                    content = self.cam_encryption_key.decrypt(content.encode('latin-1')).decode('utf-8')
                    messagebox.showinfo("Просмотр Фото (Расшифровано)", f"Содержание концептуального приватного фото (расшифровано):\n\n{content}")
                except Exception as e:
                    messagebox.showerror("Ошибка Дешифрования", f"Не удалось расшифровать фото. Возможно, неверный ключ или поврежден файл: {e}")
                    return
            else:
                messagebox.showinfo("Просмотр Фото (Публичное)", f"Содержание концептуального публичного фото:\n\n{content}")

        except Exception as e:
            messagebox.showerror("Ошибка Просмотра", f"Не удалось прочитать файл фото: {e}")

    def _delete_photo_conceptual(self):
        """Deletes the selected photo."""
        if not self.current_selected_photo_path:
            messagebox.showwarning("Выбор Фото", "Пожалуйста, выберите фото для удаления.")
            return

        filepath_to_delete = self.current_selected_photo_path

        if messagebox.askyesno("Подтверждение Удаления", f"Вы уверены, что хотите удалить фото '{os.path.basename(filepath_to_delete)}'? "
                                                      "Это действие необратимо. Помните: ваша попа — ваша, а не наша."):
            try:
                os.remove(filepath_to_delete)
                messagebox.showinfo("Фото Удалено", f"Концептуальное фото '{os.path.basename(filepath_to_delete)}' удалено.")
                self._populate_gallery_trees() # Refresh gallery
                self.current_selected_photo_path = None # Clear selected
            except Exception as e:
                messagebox.showerror("Ошибка Удаления", f"Не удалось удалить фото: {e}")

    def _extract_all_to_zip(self):
        """Conceptually extracts all photos to a ZIP archive."""
        # This is a conceptual function. In a real app, it would archive actual files.
        output_zip_name = f"lag_lmvl_gallery_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

        try:
            with zipfile.ZipFile(output_zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add dummy content to the zip
                zipf.writestr("public_photos_manifest.txt", "This ZIP contains conceptual public photos.\n")
                zipf.writestr("private_photos_manifest.txt", "This ZIP contains conceptual PRIVATE (encrypted) photos.\n")

                # Simulate adding existing files (their dummy content)
                for root_dir in [self.public_storage_dir, self.private_storage_dir]:
                    for filename in os.listdir(root_dir):
                        filepath = os.path.join(root_dir, filename)
                        if os.path.isfile(filepath):
                            with open(filepath, 'rb') as f_read:
                                zipf.writestr(os.path.join(os.path.basename(root_dir), filename), f_read.read())

            messagebox.showinfo("Извлечение", f"Все концептуальные фото извлечены в '{output_zip_name}'.")
            # Offer to open the containing folder
            if messagebox.askyesno("Открыть Папку", f"Открыть папку с ZIP-архивом '{output_zip_name}'?"):
                temp_extract_dir = os.path.dirname(os.path.abspath(output_zip_name))
                try:
                    os.startfile(temp_extract_dir) if os.name == 'nt' else os.system(f'xdg-open "{temp_extract_dir}"')
                except Exception as e:
                    messagebox.showerror("Ошибка Открытия Папки", f"Не удалось открыть папку: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка Извлечения", f"Не удалось создать ZIP-архив: {e}")

    def _show_open_source_cam_info(self):
        messagebox.showinfo("Camera Open Source Information",
                            "This section is conceptually for integrating with open-source "
                            "camera solutions like Raspberry Pi Camera, IP cameras "
                            "with open APIs, or webcams supporting V4L2 on Linux. "
                            "Actual operation would require relevant software "
                            "(e.g., ffmpeg, gstreamer) and drivers.")

    def _show_cam_keys_info(self):
        messagebox.showinfo(
            "Keys Folder (Camera & Gallery)",
            f"Эта директория ({self.cam_keys_dir}) концептуально предназначена для хранения "
            f"ключа шифрования, используемого для сохранения фото в 'Приватный Сервер'.\\n\\n"
            "⚠️ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: ⚠️\\n"
            "Хранение реальных ключей шифрования в файлах без надлежащей защиты "
            "и системы управления ключами ОЧЕНЬ ОПАСНО. Это приложение является "
            "лишь концептуальной демонстрацией.\\n"
            "**Помните: если вы потеряете эти ключи, ваши приватные фото будут навсегда недоступны. Нам похуй.**"
        )

    def refresh_page(self):
        self._populate_gallery_trees()

# This is the function the main App will call to set up the Camera & Gallery tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    camera_gallery_page_instance = CameraGalleryPage(frame, app_data)
    return frame, camera_gallery_page_instance.refresh_page
