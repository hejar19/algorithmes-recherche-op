import random
import time
import networkx as nx
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, Frame, StringVar, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def generate_random_graph(num_vertices):
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.choice([True, False]):
                G.add_edge(i, j)
    return G

def welch_powell(G):
    sommets_tries = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    couleur_sommets = {}
    for sommet in sommets_tries:
        couleurs_interdites = {couleur_sommets.get(voisin) for voisin in G.neighbors(sommet) if voisin in couleur_sommets}
        for couleur in range(len(G.nodes())):
            if couleur not in couleurs_interdites:
                couleur_sommets[sommet] = couleur
                break
    return couleur_sommets

def appliquer_couleurs(ax, G, coloration):
    n = max(coloration.values()) + 1
    couleurs_pastel = ['#FFB5B5', '#B5FFB5', '#B5B5FF', '#FFE5B5', '#E5B5FF', '#B5FFE5', 
                       '#FFB5E5', '#E5FFB5', '#B5E5FF', '#FFD700']
    couleurs_sommets = [couleurs_pastel[coloration[sommet] % len(couleurs_pastel)] for sommet in G.nodes()]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=couleurs_sommets, 
            node_size=1000, font_size=12, font_color='#2C3E50',
            edge_color='#E0E0E0', width=2)

def nombre_chromatique(coloration):
    return max(coloration.values()) + 1

class WelchPowellApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(self.parent)
        self.top.title("Welch-Powell Visualization")
        self.top.geometry("1000x800")
        
        self.colors = {
            'bg': '#F7F9FC',
            'primary': '#734158',
            'secondary': '#2C3E50',
            'rose': '#C67F89',
            'accent': '#E5E9F2',
            'text': '#2C3E50',
            'error': '#FF6B6B'
        }
        
        self.top.configure(bg=self.colors['bg'])
        self.setup_interface()

        # Added this if the user clicks on x to close the window
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def return_home(self):
        """Close the Toplevel and re-show the main window"""
        self.top.destroy()
        self.parent.deiconify()

    def on_close(self):
        """Called if user clicks x to close the window manually"""
        self.return_home()

    def setup_interface(self):
        # Container principal avec padding
        self.main_container = Frame(self.top, bg=self.colors['bg'], padx=40, pady=30)
        self.main_container.pack(fill="both", expand=True)

        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_graph_section()
        self.create_return_button()

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

    def create_header(self):
        header_frame = Frame(self.main_container, bg=self.colors['bg'])
        header_frame.pack(fill="x", pady=(0, 30))
        
        title = Label(header_frame,
                     text="Welch-Powell Graph Coloring", 
                     font=("Helvetica Neue", 32, "bold"),
                     bg=self.colors['bg'],
                     fg=self.colors['primary'])
        title.pack()
        
        subtitle = Label(header_frame,
                        text="Visualize graph coloring algorithm in real-time",
                        font=("Helvetica Neue", 14),
                        bg=self.colors['bg'],
                        fg=self.colors['secondary'])
        subtitle.pack(pady=(5, 0))

    def create_input_section(self):
        input_frame = Frame(self.main_container, bg=self.colors['bg'])
        input_frame.pack(fill="x", pady=20)

        # Label élégant
        Label(input_frame,
              text="Number of vertices",
              font=("Helvetica Neue", 12),
              bg=self.colors['bg'],
              fg=self.colors['secondary']).grid(row=0, column=0, padx=(0, 10), sticky='w')

        # Zone de texte
        self.num_vertices_entry = Entry(input_frame,
                                      font=("Helvetica Neue", 14),
                                      bd=0,
                                      bg=self.colors['accent'],
                                      fg=self.colors['secondary'],
                                      insertbackground=self.colors['primary'],
                                      relief="flat",
                                      width=50)
        self.num_vertices_entry.grid(row=0, column=1, padx=(0, 10), sticky="w")

        # Utilisation de grid_columnconfigure pour répartir l'espace
        input_frame.grid_columnconfigure(0, weight=1)  # Faire en sorte que la colonne 0 prenne plus de place
        input_frame.grid_columnconfigure(1, weight=1)  # Et la colonne 1 pour laisser de l'espace
        input_frame.grid_columnconfigure(2, weight=0)  # La colonne 2 est statique pour le bouton

        # Bouton aligné à droite
        self.run_button = Button(input_frame,
                               text="Generate Graph",
                               command=self.run_welch_powell,
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
        self.run_button.grid(row=0, column=2, sticky='e', padx=(10, 0))

    def create_result_section(self):
        self.result_var = StringVar()
        self.result_var.set("Ready to generate graph")
        
        self.result_label = Label(self.main_container,
                                textvariable=self.result_var,
                                font=("Helvetica Neue", 12),
                                bg=self.colors['bg'],
                                fg=self.colors['secondary'])
        self.result_label.pack(pady=20)

    def create_graph_section(self):
        self.graph_frame = Frame(self.main_container,
                               bg=self.colors['bg'],
                               relief="flat",
                               bd=1)
        self.graph_frame.pack(fill="both", expand=True)

    def run_welch_powell(self):
        try:
            num_vertices = int(self.num_vertices_entry.get())
            
            if num_vertices < 1:
                raise ValueError("Please enter a positive number")
                

            # Animation de chargement
            self.result_var.set("Generating graph...")
            self.main_container.update()

            random_graph = generate_random_graph(num_vertices)
            start_time = time.time()
            coloration = welch_powell(random_graph)
            end_time = time.time()
            chromatic_number = nombre_chromatique(coloration)

            self.result_var.set(
                f"Chromatic number: {chromatic_number} │ Execution time: {end_time - start_time:.3f}s")

            self.draw_graph(random_graph, coloration)

        except ValueError as e:
            self.result_var.set(f"Error: {str(e)}")
        except Exception as e:
            self.result_var.set(f"An error occurred: {str(e)}")

    def draw_graph(self, graph, coloration):
        # Nettoyer le frame précédent
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Créer une nouvelle figure avec un style moderne
        fig = Figure(figsize=(8, 6), dpi=100, facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg'])
        
        # Appliquer les couleurs et dessiner le graphe
        appliquer_couleurs(ax, graph, coloration)
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
