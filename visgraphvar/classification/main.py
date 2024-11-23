import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import random
import yaml
import os
from pathlib import Path
from visgraphvar.graph_generator import GraphGenerator

current_path = Path(__file__).resolve().parent
sns.set(style="whitegrid")

class ClassificationGraphGenerator(GraphGenerator):
    id_type_graph = {
        "complete" : 1,
        "bipartite" : 2,
        "planar": 3,
        "mesh": 4,
        "cyclic": 5,
        "acyclic": 6,
        "tree": 7,
        "regular": 8
    }
    def generate_graph(self):
        self._draw_graph()
        self._save_graph()

    def generate_complete_graph(self):
        
        self.graph = nx.complete_graph(self.num_nodes)
        pos = nx.spring_layout(self.graph)
        
        nx.draw_networkx_nodes(self.graph, pos, node_color=self.color_node,  node_size=self.node_size)
        nx.draw_networkx_labels(self.graph, pos, font_color=self.color_label)
        nx.draw_networkx_edges(self.graph, pos, edge_color=self.color_edge, arrows=self.arrowsize, arrowsize=self.arrowsize)

    def generate_bipartite_graph(self):
        self.graph = nx.Graph()
        
        left_nodes = ['A', 'B', 'C', 'D', 'E']
        right_nodes = [1, 2, 3, 4, 5]

        self.graph.add_nodes_from(left_nodes, bipartite=0)
        self.graph.add_nodes_from(right_nodes, bipartite=1)

        for left_node in left_nodes:
            for right_node in random.sample(right_nodes, random.randint(1, 3)):
                self.graph.add_edge(left_node, right_node)

        pos = nx.bipartite_layout(self.graph, left_nodes)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=left_nodes, node_color='lightblue', node_size=self.node_size)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=right_nodes, node_color='lightgreen', node_size=self.node_size)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)


    def generate_planar(self):
        self.graph = nx.wheel_graph(self.num_nodes)
        pos = nx.planar_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color=self.color_node, node_size=self.node_size, font_size=12, font_weight='bold')

    def generate_mesh(self):
        
        self.graph = nx.grid_2d_graph(5, 5)
        # Create a layout for the grid
        pos = {(x,y) : (y,-x) for x,y in self.graph.nodes()}

        nx.draw(self.graph, pos, with_labels=True, node_color=self.color_node, 
                node_size=self.node_size, font_size=8,  font_weight='bold', font_color=self.color_label, linewidths=1)
        
    def generate_cyclic(self):
        self.graph = nx.DiGraph()
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)] 
        
        self.graph.add_edges_from(edges)
        
        pos = nx.spring_layout(self.graph) 
        nx.draw(self.graph, pos, node_color=self.color_node, node_size=self.node_size, font_size=8, font_weight='bold', arrows=True, arrowsize=self.arrowsize,)
        
        labels = {i: i for i in self.graph.nodes()}  
        nx.draw_networkx_labels(self.graph, pos, labels, font_color=self.color_label)
        
    def generate_acyclic(self):
        self.graph = nx.DiGraph()
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
        
        self.graph.add_edges_from(edges)
        
        pos = nx.spring_layout(self.graph) 
        nx.draw(self.graph, pos, node_color=self.color_node, node_size=self.node_size, font_size=8, font_weight='bold', arrows=True, arrowsize=self.arrowsize)
        
        labels = {i: i for i in self.graph.nodes()}  
        nx.draw_networkx_labels(self.graph, pos, labels, font_color=self.color_label) 

    def generate_tree(self):

        sns.set(style="whitegrid")
        self.graph = nx.random_tree(n=self.num_nodes)

        pos = nx.spring_layout(self.graph) 
        nx.draw(self.graph, pos, with_labels=True, node_color=self.color_node, node_size=self.node_size, font_size=15, font_weight='bold', font_color=self.color_label, edge_color=self.color_edge, width=1)
        
    def generate_regular(self):
        self.graph = nx.Graph()

        self.graph.add_nodes_from(range(1, self.num_nodes + 1))
        self.num_edges = self.num_nodes
        max_edges = (self.num_nodes * (self.num_nodes - 1)) // 2
        if self.num_edges > max_edges:
            raise ValueError(f"Maximum edges for {self.num_nodes} nodes is {self.num_edges}.")
        
        all_possible_edges = [(i, j) for i in range(1, self.num_nodes + 1) for j in range(i + 1, self.num_nodes + 1)]
        edges = random.sample(all_possible_edges, self.num_edges)
        
        self.graph.add_edges_from(edges)

        pos = nx.spring_layout(self.graph)
        
        nx.draw_networkx_nodes(self.graph, pos, node_color=self.color_node, node_size=self.node_size, alpha=1)
        nx.draw_networkx_edges(self.graph, pos, edgelist=edges, edge_color=self.color_edge, width=1)

    def _draw_graph(self):
        plt.figure(figsize=(6, 6), dpi=100)

        if self.type_graph == "complete":
            self.generate_complete_graph()
        elif self.type_graph == "bipartite":
            self.generate_bipartite_graph()
        elif self.type_graph == "regular":
            self.generate_regular()
        elif self.type_graph == "tree":
            self.generate_tree()
        elif self.type_graph == "planar":
            self.generate_planar()
        elif self.type_graph == "mesh":
            self.generate_mesh()
        elif self.type_graph == "cyclic":
            self.generate_cyclic()
        elif self.type_graph == "acyclic":
            self.generate_acyclic()

        plt.axis('off')
        plt.tight_layout()
                
        ax = plt.gca() 
        ax.collections[0].set_edgecolor(self.color_label) 
    
    def _save_graph(self):
        file_name = f"{self.index}-{self.id_type_graph[self.type_graph]}.png"
        Path(f"{self.path}/{self.type_graph}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{self.path}/{self.type_graph}/{file_name}")
        plt.close()

def load_config():
    with open(current_path /  'config.yaml') as f:
        data = yaml.safe_load(f)
    new_class = type("Config", (object,), data)
    return new_class

Config = load_config()
config = Config()

total = 0

for t_graph in config.type_graph:
    for index in range(0, config.total_graph):
        generator = ClassificationGraphGenerator(
            num_nodes=config.num_nodes,
            path_save=os.path.join(current_path, "images"),
            is_save=True,
            directed= True,
            index=index,
            total_edge_percen=None,
            layout=None,
            color_node=config.color_node,
            color_label=config.color_label,
            color_edge=config.color_edge,
            node_size=config.size_node,
            node_border_size=config.size_border_node,
            arrowsize= config.arrowsize,
            is_label= True,
            random_color_node = False,
            type_graph=t_graph
        )
        generator.generate_graph()   
        total += 1

print(f"Images generated: {total}") 
