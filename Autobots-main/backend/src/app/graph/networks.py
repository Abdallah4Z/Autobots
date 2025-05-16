"""
Transportation network modeling and graph generation.
Centralizes all network-related functionality in a dedicated graph module.
"""
import os
import json
import networkx as nx
from typing import Dict, List, Tuple


class TransportationNetwork:
    """
    Blueprint for both public-transport connectivity and road networks,
    loading data from JSON files in a given folder.
    """

    def __init__(
        self,
        neighbourhoods: Dict[str, dict],
        facilities:    Dict[str, dict],
        bus_routes:    List[Dict],
        metro_lines:   List[Dict],
        roads:         List[Dict],
        flow:          Dict[Tuple[str,str], Dict[str,int]],
    ):
        self.neighbourhoods = neighbourhoods
        self.facilities    = facilities
        self.bus_routes    = bus_routes
        self.metro_lines   = metro_lines
        self.roads         = roads
        self.flow          = self._symmetrise_flow(flow)

    @staticmethod
    def _symmetrise_flow(raw: Dict[Tuple[str,str], dict]) -> Dict[Tuple[str,str], dict]:
        out: Dict[Tuple[str,str], dict] = {}
        for (u, v), rec in raw.items():
            out[(u, v)] = rec
            out[(v, u)] = rec
        return out

    @property
    def nodes(self) -> Dict[str, dict]:
        merged = {}
        merged.update(self.neighbourhoods)
        merged.update(self.facilities)
        return merged

    @classmethod
    def from_json_folder(cls, data_dir: str):
        def load_json(fname: str):
            path = os.path.join(data_dir, fname)
            if not os.path.exists(path):
                # Try to find the file in the app/data directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                # Go up one level since we're now in the graph folder
                app_dir = os.path.dirname(current_dir)
                app_data_path = os.path.join(app_dir, 'data', fname)
                if os.path.exists(app_data_path):
                    path = app_data_path
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Load raw JSON
        nb = load_json('neighbourhoods.json')
        fac= load_json('important_facilities.json')
        br = load_json('bus_routes.json')
        ml = load_json('current_metro_lines.json')
        re = load_json('roads_existing.json')
        rp = load_json('roads_potential.json')
        tf = load_json('traffic_flow_patterns.json')

        # Parse neighbourhoods
        neighbourhoods = {
            str(r['id']): {'name': r['name'], 'population': r['population'], 'type': r['type'], 'x': r['x'], 'y': r['y']}
            for r in nb
        }
        # Parse facilities
        facilities = {
            r['id']: {'name': r['name'], 'type': r['type'], 'x': r['x'], 'y': r['y']}
            for r in fac
        }
        # Parse bus routes
        bus_routes = [{'id': r['route_id'], 'stops': r['stops']} for r in br]
        # Parse metro lines
        metro_lines = [{'id': r['line_id'], 'stations': r['stations']} for r in ml]
        # Parse roads (distance_m to km)
        roads = [
            {'from': r['from_id'], 'to': r['to_id'], 'dist_km': r['distance_m']/1000.0, 'cap': r['capacity_vph'], 'cond': r['condition_1_10']}
            for r in re
        ]
        # Parse flow
        flow: Dict[Tuple[str,str], dict] = {}
        for rec in tf:
            flow[(rec['from_id'], rec['to_id'])] = {
                'morning': rec['morning_vph'], 'afternoon': rec['afternoon_vph'],
                'evening': rec['evening_vph'], 'night': rec['night_vph']
            }
        return cls(neighbourhoods, facilities, bus_routes, metro_lines, roads, flow)

    def build_public_transport_network(self) -> nx.DiGraph:
        G = nx.DiGraph()
        for nid, attrs in self.nodes.items():
            G.add_node(nid, **attrs)
        for route in self.bus_routes:
            for u, v in zip(route['stops'], route['stops'][1:]):
                G.add_edge(u, v, mode='bus', route=route['id'], weight=1)
                G.add_edge(v, u, mode='bus', route=route['id'], weight=1)
        for line in self.metro_lines:
            for u, v in zip(line['stations'], line['stations'][1:]):
                G.add_edge(u, v, mode='metro', route=line['id'], weight=1)
                G.add_edge(v, u, mode='metro', route=line['id'], weight=1)
        return G

    def build_road_network(self, period: str = 'morning') -> nx.Graph:
        G = nx.Graph()
        for nid, attrs in self.nodes.items():
            G.add_node(nid, **attrs)
        for r in self.roads:
            u, v = r['from'], r['to']
            dist, cap, cond = r['dist_km'], r['cap'], r['cond']
            flow = self.flow.get((u, v), {}).get(period, 0)
            weight = dist * (flow/cap)
            G.add_edge(u, v, weight=weight, dist_km=dist, capacity=cap, flow=flow, condition=cond)
        return G

    def build_combined_road_network(self, period: str = 'morning') -> nx.Graph:
        """
        Builds a road network graph with both existing and potential roads.
        Potential roads are marked with 'potential': True and 'condition': '(p)'.
        """
        G = nx.Graph()

        # Add all nodes
        for nid, attrs in self.nodes.items():
            G.add_node(nid, **attrs)

        # Add existing roads
        for r in self.roads:
            u, v = r['from'], r['to']
            dist, cap, cond = r['dist_km'], r['cap'], r['cond']
            flow = self.flow.get((u, v), {}).get(period, 0)
            weight = dist * (1 + flow / cap) if cap > 0 else dist
            G.add_edge(u, v, weight=weight, dist_km=dist, capacity=cap, flow=flow, condition=cond, potential=False)

        # Load and add potential roads from file
        # Updated path to handle being in the graph subfolder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        potential_path = os.path.join(app_dir, 'data', 'roads_potential.json')
        
        if os.path.exists(potential_path):
            with open(potential_path, 'r', encoding='utf-8') as f:
                potential_roads = json.load(f)

            for r in potential_roads:
                u, v = r['from_id'], r['to_id']
                dist = r['distance_m'] / 1000.0
                cap = r['capacity_vph']
                cond = r.get('condition_1_10', 5)
                weight = dist * (1 + 0 / cap) if cap > 0 else dist  # Assume no flow yet
                G.add_edge(
                    u, v,
                    weight=weight,
                    dist_km=dist,
                    capacity=cap,
                    flow=0,
                    condition=f"{cond}(p)",
                    potential=True
                )

        return G


if __name__ == '__main__':
    # Assumes JSON files are in './data/'
    tn = TransportationNetwork.from_json_folder('data')
    G_public = tn.build_public_transport_network()
    G_roads = tn.build_road_network(period='morning')
    print(f'Public transport graph: {G_public.number_of_nodes()} nodes, {G_public.number_of_edges()} edges')
    print(f'Road network graph:   {G_roads.number_of_nodes()} nodes, {G_roads.number_of_edges()} edges')