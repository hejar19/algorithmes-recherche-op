import tkinter as tk
from tkinter import StringVar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import numpy as np

class MetraApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(self.parent)
        self.top.title("METRA Algorithm Visualization")
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
            'path': '#C67F89',
            'critical': '#84033C'
        }
        
        self.top.configure(bg=self.colors['bg'])
        self.setup_interface()

        # Gestion de la fermeture de la fenêtre
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def return_home(self):
        """Ferme la fenêtre actuelle et revient à la fenêtre d'accueil"""
        self.top.destroy()
        self.parent.deiconify()

    def on_close(self):
        """Appelé lorsque l'utilisateur clique sur la croix pour fermer la fenêtre"""
        self.return_home()

    def setup_interface(self):
        # Container principal avec padding
        self.main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)
        
        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_graph_section()
        self.create_return_button()

    def create_return_button(self):
        # Bouton de retour
        return_button = tk.Button(
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

    def create_header(self):
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 30))
        
        title = tk.Label(header_frame,
                         text="METRA Algorithm Visualization",
                         font=("Helvetica Neue", 28, "bold"),
                         bg=self.colors['bg'],
                         fg=self.colors['primary'])
        title.pack()
        
        subtitle = tk.Label(header_frame,
                            text="Critical Path Method for Project Management",
                            font=("Helvetica Neue", 12),
                            bg=self.colors['bg'],
                            fg=self.colors['secondary'])
        subtitle.pack(pady=(5, 0))

    def create_input_section(self):
        input_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        input_frame.pack(fill="x", pady=10)
        
        tk.Label(input_frame,
                 text="Number of tasks:",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(0, 10))
        
        self.tasks_entry = tk.Entry(input_frame,
                                     font=("Helvetica Neue", 14),
                                     bd=0,
                                     bg=self.colors['accent'],
                                     fg=self.colors['secondary'],
                                     insertbackground=self.colors['primary'],
                                     relief="flat",
                                     width=40)
        self.tasks_entry.pack(side="left", padx=10)
        
        self.generate_button = tk.Button(input_frame,
                                         text="Generate Tasks",
                                         command=self.generate_tasks_action,
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

    def create_result_section(self):
        self.result_var = StringVar()
        self.result_var.set("Enter the number of tasks and click 'Generate Tasks' to begin.")
        
        self.result_label = tk.Label(self.main_container,
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

    def generate_tasks(self, num_tasks):
        tasks = {}
        for task in range(1, num_tasks + 1):
            duration = random.randint(1, 10)
            precedence = random.sample(range(1, task), min(random.randint(0, task - 1), 2))  # Limite à max 2 précédences
            tasks[task] = {"duration": duration, "precedence": precedence}
        
        tasks["Début"] = {"duration": 0, "precedence": []}
        tasks["Fin"] = {"duration": 0, "precedence": []}
        
        for task in range(1, num_tasks + 1):
            has_successor = False
            for other_task in tasks.values():
                if task in other_task["precedence"]:
                    has_successor = True
                    break
            if not has_successor:
                tasks["Fin"]["precedence"].append(task)

        for task, info in tasks.items():
            if task != "Début" and not info["precedence"]:
                tasks[task]["precedence"].append("Début")

        return tasks

    def metra_algorithm(self, tasks):
        G = nx.DiGraph()
        for task, info in tasks.items():
            G.add_node(task, duration=info["duration"])
            for pred in info["precedence"]:
                G.add_edge(pred, task)

        earliest_start = {node: 0 for node in G.nodes}
        for node in nx.topological_sort(G):
            for pred in G.predecessors(node):
                earliest_start[node] = max(earliest_start[node], 
                                        earliest_start[pred] + G.nodes[pred]["duration"])

        project_duration = max(earliest_start.values())
        latest_finish = {node: project_duration for node in G.nodes}
        for node in reversed(list(nx.topological_sort(G))):
            for succ in G.successors(node):
                latest_finish[node] = min(latest_finish[node], 
                                       latest_finish[succ] - G.nodes[node]["duration"])

        critical_nodes = [node for node in G.nodes 
                         if earliest_start[node] == latest_finish[node]]
        
        all_paths = list(nx.all_simple_paths(G, "Début", "Fin"))
        critical_path = max(all_paths, 
                          key=lambda path: sum(1 for node in path if node in critical_nodes))
        
        return G, earliest_start, latest_finish, critical_path, project_duration

    def plot_graph(self, G, critical_path):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg'])
        
        levels = {}
        levels["Début"] = 0
        
        for node in nx.topological_sort(G):
            if node == "Début":
                continue
            if node == "Fin":
                levels[node] = len(levels)
                continue
            pred_levels = [levels[pred] for pred in G.predecessors(node) if pred in levels]
            levels[node] = max(pred_levels) + 1 if pred_levels else 1

        pos = {}
        level_nodes = {}
        
        for node, level in levels.items():
            if level not in level_nodes:
                level_nodes[level] = []
            level_nodes[level].append(node)
        
        max_level = max(levels.values())
        for level, nodes in level_nodes.items():
            y_positions = np.linspace(-1, 1, len(nodes))
            for node, y in zip(nodes, y_positions):
                pos[node] = (level / max_level, y)

        # Dessiner les arêtes normales
        nx.draw_networkx_edges(G, pos,
                             edge_color=self.colors['edge'],
                             width=2,
                             ax=ax,
                             arrows=True,
                             arrowsize=20)
        
        # Dessiner les arêtes critiques
        critical_edges = [(u, v) for u, v in G.edges 
                         if u in critical_path and v in critical_path]
        nx.draw_networkx_edges(G, pos,
                             edgelist=critical_edges,
                             edge_color=self.colors['critical'],
                             width=3,
                             ax=ax,
                             arrows=True,
                             arrowsize=25)
        
        # Dessiner les nœuds
        nx.draw_networkx_nodes(G, pos,
                             node_color=[self.colors['critical'] if node in critical_path else self.colors['node'] for node in G.nodes],
                             node_size=500,
                             ax=ax)

        nx.draw_networkx_labels(G, pos,
                             font_size=12,
                             font_color=self.colors['text'],
                             font_family="sans-serif",
                             ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    def generate_tasks_action(self):
        try:
            num_tasks = int(self.tasks_entry.get())
            
            if num_tasks < 1:
                raise ValueError("Please enter a valid number of tasks.")
            
            tasks = self.generate_tasks(num_tasks)
            G, earliest_start, latest_finish, critical_path, project_duration = self.metra_algorithm(tasks)
            
            self.result_var.set(f"Critical Path: {critical_path}\nProject Duration: {project_duration}")
            self.plot_graph(G, critical_path)
        
        except ValueError as e:
            self.result_var.set(f"Error: {e}")

