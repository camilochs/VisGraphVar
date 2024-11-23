import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import random
import yaml
import os
from pathlib import Path
from visgraphvar.graph_generator import GraphGenerator
from utils.manage_file import save_graph_json

current_path = Path(__file__).resolve().parent
sns.set(style="whitegrid")

class ReasoningGraphGenerator(GraphGenerator):
    num_nodes = 0
    start_node = 0
    end_node = 0

    def generate_graph(self, num_nodes, start_node, end_node):
        self.num_nodes = num_nodes
        self.start_node = start_node
        self.end_node = end_node
        self._draw_graph()
        self._save_graph()

    def _generate_connected_directed_graph(self):
        self.graph = nx.DiGraph()  
        
        if self.num_nodes < 2:
            raise ValueError("Error. num_nodes must be >= 2.")
        
        self.graph.add_nodes_from(range(self.num_nodes))
        
        if self.start_node < self.end_node:
            for i in range(self.start_node, self.end_node):
                weight = random.randint(1, 10)
                self.graph.add_edge(i, i + 1, weight=weight)  
        else:
            for i in range(self.end_node, self.start_node):
                weight = random.randint(1, 10)
                self.graph.add_edge(i, i + 1, weight=weight)  

        for i in range(self.num_nodes):
            if i == 0:
                self.graph.add_edge(i, i + 1, weight=random.randint(1, 10))  
            elif i == self.num_nodes - 1:
                self.graph.add_edge(i - 1, i, weight=random.randint(1, 10))  
            else:
                self.graph.add_edge(i - 1, i, weight=random.randint(1, 10))  
                self.graph.add_edge(i, i + 1, weight=random.randint(1, 10))  

        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j and random.random() < 0.3:  
                    weight = random.randint(1, 10)  
                    self.graph.add_edge(i, j, weight=weight)
    
    def _get_shortest_path(self):
        try:
            path = nx.shortest_path(self.graph, source=self.start_node, target=self.end_node, weight='weight')
            return path
        except nx.NetworkXNoPath:
            return None

    def _draw_graph(self):
        plt.figure(figsize=(6, 6), dpi=100) 

        self._generate_connected_directed_graph()
        
        pos = nx.random_layout(self.graph,)
        edges = self.graph.edges(data=True)
        nx.draw(self.graph, pos, with_labels=True, node_color=self.color_node, edge_color=self.color_edge, node_size=self.node_size)

        labels = {(u, v): d['weight'] for u, v, d in edges}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_color='red')

        ax = plt.gca() 
        ax.collections[0].set_edgecolor(self.color_label) 
        plt.axis('off')
        plt.tight_layout()
    
    def _save_graph(self):
        path = f"{self.path}/{self.num_nodes}"
        shortest_path = '-'.join([str(v) for v in self._get_shortest_path()])
        file_name = f"{self.index}_{self.start_node}-{self.end_node}_{shortest_path}"
        Path(f"{path}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{path}/{file_name}.png")
        plt.close()

        save_graph_json(self.graph, f"{path}/{file_name}.json")

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
        generator = ReasoningGraphGenerator(
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
        generator.generate_graph(n_nodes, 1, n_nodes)   
        total += 1

print(f"Images generated: {total}") 
