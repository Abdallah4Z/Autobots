import React, { useState, useCallback, useEffect, useRef } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow, DirectionsService, DirectionsRenderer, Polyline } from '@react-google-maps/api';
import MapDrawer from './MapDrawer';
import { Box, Typography } from '@mui/material';
import { cityData } from '../pages/cityData';

// Map styles for different times of day
const mapStyles = {  morning: [
    {
      // Very subtle morning style - just a light overlay on the default map
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [{ "saturation": 15 }, { "lightness": 5 }]  // Slightly more vibrant water
    },
    {
      "featureType": "landscape.natural",
      "elementType": "geometry", 
      "stylers": [{ "saturation": 5 }, { "hue": "#8aff00" }, { "lightness": 5 }]  // Very subtle green tint
    },
    {
      "featureType": "poi.park",
      "elementType": "geometry",
      "stylers": [{ "hue": "#a3e36b" }, { "saturation": 10 }]  // Very subtle park highlight
    }
  ],
  afternoon: [], // Empty array = default Google Maps style
  evening: [
    {
      "elementType": "geometry",
      "stylers": [{ "color": "#eeebe5" }]
    },
    {
      "elementType": "labels.text.fill",
      "stylers": [{ "color": "#4a4a4a" }]
    },
    {
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [{ "color": "#b0d4e8" }]
    },
    {
      "featureType": "road",
      "elementType": "geometry",
      "stylers": [{ "color": "#e4bc7b" }]
    }
  ],
  night: [
    {
      "elementType": "geometry",
      "stylers": [{ "color": "#242f3e" }]
    },
    {
      "elementType": "labels.text.stroke",
      "stylers": [{ "color": "#242f3e" }]
    },
    {
      "elementType": "labels.text.fill",
      "stylers": [{ "color": "#746855" }]
    },
    {
      "featureType": "road",
      "elementType": "geometry",
      "stylers": [{ "color": "#38414e" }]
    },
    {
      "featureType": "road",
      "elementType": "geometry.stroke",
      "stylers": [{ "color": "#212a37" }]
    },
    {
      "featureType": "road",
      "elementType": "labels.text.fill",
      "stylers": [{ "color": "#9ca5b3" }]
    },
    {
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [{ "color": "#17263c" }]
    },
    {
      "featureType": "water",
      "elementType": "labels.text.fill",
      "stylers": [{ "color": "#515c6d" }]
    },
    {
      "featureType": "water",
      "elementType": "labels.text.stroke",
      "stylers": [{ "color": "#17263c" }]
    }
  ]
};

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
  edges?: Array<{from: string, to: string, mode?: string, route?: string}>;
  lineStyle?: string;
  timeOfDay?: string; // Added time of day for map styling
  isPublicTransport?: boolean;
  isEmergencyRoute?: boolean;
  emergencyType?: string;
  isMST?: boolean; // Flag for MST vs. path
  steps?: any[]; // Public transport steps data
  rawData?: any; // Raw data for MST
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
  // Time of day for styling the map
  timeOfDay?: string;
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

// Add this component before the main TransportationMap component
// This component will handle rendering directions for individual MST edges
interface EdgeDirectionsProps {
  fromNode: RouteNode;
  toNode: RouteNode;
  index: number;
}

const EdgeDirectionsRenderer: React.FC<EdgeDirectionsProps> = ({ fromNode, toNode, index }) => {
  const [directionsResponse, setDirectionsResponse] = useState<google.maps.DirectionsResult | null>(null);
  const [requestSent, setRequestSent] = useState<boolean>(false);
  
  // Callback function for the directions service
  const directionsCallback = (
    result: google.maps.DirectionsResult | null,
    status: google.maps.DirectionsStatus
  ) => {
    if (status === 'OK' && result) {
      setDirectionsResponse(result);
    } else {
      console.error(`Directions request failed for edge ${index} with status:`, status);
    }
    setRequestSent(true);
  };
  
  return (
    <>
      {!requestSent && (
        <DirectionsService
          options={{
            origin: { lat: fromNode.latitude, lng: fromNode.longitude },
            destination: { lat: toNode.latitude, lng: toNode.longitude },
            travelMode: google.maps.TravelMode.DRIVING,
          }}
          callback={directionsCallback}
        />
      )}
      
      {directionsResponse && (
        <DirectionsRenderer
          options={{
            directions: directionsResponse,
            suppressMarkers: true,
            polylineOptions: {
              strokeColor: '#FF0000',
              strokeWeight: 3,
              strokeOpacity: 0.8,
            }
          }}
        />
      )}
    </>
  );
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
  onFetchRoute,
  timeOfDay = 'morning' // Default to morning if not specified
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
  // Current time of day for map styling
  const [currentTimeOfDay, setCurrentTimeOfDay] = useState<string>(timeOfDay);
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
  
  // Effect to update the map style when timeOfDay prop changes
  useEffect(() => {
    if (timeOfDay && timeOfDay !== currentTimeOfDay) {
      setCurrentTimeOfDay(timeOfDay.toLowerCase());
    }
  }, [timeOfDay]);

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
    
    // Update time of day if provided
    if (data.timeOfDay) {
      setCurrentTimeOfDay(data.timeOfDay.toLowerCase());
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
      // Only do this for regular routes, not for MST
      if (data.lineStyle === 'Roads' && coordinates.length >= 2 && !data.isMST) {
        const originCoord = coordinates[0];
        const destCoord = coordinates[coordinates.length - 1];
        
        // If coordinates are valid, set up directions request
        if (originCoord && destCoord) {
          setDirectionsRequest(true);
        }
      } else {
        // If using StraightLine style or it's MST data, clear any directions
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
      {/* MapDrawer for controls */}      <MapDrawer 
        title="Transportation Controls" 
        showFilters={true}
        showRoute={showRoute}
        onToggleRoute={handleToggleRoute}
        onFetchRoute={handleRouteData}
        timeOfDay={currentTimeOfDay}
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
          styles: mapStyles[currentTimeOfDay as keyof typeof mapStyles] || []
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
        {shouldShowStraightLine && !routeData?.isMST && (
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

        {/* Render MST (Minimum Spanning Tree) graph */}
        {shouldShowRoute && routeData?.isMST && routeData?.edges && (
          <>
            {routeData.edges.map((edge, index) => {
              // Get coordinates for each edge in the MST
              const fromNode = getNodeLocation(edge.from);
              const toNode = getNodeLocation(edge.to);
              
              if (fromNode && toNode) {
                // For Roads style, use the Directions API to draw actual roads
                if (lineStyle === 'Roads') {
                  return (
                    <EdgeDirectionsRenderer
                      key={`mst-road-edge-${index}`}
                      fromNode={fromNode}
                      toNode={toNode}
                      index={index}
                    />
                  );
                }
                
                // For StraightLine style, draw direct lines
                const fromCoord = { lat: fromNode.latitude, lng: fromNode.longitude };
                const toCoord = { lat: toNode.latitude, lng: toNode.longitude };
                
                return (
                  <Polyline
                    key={`mst-edge-${index}`}
                    path={[fromCoord, toCoord]}
                    options={{
                      strokeColor: '#FF0000', // Red color for MST edges
                      strokeWeight: 3,
                      strokeOpacity: 0.8,
                      geodesic: true,
                    }}
                  />
                );
              }
              return null;
            })}
            
            {/* Render nodes for MST */}
            {routeData.nodes.map((nodeId, index) => {
              const node = getNodeLocation(nodeId);
              if (node) {
                const coord = { lat: node.latitude, lng: node.longitude };
                return (
                  <Marker
                    key={`mst-node-${nodeId}`}
                    position={coord}
                    title={node.name}
                    icon={{
                      path: google.maps.SymbolPath.CIRCLE,
                      scale: 6,
                      fillColor: '#0000FF', // Blue color for MST nodes
                      fillOpacity: 1,
                      strokeWeight: 2,
                      strokeColor: '#FFFFFF',
                    }}
                  />
                );
              }
              return null;
            })}
          </>
        )}

        {/* Render public transportation routes */}
        {shouldShowRoute && routeData?.isPublicTransport && routeData?.edges && 
          routeData.edges.map((edge, index) => {
            // Get coordinates for the edge
            const fromNode = getNodeLocation(edge.from);
            const toNode = getNodeLocation(edge.to);
            
            if (fromNode && toNode) {
              const fromCoord = { lat: fromNode.latitude, lng: fromNode.longitude };
              const toCoord = { lat: toNode.latitude, lng: toNode.longitude };
              
              // Different styling based on mode (bus or metro)
              const isMetro = edge.mode === 'metro';
              
              return (
                <Polyline
                  key={`pt-edge-${index}`}
                  path={[fromCoord, toCoord]}
                  options={{
                    strokeColor: isMetro ? '#0000FF' : '#FF6600', // Blue for metro, Orange for bus
                    strokeWeight: isMetro ? 5 : 4,
                    strokeOpacity: 0.8,
                    geodesic: true,
                    // Use dashed line for bus routes if in straight line mode
                    icons: !isMetro && lineStyle === 'StraightLine' ? [
                      {
                        icon: {
                          path: 'M 0,-1 0,1',
                          strokeOpacity: 1,
                          scale: 3
                        },
                        offset: '0',
                        repeat: '10px'
                      }
                    ] : undefined
                  }}
                />
              );
            }
            return null;
          })
        }

        {/* Render station/stop markers for public transportation */}
        {shouldShowRoute && routeData?.isPublicTransport && routeData?.nodes && 
          routeCoordinates.map((coord, index) => {
            // Find if this is a bus stop or metro station by checking the edges
            let stationType = 'default'; // default, bus, or metro
            let routeNumber = '';
            
            if (routeData.edges && index < routeCoordinates.length - 1) {
              const nodeId = routeData.nodes[index];
              const nextNodeId = routeData.nodes[index + 1];
              
              // Find the edge that connects this node to the next
              const edge = routeData.edges.find(e => 
                (e.from === nodeId && e.to === nextNodeId) || 
                (e.to === nodeId && e.from === nextNodeId)
              );
              
              if (edge) {
                stationType = edge.mode || 'default';
                routeNumber = edge.route || '';
              }
            } else if (routeData.edges && index > 0) {
              // For last node, check previous edge
              const nodeId = routeData.nodes[index];
              const prevNodeId = routeData.nodes[index - 1];
              
              // Find the edge that connects this node to the previous
              const edge = routeData.edges.find(e => 
                (e.from === prevNodeId && e.to === nodeId) || 
                (e.to === prevNodeId && e.from === nodeId)
              );
              
              if (edge) {
                stationType = edge.mode || 'default';
                routeNumber = edge.route || '';
              }
            }
            
            return (
              <Marker
                key={`pt-node-${index}`}
                position={coord}
                label={(index === 0 || index === routeCoordinates.length - 1) ? 
                        (index === 0 ? 'A' : 'B') : // Origin or destination
                        undefined} // Intermediate points
                icon={{
                  path: stationType === 'metro' ? 
                    google.maps.SymbolPath.CIRCLE : // Circle for metro stations
                    google.maps.SymbolPath.BACKWARD_CLOSED_ARROW, // Arrow for bus stops
                  scale: (index === 0 || index === routeCoordinates.length - 1) ? 8 : 
                         (stationType === 'metro' ? 7 : 5),
                  fillColor: (index === 0) ? '#00FF00' : 
                             (index === routeCoordinates.length - 1) ? '#FF0000' : 
                             (stationType === 'metro') ? '#0000FF' : '#FF6600',
                  fillOpacity: 1,
                  strokeWeight: 2,
                  strokeColor: '#FFFFFF',
                  // Rotate bus stop icons to match route direction if not origin/destination
                  rotation: (stationType === 'bus' && index !== 0 && 
                            index !== routeCoordinates.length - 1) ? 90 : 0,
                }}
              />
            );
          })
        }
        
        {/* Render markers for route nodes */}
        {shouldShowRoute && !routeData?.isPublicTransport && routeCoordinates.map((coord, index) => (
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

        {/* Render info about the route */}
        {shouldShowRoute && routeData && (
          <InfoWindow
            position={routeCoordinates[0]}
            options={{
              pixelOffset: new google.maps.Size(0, -50)
            }}
          >
            <div style={{ padding: '8px', maxWidth: '200px' }}>
              <Typography variant="subtitle1" fontWeight="bold">Route Information</Typography>
             
              {routeData.isPublicTransport && routeData.steps && (
                <div>
                  <Typography variant="body2" fontWeight="bold" sx={{ mt: 1 }}>
                    Public Transport:
                  </Typography>
                  {routeData.steps.map((step, idx) => (
                    <Typography key={idx} variant="caption" display="block">
                      {step.mode === 'metro' ? '🚇 Metro' : '🚌 Bus'} {step.route}: 
                      {step.start} → {step.end} ({step.stops} stops)
                    </Typography>
                  ))}
                </div>
              )}
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </Box>
  );
};

export default TransportationMap;