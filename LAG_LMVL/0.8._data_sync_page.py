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
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
import datetime
import time
import random
import string # For generating conceptual user IDs

# Import our encryption module, if available
try:
    from modules.encryption.crypto_utils import CryptoUtils
except ImportError:
    messagebox.showerror("Import Error", "Could not load encryption module. Please check the path.")
    CryptoUtils = None

# --- Conceptual Master Key for Demo ---
CONCEPTUAL_MASTER_KEY_FOR_SYNC = "SecureSyncKeyForLAGLMVL2025!"

class DataSyncPage:
    """
    Conceptual Data Synchronization Page for LAG-LMVL.
    Simulates synchronization of data between local storage and conceptual cloud/server.
    """
    # Patient Zero Principle: "I don't wipe users' asses, if you forgot your master password, die.
    # When you don't regain access, and no one else does. I don't store any data,
    # you yourselves must take care of how and where to save it and how to remember the password,
    # because the password is the key to encrypting everything on your profile. Without it, no one has access."
    # This note cannot be deleted and must remain unchanged in all document versions.

    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths for conceptual data storage
        self.sync_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sync_data")
        self.local_storage_dir = os.path.join(self.sync_data_dir, "local_storage")
        self.conceptual_cloud_dir = os.path.join(self.sync_data_dir, "conceptual_cloud_storage")
        self.sync_logs_file = os.path.join(self.sync_data_dir, "sync_log.json")
        self.sync_keys_dir = os.path.join(self.sync_data_dir, "keys")
        # NEW: Conceptual User Manifest file
        self.user_manifest_file = os.path.join(self.sync_data_dir, "user_manifest.json")

        os.makedirs(self.local_storage_dir, exist_ok=True)
        os.makedirs(self.conceptual_cloud_dir, exist_ok=True)
        os.makedirs(self.sync_keys_dir, exist_ok=True)
        os.makedirs(self.sync_data_dir, exist_ok=True)

        self.crypto_utils = None
        if CryptoUtils:
            try:
                self.crypto_utils = CryptoUtils(CONCEPTUAL_MASTER_KEY_FOR_SYNC)
            except Exception as e:
                messagebox.showerror("Crypto Error", f"Failed to initialize CryptoUtils for Data Sync: {e}")

        self._create_dummy_files()
        self._load_sync_logs()
        self._load_user_manifest() # NEW: Load user manifest

        self._setup_ui()
        self._populate_file_trees()
        self._update_sync_log_display()
        self._populate_user_manifest_tree() # NEW: Populate user manifest display

    def _create_dummy_files(self):
        """Creates some dummy files for demonstration."""
        if not os.path.exists(os.path.join(self.local_storage_dir, "local_document.txt")):
            with open(os.path.join(self.local_storage_dir, "local_document.txt"), "w", encoding="utf-8") as f:
                f.write("This is a document on local storage.\n" * 5)
        if not os.path.exists(os.path.join(self.local_storage_dir, "local_image_concept.txt")):
            with open(os.path.join(self.local_storage_dir, "local_image_concept.txt"), "w", encoding="utf-8") as f:
                f.write("This is a conceptual image file.\n")

        # Simulate some files already in the cloud, possibly encrypted
        if not os.path.exists(os.path.join(self.conceptual_cloud_dir, "cloud_report.txt")):
            with open(os.path.join(self.conceptual_cloud_dir, "cloud_report.txt"), "w", encoding="utf-8") as f:
                f.write("This is a report conceptually in the cloud.\n" * 3)
        if not os.path.exists(os.path.join(self.conceptual_cloud_dir, "cloud_secret.enc")):
            secret_content = "This is a secret document in the cloud, encrypted."
            if self.crypto_utils:
                encrypted_content = self.crypto_utils.encrypt_data(secret_content.encode('utf-8'), CONCEPTUAL_MASTER_KEY_FOR_SYNC).decode('latin-1')
                with open(os.path.join(self.conceptual_cloud_dir, "cloud_secret.enc"), "w", encoding="latin-1") as f:
                    f.write(encrypted_content)
            else:
                with open(os.path.join(self.conceptual_cloud_dir, "cloud_secret.enc"), "w", encoding="utf-8") as f:
                    f.write(secret_content + " (NOT ENCRYPTED - CryptoUtils missing)")

    def _load_sync_logs(self):
        """Loads conceptual synchronization logs."""
        if os.path.exists(self.sync_logs_file):
            try:
                with open(self.sync_logs_file, 'r', encoding='utf-8') as f:
                    self.sync_logs = json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Log Load Error", "Corrupted sync log file.")
                self.sync_logs = []
        else:
            self.sync_logs = []

    def _save_sync_logs(self):
        """Saves conceptual synchronization logs."""
        with open(self.sync_logs_file, 'w', encoding='utf-8') as f:
            json.dump(self.sync_logs, f, indent=4, ensure_ascii=False)

    def _log_sync_activity(self, action, status="success", details=""):
        """Logs a conceptual synchronization activity."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "status": status,
            "details": details
        }
        self.sync_logs.append(log_entry)
        self._save_sync_logs()
        self._update_sync_log_display()

    def _load_user_manifest(self):
        """NEW: Loads conceptual user manifest."""
        if os.path.exists(self.user_manifest_file):
            try:
                with open(self.user_manifest_file, 'r', encoding='utf-8') as f:
                    self.user_manifest = json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("User Manifest Load Error", "Corrupted user manifest file.")
                self.user_manifest = []
        else:
            self.user_manifest = []
            # Add the specific dummy entry as requested
            self.user_manifest.append({
                "id": "0!patient_zero______---developer---worldwine---'jet-lag'",
                "nickname": "jet-lag",
                "country": "worldwine",
                "category": "developer"
            })
            self._save_user_manifest() # Save initial dummy data

    def _save_user_manifest(self):
        """NEW: Saves conceptual user manifest."""
        with open(self.user_manifest_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_manifest, f, indent=4, ensure_ascii=False)

    def _setup_ui(self):
        """Sets up the UI elements for the Data Synchronization page."""
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.parent_frame, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Row for file trees

        ttk.Label(main_frame, text="LAG LMVL: Data Synchronization – Your Chaos, Our Sync", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Left Column: Local Storage
        local_frame = ttk.LabelFrame(main_frame, text="Local Storage", padding="10")
        local_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        local_frame.grid_rowconfigure(0, weight=1)
        local_frame.grid_columnconfigure(0, weight=1)

        self.local_tree = ttk.Treeview(local_frame, columns=("Size",), show="headings")
        self.local_tree.grid(row=0, column=0, sticky="nsew")
        self.local_tree.heading("#0", text="File Name")
        self.local_tree.heading("Size", text="Size")
        self.local_tree.column("Size", width=80)

        local_scrollbar = ttk.Scrollbar(local_frame, orient="vertical", command=self.local_tree.yview)
        local_scrollbar.grid(row=0, column=1, sticky="ns")
        self.local_tree.config(yscrollcommand=local_scrollbar.set)

        local_buttons_frame = ttk.Frame(local_frame)
        local_buttons_frame.grid(row=1, column=0, sticky="ew", pady=5)
        ttk.Button(local_buttons_frame, text="Create Conceptual File", command=self._create_conceptual_local_file).pack(side=tk.LEFT, padx=2, expand=True, fill="x")
        ttk.Button(local_buttons_frame, text="Delete Selected (Local)", command=lambda: self._delete_file_conceptual(self.local_tree, self.local_storage_dir)).pack(side=tk.LEFT, padx=2, expand=True, fill="x")

        # Right Column: Conceptual Cloud Storage
        cloud_frame = ttk.LabelFrame(main_frame, text="Conceptual Cloud Storage", padding="10")
        cloud_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        cloud_frame.grid_rowconfigure(0, weight=1)
        cloud_frame.grid_columnconfigure(0, weight=1)

        self.cloud_tree = ttk.Treeview(cloud_frame, columns=("Size", "Encrypted"), show="headings")
        self.cloud_tree.grid(row=0, column=0, sticky="nsew")
        self.cloud_tree.heading("#0", text="File Name")
        self.cloud_tree.heading("Size", text="Size")
        self.cloud_tree.heading("Encrypted", text="Encrypted")
        self.cloud_tree.column("Size", width=80)
        self.cloud_tree.column("Encrypted", width=80)

        cloud_scrollbar = ttk.Scrollbar(cloud_frame, orient="vertical", command=self.cloud_tree.yview)
        cloud_scrollbar.grid(row=0, column=1, sticky="ns")
        self.cloud_tree.config(yscrollcommand=cloud_scrollbar.set)

        cloud_buttons_frame = ttk.Frame(cloud_frame)
        cloud_buttons_frame.grid(row=1, column=0, sticky="ew", pady=5)
        ttk.Button(cloud_buttons_frame, text="Upload Selected (to Cloud)", command=self._upload_file_conceptual).pack(side=tk.LEFT, padx=2, expand=True, fill="x")
        ttk.Button(cloud_buttons_frame, text="Download Selected (from Cloud)", command=self._download_file_conceptual).pack(side=tk.LEFT, padx=2, expand=True, fill="x")
        ttk.Button(cloud_buttons_frame, text="Delete Selected (from Cloud)", command=lambda: self._delete_file_conceptual(self.cloud_tree, self.conceptual_cloud_dir)).pack(side=tk.LEFT, padx=2, expand=True, fill="x")

        # Synchronization Controls
        sync_controls_frame = ttk.LabelFrame(main_frame, text="Synchronization Controls", padding="10")
        sync_controls_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        sync_controls_frame.grid_columnconfigure(0, weight=1)
        sync_controls_frame.grid_columnconfigure(1, weight=1)
        sync_controls_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(sync_controls_frame, text="Sync All (Local -> Cloud)", command=self._sync_all_to_cloud).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(sync_controls_frame, text="Sync All (Cloud -> Local)", command=self._sync_all_to_local).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(sync_controls_frame, text="Run Sync Audit", command=self._run_sync_audit).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Sync Log Display
        sync_log_frame = ttk.LabelFrame(main_frame, text="Synchronization Log", padding="10")
        sync_log_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        sync_log_frame.grid_columnconfigure(0, weight=1)
        sync_log_frame.grid_rowconfigure(0, weight=1)

        self.sync_log_text = tk.Text(sync_log_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 9), height=10, state="disabled")
        self.sync_log_text.grid(row=0, column=0, sticky="nsew")
        sync_log_scrollbar = ttk.Scrollbar(sync_log_frame, orient="vertical", command=self.sync_log_text.yview)
        sync_log_scrollbar.grid(row=0, column=1, sticky="ns")
        self.sync_log_text.config(yscrollcommand=sync_log_scrollbar.set)

        # NEW: Conceptual User Manifest Section
        user_manifest_frame = ttk.LabelFrame(main_frame, text="Conceptual User Manifest", padding="10")
        user_manifest_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        user_manifest_frame.grid_columnconfigure(0, weight=1)
        user_manifest_frame.grid_rowconfigure(1, weight=1)

        # Input fields for adding users
        user_input_frame = ttk.Frame(user_manifest_frame)
        user_input_frame.grid(row=0, column=0, sticky="ew", pady=5)
        user_input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(user_input_frame, text="Nickname:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.user_nickname_entry = ttk.Entry(user_input_frame, width=30)
        self.user_nickname_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        ttk.Label(user_input_frame, text="Country:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.user_country_entry = ttk.Entry(user_input_frame, width=30)
        self.user_country_entry.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        ttk.Label(user_input_frame, text="Category:").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.user_category_combobox = ttk.Combobox(user_input_frame, values=["user", "developer"], state="readonly")
        self.user_category_combobox.grid(row=2, column=1, sticky="ew", padx=2, pady=2)
        self.user_category_combobox.set("user")

        ttk.Button(user_input_frame, text="Add Conceptual User", command=self._add_conceptual_user).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew", padx=2)

        # Treeview for displaying users
        self.user_manifest_tree = ttk.Treeview(user_manifest_frame, columns=("Nickname", "Country", "Category", "ID"), show="headings")
        self.user_manifest_tree.grid(row=1, column=0, sticky="nsew")
        self.user_manifest_tree.heading("Nickname", text="Nickname")
        self.user_manifest_tree.heading("Country", text="Country")
        self.user_manifest_tree.heading("Category", text="Category")
        self.user_manifest_tree.heading("ID", text="ID (Conceptual)")
        self.user_manifest_tree.column("Nickname", width=100)
        self.user_manifest_tree.column("Country", width=100)
        self.user_manifest_tree.column("Category", width=100)
        self.user_manifest_tree.column("ID", width=250)

        user_manifest_scrollbar = ttk.Scrollbar(user_manifest_frame, orient="vertical", command=self.user_manifest_tree.yview)
        user_manifest_scrollbar.grid(row=1, column=1, sticky="ns")
        self.user_manifest_tree.config(yscrollcommand=user_manifest_scrollbar.set)

        # Search functionality
        search_frame = ttk.LabelFrame(user_manifest_frame, text="Search Users", padding="5")
        search_frame.grid(row=2, column=0, sticky="ew", pady=5)
        search_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search by nickname:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.search_nickname_entry = ttk.Entry(search_frame, width=30)
        self.search_nickname_entry.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        ttk.Label(search_frame, text="Search by country:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.search_country_entry = ttk.Entry(search_frame, width=30)
        self.search_country_entry.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        ttk.Label(search_frame, text="Search by category:").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.search_category_combobox = ttk.Combobox(search_frame, values=["", "user", "developer"], state="readonly")
        self.search_category_combobox.grid(row=2, column=1, sticky="ew", padx=2, pady=2)
        self.search_category_combobox.set("")

        ttk.Button(search_frame, text="Find Users", command=self._search_conceptual_users).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew", padx=2)

        self.search_results_text = tk.Text(user_manifest_frame, wrap="word", bg="#e0e0e0", fg="#333", relief="sunken", bd=1, font=("Arial", 9), height=5, state="disabled")
        self.search_results_text.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)


        # Patient Zero Principle Note for DataSyncPage
        patient_zero_note_label = ttk.Label(main_frame, text=(
            "Patient Zero Principle: I don't wipe users' asses; if you forgot your master password, die. "
            "When you don't regain access, and no one else does. I don't store any data; "
            "you yourselves must take care of how and where to save it and how to remember the password, "
            "because the password is the key to encrypting everything on your profile. Without it, no one has access."
            "\n\n**This note cannot be deleted and must remain unchanged in all document versions.**"
            "\n\n**LAG LMVL Sync: 'Your data, your sync. We're just the mechanism.'**"
            "\n⚠️ We are not responsible for data loss due to sync failures or incorrect settings. "
            "If the sync aggregator doesn't see that the operation was successful on our side, that's its problem. "
            "The result is what matters, not how."
            "\nPrinciple: we send, the higher platform invisibly confirms, we get confirmation, we don't care about the aggregator; the result is what matters, not how."
        ), font=("Arial", 9, "italic"), wraplength=1000, foreground="red")
        patient_zero_note_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")


    def _populate_file_trees(self):
        """Populates both local and cloud file treeviews."""
        self._clear_file_trees()

        # Local Storage
        for filename in os.listdir(self.local_storage_dir):
            filepath = os.path.join(self.local_storage_dir, filename)
            if os.path.isfile(filepath):
                file_stat = os.stat(filepath)
                file_size = f"{file_stat.st_size / 1024:.1f} KB"
                self.local_tree.insert("", "end", iid=filepath, text=filename, values=(file_size,))

        # Conceptual Cloud Storage
        for filename in os.listdir(self.conceptual_cloud_dir):
            filepath = os.path.join(self.conceptual_cloud_dir, filename)
            if os.path.isfile(filepath):
                file_stat = os.stat(filepath)
                file_size = f"{file_stat.st_size / 1024:.1f} KB"
                is_encrypted = "Yes" if filename.endswith(".enc") else "No"
                self.cloud_tree.insert("", "end", iid=filepath, text=filename, values=(file_size, is_encrypted))

    def _clear_file_trees(self):
        """Clears all items from both file treeviews."""
        for iid in self.local_tree.get_children():
            self.local_tree.delete(iid)
        for iid in self.cloud_tree.get_children():
            self.cloud_tree.delete(iid)

    def _create_conceptual_local_file(self):
        """Creates a new dummy text file in local storage."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = simpledialog.askstring("Create File", f"Enter a name for the new local file (e.g., my_doc_{timestamp}.txt):")
        if filename:
            filepath = os.path.join(self.local_storage_dir, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"This is a new conceptual file created on {timestamp}.\n")
                messagebox.showinfo("File Created", f"File '{filename}' successfully created in local storage.")
                self._populate_file_trees()
                self._log_sync_activity("Created local file", "success", f"File: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create file: {e}")
                self._log_sync_activity("Created local file", "failed", f"File: {filename}, Error: {e}")
        else:
            messagebox.showwarning("Cancelled", "File creation cancelled.")

    def _delete_file_conceptual(self, tree_widget, base_dir):
        """Deletes the selected file from the specified storage."""
        selected_items = tree_widget.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a file to delete.")
            return

        filepath_to_delete = selected_items[0]
        filename = os.path.basename(filepath_to_delete)

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete file '{filename}' from '{os.path.basename(base_dir)}'? "
                                                      "This action is irreversible. Remember: your ass is yours, not ours."):
            try:
                os.remove(filepath_to_delete)
                messagebox.showinfo("File Deleted", f"File '{filename}' successfully deleted.")
                self._populate_file_trees()
                self._log_sync_activity("Deleted file", "success", f"File: {filename} from {os.path.basename(base_dir)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {e}")
                self._log_sync_activity("Deleted file", "failed", f"File: {filename} from {os.path.basename(base_dir)}, Error: {e}")

    def _upload_file_conceptual(self):
        """Uploads the selected local file to conceptual cloud storage."""
        selected_items = self.local_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a file to upload from local storage.")
            return

        local_filepath = selected_items[0]
        filename = os.path.basename(local_filepath)

        encrypt_choice = messagebox.askyesno("Encryption", "Upload file to cloud with conceptual encryption?")

        target_filepath_in_cloud = os.path.join(self.conceptual_cloud_dir, filename)
        if encrypt_choice:
            target_filepath_in_cloud += ".enc"

        try:
            with open(local_filepath, 'rb') as f_read:
                content = f_read.read()

            if encrypt_choice and self.crypto_utils:
                encrypted_content = self.crypto_utils.encrypt_data(content, CONCEPTUAL_MASTER_KEY_FOR_SYNC)
                with open(target_filepath_in_cloud, 'wb') as f_write:
                    f_write.write(encrypted_content)
                messagebox.showinfo("Upload", f"File '{filename}' conceptually uploaded and encrypted to cloud.")
                self._log_sync_activity("Uploaded file (encrypted)", "success", f"File: {filename}")
            else:
                with open(target_filepath_in_cloud, 'wb') as f_write:
                    f_write.write(content)
                messagebox.showinfo("Upload", f"File '{filename}' conceptually uploaded to cloud (without encryption).")
                self._log_sync_activity("Uploaded file (unencrypted)", "success", f"File: {filename}")

            self._populate_file_trees()
        except Exception as e:
            messagebox.showerror("Upload Error", f"Failed to conceptually upload file: {e}")
            self._log_sync_activity("Uploaded file", "failed", f"File: {filename}, Error: {e}")

    def _download_file_conceptual(self):
        """Downloads the selected cloud file to conceptual local storage."""
        selected_items = self.cloud_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a file to download from cloud storage.")
            return

        cloud_filepath = selected_items[0]
        filename = os.path.basename(cloud_filepath)

        decrypt_choice = False
        if filename.endswith(".enc"):
            decrypt_choice = messagebox.askyesno("Decryption", "Download and conceptually decrypt file?")

        target_local_filepath = os.path.join(self.local_storage_dir, filename.replace(".enc", ""))

        try:
            with open(cloud_filepath, 'rb') as f_read:
                content = f_read.read()

            if decrypt_choice and filename.endswith(".enc") and self.crypto_utils:
                decrypted_content = self.crypto_utils.decrypt_data(content, CONCEPTUAL_MASTER_KEY_FOR_SYNC)
                if decrypted_content is None:
                    raise ValueError("Decryption failed. Invalid key or corrupted data.")
                with open(target_local_filepath, 'wb') as f_write:
                    f_write.write(decrypted_content)
                messagebox.showinfo("Download", f"File '{filename}' conceptually downloaded and decrypted to local storage.")
                self._log_sync_activity("Downloaded file (decrypted)", "success", f"File: {filename}")
            else:
                with open(target_local_filepath, 'wb') as f_write:
                    f_write.write(content)
                messagebox.showinfo("Download", f"File '{filename}' conceptually downloaded to local storage (without decryption).")
                self._log_sync_activity("Downloaded file (undecrypted)", "success", f"File: {filename}")

            self._populate_file_trees()
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to conceptually download file: {e}")
            self._log_sync_activity("Downloaded file", "failed", f"File: {filename}, Error: {e}")

    def _sync_all_to_cloud(self):
        """Conceptually synchronizes all local files to the cloud."""
        if not messagebox.askyesno("Synchronization", "Start conceptual synchronization: Local -> Cloud? "
                                                "Existing files in the cloud will be overwritten, new ones added."):
            return

        self._log_sync_activity("Starting sync: Local -> Cloud", "info")
        sync_count = 0
        for filename in os.listdir(self.local_storage_dir):
            local_filepath = os.path.join(self.local_storage_dir, filename)
            if os.path.isfile(local_filepath):
                target_filepath_in_cloud = os.path.join(self.conceptual_cloud_dir, filename + ".enc") # Always encrypt on full sync to cloud
                try:
                    with open(local_filepath, 'rb') as f_read:
                        content = f_read.read()

                    if self.crypto_utils:
                        encrypted_content = self.crypto_utils.encrypt_data(content, CONCEPTUAL_MASTER_KEY_FOR_SYNC)
                        with open(target_filepath_in_cloud, 'wb') as f_write:
                            f_write.write(encrypted_content)
                    else:
                        with open(target_filepath_in_cloud, 'wb') as f_write:
                            f_write.write(content)

                    sync_count += 1
                    self._log_sync_activity("Upload/Sync", "success", f"File: {filename} (to cloud)")
                except Exception as e:
                    self._log_sync_activity("Upload/Sync", "failed", f"File: {filename}, Error: {e}")

        self._populate_file_trees()
        messagebox.showinfo("Synchronization Complete", f"Conceptually synchronized {sync_count} files from local storage to cloud.")
        self._log_sync_activity("Finished sync: Local -> Cloud", "success", f"{sync_count} files")

    def _sync_all_to_local(self):
        """Conceptually synchronizes all cloud files to local storage."""
        if not messagebox.askyesno("Synchronization", "Start conceptual synchronization: Cloud -> Local? "
                                                "Existing files locally will be overwritten, new ones added."):
            return

        self._log_sync_activity("Starting sync: Cloud -> Local", "info")
        sync_count = 0
        for filename_cloud in os.listdir(self.conceptual_cloud_dir):
            cloud_filepath = os.path.join(self.conceptual_cloud_dir, filename_cloud)
            if os.path.isfile(cloud_filepath):
                target_local_filename = filename_cloud.replace(".enc", "") # Decrypt/rename
                target_local_filepath = os.path.join(self.local_storage_dir, target_local_filename)
                try:
                    with open(cloud_filepath, 'rb') as f_read:
                        content = f_read.read()

                    if filename_cloud.endswith(".enc") and self.crypto_utils:
                        decrypted_content = self.crypto_utils.decrypt_data(content, CONCEPTUAL_MASTER_KEY_FOR_SYNC)
                        if decrypted_content is None:
                            raise ValueError("Decryption failed during sync.")
                        with open(target_local_filepath, 'wb') as f_write:
                            f_write.write(decrypted_content)
                    else:
                        with open(target_local_filepath, 'wb') as f_write:
                            f_write.write(content)

                    sync_count += 1
                    self._log_sync_activity("Download/Sync", "success", f"File: {filename_cloud} (to local)")
                except Exception as e:
                    self._log_sync_activity("Download/Sync", "failed", f"File: {filename_cloud}, Error: {e}")

        self._populate_file_trees()
        messagebox.showinfo("Synchronization Complete", f"Conceptually synchronized {sync_count} files from cloud to local storage.")
        self._log_sync_activity("Finished sync: Cloud -> Local", "success", f"{sync_count} files")


    def _run_sync_audit(self):
        """Conceptually audits the synchronization status."""
        self._log_sync_activity("Starting sync audit", "info")
        self.sync_log_text.config(state="normal")
        self.sync_log_text.insert(tk.END, f"\n--- Synchronization Audit ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---\n")

        local_files = set(os.listdir(self.local_storage_dir))
        cloud_files_raw = set(os.listdir(self.conceptual_cloud_dir))

        # Adjust cloud files for encryption status for comparison
        cloud_files_normalized = set()
        for f in cloud_files_raw:
            cloud_files_normalized.add(f.replace(".enc", ""))

        missing_in_cloud = local_files - cloud_files_normalized
        missing_locally = cloud_files_normalized - local_files

        if not missing_in_cloud and not missing_locally:
            self.sync_log_text.insert(tk.END, "All files conceptually synchronized and match each other.\n")
        else:
            if missing_in_cloud:
                self.sync_log_text.insert(tk.END, "Files missing in cloud (local): " + ", ".join(missing_in_cloud) + "\n")
            if missing_locally:
                self.sync_log_text.insert(tk.END, "Files missing locally (in cloud): " + ", ".join(missing_locally) + "\n")
            self.sync_log_text.insert(tk.END, "Some files need synchronization.\n")

        # Simulate integrity check for encrypted files
        encrypted_files_in_cloud = [f for f in os.listdir(self.conceptual_cloud_dir) if f.endswith(".enc")]
        if encrypted_files_in_cloud and self.crypto_utils:
            self.sync_log_text.insert(tk.END, "Checking integrity of encrypted files in cloud...\n")
            for ef in encrypted_files_in_cloud:
                ef_path = os.path.join(self.conceptual_cloud_dir, ef)
                try:
                    with open(ef_path, 'rb') as f:
                        encrypted_content = f.read()
                    decrypted = self.crypto_utils.decrypt_data(encrypted_content, CONCEPTUAL_MASTER_KEY_FOR_SYNC)
                    if decrypted is None:
                        self.sync_log_text.insert(tk.END, f"  ⚠️ {ef}: Decryption error or data corruption.\n")
                    else:
                        self.sync_log_text.insert(tk.END, f"  ✅ {ef}: Integrity check passed.\n")
                except Exception as e:
                    self.sync_log_text.insert(tk.END, f"  ❌ {ef}: Error reading or checking: {e}.\n")

        self.sync_log_text.insert(tk.END, "--- Audit complete. ---\n\n")
        self.sync_log_text.see(tk.END)
        self.sync_log_text.config(state="disabled")
        self._log_sync_activity("Finished sync audit", "success")
        messagebox.showinfo("Synchronization Audit", "Conceptual synchronization audit complete. Check the log.")

    def _update_sync_log_display(self):
        """Refreshes the sync log display."""
        self.sync_log_text.config(state="normal")
        self.sync_log_text.delete("1.0", tk.END)
        for entry in self.sync_logs:
            self.sync_log_text.insert(tk.END, f"[{entry.get('timestamp')}] Action: {entry.get('action')} | Status: {entry.get('status')} | Details: {entry.get('details')}\n")
        self.sync_log_text.see(tk.END)
        self.sync_log_text.config(state="disabled")

    def _populate_user_manifest_tree(self):
        """NEW: Populates the user manifest treeview."""
        for iid in self.user_manifest_tree.get_children():
            self.user_manifest_tree.delete(iid)

        for user in self.user_manifest:
            self.user_manifest_tree.insert("", "end", iid=user["id"], values=(
                user.get("nickname", "N/A"),
                user.get("country", "N/A"),
                user.get("category", "N/A"),
                user.get("id", "N/A")
            ))

    def _generate_conceptual_user_id(self, nickname, category, country):
        """
        NEW: Generates a conceptual user ID based on provided criteria.
        For demonstration, this will combine parts to form a unique-ish ID.
        It tries to adhere to the spirit of "first number, last number, others don't repeat"
        by ensuring starts/ends with numbers and has a unique middle part for demo purposes,
        though full uniqueness check for 20 non-repeating characters is complex for conceptual.
        """
        # Generate a random 18-character string for the middle part
        middle_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=18))
        # Ensure first and last are numbers
        first_num = random.randint(0, 9)
        last_num = random.randint(0, 9)

        # Combine into a conceptual base ID (20 chars)
        base_id = f"{first_num}{middle_chars}{last_num}"

        # Combine with user data for a complex, unique ID string (as per user's example structure)
        # This will be longer than 20 chars due to concatenation
        unique_suffix = secrets.token_hex(4) # Add a small random part for uniqueness
        conceptual_id = f"{base_id}---{category.lower()}---{country.lower()}---'{nickname.lower()}'---{unique_suffix}"

        return conceptual_id

    def _add_conceptual_user(self):
        """NEW: Adds a new conceptual user to the manifest."""
        nickname = self.user_nickname_entry.get().strip()
        country = self.user_country_entry.get().strip()
        category = self.user_category_combobox.get().strip()

        if not nickname or not country or not category:
            messagebox.showwarning("Input Error", "All fields (Nickname, Country, Category) must be filled.")
            return

        # Check for existing nickname/country/category combination (simple check for demo)
        for user in self.user_manifest:
            if user.get("nickname") == nickname and \
               user.get("country") == country and \
               user.get("category") == category:
                messagebox.showwarning("User Exists", "A user with the same nickname, country, and category already exists.")
                return

        new_user_id = self._generate_conceptual_user_id(nickname, category, country)

        new_user_entry = {
            "id": new_user_id,
            "nickname": nickname,
            "country": country,
            "category": category
        }
        self.user_manifest.append(new_user_entry)
        self._save_user_manifest()
        self._populate_user_manifest_tree()
        self._log_sync_activity("Added conceptual user", "success", f"Nickname: {nickname}, ID: {new_user_id}")
        messagebox.showinfo("Success", f"Conceptual user '{nickname}' added with ID: {new_user_id}.")

        # Clear entries
        self.user_nickname_entry.delete(0, tk.END)
        self.user_country_entry.delete(0, tk.END)
        self.user_category_combobox.set("user")

    def _search_conceptual_users(self):
        """NEW: Searches for conceptual users in the manifest."""
        search_nickname = self.search_nickname_entry.get().strip().lower()
        search_country = self.search_country_entry.get().strip().lower()
        search_category = self.search_category_combobox.get().strip().lower()

        results = []
        for user in self.user_manifest:
            match = True
            if search_nickname and search_nickname not in user.get("nickname", "").lower():
                match = False
            if search_country and search_country not in user.get("country", "").lower():
                match = False
            if search_category and search_category != user.get("category", "").lower():
                match = False

            if match:
                results.append(user)

        self.search_results_text.config(state="normal")
        self.search_results_text.delete("1.0", tk.END)

        if results:
            self.search_results_text.insert(tk.END, "Found users:\n")
            for user in results:
                self.search_results_text.insert(tk.END, f"  Nickname: {user.get('nickname')}, Country: {user.get('country')}, Category: {user.get('category')}, ID: {user.get('id')}\n")
        else:
            self.search_results_text.insert(tk.END, "No users found matching the criteria.\n")

        self.search_results_text.config(state="disabled")
        self._log_sync_activity("Searched users", "info", f"Nickname: '{search_nickname}', Country: '{search_country}', Category: '{search_category}', Found: {len(results)}")


    def refresh_page(self):
        self._load_sync_logs() # Reload logs
        self._load_user_manifest() # NEW: Reload user manifest
        self._populate_file_trees() # Re-populate file lists
        self._update_sync_log_display() # Update log display
        self._populate_user_manifest_tree() # NEW: Update user manifest display


# This is the function the main App will call to set up the Data Synchronization tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    data_sync_page_instance = DataSyncPage(frame, app_data)
    return frame, data_sync_page_instance.refresh_page
