import tkinter as tk
from tkinter import ttk, StringVar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random


class BellmanFordApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(self.parent)
        self.top.title("Bellman-Ford Algorithm Visualization")
        self.top.geometry("1200x1000")
        
        # Thème de couleurs moderne
        self.colors = {
            'bg': '#F7F9FC',
            'primary': '#734158',
            'secondary': '#2C3E50',
            'rose': '#C67F89',
            'accent': '#E5E9F2',
            'text': '#2C3E50',
            'error': '#FF6B6B',
            'node': '#7EA0B7',
            'edge': '#E0E0E0',
            'path': '#C67F89'
        }
        
        self.top.configure(bg=self.colors['bg'])
        
        # Variables globales
        self.G = None
        self.sommets = []
        
        # Container principal
        self.main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)
        
        # Bouton "Retour"
        self.add_return_button()
        
        # Création d'un conteneur supérieur pour les contrôles
        self.controls_container = tk.Frame(self.main_container, bg=self.colors['bg'])
        self.controls_container.pack(fill="x", pady=(0, 10))
        
        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_graph_section()
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def return_home(self):
        """Close the Toplevel and re-show the main window"""
        self.top.destroy()
        self.parent.deiconify()

    def on_close(self):
        """Called if user clicks x to close the window manually"""
        self.return_home()

    def add_return_button(self):
        retour_btn = tk.Button(
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
        retour_btn.pack(side="bottom", pady=20)


    def create_header(self):
        header_frame = tk.Frame(self.controls_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(header_frame, 
                        text="Bellman-Ford Algorithm Visualization", 
                        font=("Helvetica Neue", 28, "bold"),
                        bg=self.colors['bg'],
                        fg=self.colors['primary'])
        title.pack()
        
        subtitle = tk.Label(header_frame,
                          text="Find the shortest path in a directed graph",
                          font=("Helvetica Neue", 12),
                          bg=self.colors['bg'],
                          fg=self.colors['secondary'])
        subtitle.pack(pady=(5, 0))

    def create_input_section(self):
        input_frame = tk.Frame(self.controls_container, bg=self.colors['bg'])
        input_frame.pack(fill="x", pady=10)
        
        # Section nombre de sommets
        vertex_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        vertex_frame.pack(fill="x", pady=(0, 10))
        
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
                                       pady=8,
                                       cursor="hand2")
        self.generate_button.pack(side="right", padx=10)
        
        # Section source et cible
        path_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        path_frame.pack(fill="x", pady=10)
        
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                       background=self.colors['accent'],
                       fieldbackground=self.colors['accent'])
        
        tk.Label(path_frame,
                text="Source:",
                font=("Helvetica Neue", 12),
                bg=self.colors['bg'],
                fg=self.colors['secondary']).pack(side="left", padx=(0, 10))
        
        self.source_combo = ttk.Combobox(path_frame,
                                        state="readonly",
                                        font=("Helvetica Neue", 12),
                                        style='Custom.TCombobox',
                                        width=15)
        self.source_combo.pack(side="left", padx=10)
        
        tk.Label(path_frame,
                text="Target:",
                font=("Helvetica Neue", 12),
                bg=self.colors['bg'],
                fg=self.colors['secondary']).pack(side="left", padx=(20, 10))
        
        self.target_combo = ttk.Combobox(path_frame,
                                        state="readonly",
                                        font=("Helvetica Neue", 12),
                                        style='Custom.TCombobox',
                                        width=15)
        self.target_combo.pack(side="left", padx=10)
        
        self.calculate_button = tk.Button(path_frame,
                                        text="Find Shortest Path",
                                        command=self.execute_bellman_ford,
                                        font=("Helvetica Neue", 12, "bold"),
                                        bg=self.colors['rose'],
                                        fg="white",
                                        activebackground=self.colors['secondary'],
                                        activeforeground="white",
                                        relief="flat",
                                        bd=0,
                                        padx=20,
                                        pady=8,
                                        cursor="hand2")
        self.calculate_button.pack(side="right", padx=10)

    def create_result_section(self):
        self.result_var = StringVar()
        self.result_var.set("Ready to generate graph")
        
        self.result_label = tk.Label(self.controls_container,
                                   textvariable=self.result_var,
                                   font=("Helvetica Neue", 12),
                                   bg=self.colors['bg'],
                                   fg=self.colors['secondary'],
                                   justify="left",
                                   wraplength=900)
        self.result_label.pack(pady=10)

    def create_graph_section(self):
        self.graph_frame = tk.Frame(self.main_container,
                                  bg=self.colors['bg'],
                                  relief="flat",
                                  bd=1)
        self.graph_frame.pack(fill="both", expand=True)

    # Les autres méthodes (generate_graph, execute_bellman_ford, etc.) restent identiques.
    def generate_graph(self):
        try:
            n_vertices = int(self.vertices_entry.get())
            if n_vertices < 2:
                raise ValueError("Please enter at least 2 vertices")
            
            self.G = nx.DiGraph()
            self.sommets = [f"X{i}" for i in range(n_vertices)]
            
            for sommet in self.sommets:
                self.G.add_node(sommet)
            for i in range(n_vertices):
                for j in range(i + 1, n_vertices):
                    if random.choice([True, False]):
                        self.G.add_edge(self.sommets[i], self.sommets[j], weight=random.randint(1, 10))
                    else:
                        self.G.add_edge(self.sommets[j], self.sommets[i], weight=random.randint(1, 10))
            
            self.source_combo['values'] = self.sommets
            self.target_combo['values'] = self.sommets
            
            self.draw_graph()
            self.result_var.set("Graph generated successfully. Select source and target vertices.")
            
        except ValueError as e:
            self.result_var.set(f"Error: {str(e)}")

    def execute_bellman_ford(self):
        source = self.source_combo.get()
        target = self.target_combo.get()
        
        if not source or not target:
            self.result_var.set("Please select both source and target vertices")
            return
        
        try:
            # Get both distances and paths from the Bellman-Ford algorithm
            distance, path = nx.single_source_bellman_ford(self.G, source)
            
            if target not in path:
                self.result_var.set("No path exists between the selected vertices")
                self.draw_graph()  # Redraw the graph without highlighting any path
                return
            
            shortest_path = path[target]
            path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
            self.draw_graph(path_edges)
            
            path_str = " → ".join(shortest_path)
            self.result_var.set(f"Shortest path: {path_str}\nTotal distance: {distance[target]} units")
            
        except nx.NetworkXError as e:
            self.result_var.set(f"Error: {str(e)}")


    def draw_graph(self, highlighted_path=[]):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg'])
        
        pos = nx.spring_layout(self.G, k=1, iterations=50)
        
        # Dessin des arêtes avec flèches
        nx.draw_networkx_edges(self.G, pos,
                             edge_color=self.colors['edge'],
                             width=2,
                             ax=ax,
                             arrows=True,
                             arrowsize=20)
        
        if highlighted_path:
            nx.draw_networkx_edges(self.G, pos,
                                 edgelist=highlighted_path,
                                 edge_color=self.colors['path'],
                                 width=4,
                                 ax=ax,
                                 arrows=True,
                                 arrowsize=25)
        
        nx.draw_networkx_nodes(self.G, pos,
                             node_color=self.colors['node'],
                             node_size=1200,
                             ax=ax)
        
        nx.draw_networkx_labels(self.G, pos,
                              font_size=14,
                              font_color=self.colors['secondary'],
                              ax=ax)
        
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos,
                                   edge_labels=edge_labels,
                                   font_size=12,
                                   ax=ax)
        
        plt.margins(0.2)
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
