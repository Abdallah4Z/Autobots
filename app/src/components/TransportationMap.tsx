import React, { useState, useCallback, useEffect,useRef } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow, DirectionsService, DirectionsRenderer } from '@react-google-maps/api';
import MapDrawer from './MapDrawer';
import { Box,Typography } from '@mui/material';

interface Waypoint {
  location: {
    lat: number;
    lng: number;
  };
  stopover: boolean;
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
  // mapStyle prop is removed as Google Maps handles styles differently
  // Optional prop to control route display from parent
  defaultShowRoute?: boolean;
  onRouteToggle?: (showRoute: boolean) => void;
}
// Define map container style
const containerStyle = {
  width: '100vw',
  height: '100vh'
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
}) => {
  // State for directions response
  const [directionsResponse, setDirectionsResponse] = useState<google.maps.DirectionsResult | null>(null);
  // State to track if we need to request new directions
  const [directionsRequest, setDirectionsRequest] = useState<boolean>(false);
  // New state for route toggle
  const [showRoute, setShowRoute] = useState<boolean>(defaultShowRoute);
  
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
  
  // Effect to trigger directions request when origin/destination/waypoints change
  useEffect(() => {
    if (origin && destination && showRoute) {
      setDirectionsRequest(true);
    } else {
      setDirectionsResponse(null);
    }
  }, [origin, destination, waypoints, showRoute]);

 
  // Directions callback handler
  const directionsCallback = (response: google.maps.DirectionsResult | null, status: google.maps.DirectionsStatus) => {
    if (status === 'OK' && response) {
      setDirectionsResponse(response);
      setDirectionsRequest(false);
    } else {
      console.error('Directions request failed with status:', status);
      setDirectionsRequest(false);
    }
  };

  // Render loading state
  if (loadError) {
    return <div>Error loading maps. Ensure API key is correct and API is enabled.</div>;
  }

  if (!isLoaded) {
    return <div>Loading Maps...</div>;
  }

  // Determine if we should show routes based on state
  const shouldShowRoute = showRoute && origin && destination;

  // Render the map
  return (
    <Box sx={{ position: 'relative', height: '100vh', width: '100vw' }}>
      {/* Add the MapDrawer component with route toggle */}
      <MapDrawer 
        title="Transportation Controls" 
        showFilters={true}
        showRoute={showRoute}
        onToggleRoute={handleToggleRoute}
      >
        
      </MapDrawer>
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={initialViewState.zoom}
      onLoad={onMapLoad}

      options={{ // Optional: Disable some default UI elements
        
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: false,
      }}
    >
      {/* Request directions if we have origin and destination and showRoute is true */}
      {directionsRequest && shouldShowRoute && (
        <DirectionsService
          options={{
            origin: origin!,
            destination: destination!,
            waypoints: waypoints,
            travelMode: google.maps.TravelMode.DRIVING,
            optimizeWaypoints: false, // Set to false to preserve waypoint order
          }}
          callback={directionsCallback}
        />
      )}
      
      {/* Render directions if we have a response */}
      {directionsResponse && shouldShowRoute && (
        <DirectionsRenderer
          options={{
            directions: directionsResponse,
            suppressMarkers: false, // Set to true if you want to use custom markers
          }}
        />
      )}

      {/* Render markers for locations (if not using directions)
      {!directionsResponse && locations.map((location) => (
        <Marker
          key={location.id}
          position={{ lat: location.latitude, lng: location.longitude }}
          title={location.name} // Tooltip on hover
          // Optional: Add custom icons based on location.type here
        />
      ))} */}

      {/* Render waypoint markers if not using directions
      {!directionsResponse && waypoints.map((waypoint, index) => (
        <Marker
          key={`waypoint-${index}`}
          position={waypoint.location}
          icon={{
            path: google.maps.SymbolPath.CIRCLE,
            scale: 7,
            fillColor: "#0000FF",
            fillOpacity: 1,
            strokeWeight: 2,
            strokeColor: "#FFFFFF",
          }}
          title={`Waypoint ${index + 1}`}
        />
      ))} */}

    
    

    </GoogleMap>
    </Box>

  );
};

export default TransportationMap;