"""
Minimum Spanning Tree algorithm implementation.
Provides core MST functionality for infrastructure planning.
"""
import networkx as nx
from typing import Dict, List, Set, Tuple


class MSTAlgorithm:
    """
    Minimum Spanning Tree (MST) algorithm implementation.
    Provides methods for building and enhancing MST networks.
    """
    
    @staticmethod
    def build_base_mst(G: nx.Graph, weight_attr: str = "weight") -> nx.Graph:
        """
        Build a basic minimum spanning tree from a graph.
        
        Args:
            G: The input graph to build MST from
            weight_attr: Edge attribute to use as weight
            
        Returns:
            A NetworkX graph representing the MST
        """
        return nx.minimum_spanning_tree(G, weight=weight_attr)
    
    @staticmethod
    def adjust_weights_for_critical_nodes(G: nx.Graph, critical_nodes: List[str], factor: float = 0.1) -> nx.Graph:
        """
        Adjust edge weights for critical nodes in the graph.
        
        Args:
            G: The input graph
            critical_nodes: List of critical node IDs
            factor: Weight multiplication factor (< 1 to reduce weights)
            
        Returns:
            Graph with adjusted weights
        """
        G_copy = G.copy()
        
        # Make sure all critical nodes have the greatest importance
        for node in critical_nodes:
            if node in G_copy.nodes():
                # Increase attraction by decreasing weights of connected edges
                for neighbor in G_copy.neighbors(node):
                    if G_copy.has_edge(node, neighbor):
                        # Reduce weight for edges connected to critical nodes
                        G_copy.edges[node, neighbor]['weight'] *= factor
        
        return G_copy
    
    @staticmethod
    def build_enhanced_mst(G: nx.Graph, critical_nodes: List[str]) -> nx.Graph:
        """
        Build an enhanced MST that ensures critical nodes are connected.
        Uses a two-phase approach.
        
        Args:
            G: The input graph
            critical_nodes: List of critical node IDs that must be connected
            
        Returns:
            Enhanced MST graph
        """
        # First adjust weights to favor critical nodes
        G_adjusted = MSTAlgorithm.adjust_weights_for_critical_nodes(G, critical_nodes)
        
        # Build the base MST
        base_mst = MSTAlgorithm.build_base_mst(G_adjusted)
        
        # Check which critical nodes are not connected in the MST
        missing_nodes = []
        for node in critical_nodes:
            if node not in base_mst.nodes() or base_mst.degree(node) == 0:
                missing_nodes.append(node)
        
        if not missing_nodes:
            print("All critical nodes included in the initial MST.")
            return base_mst
        
        # If some critical nodes are missing, enhance the MST to include them
        enhanced_mst = base_mst.copy()
        print(f"Found {len(missing_nodes)} missing nodes: {missing_nodes}")
        
        # For each missing node, find the shortest path to the existing MST
        for node in missing_nodes:
            print(f"Finding connection path for {node}...")
            
            # Skip if node doesn't exist in the original graph
            if node not in G.nodes():
                print(f"Warning: Node {node} not found in the network")
                continue
                
            # Find the closest node in the current MST
            closest_node = None
            min_distance = float('inf')
            
            for mst_node in enhanced_mst.nodes():
                # Skip self-comparison
                if mst_node == node:
                    continue
                    
                # Check if there's a path from node to this mst_node in the original graph
                if nx.has_path(G, node, mst_node):
                    # Find the shortest path and its total weight
                    try:
                        path = nx.shortest_path(G, node, mst_node, weight="weight")
                        path_weight = sum(G[path[i]][path[i+1]]["weight"] for i in range(len(path)-1))
                        
                        if path_weight < min_distance:
                            min_distance = path_weight
                            closest_node = mst_node
                    except nx.NetworkXNoPath:
                        continue
            
            # Add the best path to the enhanced MST
            if closest_node:
                path = nx.shortest_path(G, node, closest_node, weight="weight")
                print(f"  - Adding path from {node} to {closest_node}: {path}")
                
                for i in range(len(path) - 1):
                    u, v = path[i], path[i+1]
                    # Copy all edge attributes from the original graph
                    edge_data = G.get_edge_data(u, v).copy()
                    enhanced_mst.add_edge(u, v, **edge_data)
            else:
                print(f"Warning: Could not find a path to connect node {node}")
                
        return enhanced_mst