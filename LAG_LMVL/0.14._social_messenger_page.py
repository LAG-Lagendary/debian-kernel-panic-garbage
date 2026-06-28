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
import datetime
import secrets
import json

class SocialMessengerPage:
    def __init__(self, parent_frame, app_data):
        self.parent_frame = parent_frame
        self.app_data = app_data

        # Paths specific to Social & Messenger Page (now relative to project root)
        self.social_messenger_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "social_messenger_data")
        self.sm_keys_dir = os.path.join(self.social_messenger_data_dir, "keys")
        self.profiles_dir = os.path.join(self.social_messenger_data_dir, "profiles")
        self.chats_dir = os.path.join(self.social_messenger_data_dir, "chats")
        self.developer_chats_dir = os.path.join(self.social_messenger_data_dir, "developer_chats")
        self.message_log_file = os.path.join(self.social_messenger_data_dir, "message_activity.log")

        os.makedirs(self.sm_keys_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(self.chats_dir, exist_ok=True)
        os.makedirs(self.developer_chats_dir, exist_ok=True)

        self.sm_encryption_key = self._generate_or_load_encryption_key(os.path.join(self.sm_keys_dir, "social_messenger_encryption_key.txt"), self.sm_keys_dir, "Social Messenger")

        # Create dummy profile and chat if none exist
        self._create_dummy_profile("LAG_User")
        self._create_dummy_chat("LAG_User", "Admin")
        self._create_dummy_dev_chat("Developer_A", "DevChat_SecurityAudit")

        if not os.path.exists(self.message_log_file):
            with open(self.message_log_file, 'w', encoding='utf-8') as f:
                f.write(f"[{self._get_timestamp_short()}] Message activity log initialized.\n")

        self.current_chat_path = None
        self.selected_profile_path = None

        parent_frame.grid_columnconfigure(0, weight=1) # Left: Profile & Chat Selection
        parent_frame.grid_columnconfigure(1, weight=3) # Right: Chat / Message Area
        parent_frame.grid_rowconfigure(0, weight=1)

        # Left: Profile and Chat Selection
        sidebar_frame = ttk.Frame(parent_frame, relief="ridge", borderwidth=1)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        sidebar_frame.grid_rowconfigure(1, weight=1) # Treeview expands
        sidebar_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(sidebar_frame, text="Profiles and Chats", font=("Arial", 12, "bold")).pack(pady=5)
        self.social_tree = ttk.Treeview(sidebar_frame)
        self.social_tree.pack(expand=True, fill="both", padx=5, pady=5)
        ttk.Scrollbar(self.social_tree, orient="vertical", command=self.social_tree.yview).pack(side="right", fill="y")
        self.social_tree.config(yscrollcommand=self.social_tree.set)

        self.social_tree.bind("<<TreeviewSelect>>", self._on_social_tree_select)

        social_buttons_frame = ttk.Frame(sidebar_frame)
        social_buttons_frame.pack(fill=tk.X, pady=5)
        ttk.Button(social_buttons_frame, text="Add Profile (Concept)", command=self._add_profile_concept).pack(fill=tk.X, pady=2)
        ttk.Button(social_buttons_frame, text="Create Chat (Concept)", command=self._create_chat_concept).pack(fill=tk.X, pady=2)
        ttk.Button(social_buttons_frame, text="Show Activity Log", command=self._show_message_activity_log).pack(fill=tk.X, pady=2)
        ttk.Button(social_buttons_frame, text="Show Keys Folder", command=self._show_sm_keys_info).pack(fill=tk.X, pady=2)


        # Right: Chat/Message Area
        self.chat_area_notebook = ttk.Notebook(parent_frame)
        self.chat_area_notebook.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Main Chat Tab
        self.main_chat_frame = ttk.Frame(self.chat_area_notebook)
        self.chat_area_notebook.add(self.main_chat_frame, text="General Chat")
        self.main_chat_frame.grid_rowconfigure(0, weight=1)
        self.main_chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_display = tk.Text(self.main_chat_frame, wrap="word", bg="#f0f0f0", fg="#333", relief="sunken", bd=1, font=("Arial", 11))
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Scrollbar(self.main_chat_frame, orient="vertical", command=self.chat_display.yview).grid(row=0, column=1, sticky="ns")
        self.chat_display.config(yscrollcommand=self.chat_display.set, state="disabled")

        chat_input_frame = ttk.Frame(self.main_chat_frame)
        chat_input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        chat_input_frame.grid_columnconfigure(0, weight=1)
        self.message_entry = ttk.Entry(chat_input_frame, font=("Arial", 11))
        self.message_entry.grid(row=0, column=0, sticky="ew")
        self.message_entry.bind("<Return>", self._send_message_event)
        ttk.Button(chat_input_frame, text="Send", command=self._send_message).grid(row=0, column=1, padx=5)

        # Private/Encrypted Chat Tab
        self.private_chat_frame = ttk.Frame(self.chat_area_notebook)
        self.chat_area_notebook.add(self.private_chat_frame, text="Private Chat (Encrypted)")
        self.private_chat_frame.grid_rowconfigure(0, weight=1)
        self.private_chat_frame.grid_columnconfigure(0, weight=1)
        self.private_chat_display = tk.Text(self.private_chat_frame, wrap="word", bg="#222", fg="#0f0", relief="sunken", bd=1, font=("Arial", 11))
        self.private_chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Scrollbar(self.private_chat_frame, orient="vertical", command=self.private_chat_display.yview).grid(row=0, column=1, sticky="ns")
        self.private_chat_display.config(yscrollcommand=self.private_chat_display.set, state="disabled")

        private_chat_input_frame = ttk.Frame(self.private_chat_frame)
        private_chat_input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        private_chat_input_frame.grid_columnconfigure(0, weight=1)
        self.private_message_entry = ttk.Entry(private_chat_input_frame, font=("Arial", 11))
        self.private_message_entry.grid(row=0, column=0, sticky="ew")
        self.private_message_entry.bind("<Return>", self._send_private_message_event)
        ttk.Button(private_chat_input_frame, text="Send (Private)", command=self._send_private_message).grid(row=0, column=1, padx=5)

        # Developer Chat Tab
        self.developer_chat_frame = ttk.Frame(self.chat_area_notebook)
        self.chat_area_notebook.add(self.developer_chat_frame, text="Developer Chat (Audited)")
        self.developer_chat_frame.grid_rowconfigure(0, weight=1)
        self.developer_chat_frame.grid_columnconfigure(0, weight=1)
        self.developer_chat_display = tk.Text(self.developer_chat_frame, wrap="word", bg="#333", fg="#ff0", relief="sunken", bd=1, font=("Arial", 11))
        self.developer_chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Scrollbar(self.developer_chat_frame, orient="vertical", command=self.developer_chat_display.yview).grid(row=0, column=1, sticky="ns")
        self.developer_chat_display.config(yscrollcommand=self.developer_chat_display.set, state="disabled")

        dev_chat_input_frame = ttk.Frame(self.developer_chat_frame)
        dev_chat_input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        dev_chat_input_frame.grid_columnconfigure(0, weight=1)
        self.dev_message_entry = ttk.Entry(dev_chat_input_frame, font=("Arial", 11))
        self.dev_message_entry.grid(row=0, column=0, sticky="ew")
        self.dev_message_entry.bind("<Return>", self._send_dev_message_event)
        ttk.Button(dev_chat_input_frame, text="Send (Dev)", command=self._send_dev_message).grid(row=0, column=1, padx=5)

        self.refresh_page() # Initial population

    def _get_timestamp_short(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _get_timestamp_full(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _generate_or_load_encryption_key(self, key_file_path, key_dir, purpose_name):
        """Helper to generate/load encryption keys."""
        if os.path.exists(key_file_path):
            try:
                with open(key_file_path, 'r') as f:
                    key = f.read().strip()
                messagebox.showinfo("Security Information (Conceptual)", f"Loaded dummy encryption key for {purpose_name} from:\n{key_file_path}\n"
                                                     "This is FOR DEMONSTRATION ONLY and NOT secure for real data.")
                return key
            except Exception as e:
                messagebox.showerror("Key Load Error", f"Failed to load key for {purpose_name}: {e}")
                return None
        else:
            key = secrets.token_hex(64) # Longer key for better conceptual security (128 chars hex)
            try:
                os.makedirs(key_dir, exist_ok=True)
                with open(key_file_path, 'w', encoding='utf-8') as f:
                    f.write(key)
                messagebox.showinfo("Security Information (Conceptual)", f"Generated and saved new dummy encryption key for {purpose_name} to:\n{key_file_path}\n"
                                                     "This key is FOR DEMONSTRATION ONLY and NOT secure for real data.")
                return key
            except Exception as e:
                messagebox.showerror("Key Generation Error", f"Failed to save key for {purpose_name}: {e}\n"
                                                              f"Please ensure write permissions to {key_dir}.")
                return None

    def _log_message_activity(self, message_type, sender, recipient, content, status="sent"):
        """Logs message activity to a central log file."""
        log_entry = {
            "timestamp": self._get_timestamp_full(),
            "type": message_type, # e.g., "public_chat", "private_chat", "dev_chat"
            "sender": sender,
            "recipient": recipient,
            "content_preview": content[:50] + "..." if len(content) > 50 else content,
            "status": status
        }
        try:
            with open(self.message_log_file, 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n') # Newline for each JSON object
        except Exception as e:
            print(f"Error writing to message activity log: {e}")

    def _create_dummy_profile(self, username):
        profile_path = os.path.join(self.profiles_dir, f"{username}.json")
        if not os.path.exists(profile_path):
            profile_data = {
                "username": username,
                "status": "online",
                "last_active": self._get_timestamp_full(),
                "bio": f"This is a conceptual profile for user {username}."
            }
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=4, ensure_ascii=False)

    def _create_dummy_chat(self, user1, user2):
        chat_name = f"{user1}_{user2}"
        chat_file_path = os.path.join(self.chats_dir, f"{chat_name}.json")
        if not os.path.exists(chat_file_path):
            chat_data = [
                {"sender": user1, "timestamp": self._get_timestamp_full(), "message": f"Hello, {user2}!"},
                {"sender": user2, "timestamp": self._get_timestamp_full(), "message": f"Hi, {user1}! How are you?"}
            ]
            with open(chat_file_path, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, indent=4, ensure_ascii=False)

    def _create_dummy_dev_chat(self, user, chat_topic):
        dev_chat_file_path = os.path.join(self.developer_chats_dir, f"{chat_topic}.json")
        if not os.path.exists(dev_chat_file_path):
            dev_chat_data = [
                {"sender": user, "timestamp": self._get_timestamp_full(), "message": f"[{chat_topic}] Initiating system audit."},
                {"sender": "System_Auditor", "timestamp": self._get_timestamp_full(), "message": "Checking security function logging."}
            ]
            with open(dev_chat_file_path, 'w', encoding='utf-8') as f:
                json.dump(dev_chat_data, f, indent=4, ensure_ascii=False)

    def _populate_social_tree(self):
        for iid in self.social_tree.get_children():
            self.social_tree.delete(iid)

        profiles_root = self.social_tree.insert("", "end", text="Profiles", open=True, tags=('category'))
        chats_root = self.social_tree.insert("", "end", text="Chats", open=True, tags=('category'))
        dev_chats_root = self.social_tree.insert("", "end", text="Developer Chats", open=True, tags=('category'))

        if os.path.exists(self.profiles_dir):
            for filename in os.listdir(self.profiles_dir):
                if filename.endswith(".json"):
                    profile_name = os.path.splitext(filename)[0]
                    self.social_tree.insert(profiles_root, "end", text=profile_name, values=("profile", os.path.join(self.profiles_dir, filename)))

        if os.path.exists(self.chats_dir):
            for filename in os.listdir(self.chats_dir):
                if filename.endswith(".json"):
                    chat_name = os.path.splitext(filename)[0]
                    self.social_tree.insert(chats_root, "end", text=chat_name, values=("chat", os.path.join(self.chats_dir, filename)))

        if os.path.exists(self.developer_chats_dir):
            for filename in os.listdir(self.developer_chats_dir):
                if filename.endswith(".json"):
                    dev_chat_name = os.path.splitext(filename)[0]
                    self.social_tree.insert(dev_chats_root, "end", text=dev_chat_name, values=("dev_chat", os.path.join(self.developer_chats_dir, filename)))

        self.social_tree.tag_configure('category', font=('Arial', 10, 'bold'))

    def _on_social_tree_select(self, event):
        selected_item = self.social_tree.focus()
        if not selected_item:
            return

        item_values = self.social_tree.item(selected_item, "values")
        self.current_chat_path = None
        self.selected_profile_path = None

        if item_values:
            item_type = item_values[0]
            file_path = item_values[1]

            if item_type == "profile":
                self.selected_profile_path = file_path
                self._display_profile_info(file_path)
            elif item_type == "chat":
                self.current_chat_path = file_path
                self.chat_area_notebook.select(self.main_chat_frame)
                self._load_chat_messages(self.chat_display, file_path)
            elif item_type == "dev_chat":
                self.current_chat_path = file_path
                self.chat_area_notebook.select(self.developer_chat_frame)
                self._load_chat_messages(self.developer_chat_display, file_path)
        else: # Category selected
            self.chat_display.config(state="normal")
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.insert(tk.END, "Select a chat to view or a profile for details.")
            self.chat_display.config(state="disabled")
            self.private_chat_display.config(state="normal")
            self.private_chat_display.delete("1.0", tk.END)
            self.private_chat_display.insert(tk.END, "Select a chat to view or a profile for details.")
            self.private_chat_display.config(state="disabled")
            self.developer_chat_display.config(state="normal")
            self.developer_chat_display.delete("1.0", tk.END)
            self.developer_chat_display.insert(tk.END, "Select a chat to view or a profile for details.")
            self.developer_chat_display.config(state="disabled")

    def _display_profile_info(self, profile_path):
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.private_chat_display.config(state="normal")
        self.private_chat_display.delete("1.0", tk.END)
        self.developer_chat_display.config(state="normal")
        self.developer_chat_display.delete("1.0", tk.END)

        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)

            info = f"--- Profile: {profile_data.get('username', 'N/A')} ---\n" \
                   f"Status: {profile_data.get('status', 'N/A')}\n" \
                   f"Last Active: {profile_data.get('last_active', 'N/A')}\n" \
                   f"Bio: {profile_data.get('bio', 'N/A')}\n\n" \
                   f"Select a chat from the left list to start messaging."

            self.chat_display.insert(tk.END, info)
            self.private_chat_display.insert(tk.END, info)
            self.developer_chat_display.insert(tk.END, info)

        except Exception as e:
            self.chat_display.insert(tk.END, f"Error loading profile: {e}")
            self.private_chat_display.insert(tk.END, f"Error loading profile: {e}")
            self.developer_chat_display.insert(tk.END, f"Error loading profile: {e}")
        finally:
            self.chat_display.config(state="disabled")
            self.private_chat_display.config(state="disabled")
            self.developer_chat_display.config(state="disabled")


    def _load_chat_messages(self, text_widget, chat_file_path):
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        try:
            with open(chat_file_path, 'r', encoding='utf-8') as f:
                messages = json.load(f)

            for msg in messages:
                sender = msg.get("sender", "Unknown")
                timestamp = msg.get("timestamp", "N/A")
                message_content = msg.get("message", "")
                text_widget.insert(tk.END, f"[{self._get_timestamp_short()}] {sender}: {message_content}\n")

            text_widget.see(tk.END)
        except json.JSONDecodeError:
            text_widget.insert(tk.END, "Chat log is corrupted or empty.")
        except Exception as e:
            text_widget.insert(tk.END, f"Error loading chat messages: {e}")
        finally:
            text_widget.config(state="disabled")

    def _append_message_to_chat(self, text_widget, sender, message_content):
        text_widget.config(state="normal")
        text_widget.insert(tk.END, f"[{self._get_timestamp_short()}] {sender}: {message_content}\n")
        text_widget.see(tk.END)
        text_widget.config(state="disabled")

    def _save_message_to_chat_file(self, chat_file_path, sender, message_content):
        new_message = {
            "sender": sender,
            "timestamp": self._get_timestamp_full(),
            "message": message_content
        }
        try:
            with open(chat_file_path, 'r+', encoding='utf-8') as f:
                f.seek(0)
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append(new_message)
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Chat Save Error", f"Failed to save message to chat: {e}")

    def _send_message_event(self, event=None):
        self._send_message()

    def _send_message(self):
        message_content = self.message_entry.get().strip()
        self.message_entry.delete(0, tk.END)
        if not message_content:
            return
        if not self.current_chat_path:
            messagebox.showwarning("Error", "Select a chat to send a message.")
            return

        # Conceptual sender for public chat
        sender = "You"
        self._append_message_to_chat(self.chat_display, sender, message_content)
        self._save_message_to_chat_file(self.current_chat_path, sender, message_content)
        self._log_message_activity("public_chat", sender, os.path.basename(self.current_chat_path).replace(".json", ""), message_content)

        # Simulate response
        self.master.after(1000, lambda: self._append_message_to_chat(self.chat_display, "OtherUser", f"Echo: {message_content}"))
        self._log_message_activity("public_chat", "OtherUser", sender, f"Echo: {message_content}", status="received")


    def _send_private_message_event(self, event=None):
        self._send_private_message()

    def _send_private_message(self):
        message_content = self.private_message_entry.get().strip()
        self.private_message_entry.delete(0, tk.END)
        if not message_content:
            return
        if not self.current_chat_path:
            messagebox.showwarning("Error", "Select a chat to send a message.")
            return

        if not self.sm_encryption_key:
            messagebox.showerror("Error", "Encryption key unavailable. Cannot send private message.")
            return

        sender = "You (Encrypted)"
        encrypted_content = f"[Encrypted with {self.sm_encryption_key[:5]}...]: {message_content}" # Conceptual encryption
        self._append_message_to_chat(self.private_chat_display, sender, encrypted_content)
        self._save_message_to_chat_file(self.current_chat_path, sender, encrypted_content)
        self._log_message_activity("private_chat", sender, os.path.basename(self.current_chat_path).replace(".json", ""), message_content, status="encrypted_sent")

        # Simulate response
        self.master.after(1500, lambda: self._append_message_to_chat(self.private_chat_display, "Recipient (Decrypted)", f"[Decrypted]: Echo: {message_content}"))
        self._log_message_activity("private_chat", "Recipient (Decrypted)", sender, f"Echo: {message_content}", status="decrypted_received")

    def _send_dev_message_event(self, event=None):
        self._send_dev_message()

    def _send_dev_message(self):
        message_content = self.dev_message_entry.get().strip()
        self.dev_message_entry.delete(0, tk.END)
        if not message_content:
            return
        if not self.current_chat_path:
            messagebox.showwarning("Error", "Select a chat to send a message.")
            return

        sender = "DevUser (Audited)"
        self._append_message_to_chat(self.developer_chat_display, sender, message_content)
        self._save_message_to_chat_file(self.current_chat_path, sender, message_content)
        self._log_message_activity("dev_chat", sender, os.path.basename(self.current_chat_path).replace(".json", ""), message_content, status="audited_sent")

        # Simulate response
        self.master.after(1000, lambda: self._append_message_to_chat(self.developer_chat_display, "System_Auditor", f"Audit-Response: {message_content}"))
        self._log_message_activity("dev_chat", "System_Auditor", sender, f"Audit-Response: {message_content}", status="audited_received")


    def _add_profile_concept(self):
        messagebox.showinfo("Add Profile (Concept)",
                            "Adding a new profile is conceptual. In a real application, this "
                            "would require user registration, credential creation, and "
                            "secure storage of profile information.")

    def _create_chat_concept(self):
        messagebox.showinfo("Create Chat (Concept)",
                            "Creating a new chat is conceptual. In a real application, this "
                            "would require interaction with a messenger API (e.g., Telegram API), "
                            "chat initialization, and encryption key management for private conversations.")

    def _show_message_activity_log(self):
        if os.path.exists(self.message_log_file):
            try:
                content = []
                with open(self.message_log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            content.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue # Skip malformed lines

                display_text = "--- Message Activity Log ---\n\n"
                for entry in content:
                    display_text += f"[{entry.get('timestamp', 'N/A')}] Type: {entry.get('type', 'N/A')}, From: {entry.get('sender', 'N/A')}, To: {entry.get('recipient', 'N/A')}, Message: \"{entry.get('content_preview', 'N/A')}\", Status: {entry.get('status', 'N/A')}\n"

                messagebox.showinfo("Message Activity Log", display_text)
            except Exception as e:
                messagebox.showerror("Log Read Error", f"Failed to read message activity log: {e}")
        else:
            messagebox.showinfo("Activity Log", "Message activity log not found.")

    def _show_sm_keys_info(self):
        messagebox.showinfo(
            "Keys Folder (Social Networks & Messengers)",
            f"This directory ({self.sm_keys_dir}) is conceptually intended for storing "
            f"encryption keys used for private chats, and API keys for "
            "integration with social networks/messengers.\n\n"
            "⚠️ CRITICAL SECURITY WARNING: ⚠️\n"
            "Storing actual encryption keys or API keys in files without proper protection "
            "and a key management system is EXTREMELY DANGEROUS. This application is "
            "only a conceptual demonstration."
        )

    def refresh_page(self):
        self._populate_social_tree()
        # Reset chat displays if no specific chat is selected
        if not self.current_chat_path:
            for text_widget in [self.chat_display, self.private_chat_display, self.developer_chat_display]:
                text_widget.config(state="normal")
                text_widget.delete("1.0", tk.END)
                text_widget.insert(tk.END, "Select a chat to view messages, or a profile to view details.")
                text_widget.config(state="disabled")

# This is the function the main App will call to set up the Social Messenger tab
def setup_page(notebook, app_data):
    frame = ttk.Frame(notebook)
    social_messenger_page_instance = SocialMessengerPage(frame, app_data)
    return frame, social_messenger_page_instance.refresh_page
