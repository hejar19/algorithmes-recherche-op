import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SteppingStoneApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(self.parent)
        self.top.title("Stepping Stone Algorithm")
        self.top.geometry("800x600")
        
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
        
        # Container principal
        self.main_container = tk.Frame(self.top, bg=self.colors['bg'], padx=40, pady=30)
        self.main_container.pack(fill="both", expand=True)
        
        self.create_header()
        self.create_input_section()
        self.create_graph_section()
        self.create_result_section()
        self.create_buttons()
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
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 30))

        title = tk.Label(header_frame, 
                         text="Stepping Stone Algorithm", 
                         font=("Helvetica Neue", 32, "bold"),
                         bg=self.colors['bg'],
                         fg=self.colors['primary'])
        title.pack()


    def create_input_section(self):
        input_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        input_frame.pack(fill="x", pady=20)

        # First Row: Start and End Nodes
        path_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        path_frame.pack(fill="x", pady=(0, 15))

        tk.Label(path_frame,
                 text="Start Node:",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(0, 10))

        self.start_entry = tk.Entry(path_frame,
                                    font=("Helvetica Neue", 14),
                                    bd=0,
                                    bg=self.colors['accent'],
                                    fg=self.colors['secondary'],
                                    insertbackground=self.colors['primary'],
                                    relief="flat",
                                    width=18)
        self.start_entry.pack(side="left", padx=10)

        tk.Label(path_frame,
                 text="End Node:",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(20, 10))

        self.end_entry = tk.Entry(path_frame,
                                  font=("Helvetica Neue", 14),
                                  bd=0,
                                  bg=self.colors['accent'],
                                  fg=self.colors['secondary'],
                                  insertbackground=self.colors['primary'],
                                  relief="flat",
                                  width=18)
        self.end_entry.pack(side="left", padx=10)

        # Second Row: Edges
        edges_frame = tk.Frame(input_frame, bg=self.colors['bg'])
        edges_frame.pack(fill="x", pady=10)

        tk.Label(edges_frame,
                 text="Edges (e.g., A-B-1):",
                 font=("Helvetica Neue", 12),
                 bg=self.colors['bg'],
                 fg=self.colors['secondary']).pack(side="left", padx=(0, 10))

        self.edges_entry = tk.Entry(edges_frame,
                                    font=("Helvetica Neue", 14),
                                    bd=0,
                                    bg=self.colors['accent'],
                                    fg=self.colors['secondary'],
                                    insertbackground=self.colors['primary'],
                                    relief="flat",
                                    width=40)
        self.edges_entry.pack(side="left", padx=10)

    def create_result_section(self):
        self.result_var = StringVar()
        self.result_var.set("Ready to find the shortest path")

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

        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()

    def create_return_button(self):
        return_button = tk.Button(self.main_container,
                                  text="Return",
                                  command=self.return_to_main,
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
        return_button.pack(pady=20)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.run_button = ttk.Button(button_frame, text="Run Algorithm", command=self.run_algorithm)
        self.run_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.back_button = ttk.Button(button_frame, text="Back", command=self.return_home())
        self.back_button.grid(row=0, column=1, padx=5, pady=5)

    def run_algorithm(self):
        start_node = self.start_entry.get().strip()
        end_node = self.end_entry.get().strip()
        edges_input = self.edges_entry.get().strip().split(',')

        if not start_node or not end_node or not edges_input:
            messagebox.showerror("Input Error", "Please fill all input fields.")
            return
        
        graph = nx.Graph()
        for edge in edges_input:
            try:
                u, v, weight = edge.split('-')
                graph.add_edge(u.strip(), v.strip(), weight=float(weight.strip()))
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid edge format: {edge}")
                return
        
        try:
            path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
            path_length = nx.shortest_path_length(graph, source=start_node, target=end_node, weight='weight')
            self.display_result(f"Shortest path from {start_node} to {end_node}: {' -> '.join(path)}\nPath length: {path_length}")
            self.draw_graph(graph, path)
        except nx.NetworkXNoPath:
            self.display_result("No path exists between the specified nodes.")
        except nx.NodeNotFound as e:
            self.display_result(str(e))

    def draw_graph(self, graph, path):
        self.ax.clear()
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray')
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2, ax=self.ax)
        self.canvas.draw()

    def display_result(self, text):
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state='disabled')
