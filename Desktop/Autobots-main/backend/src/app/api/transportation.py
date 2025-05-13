import networkx as nx
from typing import List, Dict, Tuple
from app.graph.networks import TransportationNetwork

# Global objects initialized once
tn = TransportationNetwork.from_json_folder('data')
G = tn.build_public_transport_network()
NODES = tn.nodes

# Memoization table to store computed routes
# Structure: {(origin_id, dest_id): {"path": [...], "itinerary": [...], "total_time": float, "total_distance": float}}
ROUTE_CACHE = {}

def calculate_metrics(G: nx.DiGraph, path: List[str]) -> Tuple[float, float]:
    """Calculate total time (minutes) and distance (km) for a given path."""
    total_time = 0.0
    total_distance = 0.0
    
    for u, v in zip(path[:-1], path[1:]):
        data = G[u][v]
        # Default values based on transportation mode if exact values not available
        mode = data["mode"]
        
        # Estimated time and distance factors by mode of transport
        time_factor = {"walk": 5, "bus": 2, "metro": 1.5, "tram": 2}.get(mode, 3)
        distance_factor = {"walk": 0.5, "bus": 1, "metro": 1.5, "tram": 1}.get(mode, 1)
        
        # Use actual values if available, otherwise estimate
        edge_distance = data.get("distance", distance_factor)
        edge_time = data.get("time", edge_distance * time_factor)
        
        total_time += edge_time
        total_distance += edge_distance
    
    return total_time, total_distance

def summarise_path(G: nx.DiGraph, path: List[str]) -> List[Dict]:
    legs = []
    cur_mode, cur_route, segment = None, None, [path[0]]

    for u, v in zip(path[:-1], path[1:]):
        data = G[u][v]
        mode, route = data["mode"], data["route"]
        if (mode, route) != (cur_mode, cur_route):
            if cur_mode is not None:
                legs.append({"mode": cur_mode, "route": cur_route, "nodes": segment})
            cur_mode, cur_route, segment = mode, route, [u]
        segment.append(v)
    legs.append({"mode": cur_mode, "route": cur_route, "nodes": segment})
    return legs


def name(nid: str) -> str:
    return NODES[nid]["name"]


def get_itinerary(origin: str, dest: str) -> Dict:
    """
    Get the itinerary between origin and destination using dynamic programming (memoization).
    If the route has been computed before, retrieve it from the cache.
    Otherwise, compute it and store in the cache for future use.
    """
    if origin not in G or dest not in G:
        raise ValueError("Origin or destination not in the graph.")
    
    # Check if the route is already in the cache
    cache_key = (origin, dest)
    if cache_key in ROUTE_CACHE:
        cached_result = ROUTE_CACHE[cache_key]
        return {
            "origin": name(origin),
            "destination": name(dest),
            "steps": cached_result["steps"],
            "total_time": cached_result["total_time"],
            "total_distance": cached_result["total_distance"]
        }
    
    # If not in cache, compute the route
    path = nx.shortest_path(G, origin, dest)
    legs = summarise_path(G, path)
    total_time, total_distance = calculate_metrics(G, path)
    
    # Format itinerary
    itinerary = []
    for leg in legs:
        start, end = leg["nodes"][0], leg["nodes"][-1]
        hops = len(leg["nodes"]) - 1
        leg_info = {
            "mode": leg["mode"],
            "route": leg["route"],
            "start": name(start),
            "end": name(end),
            "stops": hops,
            "path": leg["nodes"]
        }
        itinerary.append(leg_info)
    
    # Create the complete result including total time and distance
    result = {
        "origin": name(origin),
        "destination": name(dest),
        "steps": itinerary,
        "total_time": round(total_time, 2),
        "total_distance": round(total_distance, 2)
    }
    
    # Cache the computed result
    ROUTE_CACHE[cache_key] = {
        "steps": itinerary,
        "total_time": result["total_time"],
        "total_distance": result["total_distance"]
    }
    
    return result