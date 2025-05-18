# Transportation Network Analysis System

This documentation provides a comprehensive overview of the Transportation Network Analysis system, a Flask-based backend application for analyzing and optimizing transportation networks.

## Overview

The system provides tools for:
- Loading and visualizing transportation network data
- Finding optimal routes between locations
- Analyzing traffic patterns and congestion
- Optimizing road networks and public transportation
- Emergency route planning

## Project Structure

```
backend/
├── data/               # json data files
├── src/
│   └── app/
│       ├── api/        # API endpoints
│       ├── graph/      # Graph models and network handling
│       ├── models/     # Data models
│       ├── services/   # Business logic and algorithms
│       └── utils/      # Helper functions
```

## Key Technologies

- **Python**: Core programming language
- **Flask**: Web API framework
- **NetworkX**: Graph modeling and algorithms
- **Pandas**: Data loading and manipulation
- **JSON**: Data interchange format

## Getting Started

To run the application:

1. Ensure Python 3.7+ is installed
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python backend/src/app/app.py`
4. The API will be available at `http://localhost:5000`

## API Documentation

See [API Reference](api-reference.md) for detailed API documentation.

## Module Documentation

- [Graph Module](modules/graph.md)
- [Data Loading](modules/data-loading.md)
- [Pathfinding](modules/pathfinding.md)
- [API Routes](modules/api-routes.md)
- [Data Models](modules/data-models.md)

## Data Schema

See [Data Schema](../backend/src/app/DataSchema.md) for detailed information on the data formats.
```

## Navigation

Use the links above to navigate through the detailed documentation for each component of the system.
