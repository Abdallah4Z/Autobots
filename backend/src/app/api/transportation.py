import networkx as nx
from typing import List, Dict
from app.graph.networks import TransportationNetwork

# Global objects initialized once
tn = TransportationNetwork.from_json_folder('data')
G = tn.build_public_transport_network()
NODES = tn.nodes


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
    if origin not in G or dest not in G:
        raise ValueError("Origin or destination not in the graph.")

    path = nx.shortest_path(G, origin, dest)
    legs = summarise_path(G, path)
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

    return {
        "origin": name(origin),
        "destination": name(dest),
        "steps": itinerary
    }
