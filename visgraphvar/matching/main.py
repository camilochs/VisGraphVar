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

class MatchingGraphGenerator(GraphGenerator):
    num_nodes = 0
    match = False
    graph2 = None
    def generate_graph(self, num_nodes, match):
        self.num_nodes = num_nodes
        self.match = match
        self._draw_graph()
        self._save_graph()

    def _generate_matching_graph(self):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.num_nodes))
        
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < 0.4: 
                    self.graph.add_edge(i, j)

        self.graph2 = nx.Graph(self.graph)  

        if not self.match:
            mapping = {i: (i + 1) % self.num_nodes for i in range(self.num_nodes)}
            self.graph2 = nx.relabel_nodes(self.graph, mapping)
    

    def _draw_graph(self):
        plt.figure(figsize=(12, 6), dpi=100) 

        self._generate_matching_graph()
        
        plt.subplot(1, 2, 1)
        pos1 = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos1, with_labels=True, node_color='lightblue', edge_color='gray', node_size=self.node_size, font_size=10)
        plt.legend(["Graph 1"], loc='upper left', bbox_to_anchor=(0, 0), frameon=True)
        ax = plt.gca() 
        ax.collections[0].set_edgecolor(self.color_label) 
        
        plt.subplot(1, 2, 2)
        pos2 = nx.spring_layout(self.graph2)
        nx.draw(self.graph2, pos2, with_labels=True, node_color='lightgreen', edge_color='orange', node_size=self.node_size, font_size=10)
        
        plt.legend(["Graph 2"], loc='upper right', bbox_to_anchor=(0, 0), frameon=True)

        ax = plt.gca() 
        ax.collections[0].set_edgecolor(self.color_label) 
        plt.axis('off')
        plt.tight_layout()
    
    def _save_graph(self):
        is_match = "match" if self.match else "unmatch"
        file_name = f"{self.index}.png"
        Path(f"{self.path}/{self.num_nodes}/{is_match}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{self.path}/{self.num_nodes}/{is_match}/{file_name}")
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
    for n_nodes in config.num_nodes:
        for match in [True, False]:
            generator = MatchingGraphGenerator(
                num_nodes=n_nodes,
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
            generator.generate_graph(n_nodes, match)   
            total += 1

print(f"Images generated: {total}") 
