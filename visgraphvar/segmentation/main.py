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

class SegmentationGraphGenerator(GraphGenerator):
    cut_edge = ()
    def generate_graph(self):
        self._draw_graph()
        self._save_graph()

    def _draw_graph(self):
        plt.figure(figsize=(6, 6), dpi=100)
        sns.set(style="whitegrid")

        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.num_nodes))

        mid = self.num_nodes // 2
        group_1 = list(range(mid))  
        group_2 = list(range(mid, self.num_nodes))

        for i in range(len(group_1)):
            self.graph.add_edge(group_1[i], group_1[(i + 1) % len(group_1)]) 

        for i in range(len(group_2)):
            self.graph.add_edge(group_2[i], group_2[(i + 1) % len(group_2)]) 

        node_1 = random.choice(group_1)
        node_2 = random.choice(group_2)

        self.graph.add_edge(node_1, node_2)
        
        self.cut_edge = (node_1, node_2)

        pos = nx.spring_layout(self.graph) 
        
        nx.draw(self.graph, pos, with_labels=True, node_color=self.color_node, 
                node_size=self.node_size, font_size=15, font_weight='bold', font_color=self.color_label, edge_color=self.color_edge)
                
        ax = plt.gca() 
        ax.collections[0].set_edgecolor(self.color_label) 
        plt.axis('off')
        plt.tight_layout()
    
    def _save_graph(self):
        file_name = f"{self.index}-{self.cut_edge[0]}-{self.cut_edge[1]}.png"
        Path(f"{self.path}/{self.num_nodes}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{self.path}/{self.num_nodes}/{file_name}")
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
    generator = SegmentationGraphGenerator(
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
    generator.generate_graph()   
    total += 1

print(f"Images generated: {total}") 
