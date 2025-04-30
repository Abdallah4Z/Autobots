import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import networkx as nx

def get_graph_image_base64(graph, include_potential=False):
    """Return the graph visualization as a base64 encoded image"""
    plt.figure(figsize=(12, 10))
    G = graph.build_networkx_graph(include_potential)
    
    # Create visualization
    pos = {node: (graph.nodes[node]['x'], graph.nodes[node]['y']) for node in G.nodes()}
    
    # Draw nodes with different colors
    residential = [n for n in G.nodes() if not graph.nodes[n]['is_facility'] and graph.nodes[n]['type'] == 'Residential']
    business = [n for n in G.nodes() if not graph.nodes[n]['is_facility'] and graph.nodes[n]['type'] == 'Business']
    mixed = [n for n in G.nodes() if not graph.nodes[n]['is_facility'] and graph.nodes[n]['type'] == 'Mixed']
    other_districts = [n for n in G.nodes() if not graph.nodes[n]['is_facility'] and graph.nodes[n]['type'] not in ['Residential', 'Business', 'Mixed']]
    facilities = [n for n in G.nodes() if graph.nodes[n]['is_facility']]
    
    nx.draw_networkx_nodes(G, pos, nodelist=residential, node_color='green', node_size=300, label='Residential')
    nx.draw_networkx_nodes(G, pos, nodelist=business, node_color='red', node_size=300, label='Business')
    nx.draw_networkx_nodes(G, pos, nodelist=mixed, node_color='purple', node_size=300, label='Mixed')
    nx.draw_networkx_nodes(G, pos, nodelist=other_districts, node_color='gray', node_size=300, label='Other Districts')
    nx.draw_networkx_nodes(G, pos, nodelist=facilities, node_color='blue', node_size=200, label='Facilities', node_shape='s')
    
    # Draw existing edges
    existing_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'existing']
    nx.draw_networkx_edges(G, pos, edgelist=existing_edges, width=1.5)
    
    # Draw potential edges if requested
    if include_potential:
        potential_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'potential']
        nx.draw_networkx_edges(G, pos, edgelist=potential_edges, width=1.5, edge_color='red', style='dashed')
    
    # Add labels
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title('Greater Cairo Transportation Network')
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    
    # Save plot to a bytes buffer and convert to base64 for HTML embedding
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64