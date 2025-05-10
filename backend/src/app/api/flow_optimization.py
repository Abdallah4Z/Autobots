import networkx as nx
from typing import List, Dict, Tuple
from ..graph.networks import TransportationNetwork
from ..algorithm.path_finding import AStarAlgorithm, DijkstraAlgorithm

# Global tn and G can remain for fallback or other uses, but core logic will use passed graph.
# Renamed for clarity to avoid confusion with local graphs.
tn_global = TransportationNetwork.from_json_folder('data')
G_global = tn_global.build_road_network()  # Default global graph

def find_astar_route(origin: str, dest: str, period: str) -> Tuple[List[str], nx.Graph]:
    """Find the best route using A* algorithm and return path and the graph used."""
    tn_local = TransportationNetwork.from_json_folder('data')
    G_local = tn_local.build_road_network(period)
    path = AStarAlgorithm.find_route(G_local, origin, dest)
    return path, G_local

def find_dijkstra_route(origin: str, dest: str, period: str) -> Tuple[List[str], nx.Graph]:
    """Find the best route using Dijkstra's algorithm and return path and the graph used."""
    tn_local = TransportationNetwork.from_json_folder('data')
    G_local = tn_local.build_road_network(period)
    path = DijkstraAlgorithm.find_route(G_local, origin, dest)
    return path, G_local

def path_to_edges(path: List[str]) -> List[Dict[str, str]]:
    """Convert a path list to edge list format."""
    return [{"from": path[i], "to": path[i + 1]} for i in range(len(path) - 1)]

def calculate_total_distance(path: List[str], graph: nx.Graph) -> float:
    """Calculate total distance in kilometers using 'dist_km' edge attribute from the provided graph."""
    total_distance = 0.0
    if not path:  # Handle empty or None path
        return 0.0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = graph.get_edge_data(u, v)  # Use passed graph
        if edge_data:
            distance = edge_data.get('dist_km', 0)
            total_distance += distance
    return round(total_distance, 1)

def calculate_total_time(path: List[str], graph: nx.Graph) -> float:
    """Calculate total travel time in minutes using traffic factor and base speed logic from the provided graph."""
    total_time = 0.0
    if not path:  # Handle empty or None path
        return 0.0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = graph.get_edge_data(u, v)  # Use passed graph
        if edge_data:
            distance = edge_data.get('dist_km', 0)
            capacity = edge_data.get('capacity', 1000)
            traffic = edge_data.get('traffic', 0)
            
            if 'traffic' in edge_data and 'capacity' in edge_data:
                traffic_factor = max(0.2, 1 - (traffic / capacity))
                base_speed = edge_data.get('base_speed', 50)
            else:
                traffic_factor = 0.8
                base_speed = 90
            
            if base_speed * traffic_factor > 0:
                time = (distance / (base_speed * traffic_factor)) * 60
            else:
                time = 0
            total_time += time
    return round(total_time, 2)

def get_graph():
    """Returns the default global graph."""
    return G_global

def get_transport_network():
    """Returns the default global transportation network."""
    return tn_global
