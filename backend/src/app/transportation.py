import networkx as nx
from typing import List
from graph.networks import TransportationNetwork

# placeholder for node name lookup
NODES = {}


def summarise_path(G: nx.DiGraph, path: List[str]):
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


def print_itinerary(legs: List[dict]):
    for leg in legs:
        start, end = leg["nodes"][0], leg["nodes"][-1]
        hops = len(leg["nodes"]) - 1
        if leg["mode"] == "metro":
            # Using ASCII dash and arrow instead of Unicode characters
            print(f"Take Metro {leg['route']}  -  {name(start)} -> {name(end)}   ({hops} stops)")
        else:
            # Using ASCII dash and arrow instead of Unicode characters
            print(f"Take Bus   {leg['route']}  -  {name(start)} -> {name(end)}   ({hops} stops)")


if __name__ == "__main__":
    # load data and build public transport graph
    tn = TransportationNetwork.from_json_folder('data')  # adjust path as needed
    G = tn.build_public_transport_network()

    # prepare name lookup
    NODES = tn.nodes

    # example origin/destination
    origin, dest = "12", "13"
    path = nx.shortest_path(G, origin, dest)
    legs = summarise_path(G, path)

    print(f"Itinerary: {name(origin)} -> {name(dest)}")
    print("-" * 55)
    print_itinerary(legs)
