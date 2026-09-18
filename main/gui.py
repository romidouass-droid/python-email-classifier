import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext

from extract_email_text import extract_email_text
from api_classifier import classify_email


class EmailClassifierGUI:

    def __init__(self, root):
        self.root = root

        # ==============================
        # Window
        # ==============================
        self.root.title("AI Email Classifier")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg="#F4F5FA")

        # ==============================
        # Variables
        # ==============================
        self.selected_files = []
        self.current_email = ""
        self.current_result = ""

        # ==============================
        # Sidebar
        # ==============================
        self.sidebar = tk.Frame(
            root,
            bg="#25253D",
            width=220
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Label(
            self.sidebar,
            text="✉",
            font=("Arial", 32, "bold"),
            bg="#25253D",
            fg="#8B7CFF"
        )
        logo.pack(pady=(35, 5))

        title = tk.Label(
            self.sidebar,
            text="AI Email\nClassifier",
            font=("Arial", 18, "bold"),
            bg="#25253D",
            fg="white",
            justify="center"
        )
        title.pack(pady=(0, 40))

        # Navigation
        self.create_navigation_button(
            "📧  Classify",
            self.show_classifier
        )

        self.create_navigation_button(
            "🕘  History",
            self.show_history
        )

        self.create_navigation_button(
            "⚙  Settings",
            self.show_settings
        )

        # Bottom text
        bottom_text = tk.Label(
            self.sidebar,
            text="Student Project",
            font=("Arial", 9),
            bg="#25253D",
            fg="#9999B0"
        )
        bottom_text.pack(
            side="bottom",
            pady=25
        )

        # ==============================
        # Main content
        # ==============================
        self.content = tk.Frame(
            root,
            bg="#F4F5FA"
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.show_classifier()

    # ==========================================================
    # Navigation button
    # ==========================================================

    def create_navigation_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg="#25253D",
            fg="#DADAEA",
            activebackground="#3B3B5C",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            pady=15,
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=10,
            pady=3
        )

    # ==========================================================
    # Clear page
    # ==========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ==========================================================
    # CLASSIFIER PAGE
    # ==========================================================

    def show_classifier(self):

        self.clear_content()

        # ------------------------------
        # Header
        # ------------------------------

        header = tk.Frame(
            self.content,
            bg="#F4F5FA"
        )
        header.pack(
            fill="x",
            padx=40,
            pady=(30, 10)
        )

        page_title = tk.Label(
            header,
            text="Email Classification",
            font=("Arial", 25, "bold"),
            bg="#F4F5FA",
            fg="#25253D"
        )
        page_title.pack(anchor="w")

        description = tk.Label(
            header,
            text="Upload your emails and classify them as Important or Normal.",
            font=("Arial", 11),
            bg="#F4F5FA",
            fg="#77778A"
        )
        description.pack(
            anchor="w",
            pady=(5, 0)
        )

        # ------------------------------
        # Upload Card
        # ------------------------------

        upload_card = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E0E1E8",
            highlightthickness=1
        )
        upload_card.pack(
            fill="x",
            padx=40,
            pady=15
        )

        upload_title = tk.Label(
            upload_card,
            text="Upload Emails",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#25253D"
        )
        upload_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        upload_description = tk.Label(
            upload_card,
            text="Select one or multiple .eml files.",
            font=("Arial", 10),
            bg="white",
            fg="#888899"
        )
        upload_description.pack(
            anchor="w",
            padx=25
        )

        # ONE upload button
        upload_button = tk.Button(
            upload_card,
            text="UPLOAD EMAILS",
            command=self.upload_emails,
            font=("Arial", 11, "bold"),
            bg="#6C5CE7",
            fg="white",
            activebackground="#5849C7",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2"
        )
        upload_button.pack(
            anchor="w",
            padx=25,
            pady=15
        )

        self.file_label = tk.Label(
            upload_card,
            text="No emails selected",
            font=("Arial", 9),
            bg="white",
            fg="#9999AA"
        )
        self.file_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ------------------------------
        # Email Preview Card
        # ------------------------------

        preview_card = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E0E1E8",
            highlightthickness=1
        )
        preview_card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        preview_title = tk.Label(
            preview_card,
            text="Email Preview",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#25253D"
        )
        preview_title.pack(
            anchor="w",
            padx=25,
            pady=(18, 8)
        )

        self.email_text = scrolledtext.ScrolledText(
            preview_card,
            font=("Arial", 10),
            bg="#FAFAFC",
            fg="#333344",
            wrap=tk.WORD,
            relief="flat",
            bd=0,
            padx=15,
            pady=15
        )
        self.email_text.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # ------------------------------
        # Classification Result
        # ------------------------------

        result_title = tk.Label(
            self.content,
            text="Classification Result",
            font=("Arial", 14, "bold"),
            bg="#F4F5FA",
            fg="#25253D"
        )
        result_title.pack(
            anchor="w",
            padx=40,
            pady=(10, 5)
        )

        # Large result box
        self.result_card = tk.Frame(
            self.content,
            bg="#ECECF3",
            highlightbackground="#D8D8E2",
            highlightthickness=1,
            height=110
        )
        self.result_card.pack(
            fill="x",
            padx=40,
            pady=(0, 15)
        )
        self.result_card.pack_propagate(False)

        self.result_label = tk.Label(
            self.result_card,
            text="WAITING FOR CLASSIFICATION",
            font=("Arial", 20, "bold"),
            bg="#ECECF3",
            fg="#888899"
        )
        self.result_label.pack(
            expand=True
        )

        # ------------------------------
        # Classify button
        # ------------------------------

        classify_button = tk.Button(
            self.content,
            text="CLASSIFY EMAILS",
            command=self.test_classification,
            font=("Arial", 11, "bold"),
            bg="#6C5CE7",
            fg="white",
            activebackground="#5849C7",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=11,
            cursor="hand2"
        )
        classify_button.pack(
            pady=5
        )

        # ------------------------------
        # Save button
        # ------------------------------

        save_button = tk.Button(
            self.content,
            text="SAVE RESULT",
            command=self.save_result,
            font=("Arial", 10, "bold"),
            bg="#25253D",
            fg="white",
            activebackground="#3B3B5C",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2"
        )
        save_button.pack(
            pady=(5, 25)
        )

    # ==========================================================
    # UPLOAD EMAILS
    # ==========================================================

    def upload_emails(self):

        file_paths = filedialog.askopenfilenames(
            title="Select Email Files",
            filetypes=[
                ("Email files", "*.eml"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if not file_paths:
            return

        self.selected_files = list(file_paths)

        self.email_text.delete(
            "1.0",
            tk.END
        )

        for index, file_path in enumerate(
            self.selected_files,
            start=1
        ):

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as file:

                    content = file.read()

                file_name = (
                    file_path
                    .replace("\\", "/")
                    .split("/")[-1]
                )

                self.email_text.insert(
                    tk.END,
                    f"========== EMAIL {index}: {file_name} ==========\n\n"
                )

                self.email_text.insert(
                    tk.END,
                    content
                )

                self.email_text.insert(
                    tk.END,
                    "\n\n"
                )

            except Exception as error:

                self.email_text.insert(
                    tk.END,
                    f"Error reading file:\n{error}\n\n"
                )

        # Update file information
        if len(self.selected_files) == 1:

            self.file_label.config(
                text="1 email selected",
                fg="#6C5CE7"
            )

        else:

            self.file_label.config(
                text=f"{len(self.selected_files)} emails selected",
                fg="#6C5CE7"
            )

        # Reset classification
        self.current_email = "emails selected"
        self.current_result = ""

        self.result_card.config(
            bg="#ECECF3"
        )

        self.result_label.config(
            text="READY FOR CLASSIFICATION",
            bg="#ECECF3",
            fg="#888899"
        )

    # ==========================================================
    # TEMPORARY CLASSIFICATION
    # ==========================================================

    def test_classification(self):

        if not self.selected_files:

            messagebox.showwarning(
                "No Emails",
                "Please upload at least one email first."
            )

            return

        # Temporary result.
        # Task 3 will replace this with the real AI classifier.

        self.current_result = "Important"

        self.display_result(
            self.current_result
        )

    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    def display_result(self, result):

        if result.lower() == "important":

            self.result_card.config(
                bg="#FFE8E8"
            )

            self.result_label.config(
                text="IMPORTANT",
                bg="#FFE8E8",
                fg="#D63031"
            )

        elif result.lower() == "normal":

            self.result_card.config(
                bg="#E8F8EF"
            )

            self.result_label.config(
                text="NORMAL",
                bg="#E8F8EF",
                fg="#219653"
            )

        else:

            self.result_card.config(
                bg="#ECECF3"
            )

            self.result_label.config(
                text=result.upper(),
                bg="#ECECF3",
                fg="#333344"
            )

    # ==========================================================
    # SAVE RESULT
    # ==========================================================

    def save_result(self):

        if not self.selected_files:

            messagebox.showwarning(
                "No Emails",
                "Please upload an email first."
            )

            return

        if not self.current_result:

            messagebox.showwarning(
                "No Classification",
                "Please classify the email first."
            )

            return

        messagebox.showinfo(
            "Save Result",
            "The Save Result function is ready.\n\n"
            "Task 5 will connect the JSON saving system."
        )

    # ==========================================================
    # HISTORY PAGE
    # ==========================================================

    def show_history(self):

        self.clear_content()

        title = tk.Label(
            self.content,
            text="Saved History",
            font=("Arial", 25, "bold"),
            bg="#F4F5FA",
            fg="#25253D"
        )
        title.pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        description = tk.Label(
            self.content,
            text="View previously classified emails.",
            font=("Arial", 11),
            bg="#F4F5FA",
            fg="#77778A"
        )
        description.pack(
            anchor="w",
            padx=40
        )

        history_card = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E0E1E8",
            highlightthickness=1
        )
        history_card.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=25
        )

        empty_label = tk.Label(
            history_card,
            text="No saved emails yet.",
            font=("Arial", 14),
            bg="white",
            fg="#9999AA"
        )
        empty_label.pack(
            expand=True
        )

    # ==========================================================
    # SETTINGS PAGE
    # ==========================================================

    def show_settings(self):

        self.clear_content()

        title = tk.Label(
            self.content,
            text="Settings",
            font=("Arial", 25, "bold"),
            bg="#F4F5FA",
            fg="#25253D"
        )
        title.pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        description = tk.Label(
            self.content,
            text="Customize your email classification categories.",
            font=("Arial", 11),
            bg="#F4F5FA",
            fg="#77778A"
        )
        description.pack(
            anchor="w",
            padx=40
        )

        settings_card = tk.Frame(
            self.content,
            bg="white",
            highlightbackground="#E0E1E8",
            highlightthickness=1
        )
        settings_card.pack(
            fill="x",
            padx=40,
            pady=25
        )

        important_label = tk.Label(
            settings_card,
            text="Important categories",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#25253D"
        )
        important_label.pack(
            anchor="w",
            padx=25,
            pady=(25, 8)
        )

        important_entry = tk.Entry(
            settings_card,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        important_entry.pack(
            fill="x",
            padx=25,
            ipady=8
        )

        important_hint = tk.Label(
            settings_card,
            text="Example: exams, university, work, meetings",
            font=("Arial", 9),
            bg="white",
            fg="#9999AA"
        )
        important_hint.pack(
            anchor="w",
            padx=25,
            pady=(5, 20)
        )

        normal_label = tk.Label(
            settings_card,
            text="Normal categories",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#25253D"
        )
        normal_label.pack(
            anchor="w",
            padx=25,
            pady=(5, 8)
        )

        normal_entry = tk.Entry(
            settings_card,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        normal_entry.pack(
            fill="x",
            padx=25,
            ipady=8
        )

        normal_hint = tk.Label(
            settings_card,
            text="Example: advertisements, newsletters, promotions",
            font=("Arial", 9),
            bg="white",
            fg="#9999AA"
        )
        normal_hint.pack(
            anchor="w",
            padx=25,
            pady=(5, 25)
        )

        save_settings = tk.Button(
            settings_card,
            text="SAVE SETTINGS",
            command=lambda: messagebox.showinfo(
                "Settings",
                "Settings interface is ready.\n"
                "It can be connected to the classifier later."
            ),
            font=("Arial", 10, "bold"),
            bg="#6C5CE7",
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        save_settings.pack(
            anchor="w",
            padx=25,
            pady=(0, 25)
        )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = EmailClassifierGUI(root)

    root.mainloop()