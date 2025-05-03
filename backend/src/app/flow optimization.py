"""
Flow optimization for transportation networks.
"""
import networkx as nx
from typing import List, Tuple
from graph.networks import TransportationNetwork
from algorithm.path_finding import AStarAlgorithm, DijkstraAlgorithm, display_route

# --------------------------------------------------------------------
# 1 ▸ ROUTE FINDING API
# --------------------------------------------------------------------
def find_astar_route(G: nx.Graph, origin: str, dest: str) -> List[str]:
    """Find the best route using A* algorithm with geographic heuristic."""
    return AStarAlgorithm.find_route(G, origin, dest)

def find_dijkstra_route(G: nx.Graph, origin: str, dest: str) -> List[str]:
    """Find the best route using Dijkstra's algorithm."""
    return DijkstraAlgorithm.find_route(G, origin, dest)

def pname(nid: str, tn: TransportationNetwork) -> str:
    """Human-readable name from neighbourhoods or facilities."""
    return (tn.neighbourhoods.get(nid) or tn.facilities[nid])["name"]

def show_route(G: nx.Graph, path: List[str], tn: TransportationNetwork, title: str) -> None:
    """Display a route with details of each segment."""
    display_route(G, path, tn, title)

# --------------------------------------------------------------------
# 2 ▸ DEMO ENTRY
# --------------------------------------------------------------------
if __name__ == '__main__':
    # load data and build road network
    tn = TransportationNetwork.from_json_folder('data')  # adjust path if needed
    G = tn.build_road_network(period='morning')

    origin, dest = '10', 'F8'  # Dokki -> Cairo Festival City

    # A* route
    path_astar = find_astar_route(G, origin, dest)
    print(path_astar)
    show_route(G, path_astar, tn, 'A* Route:')

    # Dijkstra route
    path_dij = find_dijkstra_route(G, origin, dest)
    print(path_dij)
    show_route(G, path_dij, tn, 'Dijkstra Route:')
