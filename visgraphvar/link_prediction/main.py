from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import random
import yaml
import os
import numpy as np
from pathlib import Path
from visgraphvar.graph_generator import GraphGenerator

current_path = Path(__file__).resolve().parent
sns.set(style="whitegrid")

class LinkPredictionGraphGenerator(GraphGenerator):
    num_communities = 0
    nodes_per_community = 0
    communities = []
    link_prediction = ()
    def generate_graph(self, num_communities, nodes_per_community):
        self.num_communities = num_communities
        self.nodes_per_community = nodes_per_community
        self._draw_graph()
        self._save_graph()

    def _generate_graph(self):
        self.graph = nx.Graph()
        self.communities = []
        
        for i in range(self.num_communities):
            start_node = i * self.nodes_per_community + 1
            community = list(range(start_node, start_node + self.nodes_per_community))
            self.communities.append(community)
            
            self.graph.add_nodes_from(community)
            
            for u, v in combinations(community, 2):
                self.graph.add_edge(u, v)
            
            mid_node = community[len(community)//2]
            target_nodes = [community[len(community)//2 - 1], community[len(community)//2 + 1]]
            if len(community) > 3:
                self.graph.remove_edge(target_nodes[0], target_nodes[1])

        def find_most_probable_link(G, community):
            max_score = -1
            best_pair = None
            
            for u, v in combinations(community, 2):
                if not G.has_edge(u, v):
                    cn = len(list(nx.common_neighbors(G, u, v)))
                    clustering_u = nx.clustering(G, u)
                    clustering_v = nx.clustering(G, v)
                    
                    score = cn * (clustering_u + clustering_v)
                    
                    if score > max_score:
                        max_score = score
                        best_pair = (u, v)
            
            return best_pair, max_score

        
        for idx, community in enumerate(self.communities):
            link, score = find_most_probable_link(self.graph, community)
            if link:
                return link
        
    def _draw_graph(self):
        plt.figure(figsize=(6, 6), dpi=100) 

        self.link_prediction = self._generate_graph()
        pos = nx.spring_layout(self.graph, k=2, iterations=50)

        nx.draw_networkx_edges(self.graph, pos)
        
        colors = plt.cm.Set3(np.linspace(0, 1, self.num_communities))
        
        for idx, community in enumerate(self.communities):
            nx.draw_networkx_nodes(self.graph, pos,
                                nodelist=community,
                                node_color=[self.color_node],
                                edgecolors=[self.color_edge],
                                node_size=self.node_size,)
            ax = plt.gca() 
            ax.collections[0].set_edgecolor(self.color_label) 
        nx.draw_networkx_labels(self.graph, pos)
        plt.axis('off')
        plt.tight_layout()
    
    def _save_graph(self):
        file_name = f"{self.index}-{self.link_prediction[0]}-{self.link_prediction[1]}.png"
        Path(f"{self.path}/{self.num_communities}/{self.nodes_per_community}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{self.path}/{self.num_communities}/{self.nodes_per_community}/{file_name}")
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
    for n_comm in range(1, config.num_communities + 1):
        for nodes_per_comm in config.nodes_per_community:
            generator = LinkPredictionGraphGenerator(
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
            generator.generate_graph(n_comm, nodes_per_comm)   
            total += 1

print(f"Images generated: {total}") 
