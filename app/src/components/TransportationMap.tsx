import React, { useState, useCallback, useEffect } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow, DirectionsService, DirectionsRenderer } from '@react-google-maps/api';

interface MapLocation {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  // Keep the type for potential marker customization, but Google Maps doesn't use it directly for color
  type: 'bus-stop' | 'metro-station' | 'facility' | 'point-of-interest' | 'other' | 'airport' | 'train-station' | 'bus-terminal' | 'ferry-terminal'; 
}

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
  locations?: MapLocation[];
  // New prop for waypoints
  waypoints?: Waypoint[];
  // New prop for origin and destination
  origin?: { lat: number; lng: number };
  destination?: { lat: number; lng: number };
  // mapStyle prop is removed as Google Maps handles styles differently
  onMapClick?: (longitude: number, latitude: number) => void;
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
  locations = [],
  waypoints = [],
  origin,
  destination,
  onMapClick
}) => {
  // State for the selected location for InfoWindow
  const [selectedLocation, setSelectedLocation] = useState<MapLocation | null>(null);
  // State for the clicked coordinates for a temporary marker/info
  const [clickedCoords, setClickedCoords] = useState<{ lat: number; lng: number } | null>(null);
  // State for directions response
  const [directionsResponse, setDirectionsResponse] = useState<google.maps.DirectionsResult | null>(null);
  // State to track if we need to request new directions
  const [directionsRequest, setDirectionsRequest] = useState<boolean>(false);

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

  // Effect to trigger directions request when origin/destination/waypoints change
  useEffect(() => {
    if (origin && destination) {
      setDirectionsRequest(true);
    }
  }, [origin, destination, waypoints]);

  // Map click handler
  const handleMapClick = useCallback((event: google.maps.MapMouseEvent) => {
    if (event.latLng) {
      const lat = event.latLng.lat();
      const lng = event.latLng.lng();
      setClickedCoords({ lat, lng });
      setSelectedLocation(null); // Close any open info window
      if (onMapClick) {
        onMapClick(lng, lat); // Pass lng, lat order
      }
      console.log(`Clicked at: Longitude ${lng.toFixed(6)}, Latitude ${lat.toFixed(6)}`);
    }
  }, [onMapClick]);

  // Marker click handler
  const handleMarkerClick = (location: MapLocation) => {
    setSelectedLocation(location);
    setClickedCoords(null); // Clear clicked coords marker if a location marker is clicked
  };

  // Close InfoWindow handler
  const handleInfoWindowClose = () => {
    setSelectedLocation(null);
  };
  
  // Close handler for the clicked coordinate InfoWindow
  const handleClickedCoordInfoWindowClose = () => {
    setClickedCoords(null);
  };

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

  // Render the map
  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={initialViewState.zoom}
      onClick={handleMapClick}
      options={{ // Optional: Disable some default UI elements
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: false,
      }}
    >
      {/* Request directions if we have origin and destination */}
      {directionsRequest && origin && destination && (
        <DirectionsService
          options={{
            origin: origin,
            destination: destination,
            waypoints: waypoints,
            travelMode: google.maps.TravelMode.DRIVING,
            optimizeWaypoints: false, // Set to false to preserve waypoint order
          }}
          callback={directionsCallback}
        />
      )}
      
      {/* Render directions if we have a response */}
      {directionsResponse && (
        <DirectionsRenderer
          options={{
            directions: directionsResponse,
            suppressMarkers: false, // Set to true if you want to use custom markers
          }}
        />
      )}

      {/* Render markers for locations (if not using directions) */}
      {!directionsResponse && locations.map((location) => (
        <Marker
          key={location.id}
          position={{ lat: location.latitude, lng: location.longitude }}
          title={location.name} // Tooltip on hover
          onClick={() => handleMarkerClick(location)}
          // Optional: Add custom icons based on location.type here
        />
      ))}

      {/* Render waypoint markers if not using directions */}
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
      ))}

      {/* Show InfoWindow for selected location marker */}
      {selectedLocation && (
        <InfoWindow
          position={{ lat: selectedLocation.latitude, lng: selectedLocation.longitude }}
          onCloseClick={handleInfoWindowClose}
        >
          <div>
            <h4>{selectedLocation.name}</h4>
            <p>Type: {selectedLocation.type}</p>
            <p>Lat: {selectedLocation.latitude.toFixed(6)}, Lng: {selectedLocation.longitude.toFixed(6)}</p>
          </div>
        </InfoWindow>
      )}
      
      {/* Show a temporary marker and InfoWindow for clicked coordinates */}
      {clickedCoords && (
         <>
           <Marker 
             position={clickedCoords} 
             icon={{ // Simple red circle icon for clicked location
               path: google.maps.SymbolPath.CIRCLE,
               scale: 8,
               fillColor: "#FF0000",
               fillOpacity: 1,
               strokeWeight: 0,
             }}
           />
           <InfoWindow
             position={clickedCoords}
             onCloseClick={handleClickedCoordInfoWindowClose}
           >
             <div>
               <strong>Selected Coordinates</strong><br />
               Latitude: {clickedCoords.lat.toFixed(6)}<br />
               Longitude: {clickedCoords.lng.toFixed(6)}
             </div>
           </InfoWindow>
         </>
      )}

    </GoogleMap>
  );
};

export default TransportationMap;