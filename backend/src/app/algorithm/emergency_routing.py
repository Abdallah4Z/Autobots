"""
Emergency vehicle routing algorithms and priority system.
"""
import networkx as nx
from typing import List, Dict, Tuple
import math
from .path_finding import AStarAlgorithm

class EmergencyRouter:
    """
    Specialized router for emergency vehicles that considers traffic and priority.
    """
    
    def __init__(self, graph: nx.Graph, emergency_type: str = "ambulance"):
        self.G = graph
        self.emergency_type = emergency_type
        self.priority_weights = {
            "ambulance": 1.5,
            "fire_truck": 1.3,
            "police": 1.2
        }
        
    def calculate_emergency_weight(self, u: str, v: str, data: Dict) -> float:
        """
        Calculate edge weight for emergency vehicles considering:
        - Traffic conditions
        - Vehicle priority
        - Road characteristics
        """
        base_weight = data.get('dist_km', 1.0)
        traffic = data.get('traffic', 0)
        capacity = data.get('capacity', 1000)
        
        # Traffic factor (0.3 to 1.0) - emergency vehicles are less affected by traffic
        traffic_impact = max(0.3, 1.0 - (traffic / capacity) * 0.7)
        
        # Priority factor based on emergency type
        priority_factor = self.priority_weights.get(self.emergency_type, 1.0)
        
        # Calculate final weight
        emergency_weight = base_weight / (traffic_impact * priority_factor)
        
        return emergency_weight
        
    def find_emergency_route(self, origin: str, dest: str) -> Tuple[List[str], float]:
        """
        Find optimal route for emergency vehicle using modified A* algorithm.
        """
        # Create a graph copy with emergency-adjusted weights
        G_emergency = self.G.copy()
        
        # Update edge weights for emergency routing
        for u, v, data in G_emergency.edges(data=True):
            data['weight'] = self.calculate_emergency_weight(u, v, data)
        
        # Use A* algorithm with emergency-adjusted weights
        path = AStarAlgorithm.find_route(G_emergency, origin, dest)
        
        # Calculate estimated response time
        total_time = self.calculate_response_time(path)
        
        return path, total_time
    
    def calculate_response_time(self, path: List[str]) -> float:
        """
        Calculate estimated response time in minutes for the emergency route.
        """
        total_time = 0.0
        for u, v in zip(path[:-1], path[1:]):
            data = self.G[u][v]
            distance = data.get('dist_km', 0)
            # Emergency vehicles can travel faster (assumed 80 km/h average)
            emergency_speed = 80
            # Convert to minutes
            time = (distance / emergency_speed) * 60
            total_time += time
        return round(total_time, 2)
    
    @staticmethod
    def find_nearest_facility(G: nx.Graph, location: str, facility_type: str, facilities: Dict[str, Dict]) -> str:
        """
        Find the nearest emergency facility (hospital, fire station, etc.)
        """
        min_distance = float('inf')
        nearest = None
        
        for facility_id, data in facilities.items():
            if data.get('type') == facility_type:
                try:
                    distance = nx.shortest_path_length(G, location, facility_id, weight='dist_km')
                    if distance < min_distance:
                        min_distance = distance
                        nearest = facility_id
                except nx.NetworkXNoPath:
                    continue
                    
        return nearest
