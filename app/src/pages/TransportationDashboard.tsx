import React, { useState, useEffect } from 'react';
import TransportationMap from '../components/TransportationMap';
import Dropdown from '../components/Dropdown';
import '../style/transportation-map.css';
import { Box, Button, Typography } from '@mui/material';
import { cityData } from './cityData';

interface Waypoint {
  location: {
    lat: number;
    lng: number;
  };
  stopover: boolean;
}

interface RouteInfo {
  nodes: string[];
  totalDistance: number;
  totalTime: number;
}

// Default starting waypoints if needed
const DEFAULT_WAYPOINTS: Waypoint[] = [];

// Default origin and destination
const DEFAULT_ORIGIN = { lat: 30.05, lng: 31.23 }; // Cairo center
const DEFAULT_DESTINATION = { lat: 30.06, lng: 31.25 }; // Nearby location

const TransportationDashboard: React.FC = () => {
  const [waypoints, setWaypoints] = useState<Waypoint[]>(DEFAULT_WAYPOINTS);
  const [origin, setOrigin] = useState<{ lat: number; lng: number }>(DEFAULT_ORIGIN);
  const [destination, setDestination] = useState<{ lat: number; lng: number }>(DEFAULT_DESTINATION);
  const [showRoute, setShowRoute] = useState(false);
  const [showTraffic, setShowTraffic] = useState(false);  const [routeData, setRouteData] = useState<RouteInfo | null>(null);
  
  // Handler for route data from Dropdown component
  const handleRouteData = (data: RouteInfo | undefined) => {
    if (!data || !data.nodes || data.nodes.length < 2) {
      console.error("Invalid route data received:", data);
      return;
    }
    
    setRouteData(data);
    console.log("Route data received:", data);
    
    // Convert node IDs to coordinates
    try {
      const nodeCoordinates = convertNodesToCoordinates(data.nodes);
      
      // Set origin (first node)
      if (nodeCoordinates.length > 0) {
        setOrigin(nodeCoordinates[0]);
      }
      
      // Set destination (last node)
      if (nodeCoordinates.length > 1) {
        setDestination(nodeCoordinates[nodeCoordinates.length - 1]);
      }
      
      // Set waypoints (middle nodes)
      if (nodeCoordinates.length > 2) {
        const waypointsArray = nodeCoordinates.slice(1, -1).map(coord => ({
          location: coord,
          stopover: true
        }));
        setWaypoints(waypointsArray);
      } else {
        setWaypoints([]);
      }
      
      // Enable route display
      setShowRoute(true);
      
    } catch (error) {
      console.error("Error processing route data:", error);
    }
  };
  
  // Helper function to convert node IDs to lat/lng coordinates
  const convertNodesToCoordinates = (nodes: string[]): Array<{ lat: number; lng: number }> => {
    return nodes.map(nodeId => {
      // Find the node in cityData
      const location = cityData.find(loc => loc.id === nodeId);
      
      if (!location) {
        console.warn(`Location not found for node ID: ${nodeId}`);
        // Return a default coordinate if not found
        return { lat: 30.05, lng: 31.23 };
      }
      
      return { 
        lat: location.coordinates.lat, 
        lng: location.coordinates.lng 
      };
    });
  };

  // Handler for route toggle
  const handleRouteToggle = (value: boolean) => {
    setShowRoute(value);
  };
  
  // Handler for traffic toggle
  const handleTrafficToggle = (value: boolean) => {
    setShowTraffic(value);
  };

  return (
    <div className="dashboard-container">
      
      <div className="map-container">        <TransportationMap
          initialViewState={{
            longitude: 31.23, // Centered on Cairo
            latitude: 30.05,
            zoom: 11
          }}
          waypoints={waypoints}
          origin={origin}
          destination={destination}
          defaultShowRoute={showRoute}
          onRouteToggle={handleRouteToggle}
          onFetchRoute={handleRouteData} // Pass the route data handler
          timeOfDay={'morning'} // Default time of day for map styling
          defaultShowTraffic={showTraffic}
          onTrafficToggle={handleTrafficToggle}
        />
      </div>
    </div>
  );
};

export default TransportationDashboard;