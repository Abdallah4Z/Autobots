"""
Path finding algorithms for transportation networks.
Includes implementation of A* and Dijkstra algorithms.
"""
import math
import networkx as nx
from typing import List


class AStarAlgorithm:
    """
    A* algorithm for finding shortest paths in a graph using geographic distance heuristic.
    """
    
    @staticmethod
    def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """
        Calculate the great-circle distance between two points on Earth.
        
        Args:
            lon1: Longitude of the first point in degrees
            lat1: Latitude of the first point in degrees
            lon2: Longitude of the second point in degrees
            lat2: Latitude of the second point in degrees
            
        Returns:
            Distance in kilometers
        """
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert degrees to radians
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        
        # Haversine formula calculation
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        
        return 2 * R * math.asin(math.sqrt(a))
    
    @staticmethod
    def find_route(G: nx.Graph, origin: str, dest: str) -> List[str]:
        """
        Find the shortest path from origin to destination using A* with geographic heuristic.
        
        Args:
            G: NetworkX graph with x, y coordinates in node attributes
            origin: Starting node ID
            dest: Destination node ID
            
        Returns:
            List of node IDs representing the path
        """
        # Get goal coordinates
        gx, gy = G.nodes[dest]["x"], G.nodes[dest]["y"]
        
        def heuristic(u: str, v: str) -> float:
            """Geographic distance heuristic function using x/y coordinates"""
            ux, uy = G.nodes[u]["x"], G.nodes[u]["y"]
            return AStarAlgorithm.haversine(ux, uy, gx, gy)
            
        # Use NetworkX's A* implementation
        return nx.astar_path(G, origin, dest, heuristic=heuristic, weight="weight")


class DijkstraAlgorithm:
    """
    Dijkstra's algorithm for finding shortest paths in a graph.
    """
    
    @staticmethod
    def find_route(G: nx.Graph, origin: str, dest: str) -> List[str]:
        """
        Find the shortest path from origin to destination using Dijkstra's algorithm.
        
        Args:
            G: NetworkX graph
            origin: Starting node ID
            dest: Destination node ID
            
        Returns:
            List of node IDs representing the path
        """
        return nx.dijkstra_path(G, origin, dest, weight="weight")


def display_route(G: nx.Graph, path: List[str], tn, title: str) -> None:
    """
    Display detailed information about a route.
    
    Args:
        G: NetworkX graph with edge attributes
        path: List of node IDs in the path
        tn: TransportationNetwork object with node names
        title: Title for the route display
    """
    print(f"\n{title}")
    print("-" * 60)
    total = 0.0
    
    for u, v in zip(path[:-1], path[1:]):
        d = G[u][v]["dist_km"]
        total += d
        flow = G[u][v]["flow"]
        cap = G[u][v]["capacity"]
        
        # Get human-readable names for nodes
        u_name = (tn.neighbourhoods.get(u) or tn.facilities[u])["name"]
        v_name = (tn.neighbourhoods.get(v) or tn.facilities[v])["name"]
        
        # Using ASCII arrow '->' instead of Unicode arrow to avoid encoding issues
        print(f"{u_name:<30} -> {v_name:<30}  {d:5.1f} km"
              f"  (flow={flow} vph, cap={cap})")
              
    print("-" * 60)
    print(f"Total distance: {total:.1f} km")