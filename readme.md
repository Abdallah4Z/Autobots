# 🚀 Autobots - Transportation Network Analysis System

Welcome to the **Autobots** project repository! This system provides a comprehensive framework for analyzing and optimizing urban transportation networks.

## 🌟 Project Overview

The Transportation Network Analysis System is a powerful tool designed to help urban planners, transportation engineers, and policymakers analyze, visualize, and optimize transportation networks. Using advanced algorithms from graph theory and operations research, the system provides data-driven insights for improving urban mobility.

## 🎯 Key Features

- **Interactive Network Visualization**: View and interact with transportation network maps
- **Pathfinding & Routing**: Find optimal routes between locations using various algorithms
- **Traffic Analysis**: Analyze congestion patterns and identify bottlenecks
- **Public Transport Optimization**: Optimize bus routes, metro schedules, and transit connections
- **Emergency Vehicle Routing**: Specialized pathfinding for emergency services
- **Multimodal Transportation Planning**: Integrate different transportation modes for efficient travel
- **Infrastructure Planning**: Evaluate potential new roads and improvements

## 📂 Project Structure

```
project/
├── app/                          # Frontend application
│   ├── public/                   # Static assets
│   ├── src/                      # Frontend source code
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   └── utils/                # Utility functions
│   ├── package.json              # Frontend dependencies
│   └── tsconfig.json             # TypeScript configuration
│
├── backend/                      # Backend application
│   ├── data/                     # CSV and JSON data files
│   └── src/
│       └── app/
│           ├── api/              # API endpoints
│           ├── graph/            # Graph modeling
│           ├── models/           # Data models
│           ├── services/         # Business logic and algorithms
│           │   ├── analysis.py   # Traffic & network analysis
│           │   ├── optimization.py # Optimization algorithms
│           │   └── pathfinding.py # Route finding algorithms
│           └── utils/            # Helper functions
│               ├── data_loader.py # Data loading utilities
│               └── visualization.py # Graph visualization
│
├── docs/                         # Documentation
│   ├── modules/                  # Module-specific documentation
│   ├── api-reference.md          # API documentation
│   └── index.md                  # Documentation home
│
└── README.md                     # This file
```

## 📦 Frontend (React + Vite + TypeScript)

The frontend provides an intuitive, interactive user interface for the transportation network analysis system, visualizing complex network data and algorithmic results.

### 📋 Architecture

- **Component-Based Design**: Modular architecture with reusable components
- **State Management**: Context API for application-wide state management
- **API Integration**: Services layer for backend API communication
- **Responsive Design**: Mobile-friendly interface that adapts to different screen sizes

### 🔍 Key Components

- **NetworkMap**: Interactive visualization of the transportation network using Google Maps API
- **RouteSelector**: Interface for selecting origin and destination points
- **AnalyticsDashboard**: Visualization of traffic and network analytics
- **OptimizationPanel**: UI for running and viewing optimization scenarios
- **EmergencyRoutePlanner**: Specialized interface for emergency routing

### 📁 Frontend Structure

```
app/
├── src/
│   ├── components/              # Reusable UI components
│   │   ├── common/              # Generic UI components (buttons, inputs, etc.)
│   │   ├── map/                 # Map-related components
│   │   ├── analytics/           # Data visualization components
│   │   └── routing/             # Route display and selection components
│   ├── pages/                   # Page components
│   │   ├── Dashboard.tsx        # Main dashboard
│   │   ├── NetworkView.tsx      # Network visualization view
│   │   ├── RouteAnalysis.tsx    # Route analysis page
│   │   └── Optimization.tsx     # Optimization tools page
│   ├── services/                # API and data services
│   │   ├── api.ts               # API client
│   │   ├── networkService.ts    # Network data service
│   │   └── routingService.ts    # Routing service
│   ├── context/                 # React Context providers
│   │   ├── NetworkContext.tsx   # Network data context
│   │   └── UserContext.tsx      # User preferences context
│   └── utils/                   # Utility functions
│       ├── mapHelpers.ts        # Map-related utilities
│       └── dataFormatters.ts    # Data formatting utilities
```

### 🔧 Installed Libraries

Before running the frontend, ensure you have the required dependencies installed:

```bash
cd app
npm i react-router-dom
npm i axios leaflet react-leaflet
npm i recharts
npm i @react-google-maps/api
```

### 🎨 UI Libraries & Frameworks

- **Google Maps API**: Core mapping and geolocation functionality
- **Leaflet/React-Leaflet**: Alternative interactive maps
- **Recharts**: Data visualization
- **Material-UI**: UI components
- **React Router**: Navigation and routing

### 📝 Google Maps API Setup

1. Obtain a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a `.env` file in the root of the app directory
3. Add your API key: `VITE_GOOGLE_MAPS_API_KEY=your_api_key_here`
4. The application will automatically load your API key securely

### 🚀 Running the Frontend

Start the development server by navigating to the `app` directory:

```bash
cd app
npm run dev
```

This will start the development server on `http://localhost:5173` (or another port if 5173 is in use).

## 🔙 Backend (Python + Flask)

### 📋 Prerequisites
Ensure you have Python 3.7+ installed along with the following packages:
- Flask
- NetworkX
- Pandas
- Matplotlib
- Flask-CORS

You can install all dependencies with:
```bash
pip install flask networkx pandas matplotlib flask-cors
```

### 🚀 Running the Backend
To run the backend Flask server, navigate to the `backend/src/app` directory and execute the following command:

```bash
cd backend/src/app
flask --app app run
```

## 🔍 Using the Application

Once both the frontend and backend are running:

1. Open your browser and navigate to `http://localhost:5173` (or the port shown in the Vite output)
2. Use the interactive map to explore the transportation network
3. Select origin and destination points to find optimal routes
4. Analyze traffic patterns using the analysis tools
5. Explore optimization suggestions for improving the network

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **API Reference**: Details of all API endpoints 
- **Module Documentation**: Documentation for all backend modules
- **Algorithms**: Explanation of implemented algorithms
- **Data Schema**: Format of input and output data

## 🛠️ Technologies Used

- **Frontend**: React, TypeScript, Vite, React Router
- **Backend**: Python, Flask, NetworkX
- **Data Processing**: Pandas
- **Visualization**: Matplotlib, React visualization libraries

## ❓ Need Help?
If you encounter any issues during setup or development, check the documentation first or reach out to the development team.

---
