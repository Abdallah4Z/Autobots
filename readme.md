# 🚀 Autobots - Transportation Network Analysis System

Welcome to the **Autobots** project repository! This system provides a comprehensive framework for analyzing and optimizing urban transportation networks.

## 🌟 Project Overview

The Transportation Network Analysis System is a powerful tool designed to help urban planners, transportation engineers, and policymakers analyze, visualize, and optimize transportation networks. Using advanced algorithms from graph theory and operations research, the system provides data-driven insights for improving urban mobility.

## 🎯 Key Features

- **Interactive Network Visualization**: View and interact with transportation network maps
- **Pathfinding & Routing**: Find optimal routes between locations using various algorithms (A* and Dijkstra)
- **Traffic Analysis**: Analyze congestion patterns and identify bottlenecks
- **Public Transport Optimization**: Optimize bus routes, metro schedules, and transit connections
- **Emergency Vehicle Routing**: Specialized pathfinding for emergency services
- **Multimodal Transportation Planning**: Integrate different transportation modes for efficient travel
- **Infrastructure Planning**: Evaluate potential new roads and improvements using MST

## 📂 Project Structure

```
project/
├── app/                          # Frontend application
│   ├── public/                   # Static assets
│   ├── src/                      # Frontend source code
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   │   ├── FAQsPage.tsx      # Frequently asked questions
│   │   │   ├── HomePage.tsx      # Landing page
│   │   │   └── cityData.ts       # City location data
│   │   ├── styles/               # CSS styles
│   │   ├── assets/               # Images and icons
│   │   └── App.tsx               # Main application component
│   ├── package.json              # Frontend dependencies
│   └── tsconfig.json             # TypeScript configuration
│
├── backend/                      # Backend application
│   ├── src/                      # Source files
│   │   ├── app/                  # Application code
│   │   │   ├── api/              # API endpoint definitions
│   │   │   ├── graph/            # Graph data structure
│   │   │   ├── models/           # Data models 
│   │   │   │   └── graph.py      # Graph model implementation
│   │   │   ├── services/         # Business logic
│   │   │   │   └── optimization.py # Optimization algorithms (MST, etc.)
│   │   │   ├── flow/             # Flow algorithm implementations
│   │   │   ├── emergency/        # Emergency routing
│   │   │   └── planner/          # Infrastructure planning using MST
│   │   └── app.py                # Main application entry point
│   ├── test_backend.py           # Test script for backend APIs
│   └── data/                     # Data files
│       ├── bus_routes.json       # Bus route information
│       ├── current_metro_lines.json # Metro line information
│       ├── important_facilities.json # Facility locations
│       ├── neighbourhoods.json   # Neighborhood data
│       ├── public_transport_demand.json # Transport demand data
│       ├── roads_existing.json   # Existing road network 
│       ├── roads_potential.json  # Potential new roads
│       └── traffic_flow_patterns.json # Traffic data
│
├── docs/                         # Project documentation
│   ├── modules/                  # Module-specific documentation
│   │   ├── analysis.md           # Traffic & network analysis
│   │   ├── api-routes.md         # API endpoints documentation
│   │   ├── app.md                # Main application overview
│   │   ├── data-formatting.md    # Data transformation guidelines
│   │   ├── data-loading.md       # Data import processes
│   │   ├── graph-model.md        # Graph data model specification
│   │   ├── graph.md              # Graph theory concepts
│   │   ├── optimization.md       # Network optimization methods
│   │   ├── pathfinding.md        # Route-finding algorithms
│   │   ├── transportation.md     # Transportation domain knowledge
│   │   └── visualization.md      # Data visualization techniques
│   ├── api-reference.md          # Complete API documentation
│   ├── Cairo Transportation Network Optimization.md # Overview document
│   ├── CSE112-Practical Project.pdf    # Project requirements
│   ├── CSE112-Theoretical Project.pdf  # Theoretical background
│   ├── index.md                  # Documentation home
│   ├── Project_Provided_Data.pdf # Data specifications
│   ├── README.md                 # Documentation guide
│   ├── Smart City Transportation Project - Team Autobots.pdf # Project proposal
│   └── Technical_Report.pdf      # Implementation details
│
└── README.md                     # This file
```

## 📦 Frontend (React + Vite + TypeScript)

The frontend provides an intuitive, interactive user interface for the transportation network analysis system, visualizing complex network data and algorithmic results.

### 📋 Architecture

- **Component-Based Design**: Modular architecture with reusable components
- **Responsive Design**: Mobile-friendly interface that adapts to different screen sizes
- **Algorithm Selection**: Choose between Dijkstra's algorithm and A* for pathfinding

### 🔍 Key Components

- **TransportationMap**: Interactive visualization using Google Maps API, including traffic layer
- **Dropdown**: Controls for selecting origin, destination, time of day, and algorithm
- **MapDrawer**: Sidebar for map configuration and filtering options
- **RouteInfoPanel**: Displays details about the calculated route
- **FloatingHelpButton**: Quick access to FAQs and help

### 🎨 UI Libraries & Frameworks

- **Material-UI**: Core UI components and styling system
- **Google Maps API**: Interactive mapping and route visualization
- **React Router**: Navigation between pages

### 📝 Google Maps API Setup

1. Obtain a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a `.env` file in the root of the app directory
3. Add your API key: `VITE_GOOGLE_MAPS_API_KEY=your_api_key_here`
4. The application will automatically load your API key securely

### 🚀 Running the Frontend

Start the development server by navigating to the `app` directory:

```bash
cd app
npm install
npm run dev
```

This will start the development server on `http://localhost:5173` (or another port if 5173 is in use).

## 🔙 Backend (Python + Flask)

### 📋 Prerequisites
Ensure you have Python 3.7+ installed along with the following packages:
- Flask
- NetworkX
- Pandas
- Flask-CORS

You can install all dependencies with:
```bash
pip install flask networkx pandas flask-cors
```

### 🚀 Running the Backend
To run the backend Flask server, navigate to the `backend/src/app` directory and execute the following command:

```bash
cd backend/src
python app.py
```

The server will start on port 5000 by default.

## 🔍 Using the Application

Once both the frontend and backend are running:

1. Open your browser and navigate to `http://localhost:5173`
2. Use the dropdown filters to select your origin and destination
3. Choose a time of day (morning, afternoon, evening, night) to see different map styles
4. Select a routing algorithm (ASTAR or Dijkstra)
5. Choose between straight line visualization or actual road routes
6. For emergency services, select the emergency type (Ambulance, Police, Fire Truck)
7. Toggle traffic data visibility with the traffic button
8. View route details in the information panel

## 🛠️ Technologies Used

- **Frontend**: React, TypeScript, Vite, Material-UI, Google Maps API
- **Backend**: Python, Flask, NetworkX
- **Algorithms**: A*, Dijkstra's algorithm, Minimum Spanning Tree

## ❓ Need Help?
If you have questions about using the application, visit the FAQs page by clicking the help button. For technical issues, please refer to the project documentation.

Note: You'll need a valid Google Maps API key to run this application locally.


