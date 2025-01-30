# welcome.py
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys


# Utility for resource paths :
def resource_path(relative_path):
    """Retourne le chemin absolu pour la ressource, adapté au packaging PyInstaller"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class WelcomeScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # We now use master for window properties
        self.master.title("Welcome")
        self.master.configure(bg="#F4F6F6")
        self.master.geometry("1000x700")

        # Main container with two columns (now inside self, rather than self.root)
        self.container = tk.Frame(self, bg="#F4F6F6")
        self.container.pack(expand=True, fill=tk.BOTH)

        # Left column for information
        self.left_frame = tk.Frame(self.container, bg="#F4F6F6", width=500)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Right column with gradient effect
        self.right_frame = tk.Frame(self.container, bg="#EEE2DF", width=500)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._create_left_content()
        self._create_right_content()

        # Center the window:
        self.center_window()

    def _create_left_content(self):
        # Logo (path adjusted for PyInstaller packaging)
        try:
            logo_path = resource_path("logoEmsi.png")
            logo = Image.open(logo_path)
            logo = logo.resize((400, 100), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.left_frame, image=self.logo_img, bg="#F4F6F6")
            logo_label.pack(pady=(40, 30))
        except Exception as e:
            print(f"Erreur lors de l'affichage du logo : {e}")

        # Title with decorative elements
        title_frame = tk.Frame(self.left_frame, bg="#F4F6F6")
        title_frame.pack(fill=tk.X, pady=(20, 30))

        title = tk.Label(
            title_frame,
            text="Algorithms of",
            font=("Montserrat", 32, "bold"),
            bg="#F4F6F6",
            fg="#734158"
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="Operational Research",
            font=("Montserrat", 28, "bold"),
            bg="#F4F6F6",
            fg="#C67F89"
        )
        subtitle.pack()

        # Animated separator
        separator = tk.Frame(self.left_frame, height=3, width=0, bg="#C67F89")
        separator.pack(pady=(0, 30))

        def expand_line():
            current_width = separator.winfo_width()
            if current_width < 100:
                separator.configure(width=current_width + 2)
                self.master.after(10, expand_line)

        self.master.after(500, expand_line)

        # Student info
        self._create_info_card("Presented by", "ELYAMANI Hajar", 10)
        # Professor info
        self._create_info_card("Under the supervision of", "EL MKHALET Mouna", 10)

    def _create_info_card(self, label_text, name_text, pady):
        frame = tk.Frame(self.left_frame, bg="#F4F6F6")
        frame.pack(fill=tk.X, pady=pady)

        tk.Label(
            frame,
            text=label_text,
            font=("Helvetica", 12),
            bg="#F4F6F6",
            fg="#7B8D93"
        ).pack()

        tk.Label(
            frame,
            text=name_text,
            font=("Montserrat", 16, "bold"),
            bg="#F4F6F6",
            fg="#2C3E50"
        ).pack()

    def _create_right_content(self):
        content_frame = tk.Frame(self.right_frame, bg="#EEE2DF", padx=30)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome text
        welcome_label = tk.Label(
            content_frame,
            text="Welcome to",
            font=("Montserrat", 24, "bold"),
            bg="#EEE2DF",
            fg="#2C3E50"
        )
        welcome_label.pack(pady=(0, 20))

        # Description
        description = tk.Label(
            content_frame,
            text="Discover a comprehensive suite of\noperational research algorithms",
            font=("Helvetica", 14, "italic"),
            bg="#EEE2DF",
            fg="#2C3E50",
            justify="center"
        )
        description.pack(pady=(0, 30))

        # Algorithm list with custom bullets
        algorithms = [
            "Graph Coloring",
            "Minimum Spanning Trees",
            "Shortest Paths",
            "Flow Optimization"
        ]

        for algo in algorithms:
            algo_frame = tk.Frame(content_frame, bg="#EEE2DF")
            algo_frame.pack(fill=tk.X, pady=5)

            bullet = tk.Label(
                algo_frame,
                text="✦",
                font=("Helvetica", 14),
                bg="#EEE2DF",
                fg="#734158"
            )
            bullet.pack(side=tk.LEFT, padx=(0, 10))

            tk.Label(
                algo_frame,
                text=algo,
                font=("Helvetica", 13),
                bg="#EEE2DF",
                fg="#2C3E50"
            ).pack(side=tk.LEFT)

        # Start button
        start_button = tk.Button(
            content_frame,
            text="GET STARTED",
            font=("Montserrat", 14, "bold"),
            bg="white",
            fg="#734158",
            activebackground="#C67F89",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_main_app,
            width=20,
            height=2
        )
        start_button.pack(pady=(40, 0))

        # Hover effects
        def on_enter(e):
            start_button.configure(bg="#C67F89", fg="white", relief=tk.RAISED)

        def on_leave(e):
            start_button.configure(bg="white", fg="#734158", relief=tk.FLAT)

        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)

    def center_window(self):
        # Force geometry update so winfo_width/winfo_height are valid
        self.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def start_main_app(self):
        """
        When the user clicks GET STARTED, destroy the welcome screen
        and create the home screen in the same root window.
        """
        # Clear everything in the root
        for widget in self.master.winfo_children():
            widget.destroy()

        # Now import and show the home screen
        from interfaceAccueil import HomeScreen
        home = HomeScreen(self.master)
        home.pack(fill=tk.BOTH, expand=True)
