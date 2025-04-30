import networkx as nx

class CairoTransportationGraph:
    def __init__(self):
        self.nodes = {}  # Maps ID to node data
        self.existing_roads = []
        self.potential_roads = []
        self.metro_lines = []
        self.bus_routes = []
        self.traffic_data = {}
        self.transport_demand = {}
        
    def build_networkx_graph(self, include_potential=False):
        """Create a NetworkX graph from the loaded data"""
        G = nx.Graph()
        
        # Add nodes
        for node_id, data in self.nodes.items():
            G.add_node(node_id, **data)
            
        # Add existing roads as edges
        for road in self.existing_roads:
            from_id, to_id, distance, capacity, condition = road
            G.add_edge(from_id, to_id, 
                      distance=distance, 
                      capacity=capacity, 
                      condition=condition,
                      type='existing')
            
        # Add potential roads if requested
        if include_potential:
            for road in self.potential_roads:
                from_id, to_id, distance, capacity, cost = road
                G.add_edge(from_id, to_id, 
                          distance=distance, 
                          capacity=capacity, 
                          cost=cost,
                          type='potential')
                
        return G