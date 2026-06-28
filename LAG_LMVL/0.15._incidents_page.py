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
from tkinter import ttk, messagebox
import os

# Define external log paths (from the main app, as they are managed by the Bash script)
# These paths are relative to the root of the application, not this module.
# The main App passes them via app_data.
# LOG_BASE_DIR = "/var/log/monitoring_script" # Managed by main app
# CURRENT_RUN_DETAILS_LOG = os.path.join(LOG_BASE_DIR, "current_run_details.log") # Managed by main app
# LATEST_INTRUSION_LOG_PATH_FILE = os.path.join(LOG_BASE_DIR, "latest_intrusion_log_path.txt") # Managed by main app
# LATEST_CHECKLIST_REPORT_PATH_FILE = os.path.join(LOG_BASE_DIR, "latest_checklist_report_path.txt") # Managed by main app

class IncidentsPage:
    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data # Contains LOG_BASE_DIR, LATEST_INTRUSION_LOG_PATH_FILE etc.

        parent_frame.grid_columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="Мониторинг логов и отчеты по чек-листам", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        # Tabs for different reports
        report_notebook = ttk.Notebook(main_frame)
        report_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Intrusion Log Tab
        intrusion_frame = ttk.Frame(report_notebook)
        report_notebook.add(intrusion_frame, text="Журнал вторжений/аномалий")
        self.intrusion_text = tk.Text(intrusion_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1)
        self.intrusion_text.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.intrusion_text, orient="vertical", command=self.intrusion_text.yview).pack(side="right", fill="y")
        self.intrusion_text.config(yscrollcommand=self.intrusion_text.set)

        # Checklist Report Tab
        checklist_frame = ttk.Frame(report_notebook)
        report_notebook.add(checklist_frame, text="Отчет по чек-листу")
        self.checklist_text = tk.Text(checklist_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1)
        self.checklist_text.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.checklist_text, orient="vertical", command=self.checklist_text.yview).pack(side="right", fill="y")
        self.checklist_text.config(yscrollcommand=self.checklist_text.set)

        # Controls for refresh and info
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, pady=10)
        ttk.Button(controls_frame, text="Обновить отчеты", command=self.refresh_page).pack(side=tk.LEFT, padx=10)
        ttk.Button(controls_frame, text="Показать детали последнего запуска", command=self._show_current_run_details).pack(side=tk.LEFT, padx=10)

        self.refresh_page() # Load on startup

    def _show_current_run_details(self):
        """Displays the content of the current run details log."""
        current_run_details_log_path = self.app_data["CURRENT_RUN_DETAILS_LOG"]
        if os.path.exists(current_run_details_log_path):
            try:
                with open(current_run_details_log_path, 'r', encoding='utf-8') as f: # Added encoding
                    content = f.read()
                messagebox.showinfo("Детали текущего запуска скрипта", content)
            except Exception as e:
                messagebox.showerror("Ошибка чтения лога", f"Не удалось прочитать детали текущего запуска: {e}")
        else:
            messagebox.showinfo("Детали текущего запуска скрипта", "Файл деталей текущего запуска не найден.")

    def refresh_page(self):
        """Refreshes the intrusion and checklist report displays."""
        def load_report_content(file_path_file_var, text_widget):
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            file_path_file = self.app_data[file_path_file_var] # Get path from app_data
            if os.path.exists(file_path_file):
                try:
                    with open(file_path_file, 'r', encoding='utf-8') as f_path: # Added encoding
                        latest_report_path = f_path.read().strip()
                        if os.path.exists(latest_report_path):
                            with open(latest_report_path, 'r', encoding='utf-8') as f_report: # Added encoding
                                text_widget.insert(tk.END, f_report.read())
                        else:
                            text_widget.insert(tk.END, f"Файл отчета не найден: {latest_report_path}")
                except Exception as e:
                    text_widget.insert(tk.END, f"Ошибка загрузки отчета: {e}")
            else:
                text_widget.insert(tk.END, "Путь к последнему отчету не найден.")
            text_widget.config(state="disabled")

        load_report_content("LATEST_INTRUSION_LOG_PATH_FILE", self.intrusion_text)
        load_report_content("LATEST_CHECKLIST_REPORT_PATH_FILE", self.checklist_text)

# This is the function the main App will call to set up the Incidents tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    incidents_page_instance = IncidentsPage(frame, app_data)
    # The refresh method is just a wrapper around the instance's method
    return frame, incidents_page_instance.refresh_page

