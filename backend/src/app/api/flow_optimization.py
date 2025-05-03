import networkx as nx
from typing import List, Dict
from ..graph.networks import TransportationNetwork
from ..algorithm.path_finding import AStarAlgorithm, DijkstraAlgorithm

# Load once to avoid reload on every request
tn = TransportationNetwork.from_json_folder('data')
G = tn.build_road_network(period='morning')


def find_astar_route(origin: str, dest: str) -> List[str]:
    """Find the best route using A* algorithm with geographic heuristic."""
    return AStarAlgorithm.find_route(G, origin, dest)


def find_dijkstra_route(origin: str, dest: str) -> List[str]:
    """Find the best route using Dijkstra's algorithm."""
    return DijkstraAlgorithm.find_route(G, origin, dest)


def path_to_edges(path: List[str]) -> List[Dict[str, str]]:
    """Convert a path list to edge list format."""
    return [{"from": path[i], "to": path[i + 1]} for i in range(len(path) - 1)]


def calculate_total_distance(path: List[str]) -> float:
    """Calculate total distance in kilometers using 'dist_km' edge attribute."""
    total_distance = 0.0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v)
        distance = edge_data.get('dist_km', 0)
        total_distance += distance
    return round(total_distance, 1)


def get_graph():
    return G


def get_transport_network():
    return tn
