import tkinter as tk
from tkinter import ttk, StringVar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk, Label, Entry, Button, Frame, Toplevel
import random


class DijkstraApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(self.parent)
        self.top.title("Dijkstra Algorithm Visualization")
        self.top.geometry("1000x800")

        self.colors = {
            'bg': '#F7F9FC',            # Fond principal très clair
            'primary': '#734158',       # Violet moderne
            'secondary': '#2C3E50',     # Bleu foncé
            'rose': '#C67F89',          # Rose
            'accent': '#E5E9F2',        # Gris très clair
            'text': '#2C3E50',          # Couleur du texte
            'error': '#FF6B6B',         # Rouge doux
            'node': '#7EA0B7',          # Vert pastel pour les nœuds
            'edge': '#E0E0E0',          # Gris clair pour les arêtes
            'path': '#C67F89'           # Rose pour le chemin
        }

        self.top.configure(bg=self.colors['bg'])

        # Variables globales
        self.G = None
        self.sommets = []

        # Container principal
        self.main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=40, pady=30)
        self.main_container.pack(fill="both", expand=True)

        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_graph_section()
        self.create_return_button()
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def return_home(self):
        """Close the Toplevel and re-show the main window"""
        self.top.destroy()
        self.parent.deiconify()

    def on_close(self):
        """Called if user clicks x to close the window manually"""
        self.return_home()

    def create_header(self):
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 30))

        title = tk.Label(header_frame, 
                         text="Dijkstra's Algorithm Visualization", 
                         font=("Helvetica Neue", 32, "bold"),
                         bg=self.colors['bg'],
                         fg=self.colors['primary'])
        title.pack()

        subtitle = tk.Label(header_frame,
                             text="Find the shortest path between two vertices",
                             font=("Helvetica Neue", 14),
                             bg=self.colors['bg'],
                             fg=self.colors['secondary'])
        subtitle.pack(pady=(5, 0))

    def create_input_section(self):
        input_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        input_frame.pack(fill="x", pady=20)

        # Première ligne : Nombre de sommets
        vertex_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        vertex_frame.pack(fill="x", pady=(0, 15))

        tk.Label(vertex_frame,
                 text="Number of vertices",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(0, 10))

        self.vertices_entry = tk.Entry(vertex_frame,
                                        font=("Helvetica Neue", 14),
                                        bd=0,
                                        bg=self.colors['accent'],
                                        fg=self.colors['secondary'],
                                        insertbackground=self.colors['primary'],
                                        relief="flat",
                                        width=40)
        self.vertices_entry.pack(side="left", padx=10)

        self.generate_button = tk.Button(vertex_frame,
                                          text="Generate Graph",
                                          command=self.generate_graph,
                                          font=("Helvetica Neue", 12, "bold"),
                                          bg=self.colors['rose'],
                                          fg="white",
                                          activebackground=self.colors['secondary'],
                                          activeforeground="white",
                                          relief="flat",
                                          bd=0,
                                          padx=20,
                                          pady=10,
                                          cursor="hand2")
        self.generate_button.pack(side="right", padx=10)

        # Deuxième ligne : Source et destination
        path_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        path_frame.pack(fill="x", pady=10)

        # Style pour les combobox
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                        background=self.colors['accent'],
                        fieldbackground=self.colors['accent'])

        # Source
        tk.Label(path_frame,
                 text="Source:",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(0, 10))

        self.source_combo = ttk.Combobox(path_frame,
                                         state="readonly",
                                         font=("Helvetica Neue", 12),
                                         style='Custom.TCombobox',
                                         width=18)
        self.source_combo.pack(side="left", padx=20)

        # Destination
        tk.Label(path_frame,
                 text="Target:",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(20, 10))

        self.target_combo = ttk.Combobox(path_frame,
                                         state="readonly",
                                         font=("Helvetica Neue", 12),
                                         style='Custom.TCombobox',
                                         width=18)
        self.target_combo.pack(side="left", padx=30)

        # Bouton Calculate
        self.calculate_button = tk.Button(path_frame,
                                           text="Find Shortest Path",
                                           command=self.execute_dijkstra,
                                           font=("Helvetica Neue", 12, "bold"),
                                           bg=self.colors['rose'],
                                           fg="white",
                                           activebackground=self.colors['secondary'],
                                           activeforeground="white",
                                           relief="flat",
                                           bd=0,
                                           padx=20,
                                           pady=10,
                                           cursor="hand2")
        self.calculate_button.pack(side="right", padx=10)

    def create_result_section(self):
        self.result_var = StringVar()
        self.result_var.set("Ready to generate graph")

        self.result_label = tk.Label(self.main_container,
                                     textvariable=self.result_var,
                                     font=("Helvetica Neue", 12),
                                     bg=self.colors['bg'],
                                     fg=self.colors['secondary'],
                                     justify="left",
                                     wraplength=900)
        self.result_label.pack(pady=20)

    def create_graph_section(self):
        self.graph_frame = tk.Frame(self.main_container,
                                     bg=self.colors['bg'],
                                     relief="flat",
                                     bd=1)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_return_button(self):
        # Bouton de retour
        return_button = Button(
            self.main_container,
            text="Return to home",
            command=self.return_home,
            font=("Helvetica Neue", 12, "bold"),
            bg=self.colors['rose'],
            fg="white",
            activebackground=self.colors['secondary'],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        return_button.pack(side="bottom", pady=20)
        

    def generate_graph(self):
        try:
            n_vertices = int(self.vertices_entry.get())
            if n_vertices < 2:
                raise ValueError("Please enter at least 2 vertices")

            self.G = nx.Graph()
            self.sommets = [f"X{i}" for i in range(n_vertices)]

            # Créer les nœuds et les arêtes
            for sommet in self.sommets:
                self.G.add_node(sommet)
            for i in range(n_vertices):
                for j in range(i + 1, n_vertices):
                    poids = random.randint(1, 100)
                    self.G.add_edge(self.sommets[i], self.sommets[j], weight=poids)

            # Mettre à jour les combobox
            self.source_combo['values'] = self.sommets
            self.target_combo['values'] = self.sommets

            self.draw_graph()
            self.result_var.set("Graph generated successfully. Select source and target vertices.")

        except ValueError as e:
            self.result_var.set(f"Error: {str(e)}")

    def execute_dijkstra(self):
        source = self.source_combo.get()
        target = self.target_combo.get()

        if not source or not target:
            self.result_var.set("Please select both source and target vertices")
            return

        try:
            distance, path = nx.single_source_dijkstra(self.G, source, target, weight='weight')
            path_edges = list(zip(path[:-1], path[1:]))
            self.draw_graph(path_edges)

            path_str = " → ".join(path)
            self.result_var.set(f"Shortest path: {path_str}\nTotal distance: {distance} units")

        except nx.NetworkXNoPath:
            self.result_var.set("No path exists between the selected vertices")

    def draw_graph(self, highlighted_path=[]):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(8, 6), dpi=80, facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg'])

        pos = nx.spring_layout(self.G)

        # Dessiner les arêtes
        nx.draw_networkx_edges(self.G, pos,
                                edge_color=self.colors['edge'],
                                width=2,
                                ax=ax)

        # Dessiner le chemin surligné
        if highlighted_path:
            nx.draw_networkx_edges(self.G, pos,
                                    edgelist=highlighted_path,
                                    edge_color=self.colors['path'],
                                    width=3,
                                    ax=ax)

        # Dessiner les nœuds
        nx.draw_networkx_nodes(self.G, pos,
                                node_color=self.colors['node'],
                                node_size=1000,
                                ax=ax)

        # Ajouter les labels
        nx.draw_networkx_labels(self.G, pos,
                                 font_size=12,
                                 font_color=self.colors['secondary'],
                                 ax=ax)

        # Ajouter les poids des arêtes
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos,
                                      edge_labels=edge_labels,
                                      font_size=10,
                                      ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
