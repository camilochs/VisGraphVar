import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import random
import yaml
from pathlib import Path
from visgraphvar.graph_generator import GraphGenerator

current_path = Path(__file__).resolve().parent
sns.set(style="whitegrid")

class NodeEdgeDetectionGraphGenerator(GraphGenerator):
    def generate_graph(self):
        # Create a directed or undirected graph
        if self.directed:
            self.graph = nx.DiGraph()
        else:
            self.graph = nx.Graph()

        # Add nodes to the graph
        self.graph.add_nodes_from(range(self.num_nodes))

        # Calculate the number of edges based on the total_edge_percen
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j and random.random() < self.total_edge_percen:  
                    self.graph.add_edge(i, j)
            
        self._draw_graph()
        self._save_graph()

    def _draw_graph(self):
        plt.figure(figsize=(6, 6), dpi=100)
        pos = self._get_layout()

        if self.random_color_node:
            self.color_node = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(self.num_nodes)]

        # Draw the nodes, edges, and labels
        nx.draw_networkx_nodes(self.graph, pos, node_color=self.color_node, node_size=self.node_size, edgecolors=self.color_edge, linewidths=self.node_border_size)
        if self.is_label:
            nx.draw_networkx_labels(self.graph, pos, font_color=self.color_label)
        
        if self.directed:
            nx.draw_networkx_edges(self.graph, pos,  edge_color=self.color_edge, arrows=self.directed, arrowsize=self.arrowsize)
        else:
            nx.draw_networkx_edges(self.graph, pos,  edge_color=self.color_edge, arrows=self.directed)
        # Remove axis
        plt.axis('off')
        plt.tight_layout()
    
    def _save_graph(self):
        type_graph = "directed" if self.directed else "undirected"
        label = "label" if self.is_label else "unlabel"
        color = "random_color" if self.random_color_node else "constant_color"
        file_name = f"{self.index}-{self.num_nodes}-{self.graph.number_of_edges()}.png"
        Path(f"{self.path}/{type_graph}/layouts/{self.layout}/{label}/{color}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{self.path}/{type_graph}/layouts/{self.layout}/{label}/{color}/{file_name}")
        plt.close()

def load_config():
    with open(current_path /  'config.yaml') as f:
        data = yaml.safe_load(f)
    new_class = type("Config", (object,), data)
    return new_class

Config = load_config()
config = Config()

print(config.layouts)
total = 0
for type_graph in ["directed", "undirected"]:
    for index in range(0, config.total_graph):
        for layout in config.layouts:
            for label in ["label", "unlabel"]:
                for random_color_node in [True, False]:
                    generator = NodeEdgeDetectionGraphGenerator(
                        num_nodes=config.num_nodes,
                        path_save=current_path,
                        is_save=True,
                        directed= True if type_graph == "directed" else False,
                        index=index,
                        total_edge_percen=config.edge_percentage,
                        layout=layout,
                        color_node=config.color_node,
                        color_label=config.color_label,
                        color_edge=config.color_edge,
                        node_size=config.size_node,
                        node_border_size=config.size_border_node,
                        arrowsize= config.arrowsize,
                        is_label= True if label == "label" else False,
                        random_color_node = random_color_node 
                    )
                    generator.generate_graph()   
                    total += 1

print(f"Images generated: {total}") 
