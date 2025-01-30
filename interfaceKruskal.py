import tkinter as tk
from tkinter import messagebox, Frame, Label, Button, Entry, StringVar, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
import random
import string


def generate_graph(num_vertices):
    def generate_labels(n):
        labels = []
        alphabet = string.ascii_uppercase
        for i in range(n):
            label = ""
            temp = i
            while temp >= 0:
                label = alphabet[temp % 26] + label
                temp = temp // 26 - 1
            labels.append(label)
        return labels

    labels = generate_labels(num_vertices)

    G = nx.Graph()
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            weight = random.randint(1, 100)
            G.add_edge(labels[i], labels[j], weight=weight)

    return G


def apply_kruskal(G):
    mst = nx.minimum_spanning_edges(G, algorithm="kruskal", data=True)
    mst_edges = list(mst)
    total_cost = sum([data['weight'] for u, v, data in mst_edges])
    return mst_edges, total_cost


def visualize_graph(G, mst_edges):
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10,
            font_weight='bold', edge_color='gray')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    mst_edges_list = [(u, v) for u, v, data in mst_edges]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges_list, edge_color='green', width=2)

    figure = plt.gcf()
    plt.close()
    return figure


class KruskalApp:
    def __init__(self, parent):
        self.parent = parent
        self.top = Toplevel(self.parent)
        self.top.title("Kruskal's Algorithm Visualization")
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

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.return_home()

    def return_home(self):
        self.top.destroy()
        self.parent.deiconify()

    def setup_interface(self):
        self.main_container = Frame(self.top, bg=self.colors['bg'], padx=40, pady=30)
        self.main_container.pack(fill="both", expand=True)

        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_graph_section()
        self.create_return_button()

    def create_return_button(self):
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
                      text="Kruskal's Algorithm Visualization",
                      font=("Helvetica Neue", 32, "bold"),
                      bg=self.colors['bg'],
                      fg=self.colors['primary'])
        title.pack()

        subtitle = Label(header_frame,
                         text="Visualize the Minimum Spanning Tree",
                         font=("Helvetica Neue", 14),
                         bg=self.colors['bg'],
                         fg=self.colors['secondary'])
        subtitle.pack(pady=(5, 0))

    def create_input_section(self):
        input_frame = Frame(self.main_container, bg=self.colors['bg'])
        input_frame.pack(fill="x", pady=20)

        Label(input_frame,
              text="Number of vertices",
              font=("Helvetica Neue", 12),
              bg=self.colors['bg'],
              fg=self.colors['secondary']).grid(row=0, column=0, padx=(0, 10), sticky='w')

        self.num_vertices_entry = Entry(input_frame,
                                        font=("Helvetica Neue", 14),
                                        bd=0,
                                        bg=self.colors['accent'],
                                        fg=self.colors['secondary'],
                                        insertbackground=self.colors['primary'],
                                        relief="flat",
                                        width=50)
        self.num_vertices_entry.grid(row=0, column=1, padx=(0, 10), sticky="w")

        self.run_button = Button(input_frame,
                                 text="Generate Graph",
                                 command=self.generate_graph_action,
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

    def generate_graph_action(self):
        try:
            num_vertices = int(self.num_vertices_entry.get())
            if num_vertices < 2:
                raise ValueError("Please enter a number greater than 1.")

            self.result_var.set("Generating graph...")
            self.main_container.update()

            G = generate_graph(num_vertices)
            mst_edges, total_cost = apply_kruskal(G)

            self.result_var.set(f"Minimal spanning tree cost: {total_cost}")

            self.draw_graph(G, mst_edges)

        except ValueError as e:
            self.result_var.set(f"Error: {str(e)}")
        except Exception as e:
            self.result_var.set(f"An error occurred: {str(e)}")

    def draw_graph(self, G, mst_edges):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = visualize_graph(G, mst_edges)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
