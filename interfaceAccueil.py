import tkinter as tk
from tkinter.font import Font
import os


from interfaceWelshPowel import WelchPowellApp
from interfaceKruskal import KruskalApp
from interfaceDijkstra import DijkstraApp
from interfaceBellmanFord import BellmanFordApp
from interfaceSteppingStone import SteppingStoneApp
from interfaceFordFulkerson import FordFulkersonApp
from interfacePotentielMetra import MetraApp

class HomeScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        # Modern color palette with your colors
        self.colors = {
            'primary': '#734158',
            'icon': '#9AACB5',
            'secondary': '#C890A7',
            'accent': '#E195AB',
            'background': 'white',
            'card_bg': '#FFFFFF',
            'text_dark': 'black',
            'text_light': '#FFFFFF',
            'hover': '#DB617D',
            'button_bg': '#C67F89',
            'button_hover': '#A63760',
            'card_border': '#9AACB5',
            'card_hover': '#D6DEDD'
        }

        # Algorithm icons
        self.icons = {
            'Welsh-Powell': '🎨',
            'Kruskal': '🌳',
            'Dijkstra': '🚦',
            'Bellman-Ford': '🛣️',
            'Stepping Stone': '🗺️',
            'Ford-Fulkerson': '🔄',
            'Potentiel Metra': '📊'
        }

        self.master.title("Operational Research Algorithms")
        self.master.geometry("1100x750")
        self.master.configure(bg=self.colors['background'])

        self.frame_content = tk.Frame(self, bg=self.colors['background'])
        self.frame_content.pack(fill=tk.BOTH, expand=True)

        self.pack(fill=tk.BOTH, expand=True)
        self.show_home()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_hover_effect(self, widget, start_color, hover_color):
        def on_enter(e):
            widget.configure(bg=hover_color)
        def on_leave(e):
            widget.configure(bg=start_color)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def create_card_hover_effect(self, card):
        def on_enter(e):
            card.configure(bg=self.colors['card_hover'])
            for child in card.winfo_children():
                if not isinstance(child, tk.Button):  # Skip buttons
                    child.configure(bg=self.colors['card_hover'])
        def on_leave(e):
            card.configure(bg=self.colors['card_bg'])
            for child in card.winfo_children():
                if not isinstance(child, tk.Button):  # Skip buttons
                    child.configure(bg=self.colors['card_bg'])
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)

    def show_home(self):
        for widget in self.frame_content.winfo_children():
            widget.destroy()

        # Header with gradient effect
        header_frame = tk.Frame(self.frame_content, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Title with modern styling
        title_container = tk.Frame(header_frame, bg=self.colors['primary'])
        title_container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            title_container,
            text="Operational Research Algorithms",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['text_light']
        ).pack()

        # Exit Button
        exit_btn = tk.Button(
            header_frame,
            text="Exit",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['button_hover'],
            fg=self.colors['text_light'],
            activebackground=self.colors['button_hover'],
            activeforeground=self.colors['text_light'],
            command=self.on_closing,
            relief=tk.FLAT,
            width=5,
            cursor="hand2"
        )
        exit_btn.place(relx=0.95, rely=0.5, anchor="center")
        self.create_hover_effect(exit_btn, self.colors['button_bg'], self.colors['button_hover'])

        # Card container with reduced padding
        card_frame = tk.Frame(self.frame_content, bg=self.colors['background'], pady=10, padx=10)
        card_frame.pack(expand=True, fill=tk.BOTH)

        # Algorithm cards
        algorithms = [
            ("Welsh-Powell", self.open_welsh_powell, "Graph Coloring"),
            ("Kruskal", self.open_kruskal, "Minimum Spanning Trees"),
            ("Dijkstra", self.open_dijkstra, "Shortest Paths"),
            ("Bellman-Ford", self.open_bellman_ford, "Weighted Shortest Paths"),
            ("Stepping Stone", self.open_stepping_stone, "Transportation Optimization"),
            ("Ford-Fulkerson", self.open_ford_fulkerson, "Maximum Flow Calculation"),
            ("Potentiel Metra", self.open_potential_metra, "Potential Diagram"),
        ]

        for idx, (title, command, description) in enumerate(algorithms):
            # Reduced card size
            card = tk.Frame(
                card_frame,
                bg=self.colors['card_bg'],
                relief=tk.RAISED,
                bd=0,
                highlightthickness=2,
                highlightbackground=self.colors['card_border']
            )
            card.grid(row=idx // 3, column=idx % 3, padx=4, pady=4, sticky="nsew")

            # Icon with reduced padding
            tk.Label(
                card,
                text=self.icons.get(title, '📊'),
                font=("Segoe UI Emoji", 28),  # Reduced font size
                bg=self.colors['card_bg'],
                fg=self.colors['icon']
            ).pack(pady=(10, 5))  # Reduced padding

            # Title
            tk.Label(
                card,
                text=title,
                font=("Futura", 12, "bold"),  # Slightly reduced font size
                bg=self.colors['card_bg'],
                fg=self.colors['text_dark']
            ).pack(pady=3)  # Reduced padding

            # Description
            tk.Label(
                card,
                text=description,
                font=("Helvetica", 9),  # Reduced font size
                bg=self.colors['card_bg'],
                fg=self.colors['text_dark'],
                wraplength=140  # Reduced wraplength
            ).pack(pady=3)  # Reduced padding

            # Button
            btn = tk.Button(
                card,
                text="Open",
                font=("Helvetica", 10, "bold"),
                bg=self.colors['button_bg'],
                fg=self.colors['text_light'],
                activebackground=self.colors['button_hover'],
                activeforeground=self.colors['text_light'],
                command=command,
                relief=tk.FLAT,
                cursor="hand2",
                width=10  # Slightly reduced width
            )
            btn.pack(pady=(3, 10))  # Reduced padding
            
            self.create_hover_effect(btn, self.colors['button_bg'], self.colors['button_hover'])
            self.create_card_hover_effect(card)

        # Configure grid
        for col in range(3):
            card_frame.grid_columnconfigure(col, weight=1)

    def on_closing(self):
        self.master.destroy()
        os._exit(0)

    # Algorithm opening methods remain the same
    def open_welsh_powell(self):
        self.master.withdraw()
        WelchPowellApp(self.master)

    def open_kruskal(self):
        self.master.withdraw()
        KruskalApp(self.master)

    def open_dijkstra(self):
        self.master.withdraw()
        DijkstraApp(self.master)

    def open_bellman_ford(self):
        self.master.withdraw()
        BellmanFordApp(self.master)

    def open_stepping_stone(self):
        self.master.withdraw()
        SteppingStoneApp(self.master)

    def open_ford_fulkerson(self):
        self.master.withdraw()
        FordFulkersonApp(self.master)

    def open_potential_metra(self):
        self.master.withdraw()
        MetraApp(self.master)