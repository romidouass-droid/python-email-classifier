import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime, date
import calendar
import os
import re

from extract_email_text import extract_email_text
from api_classifier import classify_email


class EmailClassifierGUI:

    # ==========================================================
    # PASTEL COLOR PALETTE
    # ==========================================================

    LAVENDER = "#BBB7E5"
    LIGHT_ROSE = "#F7DFDF"
    BABY_PINK = "#EFBDDB"
    PISTACHIO = "#B6C687"
    SNOW = "#DAE9FA"
    PALE_YELLOW = "#F3EDBD"

    # Soft deadline colors
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

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, root):

        self.root = root

        self.root.title("AI Email Classifier ♡")
        self.root.geometry("1250x800")
        self.root.minsize(1050, 700)
        self.root.configure(bg=self.CREAM)

        # ------------------------------------------------------
        # Application data
        # ------------------------------------------------------

        self.selected_files = []
        self.emails = []

        # Saved email notes
        self.notes = []

        # Personal notes
        self.personal_notes = []

        # All detected deadlines
        self.deadlines = []

        self.current_result = ""

        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        # ------------------------------------------------------
        # Create interface
        # ------------------------------------------------------

        self.create_sidebar()

        self.content = tk.Frame(
            root,
            bg=self.CREAM
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.show_classifier()

    # ==========================================================
    # SIDEBAR
    # ==========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=self.LAVENDER,
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo
        tk.Label(
            self.sidebar,
            text="♡",
            font=("Arial", 38, "bold"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE
        ).pack(
            pady=(30, 0)
        )

        # Title
        tk.Label(
            self.sidebar,
            text="AI Email\nClassifier",
            font=("Arial", 20, "bold"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE,
            justify="center"
        ).pack(
            pady=(0, 8)
        )

        # Subtitle
        tk.Label(
            self.sidebar,
            text="Smart inbox ♡\nOrganized mind",
            font=("Arial", 9),
            bg=self.LAVENDER,
            fg=self.SOFT_PURPLE,
            justify="center"
        ).pack(
            pady=(0, 30)
        )

        # Navigation
        self.create_navigation_button(
            "♡  Classify",
            self.show_classifier
        )

        self.create_navigation_button(
            "◷  History",
            self.show_history
        )

        self.create_navigation_button(
            "✎  My Notes",
            self.show_notes
        )

        self.create_navigation_button(
            "⚙  Settings",
            self.show_settings
        )

        # Flowers
        tk.Label(
            self.sidebar,
            text="🌷  🌸\n  🌼  🌷\n🌸  🌿  🌸",
            font=("Arial", 19),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE
        ).pack(
            side="bottom",
            pady=20
        )

        # Motivation
        tk.Label(
            self.sidebar,
            text="You got this,\ngirl ♡",
            font=("Arial", 13, "italic"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE,
            justify="center"
        ).pack(
            side="bottom",
            pady=(0, 5)
        )

    # ==========================================================
    # NAVIGATION BUTTON
    # ==========================================================

    def create_navigation_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE,
            activebackground=self.LIGHT_ROSE,
            activeforeground=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=30,
            pady=14,
            cursor="hand2"
        )

        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

    # ==========================================================
    # CLEAR PAGE
    # ==========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ==========================================================
    # HEADER
    # ==========================================================

    def create_header(self, title, subtitle):

        header = tk.Frame(
            self.content,
            bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK,
            highlightthickness=1
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 12)
        )

        left = tk.Frame(
            header,
            bg=self.LIGHT_ROSE
        )

        left.pack(
            side="left",
            padx=25,
            pady=17
        )

        tk.Label(
            left,
            text=title + " ♡",
            font=("Arial", 23, "bold"),
            bg=self.LIGHT_ROSE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w"
        )

        tk.Label(
            left,
            text=subtitle,
            font=("Arial", 10),
            bg=self.LIGHT_ROSE,
            fg=self.SOFT_PURPLE
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        tk.Label(
            header,
            text="🌷  🌸  🌼",
            font=("Arial", 24),
            bg=self.LIGHT_ROSE
        ).pack(
            side="right",
            padx=25
        )

    # ==========================================================
    # CLASSIFIER PAGE
    # ==========================================================

    def show_classifier(self):

        self.clear_content()

        self.create_header(
            "Email Classification",
            "Upload your emails and let your little AI assistant organize them ♡"
        )

        main = tk.Frame(
            self.content,
            bg=self.CREAM
        )

        main.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        # LEFT
        left = tk.Frame(
            main,
            bg=self.CREAM
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        # RIGHT
        right = tk.Frame(
            main,
            bg=self.CREAM,
            width=340
        )

        right.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        right.pack_propagate(False)

        self.create_upload_card(left)
        self.create_email_card(left)

        self.create_result_card(right)
        self.create_calendar_card(right)

    # ==========================================================
    # UPLOAD CARD
    # ==========================================================

    def create_upload_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.WHITE,
            highlightbackground=self.LAVENDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            card,
            text="📤  Upload Emails",
            font=("Arial", 14, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=22,
            pady=(17, 3)
        )

        tk.Label(
            card,
            text="Select one or multiple .eml files",
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.LIGHT_TEXT
        ).pack(
            anchor="w",
            padx=22
        )

        tk.Button(
            card,
            text="♡  CHOOSE EMAILS",
            command=self.upload_emails,
            font=("Arial", 10, "bold"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE,
            activebackground=self.BABY_PINK,
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=22,
            pady=12
        )

        self.file_label = tk.Label(
            card,
            text="No emails selected yet ♡",
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.LIGHT_TEXT
        )

        self.file_label.pack(
            anchor="w",
            padx=22,
            pady=(0, 15)
        )

    # ==========================================================
    # EMAIL CARD
    # ==========================================================

    def create_email_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.WHITE,
            highlightbackground=self.LAVENDER,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True
        )

        # Title
        tk.Label(
            card,
            text="💌  Your Emails",
            font=("Arial", 14, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=22,
            pady=(15, 5)
        )

        # Main classification button - always visible
        tk.Button(
            card,
            text="✨  CLASSIFY EMAILS",
            command=self.test_classification,
            font=("Arial", 11, "bold"),
            bg=self.BABY_PINK,
            fg=self.DARK_PURPLE,
            activebackground=self.LAVENDER,
            activeforeground=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            padx=30,
            pady=11,
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 10)
        )

        self.email_text = scrolledtext.ScrolledText(
            card,
            font=("Arial", 9),
            bg="#FFFBFD",
            fg=self.TEXT,
            wrap=tk.WORD,
            relief="flat",
            bd=0,
            padx=12,
            pady=12
        )

        self.email_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

    # ==========================================================
    # RESULT CARD
    # ==========================================================

    def create_result_card(self, parent):

        self.result_card = tk.Frame(
            parent,
            bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK,
            highlightthickness=1
        )

        self.result_card.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            self.result_card,
            text="✨  Classification Result",
            font=("Arial", 13, "bold"),
            bg=self.LIGHT_ROSE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        self.result_label = tk.Label(
            self.result_card,
            text="WAITING ♡",
            font=("Arial", 19, "bold"),
            bg=self.LIGHT_ROSE,
            fg=self.SOFT_PURPLE
        )

        self.result_label.pack(
            pady=12
        )

        self.result_description = tk.Label(
            self.result_card,
            text="Classify your emails to see\n"
                 "what needs your attention.",
            font=("Arial", 9),
            bg=self.LIGHT_ROSE,
            fg=self.SOFT_PURPLE,
            justify="center"
        )

        self.result_description.pack(
            pady=(0, 12)
        )

        tk.Button(
            self.result_card,
            text="♡  SAVE RESULT",
            command=self.save_result,
            font=("Arial", 9, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(
            pady=(0, 17)
        )

    # ==========================================================
    # CALENDAR CARD
    # ==========================================================

    def create_calendar_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.WHITE,
            highlightbackground=self.PISTACHIO,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="📅  My Calendar",
            font=("Arial", 13, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        tk.Label(
            card,
            text="Your email deadlines appear here ♡",
            font=("Arial", 8),
            bg=self.WHITE,
            fg=self.LIGHT_TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 5)
        )

        self.calendar_frame = tk.Frame(
            card,
            bg=self.WHITE
        )

        self.calendar_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=3
        )

        self.draw_calendar()

        tk.Label(
            card,
            text="🟢 Plenty of time   🟡 Getting closer\n"
                 "🟠 Very soon   🔴 Deadline / overdue",
            font=("Arial", 8),
            bg=self.WHITE,
            fg=self.SOFT_PURPLE,
            justify="center"
        ).pack(
            pady=(4, 15)
        )

    # ==========================================================
    # CALENDAR
    # ==========================================================

    def draw_calendar(self):

        if not hasattr(self, "calendar_frame"):
            return

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        navigation = tk.Frame(
            self.calendar_frame,
            bg=self.WHITE
        )

        navigation.pack(
            fill="x",
            pady=3
        )

        tk.Button(
            navigation,
            text="‹",
            command=self.previous_month,
            font=("Arial", 14, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            side="left"
        )

        month_name = calendar.month_name[
            self.current_month
        ]

        tk.Label(
            navigation,
            text=f"{month_name} {self.current_year}",
            font=("Arial", 10, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE
        ).pack(
            side="left",
            expand=True
        )

        tk.Button(
            navigation,
            text="›",
            command=self.next_month,
            font=("Arial", 14, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            side="right"
        )

        week_frame = tk.Frame(
            self.calendar_frame,
            bg=self.WHITE
        )

        week_frame.pack(
            fill="x"
        )

        weekdays = [
            "Mo", "Tu", "We",
            "Th", "Fr", "Sa", "Su"
        ]

        for column, day_name in enumerate(weekdays):

            tk.Label(
                week_frame,
                text=day_name,
                font=("Arial", 8, "bold"),
                bg=self.WHITE,
                fg=self.SOFT_PURPLE
            ).grid(
                row=0,
                column=column,
                sticky="nsew"
            )

            week_frame.columnconfigure(
                column,
                weight=1
            )

        month_days = calendar.monthcalendar(
            self.current_year,
            self.current_month
        )

        for row_index, week in enumerate(
            month_days,
            start=1
        ):

            week_frame.rowconfigure(
                row_index,
                weight=1
            )

            for column, day_number in enumerate(week):

                if day_number == 0:
                    continue

                current_date = date(
                    self.current_year,
                    self.current_month,
                    day_number
                )

                background = self.get_calendar_color(
                    current_date
                )

                text = str(day_number)

                # Add a small marker to deadline dates
                if current_date in self.deadlines:
                    text = "•\n" + str(day_number)

                button = tk.Button(
                    week_frame,
                    text=text,
                    font=("Arial", 7, "bold"),
                    bg=background,
                    fg=self.DARK_PURPLE,
                    activebackground=self.BABY_PINK,
                    relief="flat",
                    bd=0,
                    width=4,
                    height=2,
                    cursor="hand2"
                )

                button.grid(
                    row=row_index,
                    column=column,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                )

    # ==========================================================
    # GET CALENDAR COLOR
    # ==========================================================

    def get_calendar_color(self, current_date):

        # Deadline
        if current_date in self.deadlines:

            days_left = (
                current_date - date.today()
            ).days

            # Deadline day or overdue
            if days_left <= 0:
                return self.DEADLINE_RED

            # 1-2 days
            elif days_left <= 2:
                return self.DEADLINE_ORANGE

            # 3-5 days
            elif days_left <= 5:
                return self.DEADLINE_YELLOW

            # More than 5 days
            else:
                return self.DEADLINE_GREEN

        # Today without deadline
        if current_date == date.today():
            return self.SNOW

        return self.WHITE

    # ==========================================================
    # CALENDAR NAVIGATION
    # ==========================================================

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

        self.emails = []

        # Reset deadlines from previous upload
        self.deadlines = []

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

                file_name = os.path.basename(
                    file_path
                )

                email = {
                    "name": file_name,
                    "content": content,
                    "classification": "",
                    "note": ""
                }

                self.emails.append(email)

                self.email_text.insert(
                    tk.END,
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                )

                self.email_text.insert(
                    tk.END,
                    f"💌 EMAIL {index}: {file_name}\n"
                )

                self.email_text.insert(
                    tk.END,
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                )

                self.email_text.insert(
                    tk.END,
                    content
                )

                self.email_text.insert(
                    tk.END,
                    "\n\n"
                )

                # Detect dates
                self.detect_deadlines(content)

            except Exception as error:

                self.email_text.insert(
                    tk.END,
                    f"Error reading file:\n"
                    f"{error}\n\n"
                )

        if len(self.selected_files) == 1:

            self.file_label.config(
                text="♡ 1 email selected",
                fg=self.DARK_PURPLE
            )

        else:

            self.file_label.config(
                text=f"♡ {len(self.selected_files)} emails selected",
                fg=self.DARK_PURPLE
            )

        self.current_result = ""

        self.result_label.config(
            text="READY ♡",
            bg=self.LIGHT_ROSE,
            fg=self.SOFT_PURPLE
        )

        self.result_description.config(
            text="Your emails are ready.\n"
                 "Let's see what needs your attention.",
            bg=self.LIGHT_ROSE
        )

        self.result_card.config(
            bg=self.LIGHT_ROSE
        )

        self.draw_calendar()

    # ==========================================================
    # DEADLINE DETECTION
    # ==========================================================

    def detect_deadlines(self, content):

        found_dates = []

        # ------------------------------------------------------
        # YYYY-MM-DD
        # ------------------------------------------------------

        matches = re.findall(
            r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b",
            content
        )

        for year, month, day in matches:

            try:

                found_dates.append(
                    date(
                        int(year),
                        int(month),
                        int(day)
                    )
                )

            except ValueError:
                pass

        # ------------------------------------------------------
        # DD/MM/YYYY
        # ------------------------------------------------------

        matches = re.findall(
            r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b",
            content
        )

        for day, month, year in matches:

            try:

                found_dates.append(
                    date(
                        int(year),
                        int(month),
                        int(day)
                    )
                )

            except ValueError:
                pass

        # ------------------------------------------------------
        # "25 September 2026"
        # ------------------------------------------------------

        month_names = (
            "January|February|March|April|May|June|July|"
            "August|September|October|November|December"
        )

        matches = re.findall(
            rf"\b(\d{{1,2}})\s+({month_names})"
            rf"(?:\s+(20\d{{2}}))?\b",
            content,
            re.IGNORECASE
        )

        month_numbers = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12
        }

        for day, month_name, year in matches:

            try:

                month = month_numbers[
                    month_name.lower()
                ]

                if year:
                    selected_year = int(year)
                else:
                    selected_year = datetime.now().year

                found_dates.append(
                    date(
                        selected_year,
                        month,
                        int(day)
                    )
                )

            except (ValueError, KeyError):
                pass

        # ------------------------------------------------------
        # "September 25 2026"
        # ------------------------------------------------------

        matches = re.findall(
            rf"\b({month_names})\s+(\d{{1,2}})"
            rf"(?:,\s*|\s+)(20\d{{2}})?\b",
            content,
            re.IGNORECASE
        )

        for month_name, day, year in matches:

            try:

                month = month_numbers[
                    month_name.lower()
                ]

                if year:
                    selected_year = int(year)
                else:
                    selected_year = datetime.now().year

                found_dates.append(
                    date(
                        selected_year,
                        month,
                        int(day)
                    )
                )

            except (ValueError, KeyError):
                pass

        # ------------------------------------------------------
        # Only treat dates as deadlines if nearby words indicate
        # deadline / due / submit / exam etc.
        # ------------------------------------------------------

        deadline_words = [
            "deadline",
            "due",
            "submit",
            "submission",
            "exam",
            "assignment",
            "project",
            "final",
            "application",
            "registration"
        ]

        content_lower = content.lower()

        has_deadline_context = any(
            word in content_lower
            for word in deadline_words
        )

        if has_deadline_context:

            for found_date in found_dates:

                if found_date not in self.deadlines:

                    self.deadlines.append(
                        found_date
                    )

    # ==========================================================
    # CLASSIFICATION
    # ==========================================================

    def test_classification(self):

        if not self.selected_files:

            messagebox.showwarning(
                "No Emails ♡",
                "Please upload at least one email first."
            )

            return

        important_words = [
            "deadline",
            "urgent",
            "exam",
            "assignment",
            "meeting",
            "submission",
            "important",
            "project",
            "interview",
            "application"
        ]

        # Classify EACH email separately.
        # We must not combine all email contents into one text.
        important_count = 0
        normal_count = 0

        for email in self.emails:

            email_text = email["content"].lower()

            found = any(
                word in email_text
                for word in important_words
            )

            if found:
                email["classification"] = "Important"
                important_count += 1
            else:
                email["classification"] = "Normal"
                normal_count += 1

        # Summary for the result card.
        if important_count == len(self.emails):
            self.current_result = "Important"
        elif normal_count == len(self.emails):
            self.current_result = "Normal"
        else:
            self.current_result = "Mixed"

        self.display_result(self.current_result)

        # Show the individual result beside every email.
        self.display_email_list()


    # ==========================================================
    # DISPLAY EMAIL LIST WITH INDIVIDUAL RESULTS
    # ==========================================================

    def display_email_list(self):

        self.email_text.config(state="normal")
        self.email_text.delete("1.0", tk.END)

        for index, email in enumerate(self.emails, start=1):

            classification = email.get("classification", "")

            if classification == "Important":
                label = "💗 IMPORTANT"
            elif classification == "Normal":
                label = "🌿 NORMAL"
            else:
                label = "⏳ NOT CLASSIFIED"

            self.email_text.insert(
                tk.END,
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            )

            self.email_text.insert(
                tk.END,
                f"💌 EMAIL {index}: {email['name']}    {label}\n"
            )

            self.email_text.insert(
                tk.END,
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )

            self.email_text.insert(
                tk.END,
                email["content"]
            )

            self.email_text.insert(
                tk.END,
                "\n\n"
            )

        self.email_text.config(state="disabled")


    # ==========================================================
    # DISPLAY RESULT
    # ==========================================================

    def display_result(self, result):

        if result.lower() == "important":

            background = self.LIGHT_ROSE

            self.result_label.config(
                text="💗 IMPORTANT",
                bg=background,
                fg="#C44F76"
            )

            self.result_description.config(
                text="All selected emails are Important.",
                bg=background
            )

        elif result.lower() == "mixed":

            background = self.PALE_YELLOW

            important_count = sum(
                1 for email in self.emails
                if email.get("classification") == "Important"
            )

            normal_count = sum(
                1 for email in self.emails
                if email.get("classification") == "Normal"
            )

            self.result_label.config(
                text="🌸 MIXED RESULTS",
                bg=background,
                fg=self.DARK_PURPLE
            )

            self.result_description.config(
                text=f"{important_count} Important  •  "
                     f"{normal_count} Normal\n"
                     "Each email was classified separately.",
                bg=background
            )

        else:

            background = "#EEF5E6"

            self.result_label.config(
                text="🌿 NORMAL",
                bg=background,
                fg="#65804A"
            )

            self.result_description.config(
                text="All selected emails are Normal.",
                bg=background
            )

        self.result_card.config(
            bg=background
        )


    # ==========================================================
    # SAVE RESULT
    # ==========================================================

    def save_result(self):

        if not self.selected_files:

            messagebox.showwarning(
                "No Emails ♡",
                "Please upload an email first."
            )

            return

        if not self.current_result:

            messagebox.showwarning(
                "No Classification ♡",
                "Please classify the emails first."
            )

            return

        # Keep each email's individual classification.
        # Do not replace all results with one global label.

        messagebox.showinfo(
            "Saved ♡",
            "Your classification has been saved!\n\n"
            "You can view it in History."
        )

    # ==========================================================
    # MY NOTES
    # ==========================================================

    def show_notes(self):

        self.clear_content()

        self.create_header(
            "My Notes",
            "Your little space for thoughts, ideas and important emails ♡"
        )

        # ------------------------------------------------------
        # Top buttons
        # ------------------------------------------------------

        toolbar = tk.Frame(
            self.content,
            bg=self.CREAM
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=(5, 10)
        )

        tk.Button(
            toolbar,
            text="＋  NEW NOTE",
            command=self.create_personal_note,
            font=("Arial", 10, "bold"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE,
            activebackground=self.BABY_PINK,
            relief="flat",
            bd=0,
            padx=20,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left"
        )

        tk.Label(
            toolbar,
            text="  Write anything you want ♡",
            font=("Arial", 9),
            bg=self.CREAM,
            fg=self.LIGHT_TEXT
        ).pack(
            side="left",
            padx=8
        )

        # ------------------------------------------------------
        # Notes container
        # ------------------------------------------------------

        canvas = tk.Canvas(
            self.content,
            bg=self.CREAM,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self.content,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = tk.Frame(
            canvas,
            bg=self.CREAM
        )

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(30, 0)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 30)
        )

        # ------------------------------------------------------
        # Personal notes
        # ------------------------------------------------------

        for note in self.personal_notes:

            self.create_personal_note_card(
                scroll_frame,
                note
            )

        # ------------------------------------------------------
        # Saved email notes
        # ------------------------------------------------------

        if self.notes:

            tk.Label(
                scroll_frame,
                text="💌 Saved Emails",
                font=("Arial", 15, "bold"),
                bg=self.CREAM,
                fg=self.DARK_PURPLE
            ).pack(
                anchor="w",
                pady=(20, 10)
            )

            for email in self.notes:

                self.create_email_note_card(
                    scroll_frame,
                    email
                )

        elif not self.personal_notes:

            tk.Label(
                scroll_frame,
                text="♡\n\nYour notes are empty.\n\n"
                     "Create a note or save an email here.",
                font=("Arial", 14),
                bg=self.CREAM,
                fg=self.LIGHT_TEXT,
                justify="center"
            ).pack(
                pady=100
            )

    # ==========================================================
    # CREATE PERSONAL NOTE
    # ==========================================================

    def create_personal_note(self):

        note_window = tk.Toplevel(
            self.root
        )

        note_window.title("New Note ♡")
        note_window.geometry("550x450")
        note_window.configure(
            bg=self.CREAM
        )

        tk.Label(
            note_window,
            text="🌸 New Personal Note",
            font=("Arial", 18, "bold"),
            bg=self.CREAM,
            fg=self.DARK_PURPLE
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            note_window,
            text="Write whatever is on your mind ♡",
            font=("Arial", 9),
            bg=self.CREAM,
            fg=self.LIGHT_TEXT
        ).pack(
            pady=(0, 15)
        )

        title_entry = tk.Entry(
            note_window,
            font=("Arial", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            relief="solid",
            bd=1
        )

        title_entry.pack(
            fill="x",
            padx=35,
            ipady=8
        )

        title_entry.insert(
            0,
            "Note title..."
        )

        note_text = scrolledtext.ScrolledText(
            note_window,
            font=("Arial", 10),
            bg=self.WHITE,
            fg=self.TEXT,
            wrap=tk.WORD,
            relief="solid",
            bd=1
        )

        note_text.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        def save_note():

            title = title_entry.get().strip()
            content = note_text.get(
                "1.0",
                tk.END
            ).strip()

            if not content:

                messagebox.showwarning(
                    "Empty Note",
                    "Please write something first ♡",
                    parent=note_window
                )

                return

            if not title or title == "Note title...":

                title = "My Note"

            self.personal_notes.append({
                "title": title,
                "content": content,
                "date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
            })

            note_window.destroy()

            self.show_notes()

        tk.Button(
            note_window,
            text="♡  SAVE NOTE",
            command=save_note,
            font=("Arial", 10, "bold"),
            bg=self.BABY_PINK,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2"
        ).pack(
            pady=(0, 20)
        )

    # ==========================================================
    # PERSONAL NOTE CARD
    # ==========================================================

    def create_personal_note_card(self, parent, note):

        card = tk.Frame(
            parent,
            bg=self.PALE_YELLOW,
            highlightbackground=self.LAVENDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=7
        )

        tk.Label(
            card,
            text="📝  " + note["title"],
            font=("Arial", 12, "bold"),
            bg=self.PALE_YELLOW,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 3)
        )

        tk.Label(
            card,
            text=note["date"],
            font=("Arial", 8),
            bg=self.PALE_YELLOW,
            fg=self.LIGHT_TEXT
        ).pack(
            anchor="w",
            padx=18
        )

        tk.Label(
            card,
            text=note["content"],
            font=("Arial", 10),
            bg=self.PALE_YELLOW,
            fg=self.TEXT,
            justify="left",
            wraplength=750
        ).pack(
            anchor="w",
            padx=18,
            pady=10
        )

        tk.Button(
            card,
            text="🗑 Delete",
            command=lambda n=note: self.delete_personal_note(n),
            font=("Arial", 8),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            anchor="e",
            padx=18,
            pady=(0, 12)
        )

    # ==========================================================
    # DELETE PERSONAL NOTE
    # ==========================================================

    def delete_personal_note(self, note):

        if note in self.personal_notes:

            self.personal_notes.remove(note)

        self.show_notes()

    # ==========================================================
    # EMAIL NOTE CARD
    # ==========================================================

    def create_email_note_card(self, parent, email):

        card = tk.Frame(
            parent,
            bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=7
        )

        # Email title + small ADD A NOTE button
        title_row = tk.Frame(
            card,
            bg=self.LIGHT_ROSE
        )

        title_row.pack(
            fill="x",
            padx=18,
            pady=(12, 8)
        )

        tk.Label(
            title_row,
            text="💌  " + email["name"],
            font=("Arial", 11, "bold"),
            bg=self.LIGHT_ROSE,
            fg=self.DARK_PURPLE
        ).pack(
            side="left",
            anchor="w",
            fill="x",
            expand=True
        )

        note_area = tk.Frame(
            card,
            bg=self.LIGHT_ROSE
        )

        def show_note_editor():

            if note_area.winfo_ismapped():
                return

            note_area.pack(
                fill="x",
                padx=18,
                pady=(0, 12)
            )

            add_button.config(
                text="✓  NOTE OPEN",
                state="disabled"
            )

        add_button = tk.Button(
            title_row,
            text="＋ ADD A NOTE",
            command=show_note_editor,
            font=("Arial", 8, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            activebackground=self.BABY_PINK,
            relief="flat",
            bd=0,
            padx=9,
            pady=5,
            cursor="hand2"
        )

        add_button.pack(
            side="right"
        )

        tk.Label(
            note_area,
            text="📝  " + email["name"],
            font=("Arial", 9, "bold"),
            bg=self.LIGHT_ROSE,
            fg=self.SOFT_PURPLE
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        note_box = tk.Text(
            note_area,
            height=5,
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.TEXT,
            wrap=tk.WORD,
            relief="solid",
            bd=1
        )

        note_box.pack(
            fill="x",
            pady=5
        )

        if email.get("note"):
            note_box.insert(
                "1.0",
                email["note"]
            )
            show_note_editor()

        def save_email_note():

            note = note_box.get(
                "1.0",
                tk.END
            ).strip()

            if not note:
                messagebox.showwarning(
                    "Empty Note ♡",
                    "Please write something before saving."
                )
                return

            email["note"] = note

            messagebox.showinfo(
                "Note Saved ♡",
                "Your note has been saved."
            )

        buttons = tk.Frame(
            note_area,
            bg=self.LIGHT_ROSE
        )

        buttons.pack(
            fill="x",
            pady=(5, 0)
        )

        tk.Button(
            buttons,
            text="♡ SAVE NOTE",
            command=save_email_note,
            font=("Arial", 8, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            activebackground=self.BABY_PINK,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            side="left"
        )

        tk.Button(
            buttons,
            text="🗑 REMOVE EMAIL",
            command=lambda e=email: self.remove_email_note(e),
            font=("Arial", 8),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            side="right"
        )

    # ==========================================================
    # REMOVE EMAIL NOTE
    # ==========================================================

    def remove_email_note(self, email):

        if email in self.notes:

            self.notes.remove(email)

        self.show_notes()

    # ==========================================================
    # ADD EMAIL TO NOTES
    # ==========================================================

    def add_email_to_notes(self, email):

        if email not in self.notes:

            self.notes.append(email)

            messagebox.showinfo(
                "Added to My Notes ♡",
                f"'{email['name']}' was added to My Notes."
            )

        else:

            messagebox.showinfo(
                "Already Saved ♡",
                "This email is already in My Notes."
            )

        self.show_classifier()

    # ==========================================================
    # HISTORY
    # ==========================================================

    def show_history(self):

        self.clear_content()

        self.create_header(
            "Saved History",
            "Your previously classified emails ♡"
        )

        card = tk.Frame(
            self.content,
            bg=self.WHITE,
            highlightbackground=self.LAVENDER,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        saved = [
            email
            for email in self.emails
            if email.get("classification")
        ]

        if not saved:

            tk.Label(
                card,
                text="♡\n\nNo saved emails yet.\n\n"
                     "Classify an email and save it here.",
                font=("Arial", 14),
                bg=self.WHITE,
                fg=self.LIGHT_TEXT,
                justify="center"
            ).pack(
                expand=True
            )

            return

        for email in saved:

            self.create_history_item(
                card,
                email
            )

    # ==========================================================
    # HISTORY ITEM
    # ==========================================================

    def create_history_item(self, parent, email):

        item = tk.Frame(
            parent,
            bg=self.LIGHT_ROSE,
            highlightbackground=self.BABY_PINK,
            highlightthickness=1
        )

        item.pack(
            fill="x",
            padx=20,
            pady=8
        )

        tk.Label(
            item,
            text="💌 " + email["name"],
            font=("Arial", 10, "bold"),
            bg=self.LIGHT_ROSE,
            fg=self.DARK_PURPLE
        ).pack(
            side="left",
            padx=15,
            pady=12
        )

        classification = email.get(
            "classification",
            "Normal"
        )

        tk.Label(
            item,
            text=classification.upper(),
            font=("Arial", 8, "bold"),
            bg=self.LIGHT_ROSE,
            fg="#C44F76"
            if classification == "Important"
            else "#65804A"
        ).pack(
            side="left",
            padx=10
        )

        # Add to notes
        tk.Button(
            item,
            text="♡ Add to Notes",
            command=lambda e=email:
                self.add_email_to_notes(e),
            font=("Arial", 8),
            bg=self.WHITE,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            side="right",
            padx=15
        )

    # ==========================================================
    # SETTINGS
    # ==========================================================

    def show_settings(self):

        self.clear_content()

        self.create_header(
            "Settings",
            "Make your little workspace feel like you ♡"
        )

        card = tk.Frame(
            self.content,
            bg=self.WHITE,
            highlightbackground=self.LAVENDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=30,
            pady=15
        )

        tk.Label(
            card,
            text="🌸 Important Categories",
            font=("Arial", 13, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 8)
        )

        important_entry = tk.Entry(
            card,
            font=("Arial", 10),
            bg="#FFFBFD",
            fg=self.TEXT,
            relief="solid",
            bd=1
        )

        important_entry.pack(
            fill="x",
            padx=25,
            ipady=8
        )

        tk.Label(
            card,
            text="Example: exams, university, work, meetings",
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.LIGHT_TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 20)
        )

        tk.Label(
            card,
            text="🌿 Normal Categories",
            font=("Arial", 13, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PURPLE
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 8)
        )

        normal_entry = tk.Entry(
            card,
            font=("Arial", 10),
            bg="#FFFBFD",
            fg=self.TEXT,
            relief="solid",
            bd=1
        )

        normal_entry.pack(
            fill="x",
            padx=25,
            ipady=8
        )

        tk.Label(
            card,
            text="Example: advertisements, newsletters, promotions",
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.LIGHT_TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 25)
        )

        tk.Button(
            card,
            text="♡  SAVE SETTINGS",
            command=lambda: messagebox.showinfo(
                "Settings Saved ♡",
                "Your preferences have been saved."
            ),
            font=("Arial", 10, "bold"),
            bg=self.LAVENDER,
            fg=self.DARK_PURPLE,
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2"
        ).pack(
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