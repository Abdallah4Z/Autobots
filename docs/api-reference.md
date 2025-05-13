# API Reference

This document provides a detailed reference for all API endpoints in the Transportation Network Analysis system.

## Base URL

All API URLs are relative to the base URL:

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication.

## Data Formats

All responses are in JSON format. Most requests that require a request body expect JSON as well.

## Common Response Structure

Most endpoints return responses with this common structure:

```json
{
  "success": true|false,
  "message": "Error message (only included on failure)",
  "...": "Additional endpoint-specific data"
}
```

## Endpoints

### Graph Data

#### GET `/api/graph_data`

Returns graph data for visualization.

**Query Parameters:**
- `potential` (optional): `true` to include potential roads

**Response:**
```json
{
  "nodes": [
    { "id": "1", "name": "Downtown", "x": 31.23, "y": 30.05, "type": "residential" },
    ...
  ],
  "edges": [
    { "source": "1", "target": "2", "distance": 2.3, "congestion": 0.7 },
    ...
  ]
}
```

#### GET `/api/graph_image`

Returns a base64 encoded image of the graph.

**Query Parameters:**
- `potential` (optional): `true` to include potential roads

**Response:**
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGg..."
}
```

### Network Data

#### GET `/api/nodes`

Returns all nodes (locations) in the network.

**Response:**
```json
{
  "success": true,
  "nodes": [
    { "id": "1", "name": "Downtown", "type": "residential", "population": 25000 },
    ...
  ]
}
```

#### GET `/api/metro_lines`

Returns all metro lines data.

**Response:**
```json
{
  "success": true,
  "metro_lines": [
    {
      "id": "M1", 
      "name": "Red Line",
      "stations": ["1", "5", "10", "15"],
      "daily_passengers": 250000
    },
    ...
  ]
}
```

#### GET `/api/bus_routes`

Returns all bus routes data.

**Response:**
```json
{
  "success": true,
  "bus_routes": [
    {
      "id": "B1",
      "stops": ["2", "7", "12", "18"],
      "buses": 12,
      "daily_passengers": 15000
    },
    ...
  ]
}
```

### Pathfinding

#### POST `/api/find_path`

Finds the shortest/fastest path between two locations.

**Request Body:**
```json
{
  "start_id": "1",
  "end_id": "15",
  "mode": "distance",  // or "time"
  "time_of_day": "morning"  // or "afternoon", "evening", "night"
}
```

**Response (success):**
```json
{
  "success": true,
  "path": ["1", "5", "10", "15"],
  "path_names": ["Downtown", "Central Park", "Business District", "Suburb East"],
  "distance": 12.5,
  "time": 24.3,  // only if mode is "time"
  "edges": ["1_5", "5_10", "10_15"]
}
```

**Response (failure):**
```json
{
  "success": false,
  "message": "No path found between these locations",
  "details": "Node 1 is in component 1, Node 15 is in component 2"
}
```

#### POST `/api/emergency_route`

Finds optimal routes for emergency vehicles.

**Request Body:**
```json
{
  "start_id": "H1",
  "end_id": "7",
  "emergency_type": "ambulance", // or "fire", "police"
  "time_of_day": "morning" // or "afternoon", "evening", "night"
}
```

**Response:**
```json
{
  "success": true,
  "path": ["H1", "3", "5", "7"],
  "path_names": ["Central Hospital", "Junction 3", "Central Park", "North Residential"],
  "distance": 7.2,
  "time": 9.8,
  "time_saved_vs_normal": 6.3,
  "percent_improvement": 39.1,
  "edges": ["H1_3", "3_5", "5_7"]
}
```

#### POST `/api/multimodal_route`

Finds optimal route using multiple transportation modes.

**Request Body:**
```json
{
  "start_id": "2",
  "end_id": "12",
  "time_of_day": "morning",
  "preferred_modes": ["metro", "road"],
  "max_transfers": 2
}
```

**Response:**
```json
{
  "success": true,
  "path": ["2", "5", "10", "12"],
  "path_names": ["West End", "Central Park", "Business District", "East End"],
  "distance": 13.7,
  "time": 28.5,
  "modes": ["road", "metro", "road"],
  "transfers": 2,
  "edges": ["2_5", "5_10", "10_12"]
}
```

### Analysis

#### GET `/api/statistics`

Returns network statistics.

**Response:**
```json
{
  "success": true,
  "statistics": {
    "node_count": 35,
    "edge_count": 58,
    "total_road_length_km": 128.5,
    "average_congestion": 0.68,
    "connected_components": 2,
    "metro_stations": 18,
    "bus_stops": 42,
    "population_covered": 950000
  }
}
```

#### GET `/api/traffic_analysis`

Analyzes traffic patterns and congestion.

**Query Parameters:**
- `time` (optional): 'morning', 'afternoon', 'evening', 'night' (default: 'morning')

**Response:**
```json
{
  "success": true,
  "congestion_data": {
    "congestion_by_road": {
      "1_2": 0.85,
      "2_3": 0.67,
      ...
    },
    "highest_congestion_roads": [
      { "road": "1_2", "congestion": 0.85, "from": "Downtown", "to": "West End" },
      ...
    ],
    "average_congestion": 0.58,
    "congestion_histogram": {
      "0.0-0.2": 8,
      "0.2-0.4": 15,
      "0.4-0.6": 20,
      "0.6-0.8": 10,
      "0.8-1.0": 5
    }
  }
}
```

#### GET `/api/transport_suggestions`

Gets suggestions for public transportation improvements.

**Response:**
```json
{
  "success": true,
  "suggestions": [
    {
      "type": "new_bus_route",
      "from": "North Residential",
      "to": "West Industrial",
      "stops": ["7", "8", "13", "16"],
      "expected_ridership": 12000,
      "priority": "high"
    },
    {
      "type": "increase_frequency",
      "route": "M2",
      "current_headway_minutes": 8,
      "suggested_headway_minutes": 5,
      "expected_new_riders": 3500,
      "priority": "medium"
    },
    ...
  ]
}
```

### Optimization

#### GET `/api/optimize_road_network`

Optimizes road network using MST algorithm.

**Query Parameters:**
- `prioritize_population` (optional): 'true' or 'false' (default: 'false')
- `include_existing` (optional): 'true' or 'false' (default: 'true')
- `max_budget` (optional): Maximum budget in million EGP (default: 1000000)

**Response:**
```json
{
  "success": true,
  "optimized_roads": [
    { "from": "3", "to": "8", "distance": 2.1, "cost": 15 },
    { "from": "8", "to": "12", "distance": 3.4, "cost": 28 },
    ...
  ],
  "total_cost": 143,
  "total_distance": 24.7,
  "population_covered": 820000,
  "connectivity_improvement": 35
}
```

#### GET `/api/optimize_bus_routes`

Optimizes bus routes using dynamic programming.

**Query Parameters:**
- `max_buses` (optional): Maximum number of buses (default: 100)
- `target_coverage` (optional): Target population coverage (0.0-1.0, default: 0.8)

**Response:**
```json
{
  "success": true,
  "optimized_routes": [
    {
      "route_id": "B1",
      "stops": ["2", "7", "12", "18"],
      "buses_assigned": 12,
      "expected_ridership": 15000
    },
    ...
  ],
  "total_buses": 78,
  "population_coverage": 0.83,
  "estimated_total_ridership": 320000
}
```

#### GET `/api/optimize_metro_schedule`

Optimizes metro schedule using dynamic programming.

**Query Parameters:**
- `peak_hours` (optional): Comma-separated peak hours (default: 'morning,evening')
- `off_peak_hours` (optional): Comma-separated off-peak hours (default: 'afternoon,night')

**Response:**
```json
{
  "success": true,
  "optimized_schedules": [
    {
      "line_id": "M1",
      "peak_headway_minutes": 3,
      "off_peak_headway_minutes": 8,
      "trains_required": 12,
      "daily_capacity": 280000
    },
    ...
  ]
}
```

## Error Codes

The API uses standard HTTP status codes:

- `200 OK`: The request was successful
- `400 Bad Request`: The request was malformed
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

## Rate Limiting

Currently, the API does not implement rate limiting.
