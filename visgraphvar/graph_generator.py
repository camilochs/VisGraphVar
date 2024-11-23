import networkx as nx
class GraphGenerator:
    def __init__(self, path_save, is_save, num_nodes, directed, index, total_edge_percen, layout, 
                 color_node, color_label, color_edge, node_size, node_border_size, arrowsize,
                 is_label, random_color_node, type_graph=None, num_edges=None):
        self.path = path_save
        self.is_save = is_save
        self.num_nodes = num_nodes
        self.directed = directed
        self.index = index
        self.total_edge_percen = total_edge_percen
        self.layout = layout
        self.color_node = color_node
        self.color_label = color_label
        self.color_edge = color_edge
        self.node_size = node_size
        self.node_border_size = node_border_size
        self.arrowsize = arrowsize
        self.is_label=is_label
        self.random_color_node = random_color_node
        self.type_graph = type_graph
        self.num_edges = num_edges
        self.graph = None
        
        
    def _draw_graph(self, graph_type=None):
        pass
    
    def _save_graph():
        pass

    def _get_layout(self):
        if self.layout == 'spring':
            return nx.spring_layout(self.graph)
        elif self.layout == 'circular':
            return nx.circular_layout(self.graph)
        elif self.layout == 'random':
            return nx.random_layout(self.graph)
        elif self.layout == 'kamada':
            return nx.kamada_kawai_layout(self.graph)
        elif self.layout == 'spectral':
            return nx.spectral_layout(self.graph)
        elif self.layout == 'shell':
            return nx.shell_layout(self.graph)
        elif self.layout == 'spiral':
            return nx.spiral_layout(self.graph)
        elif self.layout == 'planar':
            return nx.planar_layout(self.graph)
        else:
            raise ValueError("Layout not recognized")