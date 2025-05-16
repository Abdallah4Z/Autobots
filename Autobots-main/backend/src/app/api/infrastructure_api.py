# infrastructure.py
import networkx as nx
from ..graph.networks import TransportationNetwork
import os
import json

class InfrastructurePlanner:
    def __init__(self, tn: TransportationNetwork, period: str = "morning"):
        self.tn = tn
        self.period = period
        self.G = tn.build_combined_road_network(period=period)
        self.mst = self._build_mst()

    def _build_mst(self) -> nx.Graph:
        G = self.G.copy()
        for u, v, data in G.edges(data=True):
            pop_u = self.tn.nodes.get(u, {}).get("population", 1)
            pop_v = self.tn.nodes.get(v, {}).get("population", 1)
            importance_u = self.tn.nodes.get(u, {}).get("importance", 1)
            importance_v = self.tn.nodes.get(v, {}).get("importance", 1)
            factor = 1 / (pop_u + pop_v + importance_u + importance_v)
            data["adjusted_weight"] = data["weight"] * factor
        return nx.minimum_spanning_tree(G, weight="adjusted_weight")

    def get_mst_edges(self):
        return {
            "edges": [
                {"from": u, "to": v} for u, v in self.mst.edges()
            ]
        }

    def analyze_cost_effectiveness(self):
        """
        Estimate total cost based on:
        - Existing roads (maintenance)
        - Potential roads (construction costs from roads_potential.json)
        """
        maintenance_cost_per_km = 100_000  # arbitrary maintenance cost
        
        # Load actual construction costs from roads_potential.json
        roads_potential_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'roads_potential.json')
        potential_roads_data = {}
        
        try:
            with open(roads_potential_path, 'r') as f:
                potential_roads = json.load(f)
                # Create a lookup dictionary for potential roads by their endpoints
                for road in potential_roads:
                    from_id = road['from_id']
                    to_id = road['to_id']
                    # Store costs both ways since the graph is undirected
                    potential_roads_data[(from_id, to_id)] = road['construction_cost_m_egp']
                    potential_roads_data[(to_id, from_id)] = road['construction_cost_m_egp']
        except Exception as e:
            print(f"Error loading potential roads data: {e}")
            potential_roads_data = {}

        maintenance_total = 0
        construction_total = 0
        maintenance_dist = 0
        construction_dist = 0

        for u, v, data in self.mst.edges(data=True):
            dist = data.get("dist_km", 0.0)
            status = data.get('potential')
            
            if status:  # potential road
                # Look up the construction cost from the loaded data
                if (u, v) in potential_roads_data:
                    # Add the cost in millions EGP
                    construction_total += potential_roads_data[(u, v)]
                elif (v, u) in potential_roads_data:
                    construction_total += potential_roads_data[(v, u)]
                else:
                    # Fallback if the road isn't found in the data
                    print(f"Warning: Construction cost not found for potential road {u}-{v}")
                construction_dist += dist
            else:
                maintenance_total += dist * maintenance_cost_per_km / 1000000  # Convert to million EGP
                maintenance_dist += dist

        return {
            "construction": {
                "cost": round(construction_total, 2),  # Already in million EGP
                "distance_km": round(construction_dist, 2)
            },
            "maintenance": {
                "cost": round(maintenance_total, 2),  # Now in million EGP
                "distance_km": round(maintenance_dist, 2)
            },
            "total_distance_km": round(construction_dist + maintenance_dist, 2)
        }
