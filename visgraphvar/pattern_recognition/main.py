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

class PatternRecognitionGraphGenerator(GraphGenerator):
    num_elements = 0
    nodes_per_element = 0
    type_pattern = None

    def generate_graph(self, type_pattern, num_elements, nodes_per_element):
        self.type_pattern = type_pattern
        self.num_elements = num_elements
        self.nodes_per_element = nodes_per_element
        self._draw_graph()
        self._save_graph()

    def _generate_clique(self):
        self.graph = nx.Graph()

        node_counter = 0
        for _ in range(self.num_elements):
            clique_nodes = range(node_counter, node_counter + self.nodes_per_element)
            
            self.graph.add_nodes_from(clique_nodes)
            self.graph.add_edges_from([(u, v) for u in clique_nodes for v in clique_nodes if u != v])
            node_counter += self.nodes_per_element
    
    def _generate_chain(self):
        self.graph = nx.Graph()
        current_node = 0
    
        for _ in range(self.num_elements):
            for i in range(self.nodes_per_element - 1):
                self.graph.add_edge(current_node + i, current_node + i + 1)
            current_node += self.nodes_per_element
    
    def _generate_star(self):
        self.nodes_per_element = 5
        self.graph = nx.Graph()
        current_node = 0
        
        for _ in range(self.num_elements):
            central_node = current_node
            for i in range(1, self.nodes_per_element):
                self.graph.add_edge(central_node, current_node + i)
            current_node += self.nodes_per_element
        
    def _draw_graph(self):
        plt.figure(figsize=(6, 6), dpi=100) 

        if self.type_pattern == "clique":
            self._generate_clique()
        elif self.type_pattern == "chain":
            self._generate_chain()
        elif self.type_pattern == "star":
            self._generate_star()
        
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color=self.color_node, edge_color=self.color_edge, node_size=self.node_size)

        ax = plt.gca() 
        ax.collections[0].set_edgecolor(self.color_label) 
        plt.axis('off')
        plt.tight_layout()
    
    def _save_graph(self):
        file_name = f"{self.index}-{self.num_elements}-{self.nodes_per_element}.png"
        Path(f"{self.path}/{self.type_pattern}/{self.num_elements}").mkdir(parents=True, exist_ok=True)
        if not os.path.exists(f"{self.path}/{self.type_pattern}/{self.num_elements}/{file_name}"):
            plt.savefig(f"{self.path}/{self.type_pattern}/{self.num_elements}/{file_name}")
        plt.close()

def load_config():
    with open(current_path /  'config.yaml') as f:
        data = yaml.safe_load(f)
    new_class = type("Config", (object,), data)
    return new_class

Config = load_config()
config = Config()

total = 0

for index in range(0, config.total_graph):
    for t_pattern in config.type_pattern:
        for n_element in config.num_elements:
            for nodes_per_element in config.nodes_per_element:
                generator = PatternRecognitionGraphGenerator(
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
                    random_color_node = False
                )
                generator.generate_graph(t_pattern, n_element, nodes_per_element)   
                total += 1

print(f"Images generated: {total}") 
