import tkinter as tk
from tkinter import ttk, StringVar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

class FordFulkersonApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(self.parent)
        self.top.title("Ford-Fulkerson Algorithm Visualization")
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
        self.graph = None
        self.initial_graph = None
        
        # Container principal
        self.main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)
        
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
            pady=8,
            cursor="hand2"
        )
        retour_btn.pack(anchor="ne", pady=10, padx=10)

    def create_header(self):
        header_frame = tk.Frame(self.controls_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(header_frame, 
                        text="Ford-Fulkerson Algorithm Visualization", 
                        font=("Helvetica Neue", 28, "bold"),
                        bg=self.colors['bg'],
                        fg=self.colors['primary'])
        title.pack()
        
        subtitle = tk.Label(header_frame,
                          text="Find the maximum flow in a network",
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
                                     width=20)
        self.vertices_entry.pack(side="left", padx=10)

        tk.Label(vertex_frame,
                text="Maximum capacity",
                font=("Helvetica Neue", 12),
                bg=self.colors['bg'],
                fg=self.colors['secondary']).pack(side="left", padx=(20, 10))
        
        self.capacity_entry = tk.Entry(vertex_frame,
                                     font=("Helvetica Neue", 14),
                                     bd=0,
                                     bg=self.colors['accent'],
                                     fg=self.colors['secondary'],
                                     insertbackground=self.colors['primary'],
                                     relief="flat",
                                     width=20)
        self.capacity_entry.pack(side="left", padx=10)
        
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

        # Section calcul
        calc_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        calc_frame.pack(fill="x", pady=10)
        
        self.calculate_button = tk.Button(calc_frame,
                                        text="Calculate Maximum Flow",
                                        command=self.execute_ford_fulkerson,
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

    def generate_valid_graph(self, num_vertices, max_capacity):
        graph = [[0] * num_vertices for _ in range(num_vertices)]
        for _ in range(random.randint(1, 2)):
            intermediate = random.randint(1, num_vertices - 2)
            graph[0][intermediate] = random.randint(1, max_capacity)

        for i in range(1, num_vertices - 1):
            if not any(graph[u][i] > 0 for u in range(0, i)):
                predecessor = random.randint(0, i - 1)
                graph[predecessor][i] = random.randint(1, max_capacity)

            num_edges = random.randint(1, 2)
            possible_targets = [v for v in range(i + 1, num_vertices)]
            for _ in range(num_edges):
                if possible_targets:
                    successor = random.choice(possible_targets)
                    graph[i][successor] = random.randint(1, max_capacity)

        if not any(graph[i][num_vertices - 1] > 0 for i in range(1, num_vertices - 1)):
            forced_task = random.randint(1, num_vertices - 2)
            graph[forced_task][num_vertices - 1] = random.randint(1, max_capacity)

        return graph

    def generate_graph(self):
        try:
            num_vertices = int(self.vertices_entry.get())
            max_capacity = int(self.capacity_entry.get())
            
            if num_vertices < 3:
                raise ValueError("Please enter at least 3 vertices")
            
            self.graph = self.generate_valid_graph(num_vertices, max_capacity)
            self.initial_graph = [row[:] for row in self.graph]
            
            self.draw_graph()
            self.result_var.set("Graph generated successfully. Click 'Calculate Maximum Flow' to find the maximum flow.")
            
        except ValueError as e:
            self.result_var.set(f"Error: {str(e)}")

    def BFS(self, s, t, parent):
        ROW = len(self.graph)
        visited = [False] * ROW
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False

    def execute_ford_fulkerson(self):
        try:
            source = 0
            sink = len(self.graph) - 1
            parent = [-1] * len(self.graph)
            max_flow = 0
            flows = [[0] * len(self.graph) for _ in range(len(self.graph))]

            while self.BFS(source, sink, parent):
                path_flow = float("Inf")
                s = sink
                while s != source:
                    path_flow = min(path_flow, self.graph[parent[s]][s])
                    s = parent[s]

                max_flow += path_flow

                v = sink
                while v != source:
                    u = parent[v]
                    self.graph[u][v] -= path_flow
                    flows[u][v] += path_flow
                    v = parent[v]

            self.draw_graph(flows=flows)
            self.result_var.set(f"Maximum flow: {max_flow}")
            
        except Exception as e:
            self.result_var.set(f"Error during calculation: {str(e)}")

    def draw_graph(self, flows=None):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg'])
        
        G = nx.DiGraph()
        node_labels = {0: 'S', len(self.initial_graph) - 1: 'T'}
        for i in range(1, len(self.initial_graph) - 1):
            node_labels[i] = f'X{i}'

        # Add edges to the graph
        edge_labels = {}
        for u in range(len(self.initial_graph)):
            for v in range(len(self.initial_graph[u])):
                if self.initial_graph[u][v] > 0:
                    G.add_edge(u, v)
                    if flows:
                        edge_labels[(u, v)] = f"{flows[u][v]}/{self.initial_graph[u][v]}"
                    else:
                        edge_labels[(u, v)] = str(self.initial_graph[u][v])
        
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos,
                             edge_color=self.colors['edge'],
                             width=2,
                             ax=ax,
                             arrows=True,
                             arrowsize=20)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos,
                             node_color=self.colors['node'],
                             node_size=1200,
                             ax=ax)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos,
                              labels=node_labels,
                              font_size=14,
                              font_color=self.colors['secondary'],
                              ax=ax)
        
        nx.draw_networkx_edge_labels(G, pos,
                                   edge_labels=edge_labels,
                                   font_size=12,
                                   ax=ax)
        
        plt.margins(0.2)
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


