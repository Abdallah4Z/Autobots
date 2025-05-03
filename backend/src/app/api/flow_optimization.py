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


def calculate_total_time(path: list) -> float:
    """Calculate total travel time in minutes using traffic factor and base speed logic."""
    total_time = 0.0
    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v)
        distance = edge_data.get('dist_km', 0)
        capacity = edge_data.get('capacity', 1000)
        traffic = edge_data.get('traffic', 0)
        # If traffic data exists, use it; else use default factor and base speed
        if 'traffic' in edge_data and 'capacity' in edge_data:
            traffic_factor = max(0.2, 1 - (traffic / capacity))
            base_speed = edge_data.get('base_speed', 50)
        else:
            traffic_factor = 0.8
            base_speed = 90
        # Calculate time in minutes
        if base_speed * traffic_factor > 0:
            time = (distance / (base_speed * traffic_factor)) * 60
        else:
            time = 0
        total_time += time
    return round(total_time, 2)


def get_graph():
    return G


def get_transport_network():
    return tn
