import requests
import json
import time
import sys
from collections import defaultdict
from tabulate import tabulate

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

class TestResult:
    def __init__(self, endpoint, status, success=None, message=None, data=None):
        self.endpoint = endpoint
        self.status = status
        self.success = success
        self.message = message
        self.data = data

    @property
    def passed(self):
        return self.status == 200 and self.success is True

def test_api_endpoint(endpoint, method="GET", payload=None, params=None, silent=False):
    """Test an API endpoint and print the result"""
    url = f"{BASE_URL}/{endpoint}"
    
    if not silent:
        print(f"\n===== Testing {method} {url} =====")
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=payload)
        else:
            if not silent:
                print(f"Method {method} not supported")
            return TestResult(endpoint, 0, False, f"Method {method} not supported")
        
        if not silent:
            print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if not silent:
                print(f"Success: {data.get('success', 'N/A')}")
                
                # Print a summarized version of the response
                if 'nodes' in data:
                    nodes = data['nodes']
                    print(f"Nodes: {len(nodes)} items (showing first 2)")
                    sample = nodes[:2] if isinstance(nodes, list) and len(nodes) >= 2 else nodes
                    print(json.dumps(sample, indent=2))
                elif 'edges' in data:
                    edges = data['edges']
                    print(f"Edges: {len(edges)} items (showing first 2)")
                    sample = edges[:2] if isinstance(edges, list) and len(edges) >= 2 else edges
                    print(json.dumps(sample, indent=2))
                else:
                    # Print other relevant data with reasonable limits
                    cleaned_data = {}
                    
                    for k, v in data.items():
                        if isinstance(v, list) and len(v) > 5:
                            cleaned_data[k] = f"{len(v)} items"
                            if len(v) > 0:
                                cleaned_data[f"{k}_sample"] = v[:2] if len(v) >= 2 else v
                        else:
                            cleaned_data[k] = v
                    
                    print(json.dumps(cleaned_data, indent=2))
            
            return TestResult(endpoint, response.status_code, data.get('success', False), 
                             data.get('message', ''), data)
        else:
            if not silent:
                print(f"Error: {response.text}")
            return TestResult(endpoint, response.status_code, False, response.text)
    
    except requests.RequestException as e:
        if not silent:
            print(f"Request failed: {e}")
        return TestResult(endpoint, 0, False, f"Request failed: {e}")
    except json.JSONDecodeError:
        if not silent:
            print(f"Response is not valid JSON: {response.text}")
        return TestResult(endpoint, response.status_code, False, "Invalid JSON response")
    except Exception as e:
        if not silent:
            print(f"Error processing response: {e}")
        return TestResult(endpoint, 0, False, f"Error: {str(e)}")
    
    if not silent:
        print("=" * 50)

def test_connectivity(all_nodes):
    """Test connectivity between key node pairs"""
    print("\n===== Testing Network Connectivity =====")
    
    # Define key node pairs to test (important locations that should be connected)
    key_pairs = [
        (1, 10),  # Basic path in central area
        (1, 15),  # Longer path
        (2, 11),  # Different area
        (3, 12),  # Another path
        (4, 13),  # Long distance connection
    ]
    
    # Check if all_nodes is a dictionary (keyed by ID) or a list of nodes
    if isinstance(all_nodes, dict):
        valid_node_ids = list(all_nodes.keys())
    else:
        # Assume it's a list of node objects
        valid_node_ids = [n['id'] for n in all_nodes]
    
    # Convert node IDs to correct type if needed
    valid_node_ids = [int(nid) if isinstance(nid, str) and nid.isdigit() else nid for nid in valid_node_ids]
    
    if not all(n[0] in valid_node_ids and n[1] in valid_node_ids for n in key_pairs):
        import random
        random.seed(42)
        
        # If using a dictionary structure
        if isinstance(all_nodes, dict):
            facilities = [nid for nid, data in all_nodes.items() if data.get('is_facility', False)]
            residential = [nid for nid, data in all_nodes.items() if data.get('type') == 'Residential']
            business = [nid for nid, data in all_nodes.items() if data.get('type') == 'Business']
        else:
            # If using a list structure
            facilities = [n['id'] for n in all_nodes if n.get('is_facility', False)]
            residential = [n['id'] for n in all_nodes if n.get('type') == 'Residential']
            business = [n['id'] for n in all_nodes if n.get('type') == 'Business']
        
        key_pairs = []
        if residential and facilities:
            key_pairs.append((random.choice(residential), random.choice(facilities)))
        if business and residential:
            key_pairs.append((random.choice(business), random.choice(residential)))
        all_nodes_sample = random.sample(valid_node_ids, min(10, len(valid_node_ids)))
        for i in range(min(5, len(all_nodes_sample) // 2)):
            key_pairs.append((all_nodes_sample[i*2], all_nodes_sample[i*2+1]))
    
    results = []
    modes = ["distance", "time"]
    
    for start_id, end_id in key_pairs:
        for mode in modes:
            result = test_api_endpoint("find_path", method="POST", payload={
                "start_id": start_id,
                "end_id": end_id,
                "mode": mode,
                "time_of_day": "morning"
            }, silent=True)
            
            results.append({
                "start_id": start_id,
                "end_id": end_id,
                "mode": mode,
                "connected": result.success is True,
                "path_length": len(result.data.get('path', [])) if result.success else 0,
                "message": result.message if not result.success else ""
            })
    
    table_data = [[r['start_id'], r['end_id'], r['mode'], '✓' if r['connected'] else '✗', 
                r['path_length'], r['message']] for r in results]
    print(tabulate(table_data, headers=["Start", "End", "Mode", "Connected", "Path Length", "Message"]))
    
    connected_count = sum(1 for r in results if r['connected'])
    total_tests = len(results)
    connectivity_rate = (connected_count / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\nConnectivity Rate: {connectivity_rate:.1f}% ({connected_count}/{total_tests} tests passed)")
    print("=" * 50)
    
    return connectivity_rate > 50

def compare_pathfinding_algorithms(valid_node_pairs):
    """Compare different pathfinding algorithms on the same node pairs"""
    print("\n===== Comparing Pathfinding Algorithms =====")
    
    results = []
    
    for start_id, end_id in valid_node_pairs:
        algorithms = [
            {"name": "Normal (Dijkstra)", "endpoint": "find_path", "payload": {
                "start_id": start_id, "end_id": end_id, "mode": "time", "time_of_day": "morning"
            }},
            {"name": "Emergency (A* + Haversine)", "endpoint": "emergency_route", "payload": {
                "start_id": start_id, "end_id": end_id, "emergency_type": "ambulance", "time_of_day": "morning"
            }},
            {"name": "Multimodal", "endpoint": "multimodal_route", "payload": {
                "start_id": start_id, "end_id": end_id, "time_of_day": "morning"
            }}
        ]
        
        comparison = {"start_id": start_id, "end_id": end_id, "algorithms": []}
        
        for algo in algorithms:
            result = test_api_endpoint(algo["endpoint"], method="POST", 
                                      payload=algo["payload"], silent=True)
            
            if result.success:
                time_minutes = result.data.get('total_time_minutes', 
                                              result.data.get('time', 0))
                distance_km = result.data.get('total_distance_km', 
                                             result.data.get('distance', 0))
                
                comparison["algorithms"].append({
                    "name": algo["name"],
                    "success": True,
                    "time_minutes": time_minutes,
                    "distance_km": distance_km,
                    "path_length": len(result.data.get('path', []))
                })
            else:
                comparison["algorithms"].append({
                    "name": algo["name"],
                    "success": False,
                    "message": result.message
                })
        
        results.append(comparison)
    
    for r in results:
        print(f"\nPath from {r['start_id']} to {r['end_id']}:")
        
        table_data = []
        for algo in r['algorithms']:
            if algo['success']:
                table_data.append([
                    algo['name'], 
                    '✓', 
                    f"{algo['time_minutes']:.1f} mins",
                    f"{algo['distance_km']:.1f} km",
                    algo['path_length']
                ])
            else:
                table_data.append([
                    algo['name'], 
                    '✗', 
                    'N/A', 
                    'N/A',
                    'N/A'
                ])
                
        print(tabulate(table_data, headers=["Algorithm", "Success", "Time", "Distance", "Hops"]))
    
    print("=" * 50)

def test_multimodal_routing():
    """Test the multimodal routing functionality with different parameters"""
    print("\n===== Testing Multimodal Routing =====")
    
    nodes_result = test_api_endpoint("nodes", silent=True)
    if not nodes_result.passed or 'nodes' not in nodes_result.data:
        print("Failed to get nodes for multimodal testing")
        return False
    
    stats_result = test_api_endpoint("statistics", silent=True)
    
    is_connected = False
    components = 1
    
    if stats_result.passed and 'statistics' in stats_result.data:
        stats = stats_result.data['statistics']
        if 'connectivity' in stats:
            is_connected = stats['connectivity'].get('connected', False)
            components = stats['connectivity'].get('components', 1)
    
    print(f"Network connected: {'Yes' if is_connected else 'No'} ({components} components)")
    
    valid_pairs = []
    all_nodes = nodes_result.data['nodes']
    
    import random
    random.seed(42)
    
    node_ids = [n['id'] for n in all_nodes]
    facilities = [n['id'] for n in all_nodes if n.get('is_facility', True)]
    
    test_pairs = []
    
    if len(facilities) >= 2:
        test_pairs.extend([(facilities[i], facilities[j]) 
                           for i in range(len(facilities)) 
                           for j in range(i+1, len(facilities)) 
                           if i != j][:3])
    
    sample_size = min(10, len(node_ids))
    random_pairs = []
    while len(random_pairs) < sample_size and len(node_ids) >= 2:
        pair = random.sample(node_ids, 2)
        if pair not in random_pairs:
            random_pairs.append((pair[0], pair[1]))
    
    test_pairs.extend(random_pairs)
    
    for start_id, end_id in test_pairs:
        result = test_api_endpoint("find_path", method="POST", payload={
            "start_id": start_id,
            "end_id": end_id,
            "mode": "distance"
        }, silent=True)
        
        if result.passed:
            valid_pairs.append((start_id, end_id))
            if len(valid_pairs) >= 3:
                break
    
    if not valid_pairs:
        print("Could not find any connected node pairs for testing")
        valid_pairs = [(1, 3), (1, 10), (2, 5)]
    
    test_configs = [
        {"title": "Default", "params": {}},
        {"title": "Prefer Metro", "params": {"preferred_modes": ["metro"]}},
        {"title": "Road Only", "params": {"preferred_modes": ["road"]}},
        {"title": "Limited Transfers", "params": {"max_transfers": 1}},
        {"title": "Evening Rush Hour", "params": {"time_of_day": "evening"}}
    ]
    
    results = []
    
    for start_id, end_id in valid_pairs:
        pair_results = []
        
        for config in test_configs:
            payload = {
                "start_id": start_id,
                "end_id": end_id,
                **config["params"]
            }
            
            result = test_api_endpoint("multimodal_route", method="POST", 
                                      payload=payload, silent=True)
            
            if result.passed:
                pair_results.append({
                    "config": config["title"],
                    "success": True,
                    "time_minutes": result.data.get('total_time_minutes', 0),
                    "distance_km": result.data.get('total_distance_km', 0),
                    "transfers": result.data.get('transfers', 0),
                    "improvement": result.data.get('percent_improvement', 0)
                })
            else:
                pair_results.append({
                    "config": config["title"],
                    "success": False,
                    "message": result.message
                })
        
        results.append({"start_id": start_id, "end_id": end_id, "configs": pair_results})
    
    for r in results:
        print(f"\nMultimodal routing from {r['start_id']} to {r['end_id']}:")
        
        table_data = []
        for config in r['configs']:
            if config['success']:
                table_data.append([
                    config['config'],
                    '✓',
                    f"{config['time_minutes']:.1f} mins",
                    f"{config['distance_km']:.1f} km",
                    config['transfers'],
                    f"{config['improvement']:.1f}%"
                ])
            else:
                table_data.append([
                    config['config'],
                    '✗',
                    'N/A',
                    'N/A',
                    'N/A',
                    'N/A'
                ])
        
        print(tabulate(table_data, 
                      headers=["Configuration", "Success", "Time", "Distance", "Transfers", "Improvement"]))
    
    success_count = sum(1 for r in results for c in r['configs'] if c['success'])
    total_tests = sum(len(r['configs']) for r in results)
    success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\nMultimodal Routing Success Rate: {success_rate:.1f}% ({success_count}/{total_tests} tests passed)")
    print("=" * 50)
    
    return success_rate > 60

def run_comprehensive_tests():
    """Run all API tests with more thorough validation"""
    print("Starting comprehensive backend API tests...")
    
    results = []
    summary = defaultdict(int)
    
    for endpoint in ["nodes", "graph_data", "statistics", "metro_lines", "bus_routes", "population_density"]:
        result = test_api_endpoint(endpoint)
        results.append(result)
        
        if result.passed:
            summary["passed"] += 1
        else:
            summary["failed"] += 1
    
    nodes_data = next((r.data.get('nodes') for r in results 
                      if r.endpoint == "nodes" and r.passed), None)
    
    if nodes_data:
        connectivity_passed = test_connectivity(nodes_data)
        if connectivity_passed:
            summary["connectivity"] = "PASS"
        else:
            summary["connectivity"] = "FAIL"
        
        valid_node_pairs = []
        
        import random
        random.seed(42)
        
        node_ids = [n['id'] for n in nodes_data]
        for _ in range(10):
            if len(node_ids) < 2:
                break
                
            start_id, end_id = random.sample(node_ids, 2)
            
            result = test_api_endpoint("find_path", method="POST", payload={
                "start_id": start_id,
                "end_id": end_id,
                "mode": "distance"
            }, silent=True)
            
            if result.passed:
                valid_node_pairs.append((start_id, end_id))
                if len(valid_node_pairs) >= 3:
                    break
        
        if valid_node_pairs:
            summary["valid_paths"] = len(valid_node_pairs)
            compare_pathfinding_algorithms(valid_node_pairs[:3])
        else:
            summary["valid_paths"] = 0
            print("\nCould not find valid node pairs for algorithm comparison")
        
        multimodal_passed = test_multimodal_routing()
        if multimodal_passed:
            summary["multimodal"] = "PASS"
        else:
            summary["multimodal"] = "FAIL"
    else:
        summary["connectivity"] = "SKIP"
        summary["valid_paths"] = "SKIP"
        summary["multimodal"] = "SKIP"
    
    for endpoint in ["traffic_analysis", "transport_suggestions"]:
        params = {"time": "morning"} if endpoint == "traffic_analysis" else None
        result = test_api_endpoint(endpoint, params=params)
        results.append(result)
        
        if result.passed:
            summary["passed"] += 1
        else:
            summary["failed"] += 1
    
    optimization_tests = [
        {"endpoint": "optimize_road_network", "params": {
            "prioritize_population": "true",
            "include_existing": "true"
        }},
        {"endpoint": "optimize_bus_routes", "params": {
            "max_buses": 50,
            "target_coverage": 0.8
        }},
        {"endpoint": "optimize_metro_schedule", "params": {
            "peak_hours": "morning,evening",
            "off_peak_hours": "afternoon,night"
        }}
    ]
    
    for test in optimization_tests:
        result = test_api_endpoint(test["endpoint"], params=test["params"])
        results.append(result)
        
        if result.passed:
            summary["passed"] += 1
        else:
            summary["failed"] += 1
    
    print("\n===== Test Summary =====")
    print(f"Basic Endpoints: {summary['passed']}/{summary['passed'] + summary['failed']} passed")
    print(f"Network Connectivity: {summary['connectivity']}")
    print(f"Valid Paths Found: {summary['valid_paths']}")
    print(f"Multimodal Routing: {summary['multimodal']}")
    
    pass_rate = (summary['passed'] / (summary['passed'] + summary['failed'])) * 100
    print(f"\nOverall API Success Rate: {pass_rate:.1f}%")
    
    print("\nAll tests completed!")

def run_tests():
    """Run basic API tests (for backward compatibility)"""
    print("Starting backend API tests...")
    
    test_api_endpoint("nodes")
    test_api_endpoint("graph_data")
    test_api_endpoint("statistics")
    
    test_api_endpoint("metro_lines")
    test_api_endpoint("bus_routes")
    test_api_endpoint("population_density")
    
    test_api_endpoint("traffic_analysis", params={"time": "morning"})
    test_api_endpoint("transport_suggestions")
    
    test_api_endpoint("find_path", method="POST", payload={
        "start_id": 1,
        "end_id": 10,
        "mode": "distance"
    })
    
    test_api_endpoint("find_path", method="POST", payload={
        "start_id": 1,
        "end_id": 10,
        "mode": "time",
        "time_of_day": "morning"
    })
    
    test_api_endpoint("emergency_route", method="POST", payload={
        "start_id": 1,
        "end_id": 10,
        "emergency_type": "ambulance",
        "time_of_day": "morning"
    })
    
    test_api_endpoint("multimodal_route", method="POST", payload={
        "start_id": 1,
        "end_id": 10,
        "time_of_day": "morning"
    })
    
    test_api_endpoint("optimize_road_network", params={
        "prioritize_population": "true",
        "include_existing": "true"
    })
    
    test_api_endpoint("optimize_bus_routes", params={
        "max_buses": 50,
        "target_coverage": 0.8
    })
    
    test_api_endpoint("optimize_metro_schedule", params={
        "peak_hours": "morning,evening",
        "off_peak_hours": "afternoon,night"
    })
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--comprehensive":
        run_comprehensive_tests()
    else:
        run_tests()