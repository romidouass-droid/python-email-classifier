import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext

from extract_email_text import extract_email_text
from api_classifier import classify_email


class EmailClassifierGUI:
    def __init__(self, root):
        self.root = root

        # Main window
        self.root.title("AI Email Classifier")
        self.root.geometry("800x650")
        self.root.minsize(700, 550)

        # Variables
        self.current_file = None
        self.current_email = ""
        self.current_result = ""

        # -----------------------------
        # Title
        # -----------------------------
        title_label = tk.Label(
            self.root,
            text="AI Email Classifier",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = tk.Label(
            self.root,
            text="Classify emails as Important or Normal",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=(0, 20))

        # -----------------------------
        # Upload button
        # -----------------------------
        self.upload_button = tk.Button(
            self.root,
            text="Upload Email File",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            command=self.upload_email
        )
        self.upload_button.pack(pady=10)

        # -----------------------------
        # File name
        # -----------------------------
        self.file_label = tk.Label(
            self.root,
            text="No email file selected",
            font=("Arial", 10)
        )
        self.file_label.pack(pady=5)

        # -----------------------------
        # Email preview label
        # -----------------------------
        preview_label = tk.Label(
            self.root,
            text="Email Preview",
            font=("Arial", 14, "bold")
        )
        preview_label.pack(anchor="w", padx=30, pady=(20, 5))

        # -----------------------------
        # Email preview box
        # -----------------------------
        self.email_text = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=15,
            font=("Arial", 11),
            wrap=tk.WORD
        )
        self.email_text.pack(
            padx=30,
            pady=5,
            fill=tk.BOTH,
            expand=True
        )

        # -----------------------------
        # Classification result
        # -----------------------------
        result_title = tk.Label(
            self.root,
            text="Classification Result",
            font=("Arial", 14, "bold")
        )
        result_title.pack(pady=(15, 5))

        self.result_label = tk.Label(
            self.root,
            text="Waiting for classification...",
            font=("Arial", 18, "bold")
        )
        self.result_label.pack(pady=5)

        # -----------------------------
        # Buttons
        # -----------------------------
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.classify_button = tk.Button(
            button_frame,
            text="Test Classification",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            command=self.test_classification
        )
        self.classify_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(
            button_frame,
            text="Save Result",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            command=self.save_result
        )
        self.save_button.grid(row=0, column=1, padx=10)

    # ==========================================================
    # Upload email
    # ==========================================================
    def upload_email(self):
        file_path = filedialog.askopenfilename(
            title="Select Email File",
            filetypes=[
                ("Email files", "*.eml"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return

        self.current_file = file_path

        try:
            email_content = extract_email_text(file_path)

            self.current_email = email_content

            self.email_text.delete("1.0", tk.END)
            self.email_text.insert(tk.END, email_content)

            self.file_label.config(
                text=f"Selected: {file_path.split('/')[-1]}"
            )

            self.result_label.config(
                text="Waiting for classification..."
            )

            self.current_result = ""

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not open the email file.\n\n{error}"
            )

    # ==========================================================
    # Classification (now connected to the real AI)
    # ==========================================================
    def test_classification(self):
        if not self.current_email:
            messagebox.showwarning(
                "No Email",
                "Please upload an email file first."
            )
            return

        try:
            result = classify_email(self.current_email)
            self.current_result = result
            self.display_result(result)

        except Exception as error:
            messagebox.showerror(
                "Classification Error",
                f"Could not classify the email.\n\n{error}"
            )

    # ==========================================================
    # Display result
    # ==========================================================
    def display_result(self, result):

        if result.lower() == "important":

            self.result_label.config(
                text="IMPORTANT",
                fg="red"
            )

        elif result.lower() == "normal":

            self.result_label.config(
                text="NORMAL",
                fg="green"
            )

        else:

            self.result_label.config(
                text=result,
                fg="black"
            )

    # ==========================================================
    # Save result
    # ==========================================================
    def save_result(self):
        import json
        from datetime import datetime

        if not self.current_email:
            messagebox.showwarning(
                "No Email",
                "Please upload an email first."
            )
            return

        if not self.current_result:
            messagebox.showwarning(
                "No Classification",
                "Please classify the email first."
            )
            return

        record = {
            "file": self.current_file,
            "result": self.current_result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open("../saved_results/history.json", "a") as f:
                f.write(json.dumps(record) + "\n")

            messagebox.showinfo(
                "Save Result",
                "Result saved successfully!"
            )

        except Exception as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the result.\n\n{error}"
            )


# ==============================================================
# Start application
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = EmailClassifierGUI(root)

    root.mainloop()