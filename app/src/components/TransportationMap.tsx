import React, { useState, useCallback, useEffect, useRef } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow, DirectionsService, DirectionsRenderer, Polyline } from '@react-google-maps/api';
import MapDrawer from './MapDrawer';
import { Box, Typography } from '@mui/material';
import { cityData } from '../pages/cityData';

interface Waypoint {
  location: {
    lat: number;
    lng: number;
  };
  stopover: boolean;
}

interface RouteNode {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
}

interface RouteData {
  nodes: string[];
  totalDistance?: number;
  totalTime?: number;
  edges?: Array<{from: string, to: string}>;
  lineStyle?: string;
}

interface TransportationMapProps {
  initialViewState?: {
    longitude: number;
    latitude: number;
    zoom: number;
  };
  // New prop for waypoints
  waypoints?: Waypoint[];
  // New prop for origin and destination
  origin?: { lat: number; lng: number };
  destination?: { lat: number; lng: number };
  // Optional prop to control route display from parent
  defaultShowRoute?: boolean;
  onRouteToggle?: (showRoute: boolean) => void;
  // Add route data handler
  onFetchRoute?: (data: any) => void;
}

// Define map container style
const containerStyle = {
  width: '100vw',
  height: '100vh'
};

// Map node IDs to location data
const getNodeLocation = (nodeId: string): RouteNode | undefined => {
  const nodeData = cityData.find(location => location.id === nodeId);
  if (nodeData) {
    return {
      id: nodeData.id,
      name: nodeData.name,
      latitude: nodeData.coordinates.lat,
      longitude: nodeData.coordinates.lng
    };
  }
  return undefined;
};

const TransportationMap: React.FC<TransportationMapProps> = ({
  initialViewState = {
    longitude: 31.23, // Default to Cairo center
    latitude: 30.05, 
    zoom: 11
  },
  waypoints = [],
  origin,
  destination,
  defaultShowRoute = false,
  onRouteToggle,
  onFetchRoute
}) => {
  // State for directions response
  const [directionsResponse, setDirectionsResponse] = useState<google.maps.DirectionsResult | null>(null);
  // State to track if we need to request new directions
  const [directionsRequest, setDirectionsRequest] = useState<boolean>(false);
  // New state for route toggle
  const [showRoute, setShowRoute] = useState<boolean>(defaultShowRoute);
  // Route data from the dropdown
  const [routeData, setRouteData] = useState<RouteData | null>(null);
  // Line style preference (straight line or roads)
  const [lineStyle, setLineStyle] = useState<string>("Roads");
  // Route nodes converted to coordinates
  const [routeCoordinates, setRouteCoordinates] = useState<google.maps.LatLngLiteral[]>([]);
  
  const mapRef = useRef<google.maps.Map | null>(null);

  // Load the Google Maps script
  const { isLoaded, loadError } = useJsApiLoader({
    id: 'google-map-script',
    // Using the API key from the environment variables
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries: ['places']
  });
  
  // Define the map center based on initialViewState
  const center = {
    lat: initialViewState.latitude,
    lng: initialViewState.longitude
  };

  const onMapLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
  }, []);

  // Handle route toggle
  const handleToggleRoute = useCallback(() => {
    const newShowRoute = !showRoute;
    setShowRoute(newShowRoute);
    if (onRouteToggle) {
      onRouteToggle(newShowRoute);
    }
  }, [showRoute, onRouteToggle]);
  
  // Handle route data from dropdown
  const handleRouteData = useCallback((data: RouteData) => {
    console.log('Route data received in TransportationMap:', data);
    setRouteData(data);
    
    // Update line style preference if provided
    if (data.lineStyle) {
      setLineStyle(data.lineStyle);
    }
    
    // Convert node IDs to coordinates for straight line rendering
    if (data.nodes && Array.isArray(data.nodes)) {
      const coordinates = data.nodes.map(nodeId => {
        const node = getNodeLocation(nodeId);
        if (node) {
          return { lat: node.latitude, lng: node.longitude };
        }
        return null;
      }).filter(coord => coord !== null) as google.maps.LatLngLiteral[];
      
      setRouteCoordinates(coordinates);
      
      // If using Roads style, set up origin/destination for DirectionsService
      if (data.lineStyle === 'Roads' && coordinates.length >= 2) {
        const originCoord = coordinates[0];
        const destCoord = coordinates[coordinates.length - 1];
        
        // If coordinates are valid, set up directions request
        if (originCoord && destCoord) {
          setDirectionsRequest(true);
        }
      } else {
        // If using StraightLine style, clear any directions
        setDirectionsResponse(null);
        setDirectionsRequest(false);
      }
    }
    
    // Pass data to parent if needed
    if (onFetchRoute) {
      onFetchRoute(data);
    }
  }, [onFetchRoute]);
  
  // Effect to handle line style changes
  useEffect(() => {
    if (routeData && routeData.lineStyle !== lineStyle) {
      // Update the routeData with the new line style
      const updatedRouteData = {
        ...routeData,
        lineStyle
      };
      
      // Process the updated route data
      handleRouteData(updatedRouteData);
    }
  }, [lineStyle, routeData]);

  // Directions callback handler
  const directionsCallback = (response: google.maps.DirectionsResult | null, status: google.maps.DirectionsStatus) => {
    console.log('Directions response:', status, response);
    if (status === 'OK' && response) {
      setDirectionsResponse(response);
    } else {
      console.error('Directions request failed with status:', status);
      // If directions fail, fall back to straight lines
      if (lineStyle === 'Roads') {
        console.log('Falling back to straight line rendering');
        setLineStyle('StraightLine');
      }
    }
    setDirectionsRequest(false);
  };

  // Generate waypoints for directions service from route coordinates
  const generateWaypoints = useCallback((): google.maps.DirectionsWaypoint[] => {
    if (routeCoordinates.length <= 2) {
      return []; // No waypoints needed for just origin and destination
    }
    
    // Use all points except first and last as waypoints
    return routeCoordinates.slice(1, -1).map(coord => ({
      location: new google.maps.LatLng(coord.lat, coord.lng),
      stopover: true
    }));
  }, [routeCoordinates]);

  // Render loading state
  if (loadError) {
    return <div>Error loading maps. Ensure API key is correct and API is enabled.</div>;
  }

  if (!isLoaded) {
    return <div>Loading Maps...</div>;
  }

  // Determine if we should show routes based on state and if we have route data
  const shouldShowRoute = showRoute && routeCoordinates.length >= 2;
  
  // Determine if we should show the Google Maps directions or our straight line
  const shouldShowDirections = shouldShowRoute && lineStyle === 'Roads' && directionsResponse;
  const shouldShowStraightLine = shouldShowRoute && lineStyle === 'StraightLine';

  // Render the map
  return (
    <Box sx={{ position: 'relative', height: '100vh', width: '100vw' }}>
      {/* MapDrawer for controls */}
      <MapDrawer 
        title="Transportation Controls" 
        showFilters={true}
        showRoute={showRoute}
        onToggleRoute={handleToggleRoute}
        onFetchRoute={handleRouteData}
      />
      
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={initialViewState.zoom}
        onLoad={onMapLoad}
        options={{ 
          streetViewControl: false,
          mapTypeControl: false,
          fullscreenControl: false,
        }}
      >
        {/* Request directions if we should show route with Roads style */}
        {directionsRequest && shouldShowRoute && lineStyle === 'Roads' && routeCoordinates.length >= 2 && (
          <DirectionsService
            options={{
              origin: routeCoordinates[0],
              destination: routeCoordinates[routeCoordinates.length - 1],
              waypoints: generateWaypoints(),
              travelMode: google.maps.TravelMode.DRIVING,
              optimizeWaypoints: false, // Preserve waypoint order
            }}
            callback={directionsCallback}
          />
        )}
        
        {/* Render directions if we have a response and should show directions */}
        {shouldShowDirections && (
          <DirectionsRenderer
            options={{
              directions: directionsResponse,
              suppressMarkers: false,
              polylineOptions: {
                strokeColor: '#4285F4',
                strokeWeight: 5,
                strokeOpacity: 0.8,
              }
            }}
          />
        )}

        {/* Render straight line if that style is selected */}
        {shouldShowStraightLine && (
          <Polyline
            path={routeCoordinates}
            options={{
              strokeColor: '#FF0000',
              strokeWeight: 4,
              strokeOpacity: 0.7,
              geodesic: true, // Draw great circle between points
            }}
          />
        )}

        {/* Render markers for route nodes */}
        {shouldShowRoute && routeCoordinates.map((coord, index) => (
          <Marker
            key={`node-${index}`}
            position={coord}
            label={(index === 0 || index === routeCoordinates.length - 1) ? 
                    (index === 0 ? 'A' : 'B') : // Origin or destination
                    undefined} // Intermediate points
            icon={{
              path: google.maps.SymbolPath.CIRCLE,
              scale: (index === 0 || index === routeCoordinates.length - 1) ? 10 : 6,
              fillColor: (index === 0) ? '#00FF00' : (index === routeCoordinates.length - 1) ? '#FF0000' : '#0000FF',
              fillOpacity: 1,
              strokeWeight: 2,
              strokeColor: '#FFFFFF',
            }}
          />
        ))}
      </GoogleMap>
    </Box>
  );
};

export default TransportationMap;