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
    
    def __init__(self, graph: nx.Graph, emergency_type: str = "ambulance", period: str = "morning"):
        """
        Initialize emergency router with graph, vehicle type and time period.
        
        Args:
            graph: Road network graph with traffic data
            emergency_type: Type of emergency vehicle (ambulance, fire_truck, police)
            period: Time period for traffic data (morning, afternoon, evening, night)
        """
        self.G = graph
        self.emergency_type = emergency_type
        self.period = period
        self.priority_weights = {
            "ambulance": 1.5,
            "fire_truck": 1.3,
            "police": 1.2
        }
        
    def calculate_emergency_weight(self, u: str, v: str, data: Dict) -> float:
        """
        Calculate edge weight for emergency vehicles considering:
        - Traffic conditions from the current time period
        - Vehicle priority
        - Road characteristics
        """
        try:
            base_weight = data.get('dist_km', 1.0)
            capacity = data.get('capacity', 1000)
            
            # Get traffic flow for the current time period
            # This comes from TransportationNetwork's build_road_network method
            traffic_flow = data.get('flow', 0)
            
            # Traffic factor (0.3 to 1.0) - emergency vehicles are less affected by traffic
            # Even in maximum traffic, emergency vehicles can still move at 30% of normal speed
            traffic_ratio = traffic_flow / capacity if capacity > 0 else 0
            traffic_impact = max(0.3, 1.0 - traffic_ratio * 0.7)
            
            # Priority factor based on emergency type
            priority_factor = self.priority_weights.get(self.emergency_type, 1.0)
            
            # Calculate final weight - lower weight means more likely to choose this path
            # Base weight is divided by both traffic impact and priority to prefer:
            # 1. Roads with less traffic (higher traffic_impact)
            # 2. Routes for higher priority vehicles (higher priority_factor)
            emergency_weight = base_weight / (traffic_impact * priority_factor)
            
            return emergency_weight
            
        except Exception as e:
            print(f"Error calculating emergency weight: {e}")
            return base_weight  # Fallback to basic distance if calculation fails
        
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
        Takes into account:
        - Road distances 
        - Current traffic conditions
        - Emergency vehicle type
        """
        total_time = 0.0
        for u, v in zip(path[:-1], path[1:]):
            data = self.G[u][v]
            distance = data.get('dist_km', 0)
            
            # Get traffic data 
            traffic_flow = data.get('flow', 0)
            capacity = data.get('capacity', 1000)
            
            # Calculate traffic impact on speed
            traffic_ratio = traffic_flow / capacity if capacity > 0 else 0
            traffic_impact = max(0.3, 1.0 - traffic_ratio * 0.7)
            
            # Base emergency vehicle speed (80 km/h) adjusted for traffic
            # Higher priority vehicles can maintain better speeds in traffic
            priority_factor = self.priority_weights.get(self.emergency_type, 1.0)
            emergency_speed = 80 * traffic_impact * priority_factor
            
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