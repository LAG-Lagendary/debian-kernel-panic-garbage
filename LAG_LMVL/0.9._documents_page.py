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
import json
import datetime

class DocumentsPage:
    # Patient Zero Principle: "I don't wipe users' asses, if you forgot your master password, die.
    # When you don't regain access, and no one else does. I don't store any data,
    # you yourselves must take care of how and where to save it and how to remember the password,
    # because the password is the key to encrypting everything on your profile. Without it, no one has access."
    # This note cannot be deleted and must remain unchanged in all document versions.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths for conceptual document storage
        self.documents_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "documents_data")
        self.notes_file = os.path.join(self.documents_data_dir, "my_notes.json")
        self.dummy_pdf_path = os.path.join(self.documents_data_dir, "conceptual_document.pdf")
        self.dummy_table_path = os.path.join(self.documents_data_dir, "conceptual_table.csv")
        self.dummy_word_path = os.path.join(self.documents_data_dir, "conceptual_report.docx")

        os.makedirs(self.documents_data_dir, exist_ok=True)
        self._create_dummy_files()

        self._load_notes()
        self._setup_ui()

    def _create_dummy_files(self):
        """Создает фиктивные файлы для демонстрации, если они не существуют."""
        if not os.path.exists(self.dummy_pdf_path):
            with open(self.dummy_pdf_path, 'w', encoding='utf-8') as f:
                f.write("Это концептуальный PDF-документ.\n\n"
                        "В реальном приложении здесь будет отображаться содержимое PDF-файла.")
        if not os.path.exists(self.dummy_table_path):
            with open(self.dummy_table_path, 'w', encoding='utf-8') as f:
                f.write("Header1,Header2,Header3\n")
                f.write("Row1Col1,Row1Col2,Row1Col3\n")
                f.write("Row2Col1,Row2Col2,Row2Col3\n")
                f.write("Row3Col1,Row3Col2,Row3Col3\n")
        if not os.path.exists(self.dummy_word_path):
            with open(self.dummy_word_path, 'w', encoding='utf-8') as f:
                f.write("Это концептуальный Word-документ.\n\n"
                        "В реальном приложении здесь будет отображаться содержимое DOCX-файла.\n"
                        "Может включать текст, изображения и форматирование.")
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump({"default_note": "Это ваша первая заметка. Вы можете редактировать ее и сохранять."}, f, indent=4, ensure_ascii=False)


    def _load_notes(self):
        """Загружает заметки из файла."""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка загрузки", "Файл заметок поврежден. Загружена пустая заметка.")
                self.notes = {"default_note": "Ошибка: файл заметок поврежден. Эта заметка по умолчанию."}
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить заметки: {e}")
                self.notes = {"default_note": "Ошибка загрузки заметок. Эта заметка по умолчанию."}
        else:
            self.notes = {"default_note": "Начните писать свою заметку здесь."}
        self.current_note_name = list(self.notes.keys())[0] # Set first note as current


    def _save_notes(self):
        """Сохраняет заметки в файл."""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Сохранение", "Заметки успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить заметки: {e}")

    def _setup_ui(self):
        """Настраивает пользовательский интерфейс для страницы документов."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="Управление Документами и Заметками", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        self.documents_notebook = ttk.Notebook(main_frame)
        self.documents_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Notes Tab ---
        self.notes_frame = ttk.Frame(self.documents_notebook, padding="10")
        self.documents_notebook.add(self.notes_frame, text="Заметки (Текст)")
        self._setup_notes_tab(self.notes_frame)

        # --- PDF Viewer Tab ---
        self.pdf_viewer_frame = ttk.Frame(self.documents_notebook, padding="10")
        self.documents_notebook.add(self.pdf_viewer_frame, text="Просмотр PDF (Концепт)")
        self._setup_pdf_viewer_tab(self.pdf_viewer_frame)

        # --- Table Viewer Tab ---
        self.table_viewer_frame = ttk.Frame(self.documents_notebook, padding="10")
        self.documents_notebook.add(self.table_viewer_frame, text="Просмотр Таблиц (Концепт)")
        self._setup_table_viewer_tab(self.table_viewer_frame)

        # --- Word Analog Tab ---
        self.word_analog_frame = ttk.Frame(self.documents_notebook, padding="10")
        self.documents_notebook.add(self.word_analog_frame, text="Аналог Word (Концепт)")
        self._setup_word_analog_tab(self.word_analog_frame)

        # Patient Zero Principle Note
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Примечание от Пациента Зеро: Я не вытираю попу пользователям, забыл мастер пароль — сдохни. "
            "Когда не получишь доступ обратно, и никто не получит. Я не храню никакие данные, "
            "только вы сами должны позаботиться, как и куда их сохранить и как запомнить пароль, "
            "потому что пароль — это ключ к шифрованию всего на вашем профиле. Без этого нет доступа никому."
            "\n\n**Эту пометку нельзя удалять, и она должна оставаться неизменной во всех версиях документа.**"
        ), font=("Arial", 9, "italic"), wraplength=700, foreground="red")
        patient_zero_note_label.grid(row=2, column=0, pady=10, sticky="ew")

        # Initial population for notes
        self._populate_notes_listbox()
        self._display_current_note()


    def _setup_notes_tab(self, parent_frame):
        """Настраивает UI для вкладки Заметки."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_columnconfigure(1, weight=3)
        parent_frame.grid_rowconfigure(1, weight=1)

        # Left: Note list and controls
        notes_controls_frame = ttk.Frame(parent_frame, padding="5")
        notes_controls_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        notes_controls_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(notes_controls_frame, text="Мои Заметки", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, sticky="w")

        self.notes_listbox = tk.Listbox(notes_controls_frame, height=15, font=("Arial", 10))
        self.notes_listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.notes_listbox.bind("<<ListboxSelect>>", self._on_note_select)

        notes_listbox_scrollbar = ttk.Scrollbar(notes_controls_frame, orient="vertical", command=self.notes_listbox.yview)
        notes_listbox_scrollbar.grid(row=1, column=1, sticky="ns")
        self.notes_listbox.config(yscrollcommand=notes_listbox_scrollbar.set)

        button_frame = ttk.Frame(notes_controls_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Новая Заметка", command=self._new_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Удалить Заметку", command=self._delete_note).pack(side=tk.LEFT, padx=2)

        # Right: Note content editor
        note_editor_frame = ttk.Frame(parent_frame, padding="5")
        note_editor_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        note_editor_frame.grid_rowconfigure(1, weight=1)
        note_editor_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(note_editor_frame, text="Название Заметки:").grid(row=0, column=0, sticky="w", pady=2)
        self.note_name_entry = ttk.Entry(note_editor_frame, font=("Arial", 12))
        self.note_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        self.note_text_editor = tk.Text(note_editor_frame, wrap="word", font=("Arial", 10))
        self.note_text_editor.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        note_editor_scrollbar = ttk.Scrollbar(note_editor_frame, orient="vertical", command=self.note_text_editor.yview)
        note_editor_scrollbar.grid(row=1, column=2, sticky="ns")
        self.note_text_editor.config(yscrollcommand=note_editor_scrollbar.set)

        ttk.Button(note_editor_frame, text="Сохранить Текущую Заметку", command=self._save_current_note).grid(row=2, column=0, columnspan=3, pady=5)


    def _populate_notes_listbox(self):
        """Заполняет список заметок."""
        self.notes_listbox.delete(0, tk.END)
        for name in self.notes.keys():
            self.notes_listbox.insert(tk.END, name)

        if self.current_note_name in self.notes:
            index = list(self.notes.keys()).index(self.current_note_name)
            self.notes_listbox.selection_set(index)
            self.notes_listbox.see(index)

    def _display_current_note(self):
        """Отображает содержимое текущей выбранной заметки."""
        self.note_name_entry.delete(0, tk.END)
        self.note_text_editor.delete("1.0", tk.END)
        if self.current_note_name in self.notes:
            self.note_name_entry.insert(0, self.current_note_name)
            self.note_text_editor.insert(tk.END, self.notes[self.current_note_name])
        else:
            self.note_name_entry.insert(0, "Новая заметка")
            self.note_text_editor.insert(tk.END, "")


    def _on_note_select(self, event):
        """Обрабатывает выбор заметки из списка."""
        selected_indices = self.notes_listbox.curselection()
        if selected_indices:
            new_note_name = self.notes_listbox.get(selected_indices[0])
            if new_note_name != self.current_note_name:
                self._save_current_note(silent=True) # Silently save changes to previous note
                self.current_note_name = new_note_name
                self._display_current_note()

    def _new_note(self):
        """Создает новую пустую заметку."""
        self._save_current_note(silent=True) # Save current note before creating new
        new_name = simpledialog.askstring("Новая Заметка", "Введите название для новой заметки:")
        if new_name and new_name.strip() != "":
            if new_name in self.notes:
                messagebox.showwarning("Предупреждение", "Заметка с таким именем уже существует.")
                return
            self.notes[new_name] = ""
            self.current_note_name = new_name
            self._save_notes() # Save immediately to update file
            self._populate_notes_listbox()
            self._display_current_note()
        else:
            messagebox.showwarning("Ошибка ввода", "Название заметки не может быть пустым.")

    def _delete_note(self):
        """Удаляет выбранную заметку."""
        selected_indices = self.notes_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите заметку для удаления.")
            return

        note_to_delete = self.notes_listbox.get(selected_indices[0])
        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить заметку '{note_to_delete}'?"):
            del self.notes[note_to_delete]
            if note_to_delete == self.current_note_name:
                self.current_note_name = list(self.notes.keys())[0] if self.notes else "default_note"
                if not self.notes: # If no notes left, add a default one
                    self.notes["default_note"] = "Начните писать свою заметку здесь."
                    self.current_note_name = "default_note"

            self._save_notes()
            self._populate_notes_listbox()
            self._display_current_note()


    def _save_current_note(self, silent=False):
        """Сохраняет содержимое текущей заметки."""
        current_name_in_entry = self.note_name_entry.get().strip()
        current_content_in_editor = self.note_text_editor.get("1.0", tk.END).strip()

        if self.current_note_name not in self.notes: # Should not happen if logic is correct
            self.notes[self.current_note_name] = current_content_in_editor
            if not silent: messagebox.showinfo("Сохранение", "Новая заметка сохранена.")
        else:
            if current_name_in_entry != self.current_note_name:
                # If name was changed, create new entry and delete old
                if current_name_in_entry in self.notes and current_name_in_entry != self.current_note_name:
                    if not silent: messagebox.showwarning("Ошибка сохранения", "Новое название заметки уже существует.")
                    return
                self.notes[current_name_in_entry] = current_content_in_editor
                del self.notes[self.current_note_name]
                self.current_note_name = current_name_in_entry
                self._populate_notes_listbox() # Refresh list to reflect name change
                if not silent: messagebox.showinfo("Сохранение", f"Заметка переименована и сохранена как '{self.current_note_name}'.")
            else:
                self.notes[self.current_note_name] = current_content_in_editor
                if not silent: messagebox.showinfo("Сохранение", "Текущая заметка сохранена.")

        self._save_notes() # Always save to disk
        self._populate_notes_listbox() # Ensure listbox is up-to-date


    def _setup_pdf_viewer_tab(self, parent_frame):
        """Настраивает UI для вкладки Просмотр PDF."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальный Просмотр PDF", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.pdf_display_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 10), height=20)
        self.pdf_display_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.pdf_display_text.config(state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Загрузить PDF (Концепт)", command=self._load_pdf_concept).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Открыть PDF в Программе по Умолчанию (Концепт)", command=self._open_pdf_external_concept).pack(side=tk.LEFT, padx=5)

        self._load_pdf_concept(initial_load=True) # Load dummy content on startup


    def _load_pdf_concept(self, initial_load=False):
        """Концептуальная загрузка PDF-файла."""
        file_path = self.dummy_pdf_path
        if not initial_load:
            file_path = filedialog.askopenfilename(
                title="Выберите PDF-файл (Концепт)",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if not file_path:
                return

        self.pdf_display_text.config(state="normal")
        self.pdf_display_text.delete("1.0", tk.END)
        if os.path.exists(file_path):
            try:
                # In a real app, you'd use a PDF rendering library here (e.g., PyMuPDF)
                with open(file_path, 'r', encoding='utf-8') as f: # Reading as text for conceptual demo
                    content = f.read()
                    self.pdf_display_text.insert(tk.END, f"--- Содержимое концептуального PDF-файла: {os.path.basename(file_path)} ---\n\n")
                    self.pdf_display_text.insert(tk.END, content)
                messagebox.showinfo("Загрузка PDF", f"Концептуальный PDF '{os.path.basename(file_path)}' загружен.")
            except Exception as e:
                self.pdf_display_text.insert(tk.END, f"Ошибка загрузки концептуального PDF: {e}")
                messagebox.showerror("Ошибка", f"Не удалось загрузить концептуальный PDF: {e}")
        else:
            self.pdf_display_text.insert(tk.END, "Файл PDF не найден для отображения концептуального содержимого.")
            if not initial_load:
                messagebox.showwarning("Файл не найден", "Выбранный PDF-файл не найден.")
        self.pdf_display_text.config(state="disabled")

    def _open_pdf_external_concept(self):
        """Концептуальное открытие PDF во внешней программе."""
        file_path = self.dummy_pdf_path # Use dummy for concept
        messagebox.showinfo("Открыть PDF (Концепт)",
                            f"В реальном приложении файл '{os.path.basename(file_path)}' "
                            "был бы открыт в программе для просмотра PDF по умолчанию на вашей системе.")

    def _setup_table_viewer_tab(self, parent_frame):
        """Настраивает UI для вкладки Просмотр Таблиц."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальный Просмотр Таблиц", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.table_display_text = tk.Text(parent_frame, wrap="none", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Courier New", 10), height=20)
        self.table_display_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        table_xscrollbar = ttk.Scrollbar(parent_frame, orient="horizontal", command=self.table_display_text.xview)
        table_xscrollbar.grid(row=2, column=0, sticky="ew")
        self.table_display_text.config(xscrollcommand=table_xscrollbar.set)

        table_yscrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.table_display_text.yview)
        table_yscrollbar.grid(row=1, column=1, sticky="ns")
        self.table_display_text.config(yscrollcommand=table_yscrollbar.set, state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=3, column=0, pady=5)
        ttk.Button(button_frame, text="Загрузить Таблицу (Концепт)", command=self._load_table_concept).pack(side=tk.LEFT, padx=5)

        self._load_table_concept(initial_load=True) # Load dummy content on startup


    def _load_table_concept(self, initial_load=False):
        """Концептуальная загрузка табличного файла (например, CSV)."""
        file_path = self.dummy_table_path
        if not initial_load:
            file_path = filedialog.askopenfilename(
                title="Выберите Табличный файл (Концепт)",
                filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return

        self.table_display_text.config(state="normal")
        self.table_display_text.delete("1.0", tk.END)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.table_display_text.insert(tk.END, f"--- Содержимое концептуальной таблицы: {os.path.basename(file_path)} ---\n\n")
                    self.table_display_text.insert(tk.END, content)
                messagebox.showinfo("Загрузка Таблицы", f"Концептуальная таблица '{os.path.basename(file_path)}' загружена.")
            except Exception as e:
                self.table_display_text.insert(tk.END, f"Ошибка загрузки концептуальной таблицы: {e}")
                messagebox.showerror("Ошибка", f"Не удалось загрузить концептуальную таблицу: {e}")
        else:
            self.table_display_text.insert(tk.END, "Файл таблицы не найден для отображения концептуального содержимого.")
            if not initial_load:
                messagebox.showwarning("Файл не найден", "Выбранный табличный файл не найден.")
        self.table_display_text.config(state="disabled")

    def _setup_word_analog_tab(self, parent_frame):
        """Настраивает UI для вкладки Аналог Word."""
        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Концептуальный Аналог Word-Документа", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

        self.word_analog_text = tk.Text(parent_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 11), height=20)
        self.word_analog_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        word_analog_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.word_analog_text.yview)
        word_analog_scrollbar.grid(row=1, column=1, sticky="ns")
        self.word_analog_text.config(yscrollcommand=word_analog_scrollbar.set, state="disabled")

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=2, column=0, pady=5)
        ttk.Button(button_frame, text="Загрузить Документ (Концепт)", command=self._load_word_analog_concept).pack(side=tk.LEFT, padx=5)

        self._load_word_analog_concept(initial_load=True) # Load dummy content on startup


    def _load_word_analog_concept(self, initial_load=False):
        """Концептуальная загрузка Word-аналога (например, DOCX)."""
        file_path = self.dummy_word_path
        if not initial_load:
            file_path = filedialog.askopenfilename(
                title="Выберите Документ (Концепт)",
                filetypes=[("Word documents", "*.docx"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return

        self.word_analog_text.config(state="normal")
        self.word_analog_text.delete("1.0", tk.END)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f: # Reading as text for conceptual demo
                    content = f.read()
                    self.word_analog_text.insert(tk.END, f"--- Содержимое концептуального Word-документа: {os.path.basename(file_path)} ---\n\n")
                    self.word_analog_text.insert(tk.END, content)
                messagebox.showinfo("Загрузка Документа", f"Концептуальный документ '{os.path.basename(file_path)}' загружен.")
            except Exception as e:
                self.word_analog_text.insert(tk.END, f"Ошибка загрузки концептуального документа: {e}")
                messagebox.showerror("Ошибка", f"Не удалось загрузить концептуальный документ: {e}")
        else:
            self.word_analog_text.insert(tk.END, "Файл документа не найден для отображения концептуального содержимого.")
            if not initial_load:
                messagebox.showwarning("Файл не найден", "Выбранный документ не найден.")
        self.word_analog_text.config(state="disabled")

    def refresh_page(self):
        """Обновляет содержимое страницы документов."""
        self._load_notes()
        self._populate_notes_listbox()
        self._display_current_note()
        self._load_pdf_concept(initial_load=True)
        self._load_table_concept(initial_load=True)
        self._load_word_analog_concept(initial_load=True)


# This is the function the main App will call to set up the Documents tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    documents_page_instance = DocumentsPage(frame, app_data)
    return frame, documents_page_instance.refresh_page

