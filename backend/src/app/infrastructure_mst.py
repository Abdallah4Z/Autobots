import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from graph.networks import TransportationNetwork


class InfrastructurePlanner:
    def __init__(self, tn: TransportationNetwork, period: str = "morning"):
        """
        Initializes the planner with full road network (existing + potential roads) and MST.
        Considers population and importance in edge weight adjustments.
        """
        self.tn = tn
        self.period = period
        self.G = tn.build_combined_road_network(period=period)  # Includes potential roads
        self.mst = self._build_mst()

    def _build_mst(self) -> nx.Graph:
        """
        Compute MST using adjusted weights based on population and importance.
        Potential roads are marked with (p) in their 'status'.
        """
        G = self.G.copy()
        for u, v, data in G.edges(data=True):
            pop_u = self.tn.nodes.get(u, {}).get("population", 1)
            pop_v = self.tn.nodes.get(v, {}).get("population", 1)
            importance_u = self.tn.nodes.get(u, {}).get("importance", 1)
            importance_v = self.tn.nodes.get(v, {}).get("importance", 1)
            factor = 1 / (pop_u + pop_v + importance_u + importance_v)
            data["adjusted_weight"] = data["weight"] * factor
        return nx.minimum_spanning_tree(G, weight="adjusted_weight")

    def show_mst_edges(self):
        """
        Print MST edges with distances, conditions, and potential/existing status.
        """
        print("\nMST Edge List")
        print("-" * 80)
        total_dist = 0.0
        for u, v, data in self.mst.edges(data=True):
            dist = data.get("dist_km", 0.0)
            cond = data.get("condition", "-")
            status = data.get("status", "existing")
            status_label = "potential" if "p" in status.lower() else "existing"
            print(f"{u:<10} <-> {v:<10} | {dist:5.2f} km | condition: {cond} ")
            total_dist += dist
        print("-" * 80)
        print(f"Total network distance: {total_dist:.2f} km")

    def analyze_cost_effectiveness(self):
        """
        Estimate total cost based on:
        - Existing roads (maintenance)
        - Potential roads (construction costs from roads_potential.json)
        """
        maintenance_cost_per_km = 100_000  # arbitrary maintenance cost

        # Load actual construction costs from roads_potential.json
        roads_potential_path = os.path.join(os.path.dirname(__file__), 'data', 'roads_potential.json')
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
        
        existing_roads_km = 0
        potential_roads_km = 0

        for u, v, data in self.mst.edges(data=True):
            dist = data.get("dist_km", 0.0)
            status = data.get('potential')  # Default to 'existing' if not found
            
            if status:  # potential road
                # Look up the construction cost from the loaded data
                if (u, v) in potential_roads_data:
                    # Add the cost in millions EGP converted to a regular number
                    construction_total += potential_roads_data[(u, v)]
                elif (v, u) in potential_roads_data:
                    construction_total += potential_roads_data[(v, u)]
                else:
                    # Fallback if the road isn't found in the data
                    print(f"Warning: Construction cost not found for potential road {u}-{v}")
                potential_roads_km += dist
            else:
                maintenance_total += dist * maintenance_cost_per_km
                existing_roads_km += dist

        print("\nCost-Effectiveness Analysis")
        print("-" * 50)
        print(f"Existing roads: {existing_roads_km:.2f} km")
        print(f"Potential roads: {potential_roads_km:.2f} km")
        print(f"Maintenance cost: ${maintenance_total/1000000:,.4f}million EGP")
        print(f"Construction cost: {construction_total:,.0f} million EGP")

    def visualize_network(self):
        """
        Visualize MST network with color-coded existing and potential roads.
        """
        pos = {n: (self.tn.nodes[n]['x'], self.tn.nodes[n]['y']) for n in self.mst.nodes}
        edge_colors = [
            'red' if "p" in data.get("status", "").lower() else 'green'
            for _, _, data in self.mst.edges(data=True)
        ]

        plt.figure(figsize=(10, 8))
        nx.draw(self.mst, pos, with_labels=True, node_size=50, edge_color=edge_colors, width=2)
        plt.title("Optimized Road Network (MST)")
        plt.show()


if __name__ == '__main__':
    tn = TransportationNetwork.from_json_folder("data")
    planner = InfrastructurePlanner(tn, period="evening")

    planner.show_mst_edges()
    planner.analyze_cost_effectiveness()
    planner.visualize_network()
