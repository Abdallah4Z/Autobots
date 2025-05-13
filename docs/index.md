# Transportation Network Analysis System

## Project Overview

This system provides a comprehensive framework for analyzing and optimizing transportation networks, with a focus on urban infrastructure. It combines graph theory, algorithmic optimization, and transportation planning principles to support decision-making for urban mobility.

## Key Features

- **Network Visualization**: Interactive visualization of transportation networks
- **Pathfinding**: Multiple algorithms for optimal route finding
- **Traffic Analysis**: Tools to analyze congestion and traffic patterns
- **Public Transport Optimization**: Bus and metro route/schedule optimization
- **Multimodal Routing**: Integrated routing across different transportation modes
- **Emergency Routing**: Specialized routing for emergency vehicles

## Technical Architecture

The application is built using a modern stack:

- **Backend**: Python with Flask for the API server
- **Data Structure**: NetworkX for graph algorithms
- **Data Loading**: Pandas for CSV data processing
- **Visualization**: Matplotlib and NetworkX for network visualization

## Documentation

### User Guides
- [Getting Started](README.md)
- [API Reference](api-reference.md)

### Technical Documentation
- [Data Models](modules/graph-model.md)
- [Graph Module](modules/graph.md)
- [Pathfinding Algorithms](modules/pathfinding.md)
- [Data Loading](modules/data-loading.md)
- [Data Formatting](modules/data-formatting.md)
- [Visualization](modules/visualization.md)
- [Analysis Tools](modules/analysis.md)
- [Optimization Algorithms](modules/optimization.md)
- [Application Core](modules/app.md)
- [Transportation API](modules/transportation.md)
- [API Routes](modules/api-routes.md)

### Schema and Data Formats
- [Data Schema](../backend/src/app/DataSchema.md)

## Algorithms Implemented

### Pathfinding
- Dijkstra's Algorithm
- A* Search
- Multi-criteria optimization

### Optimization
- Minimum Spanning Tree (MST)
- Dynamic Programming
- Greedy Algorithms

### Analysis
- Connected Components
- Centrality Measures
- Traffic Flow Analysis

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python backend/src/app/app.py`
4. Access the API at `http://localhost:5000`

## Contributing

See [Contributing Guidelines](CONTRIBUTING.md) for information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
