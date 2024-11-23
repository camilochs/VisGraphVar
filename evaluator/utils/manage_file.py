import json 
import networkx as nx

def read_prompt(path_prompt):
    with open(path_prompt, "r") as f:
        return f.read()

def write_result_llm(path_file, content):
    with open(path_file, "w") as f:
        f.write(content)

def save_graph_json(G, filename):
    graph_data = {
        'nodes': [[n, G.nodes[n]] for n in G.nodes()],
        'edges': [[u, v, G.edges[u,v]] for u,v in G.edges()]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)

def load_graph_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    G = nx.Graph()
    
    for node, attr in graph_data['nodes']:
        G.add_node(node, **attr)
    
    for u, v, attr in graph_data['edges']:
        G.add_edge(u, v, **attr)
    
    return G