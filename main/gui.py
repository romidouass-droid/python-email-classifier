import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime, date
import calendar
import os
import re

from extract_email_text import extract_email_text
from api_classifier import classify_email
from reply_generator import generate_reply


class EmailClassifierGUI:

    LAVENDER = "#BBB7E5"
    LIGHT_ROSE = "#F7DFDF"
    BABY_PINK = "#EFBDDB"
    PISTACHIO = "#B6C687"
    SNOW = "#DAE9FA"
    PALE_YELLOW = "#F3EDBD"

    DEADLINE_GREEN = "#E4EBCF"
    DEADLINE_YELLOW = "#F8F3D7"
    DEADLINE_ORANGE = "#F9DCC7"
    DEADLINE_RED = "#F7C9D2"

    CREAM = "#FFFDFB"
    WHITE = "#FFFFFF"
    DARK_PURPLE = "#57527F"
    SOFT_PURPLE = "#7771A8"
    TEXT = "#514C69"
    LIGHT_TEXT = "#9691AD"

    def __init__(self, root):

        self.root = root
        self.root.title("AI Email Classifier 鈾�")
        self.root.geometry("1250x800")
        self.root.minsize(1050, 700)
        self.root.configure(bg=self.CREAM)

        self.selected_files = []
        self.emails = []
        self.notes = []
        self.personal_notes = []
        self.deadlines = []
        self.current_result = ""
        self.selected_email = None

        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        self.create_sidebar()

        self.content = tk.Frame(root, bg=self.CREAM)
        self.content.pack(side="left", fill="both", expand=True)

        self.show_classifier()

    def create_sidebar(self):

        self.sidebar = tk.Frame(self.root, bg=self.LAVENDER, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="鈾�", font=("Arial", 38, "bold"),
            bg=self.LAVENDER, fg=self.DARK_PURPLE
        ).pack(pady=(30, 0))

        tk.Label(
            self.sidebar, text="AI Email\nClassifier", font=("Arial", 20, "bold"),
            bg=self.LAVENDER, fg=self.DARK_PURPLE, justify="center"
        ).pack(pady=(0, 8))

        tk.Label(
            self.sidebar, text="Smart inbox 鈾nOrganized mind", font=("Arial", 9),
            bg=self.LAVENDER, fg=self.SOFT_PURPLE, justify="center"
        ).pack(pady=(0, 30))

        self.create_navigation_button("鈾�  Classify", self.show_classifier)
        self.create_navigation_button("鈼�  History", self.show_history)
        self.create_navigation_button("鉁�  My Notes", self.show_notes)

        tk.Label(
            self.sidebar, text="馃尫  馃尭\n  馃尲  馃尫\n馃尭  馃尶  馃尭", font=("Arial", 19),
            bg=self.LAVENDER, fg=self.DARK_PURPLE
        ).pack(side="bottom", pady=20)

        tk.Label(
            self.sidebar, text="You got this,\ngirl 鈾�", font=("Arial", 13, "italic"),
            bg=self.LAVENDER, fg=self.DARK_PURPLE, justify="center"
        ).pack(side="bottom", pady=(0, 5))

    def create_navigation_button(self, text, command):

        button = tk.Button(
            self.sidebar, text=text, command=command, font=("Arial", 11, "bold"),
            bg=self.LAVENDER, fg=self.DARK_PURPLE, activebackground=self.LIGHT_ROSE,
            activeforeground=self.DARK_PURPLE, relief="flat", bd=0, anchor="w",
            padx=30, pady=14, cursor="hand2"
        )
        button.pack(fill="x", padx=12, pady=3)

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle):

        header = tk.Frame(
            self.content, bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK, highlightthickness=1
        )
        header.pack(fill="x", padx=30, pady=(25, 12))

        left = tk.Frame(header, bg=self.LIGHT_ROSE)
        left.pack(side="left", padx=25, pady=17)

        tk.Label(
            left, text=title + " 鈾�", font=("Arial", 23, "bold"),
            bg=self.LIGHT_ROSE, fg=self.DARK_PURPLE
        ).pack(anchor="w")

        tk.Label(
            left, text=subtitle, font=("Arial", 10),
            bg=self.LIGHT_ROSE, fg=self.SOFT_PURPLE
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            header, text="馃尫  馃尭  馃尲", font=("Arial", 24), bg=self.LIGHT_ROSE
        ).pack(side="right", padx=25)

    def show_classifier(self):

        self.clear_content()
        self.create_header(
            "Email Classification",
            "Upload your emails and let your little AI assistant organize them 鈾�"
        )

        main = tk.Frame(self.content, bg=self.CREAM)
        main.pack(fill="both", expand=True, padx=30, pady=5)

        left = tk.Frame(main, bg=self.CREAM)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = tk.Frame(main, bg=self.CREAM, width=340)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.pack_propagate(False)

        self.create_upload_card(left)
        self.create_email_card(left)

        self.create_result_card(right)
        self.create_calendar_card(right)

    def create_upload_card(self, parent):

        card = tk.Frame(
            parent, bg=self.WHITE,
            highlightbackground=self.LAVENDER, highlightthickness=1
        )
        card.pack(fill="x", pady=(0, 10))

        tk.Label(
            card, text="馃摛  Upload Emails", font=("Arial", 14, "bold"),
            bg=self.WHITE, fg=self.DARK_PURPLE
        ).pack(anchor="w", padx=22, pady=(17, 3))

        tk.Label(
            card, text="Select one or multiple .eml files", font=("Arial", 9),
            bg=self.WHITE, fg=self.LIGHT_TEXT
        ).pack(anchor="w", padx=22)

        tk.Button(
            card, text="鈾�  CHOOSE EMAILS", command=self.upload_emails,
            font=("Arial", 10, "bold"), bg=self.LAVENDER, fg=self.DARK_PURPLE,
            activebackground=self.BABY_PINK, relief="flat", bd=0,
            padx=25, pady=10, cursor="hand2"
        ).pack(anchor="w", padx=22, pady=12)

        self.file_label = tk.Label(
            card, text="No emails selected yet 鈾�", font=("Arial", 9),
            bg=self.WHITE, fg=self.LIGHT_TEXT
        )
        self.file_label.pack(anchor="w", padx=22, pady=(0, 15))

    def create_email_card(self, parent):

        card = tk.Frame(
            parent, bg=self.WHITE,
            highlightbackground=self.LAVENDER, highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        header_row = tk.Frame(card, bg=self.WHITE)
        header_row.pack(fill="x", padx=22, pady=(15, 5))

        tk.Label(
            header_row, text="馃拰  Your Emails", font=("Arial", 14, "bold"),
            bg=self.WHITE, fg=self.DARK_PURPLE
        ).pack(side="left")

        tk.Button(
            header_row, text="馃挰  AI Reply", command=self.open_reply_window,
            font=("Arial", 9, "bold"), bg=self.SNOW, fg=self.DARK_PURPLE,
            activebackground=self.LAVENDER, activeforeground=self.DARK_PURPLE,
            relief="flat", bd=0, padx=16, pady=6, cursor="hand2"
        ).pack(side="right")

        tk.Button(
            card, text="鉁�  CLASSIFY EMAILS", command=self.test_classification,
            font=("Arial", 11, "bold"), bg=self.BABY_PINK, fg=self.DARK_PURPLE,
            activebackground=self.LAVENDER, activeforeground=self.DARK_PURPLE,
            relief="flat", bd=0, padx=30, pady=11, cursor="hand2"
        ).pack(anchor="w", padx=22, pady=(0, 10))

        # List of uploaded emails 鈥� click one to see its own result
        self.email_listbox = tk.Listbox(
            card, font=("Arial", 9), bg="#FFFBFD", fg=self.TEXT,
            relief="flat", height=5,
            selectbackground=self.BABY_PINK, selectforeground=self.DARK_PURPLE
        )
        self.email_listbox.pack(fill="x", padx=20, pady=(0, 8))
        self.email_listbox.bind("<<ListboxSelect>>", self.on_email_select)

        self.email_text = scrolledtext.ScrolledText(
            card, font=("Arial", 9), bg="#FFFBFD", fg=self.TEXT,
            wrap=tk.WORD, relief="flat", bd=0, padx=12, pady=12
        )
        self.email_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    def create_result_card(self, parent):

        self.result_card = tk.Frame(
            parent, bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK, highlightthickness=1
        )
        self.result_card.pack(fill="x", pady=(0, 10))

        tk.Label(
            self.result_card, text="鉁�  Classification Result",
            font=("Arial", 13, "bold"), bg=self.LIGHT_ROSE, fg=self.DARK_PURPLE
        ).pack(anchor="w", padx=20, pady=(15, 10))

        self.result_label = tk.Label(
            self.result_card, text="WAITING 鈾�", font=("Arial", 19, "bold"),
            bg=self.LIGHT_ROSE, fg=self.SOFT_PURPLE
        )
        self.result_label.pack(pady=12)

        self.result_description = tk.Label(
            self.result_card,
            text="Classify your emails to see\nwhat needs your attention.",
            font=("Arial", 9), bg=self.LIGHT_ROSE, fg=self.SOFT_PURPLE, justify="center"
        )
        self.result_description.pack(pady=(0, 12))

        tk.Button(
            self.result_card, text="鈾�  SAVE RESULT", command=self.save_result,
            font=("Arial", 9, "bold"), bg=self.WHITE, fg=self.DARK_PURPLE,
            relief="flat", bd=0, padx=20, pady=8, cursor="hand2"
        ).pack(pady=(0, 17))

    def create_calendar_card(self, parent):

        card = tk.Frame(
            parent, bg=self.WHITE,
            highlightbackground=self.PISTACHIO, highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        tk.Label(
            card, text="馃搮  My Calendar", font=("Arial", 13, "bold"),
            bg=self.WHITE, fg=self.DARK_PURPLE
        ).pack(anchor="w", padx=18, pady=(15, 5))

        tk.Label(
            card, text="Your email deadlines appear here 鈾�", font=("Arial", 8),
            bg=self.WHITE, fg=self.LIGHT_TEXT
        ).pack(anchor="w", padx=18, pady=(0, 5))

        self.calendar_frame = tk.Frame(card, bg=self.WHITE)
        self.calendar_frame.pack(fill="both", expand=True, padx=10, pady=3)

        self.draw_calendar()

        tk.Label(
            card,
            text="馃煝 Plenty of time   馃煛 Getting closer\n馃煚 Very soon   馃敶 Deadline / overdue",
            font=("Arial", 8), bg=self.WHITE, fg=self.SOFT_PURPLE, justify="center"
        ).pack(pady=(4, 15))

    def draw_calendar(self):

        if not hasattr(self, "calendar_frame"):
            return

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        navigation = tk.Frame(self.calendar_frame, bg=self.WHITE)
        navigation.pack(fill="x", pady=3)

        tk.Button(
            navigation, text="鈥�", command=self.previous_month,
            font=("Arial", 14, "bold"), bg=self.WHITE, fg=self.DARK_PURPLE,
            relief="flat", bd=0, cursor="hand2"
        ).pack(side="left")

        month_name = calendar.month_name[self.current_month]

        tk.Label(
            navigation, text=f"{month_name} {self.current_year}",
            font=("Arial", 10, "bold"), bg=self.WHITE, fg=self.DARK_PURPLE
        ).pack(side="left", expand=True)

        tk.Button(
            navigation, text="鈥�", command=self.next_month,
            font=("Arial", 14, "bold"), bg=self.WHITE, fg=self.DARK_PURPLE,
            relief="flat", bd=0, cursor="hand2"
        ).pack(side="right")

        week_frame = tk.Frame(self.calendar_frame, bg=self.WHITE)
        week_frame.pack(fill="x")

        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        for column, day_name in enumerate(weekdays):
            tk.Label(
                week_frame, text=day_name, font=("Arial", 8, "bold"),
                bg=self.WHITE, fg=self.SOFT_PURPLE
            ).grid(row=0, column=column, sticky="nsew")
            week_frame.columnconfigure(column, weight=1)

        month_days = calendar.monthcalendar(self.current_year, self.current_month)

        for row_index, week in enumerate(month_days, start=1):
            week_frame.rowconfigure(row_index, weight=1)

            for column, day_number in enumerate(week):
                if day_number == 0:
                    continue

                current_date = date(self.current_year, self.current_month, day_number)
                background = self.get_calendar_color(current_date)
                text = str(day_number)

                if current_date in self.deadlines:
                    text = "鈥n" + str(day_number)

                button = tk.Button(
                    week_frame, text=text, font=("Arial", 7, "bold"),
                    bg=background, fg=self.DARK_PURPLE,
                    activebackground=self.BABY_PINK, relief="flat", bd=0,
                    width=4, height=2, cursor="hand2"
                )
                button.grid(row=row_index, column=column, padx=2, pady=2, sticky="nsew")

    def get_calendar_color(self, current_date):

        if current_date in self.deadlines:
            days_left = (current_date - date.today()).days

            if days_left <= 0:
                return self.DEADLINE_RED
            elif days_left <= 2:
                return self.DEADLINE_ORANGE
            elif days_left <= 5:
                return self.DEADLINE_YELLOW
            else:
                return self.DEADLINE_GREEN

        if current_date == date.today():
            return self.SNOW

        return self.WHITE

    def previous_month(self):

        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

        self.draw_calendar()

    def next_month(self):

        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

        self.draw_calendar()

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
        self.emails = []
        self.deadlines = []
        self.selected_email = None

        self.email_text.delete("1.0", tk.END)
        self.email_listbox.delete(0, tk.END)

        for index, file_path in enumerate(self.selected_files, start=1):

            try:
                content = extract_email_text(file_path)
                file_name = os.path.basename(file_path)

                email = {
                    "name": file_name,
                    "content": content,
                    "classification": "",
                    "note": ""
                }

                self.emails.append(email)
                self.email_listbox.insert(tk.END, file_name)

                self.email_text.insert(tk.END, "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣\n")
                self.email_text.insert(tk.END, f"馃拰 EMAIL {index}: {file_name}\n")
                self.email_text.insert(tk.END, "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣\n\n")
                self.email_text.insert(tk.END, content)
                self.email_text.insert(tk.END, "\n\n")

                self.detect_deadlines(content)

            except Exception as error:
                self.email_text.insert(tk.END, f"Error reading file:\n{error}\n\n")

        if len(self.selected_files) == 1:
            self.file_label.config(text="鈾� 1 email selected", fg=self.DARK_PURPLE)
        else:
            self.file_label.config(
                text=f"鈾� {len(self.selected_files)} emails selected",
                fg=self.DARK_PURPLE
            )

        self.current_result = ""

        self.result_label.config(text="READY 鈾�", bg=self.LIGHT_ROSE, fg=self.SOFT_PURPLE)
        self.result_description.config(
            text="Your emails are ready.\nLet's see what needs your attention.",
            bg=self.LIGHT_ROSE
        )
        self.result_card.config(bg=self.LIGHT_ROSE)

        self.draw_calendar()

    def detect_deadlines(self, content):

        found_dates = []

        matches = re.findall(r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b", content)
        for year, month, day in matches:
            try:
                found_dates.append(date(int(year), int(month), int(day)))
            except ValueError:
                pass

        matches = re.findall(r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b", content)
        for day, month, year in matches:
            try:
                found_dates.append(date(int(year), int(month), int(day)))
            except ValueError:
                pass

        month_names = (
            "January|February|March|April|May|June|July|"
            "August|September|October|November|December"
        )

        matches = re.findall(
            rf"\b(\d{{1,2}})\s+({month_names})(?:\s+(20\d{{2}}))?\b",
            content, re.IGNORECASE
        )

        month_numbers = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }

        for day, month_name, year in matches:
            try:
                month = month_numbers[month_name.lower()]
                selected_year = int(year) if year else datetime.now().year
                found_dates.append(date(selected_year, month, int(day)))
            except (ValueError, KeyError):
                pass

        matches = re.findall(
            rf"\b({month_names})\s+(\d{{1,2}})(?:,\s*|\s+)(20\d{{2}})?\b",
            content, re.IGNORECASE
        )

        for month_name, day, year in matches:
            try:
                month = month_numbers[month_name.lower()]
                selected_year = int(year) if year else datetime.now().year
                found_dates.append(date(selected_year, month, int(day)))
            except (ValueError, KeyError):
                pass

        deadline_words = [
            "deadline", "due", "submit", "submission", "exam",
            "assignment", "project", "final", "application", "registration"
        ]

        content_lower = content.lower()
        has_deadline_context = any(word in content_lower for word in deadline_words)

        if has_deadline_context:
            for found_date in found_dates:
                if found_date not in self.deadlines:
                    self.deadlines.append(found_date)

    def test_classification(self):

        if not self.selected_files:
            messagebox.showwarning(
                "No Emails 鈾�",
                "Please upload at least one email first."
            )
            return

        self.email_text.delete("1.0", tk.END)

        results = []

        for index, email in enumerate(self.emails, start=1):

            try:
                result = classify_email(email["content"])
                email["classification"] = result
                results.append(result)

            except Exception as error:
                messagebox.showerror(
                    "Classification Error",
                    f"Could not classify {email['name']}.\n\n{error}"
                )
                return

            self.email_text.insert(tk.END, "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣\n")
            self.email_text.insert(
                tk.END, f"馃拰 EMAIL {index}: {email['name']} 鈥� {result.upper()}\n"
            )
            self.email_text.insert(tk.END, "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣\n\n")
            self.email_text.insert(tk.END, email["content"])
            self.email_text.insert(tk.END, "\n\n")

        if "Important" in results:
            self.current_result = "Important"
        else:
            self.current_result = "Normal"

        self.display_result(self.current_result)

    def on_email_select(self, event):
        """Show the result for whichever email is clicked in the list."""

        selection = self.email_listbox.curselection()

        if not selection:
            return

        index = selection[0]
        email = self.emails[index]
        self.selected_email = email

        self.email_text.delete("1.0", tk.END)
        self.email_text.insert(tk.END, email["content"])

        if email.get("classification"):
            self.display_result(email["classification"])
        else:
            self.result_label.config(
                text="NOT CLASSIFIED YET 鈾�",
                bg=self.LIGHT_ROSE,
                fg=self.SOFT_PURPLE
            )
            self.result_description.config(
                text="Click 'CLASSIFY EMAILS' first.",
                bg=self.LIGHT_ROSE
            )
            self.result_card.config(bg=self.LIGHT_ROSE)

    def display_result(self, result):

        if result.lower() == "important":
            background = self.LIGHT_ROSE
            self.result_label.config(text="馃挆 IMPORTANT", bg=background, fg="#C44F76")
            self.result_description.config(
                text="These emails may contain\ndeadlines or important information.",
                bg=background
            )
        else:
            background = "#EEF5E6"
            self.result_label.config(text="馃尶 NORMAL", bg=background, fg="#65804A")
            self.result_description.config(
                text="Nothing urgent detected.\nYou can check these when you have time.",
                bg=background
            )

        self.result_card.config(bg=background)

    def save_result(self):

        if not self.selected_files:
            messagebox.showwarning("No Emails 鈾�", "Please upload an email first.")
            return

        if not self.current_result:
            messagebox.showwarning(
                "No Classification 鈾�",
                "Please classify the emails first."
            )
            return

        for email in self.emails:
            email["classification"] = self.current_result

        messagebox.showinfo(
            "Saved 鈾�",
            "Your classification has been saved!\n\nYou can view it in History."
        )

    # ---------------------------------------------------------------
    # AI Reply window
    # ---------------------------------------------------------------

    def open_reply_window(self):
        """Open a small popup where the user types a few short words and
        the AI turns them into a full email reply."""

        if not self.selected_email:
            messagebox.showwarning(
                "No Email Selected 鈾�",
                "Please click on an email in the list first."
            )
            return

        email = self.selected_email

        reply_window = tk.Toplevel(self.root)
        reply_window.title("AI Reply 鈾�")
        reply_window.geometry("560x650")
        reply_window.minsize(480, 560)
        reply_window.configure(bg=self.CREAM)

        reply_window.grid_rowconfigure(4, weight=1)
        reply_window.grid_columnconfigure(0, weight=1)

        # --- Header ---
        tk.Label(
            reply_window, text="馃挰  AI Reply", font=("Arial", 18, "bold"),
            bg=self.CREAM, fg=self.DARK_PURPLE
        ).grid(row=0, column=0, sticky="w", padx=30, pady=(22, 2))

        tk.Label(
            reply_window, text="Replying to: " + email.get("name", "this email"),
            font=("Arial", 9), bg=self.CREAM, fg=self.LIGHT_TEXT,
            wraplength=480, justify="left"
        ).grid(row=1, column=0, sticky="w", padx=30, pady=(0, 15))

        # --- Quick reply notes card ---
        notes_card = tk.Frame(
            reply_window, bg=self.WHITE,
            highlightbackground=self.LAVENDER, highlightthickness=1
        )
        notes_card.grid(row=2, column=0, sticky="ew", padx=30)

        tk.Label(
            notes_card, text="鉁�  Quick reply notes", font=("Arial", 11, "bold"),
            bg=self.WHITE, fg=self.DARK_PURPLE
        ).pack(anchor="w", padx=16, pady=(12, 2))

        tk.Label(
            notes_card,
            text="A few short words, e.g. \"yes tomorrow works, send location\"",
            font=("Arial", 8), bg=self.WHITE, fg=self.LIGHT_TEXT
        ).pack(anchor="w", padx=16, pady=(0, 8))

        notes_entry = tk.Text(
            notes_card, font=("Arial", 10), bg="#FFFBFD", fg=self.TEXT,
            relief="flat", bd=0, height=3, wrap=tk.WORD, padx=10, pady=8
        )
        notes_entry.pack(fill="x", padx=14, pady=(0, 14))

        # --- Generate button ---
        status_label = tk.Label(
            reply_window, text="", font=("Arial", 9, "italic"),
            bg=self.CREAM, fg=self.SOFT_PURPLE
        )
        status_label.grid(row=3, column=0, pady=(10, 0))

        # --- Generated reply card ---
        reply_card = tk.Frame(
            reply_window, bg=self.WHITE,
            highlightbackground=self.BABY_PINK, highlightthickness=1
        )
        reply_card.grid(row=4, column=0, sticky="nsew", padx=30, pady=(10, 10))
        reply_card.grid_rowconfigure(1, weight=1)
        reply_card.grid_columnconfigure(0, weight=1)

        tk.Label(
            reply_card, text="馃挆  Generated Reply", font=("Arial", 11, "bold"),
            bg=self.WHITE, fg=self.DARK_PURPLE
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 6))

        reply_output = scrolledtext.ScrolledText(
            reply_card, font=("Arial", 10), bg="#FFFBFD", fg=self.TEXT,
            wrap=tk.WORD, relief="flat", bd=0, padx=12, pady=10
        )
        reply_output.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        reply_output.insert(
            "1.0", "Your AI-written reply will appear here 鈾�"
        )
        reply_output.config(state="disabled")

        def generate():
            short_notes = notes_entry.get("1.0", tk.END).strip()

            if not short_notes:
                messagebox.showwarning(
                    "Empty Notes 鈾�",
                    "Please write a few words about how you want to reply.",
                    parent=reply_window
                )
                return

            status_label.config(text="Writing your reply... 鈾�")
            reply_window.update_idletasks()

            try:
                generated = generate_reply(email["content"], short_notes)
            except Exception as error:
                status_label.config(text="")
                messagebox.showerror(
                    "Reply Generation Error",
                    f"Could not generate a reply.\n\n{error}",
                    parent=reply_window
                )
                return

            status_label.config(text="")
            reply_output.config(state="normal")
            reply_output.delete("1.0", tk.END)
            reply_output.insert("1.0", generated)

        tk.Button(
            reply_window, text="鉁�  GENERATE REPLY", command=generate,
            font=("Arial", 10, "bold"), bg=self.BABY_PINK, fg=self.DARK_PURPLE,
            activebackground=self.LAVENDER, activeforeground=self.DARK_PURPLE,
            relief="flat", bd=0, padx=25, pady=10, cursor="hand2"
        ).grid(row=2, column=0, pady=(72, 0))

        def copy_reply():
            reply_window.clipboard_clear()
            reply_window.clipboard_append(reply_output.get("1.0", tk.END).strip())
            status_label.config(text="Copied to clipboard 鈾�")

        button_row = tk.Frame(reply_window, bg=self.CREAM)
        button_row.grid(row=5, column=0, sticky="ew", padx=30, pady=(0, 20))

        tk.Button(
            button_row, text="猝�  COPY REPLY", command=copy_reply,
            font=("Arial", 9, "bold"), bg=self.SNOW, fg=self.DARK_PURPLE,
            relief="flat", bd=0, padx=18, pady=9, cursor="hand2"
        ).pack(side="left")

        tk.Button(
            button_row, text="鈾�  CLOSE", command=reply_window.destroy,
            font=("Arial", 9, "bold"), bg=self.LAVENDER, fg=self.DARK_PURPLE,
            relief="flat", bd=0, padx=25, pady=9, cursor="hand2"
        ).pack(side="right")

    def show_notes(self):

        self.clear_content()
        self.create_header(
            "My Notes",
            "Your little space for thoughts, ideas and important emails 鈾�"
        )

        # Saved notes are shown only by title.
        title_card = tk.Frame(
            self.content, bg=self.WHITE,
            highlightbackground=self.LAVENDER, highlightthickness=1
        )
        title_card.pack(fill="both", expand=True, padx=30, pady=(5, 10))

        tk.Label(
            title_card, text="馃摑  SAVED NOTES",
            font=("Arial", 13, "bold"), bg=self.WHITE, fg=self.DARK_PURPLE
        ).pack(anchor="w", padx=18, pady=(14, 5))

        tk.Label(
            title_card,
            text="Double-click a title to open the saved note 鈾�",
            font=("Arial", 9), bg=self.WHITE, fg=self.LIGHT_TEXT
        ).pack(anchor="w", padx=18, pady=(0, 8))

        # Store the real note objects so the title list can open them.
        saved_note_items = []

        for note in self.personal_notes:
            saved_note_items.append({
                "title": note.get("title", "My Note"),
                "content": note.get("content", ""),
                "date": note.get("date", ""),
                "type": "Personal Note"
            })

        for email in self.notes:
            if email.get("note"):
                saved_note_items.append({
                    "title": email.get("name", "Saved Email"),
                    "content": email.get("note", ""),
                    "date": "",
                    "type": "Email Note"
                })

        if saved_note_items:
            notes_list = tk.Listbox(
                title_card,
                font=("Arial", 11, "bold"),
                bg="#FFFBFD",
                fg=self.DARK_PURPLE,
                relief="flat",
                selectbackground=self.BABY_PINK,
                selectforeground=self.DARK_PURPLE,
                activestyle="none"
            )
            notes_list.pack(fill="both", expand=True, padx=18, pady=(0, 18))

            for item in saved_note_items:
                # Only the title is displayed in the saved-notes list.
                notes_list.insert(tk.END, item["title"])

            def open_selected_note(event=None):
                selection = notes_list.curselection()
                if not selection:
                    return

                item = saved_note_items[selection[0]]

                viewer = tk.Toplevel(self.root)
                viewer.title(item["title"])
                viewer.geometry("600x450")
                viewer.configure(bg=self.CREAM)

                tk.Label(
                    viewer,
                    text=item["title"],
                    font=("Arial", 17, "bold"),
                    bg=self.CREAM,
                    fg=self.DARK_PURPLE
                ).pack(anchor="w", padx=25, pady=(25, 5))

                note_view = scrolledtext.ScrolledText(
                    viewer,
                    font=("Arial", 10),
                    bg=self.WHITE,
                    fg=self.TEXT,
                    wrap=tk.WORD,
                    relief="solid",
                    bd=1,
                    padx=12,
                    pady=12
                )
                note_view.pack(fill="both", expand=True, padx=25, pady=(10, 15))
                note_view.insert("1.0", item["content"])
                note_view.config(state="disabled")

                tk.Button(
                    viewer,
                    text="鈾�  CLOSE",
                    command=viewer.destroy,
                    font=("Arial", 9, "bold"),
                    bg=self.LAVENDER,
                    fg=self.DARK_PURPLE,
                    relief="flat",
                    bd=0,
                    padx=20,
                    pady=8,
                    cursor="hand2"
                ).pack(pady=(0, 20))

            notes_list.bind("<Double-Button-1>", open_selected_note)

        else:
            tk.Label(
                title_card,
                text="鈾�  No saved notes yet",
                font=("Arial", 11),
                bg=self.WHITE,
                fg=self.LIGHT_TEXT
            ).pack(anchor="w", padx=18, pady=(0, 15))

        # New note button stays outside the list.
        toolbar = tk.Frame(self.content, bg=self.CREAM)
        toolbar.pack(fill="x", padx=30, pady=(0, 15))

        tk.Button(
            toolbar, text="锛�  NEW NOTE", command=self.create_personal_note,
            font=("Arial", 10, "bold"), bg=self.LAVENDER, fg=self.DARK_PURPLE,
            activebackground=self.BABY_PINK, relief="flat", bd=0,
            padx=20, pady=9, cursor="hand2"
        ).pack(side="left")

        tk.Label(
            toolbar, text="  Write anything you want 鈾�", font=("Arial", 9),
            bg=self.CREAM, fg=self.LIGHT_TEXT
        ).pack(side="left", padx=8)

    def create_personal_note(self):

        note_window = tk.Toplevel(self.root)
        note_window.title("New Note 鈾�")
        note_window.geometry("550x560")
        note_window.minsize(500, 500)
        note_window.configure(bg=self.CREAM)

        # Use grid so the SAVE NOTE button always stays visible at the bottom.
        note_window.grid_rowconfigure(2, weight=1)
        note_window.grid_columnconfigure(0, weight=1)

        tk.Label(
            note_window, text="馃尭 New Personal Note", font=("Arial", 18, "bold"),
            bg=self.CREAM, fg=self.DARK_PURPLE
        ).grid(row=0, column=0, pady=(22, 5))

        tk.Label(
            note_window, text="Write whatever is on your mind 鈾�", font=("Arial", 9),
            bg=self.CREAM, fg=self.LIGHT_TEXT
        ).grid(row=1, column=0, pady=(0, 12))

        editor_frame = tk.Frame(note_window, bg=self.CREAM)
        editor_frame.grid(row=2, column=0, sticky="nsew", padx=35)
        editor_frame.grid_rowconfigure(1, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)

        title_entry = tk.Entry(
            editor_frame, font=("Arial", 11), bg=self.WHITE, fg=self.TEXT,
            relief="solid", bd=1
        )
        title_entry.grid(row=0, column=0, sticky="ew", ipady=8, pady=(0, 8))
        title_entry.insert(0, "Note title...")

        note_text = scrolledtext.ScrolledText(
            editor_frame, font=("Arial", 10), bg=self.WHITE, fg=self.TEXT,
            wrap=tk.WORD, relief="solid", bd=1
        )
        note_text.grid(row=1, column=0, sticky="nsew")

        def save_note():
            title = title_entry.get().strip()
            content = note_text.get("1.0", tk.END).strip()

            if not content:
                messagebox.showwarning(
                    "Empty Note", "Please write something first 鈾�", parent=note_window
                )
                return

            if not title or title == "Note title...":
                title = "My Note"

            self.personal_notes.append({
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            note_window.destroy()
            self.show_notes()

        button_frame = tk.Frame(note_window, bg=self.CREAM)
        button_frame.grid(row=3, column=0, sticky="ew", padx=35, pady=(12, 18))

        tk.Button(
            button_frame, text="鈾�  SAVE NOTE", command=save_note,
            font=("Arial", 11, "bold"), bg=self.BABY_PINK, fg=self.DARK_PURPLE,
            activebackground=self.LAVENDER, activeforeground=self.DARK_PURPLE,
            relief="flat", bd=0, padx=35, pady=11, cursor="hand2"
        ).pack(anchor="center")

    def edit_email_note(self, email):

        note_window = tk.Toplevel(self.root)
        note_window.title("Email Note 鈾�")
        note_window.geometry("550x560")
        note_window.minsize(500, 500)
        note_window.configure(bg=self.CREAM)

        note_window.grid_rowconfigure(2, weight=1)
        note_window.grid_columnconfigure(0, weight=1)

        tk.Label(
            note_window, text="馃拰  " + email.get("name", "Email Note"),
            font=("Arial", 16, "bold"),
            bg=self.CREAM, fg=self.DARK_PURPLE,
            wraplength=480, justify="left"
        ).grid(row=0, column=0, sticky="w", padx=35, pady=(22, 8))

        tk.Label(
            note_window, text="Write your personal note below 鈾�",
            font=("Arial", 9), bg=self.CREAM, fg=self.LIGHT_TEXT
        ).grid(row=1, column=0, sticky="w", padx=35, pady=(0, 12))

        note_text = scrolledtext.ScrolledText(
            note_window, font=("Arial", 10), bg=self.WHITE, fg=self.TEXT,
            wrap=tk.WORD, relief="solid", bd=1
        )
        note_text.grid(row=2, column=0, sticky="nsew", padx=35)

        if email.get("note"):
            note_text.insert("1.0", email["note"])

        def save_email_note():
            note = note_text.get("1.0", tk.END).strip()

            if not note:
                messagebox.showwarning(
                    "Empty Note 鈾�",
                    "Please write something before saving.",
                    parent=note_window
                )
                return

            email["note"] = note
            note_window.destroy()
            self.show_notes()

        button_frame = tk.Frame(note_window, bg=self.CREAM)
        button_frame.grid(row=3, column=0, sticky="ew", padx=35, pady=(12, 18))

        tk.Button(
            button_frame, text="鈾�  SAVE NOTE", command=save_email_note,
            font=("Arial", 11, "bold"), bg=self.BABY_PINK, fg=self.DARK_PURPLE,
            activebackground=self.LAVENDER, activeforeground=self.DARK_PURPLE,
            relief="flat", bd=0, padx=35, pady=11, cursor="hand2"
        ).pack(anchor="center")

    def remove_email_note(self, email):

        if email in self.notes:
            self.notes.remove(email)

        self.show_notes()

    def add_email_to_notes(self, email):

        if email not in self.notes:
            self.notes.append(email)

        # Open the note editor immediately so the user can write and save the note.
        self.edit_email_note(email)

    def show_history(self):

        self.clear_content()
        self.create_header("Saved History", "Your previously classified emails 鈾�")

        card = tk.Frame(
            self.content, bg=self.WHITE,
            highlightbackground=self.LAVENDER, highlightthickness=1
        )
        card.pack(fill="both", expand=True, padx=30, pady=15)

        saved = [email for email in self.emails if email.get("classification")]

        if not saved:
            tk.Label(
                card,
                text="鈾n\nNo saved emails yet.\n\nClassify an email and save it here.",
                font=("Arial", 14), bg=self.WHITE, fg=self.LIGHT_TEXT, justify="center"
            ).pack(expand=True)
            return

        for email in saved:
            self.create_history_item(card, email)

    def create_history_item(self, parent, email):

        item = tk.Frame(
            parent, bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK, highlightthickness=1
        )
        item.pack(fill="x", padx=20, pady=8)

        tk.Label(
            item, text="馃拰 " + email["name"], font=("Arial", 10, "bold"),
            bg=self.LIGHT_ROSE, fg=self.DARK_PURPLE
        ).pack(side="left", padx=15, pady=12)

        classification = email.get("classification", "Normal")

        tk.Label(
            item, text=classification.upper(), font=("Arial", 8, "bold"),
            bg=self.LIGHT_ROSE,
            fg="#C44F76" if classification == "Important" else "#65804A"
        ).pack(side="left", padx=10)

        tk.Button(
            item, text="鈾� Add to Notes",
            command=lambda e=email: self.add_email_to_notes(e),
            font=("Arial", 8), bg=self.WHITE, fg=self.DARK_PURPLE,
            relief="flat", bd=0, cursor="hand2"
        ).pack(side="right", padx=15)



if __name__ == "__main__":

    root = tk.Tk()
    app = EmailClassifierGUI(root)
    root.mainloop()

