import React, { useRef, useState } from 'react';
import Map, { 
  Marker, 
  NavigationControl,
  ScaleControl,
  Popup
} from 'react-map-gl/maplibre';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

// No need for API token with OpenStreetMap
const OSM_STYLE = {
  version: 8,
  sources: {
    osm: {
      type: 'raster',
      tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
      tileSize: 256,
      attribution: '&copy; OpenStreetMap Contributors',
      maxzoom: 19
    }
  },
  layers: [
    {
      id: 'osm',
      type: 'raster',
      source: 'osm',
      minzoom: 0,
      maxzoom: 19
    }
  ]
};

interface MapLocation {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  type: 'bus-stop' | 'metro-station' | 'facility' | 'point-of-interest'| 'other';
}

interface TransportationMapProps {
  initialViewState?: {
    longitude: number;
    latitude: number;
    zoom: number;
  };
  locations?: MapLocation[];
  mapStyle?: 'streets' | 'satellite' | 'dark' | 'light';
  onMapClick?: (longitude: number, latitude: number) => void;
}

const TransportationMap: React.FC<TransportationMapProps> = ({
  initialViewState = {
    longitude: 31.41,
    latitude: 30.11, // Default to NYC
    zoom: 12
  },
  locations = [],
  mapStyle = 'dark',
  onMapClick
}) => {
  const mapRef = useRef(null);
  const [clickedPosition, setClickedPosition] = useState<{longitude: number, latitude: number} | null>(null);

  // Get the appropriate map style based on the selected style
  const getMapStyle = () => {
    switch (mapStyle) {
      case 'satellite':
        return 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json';
      case 'dark':
        return 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';
      case 'light':
        return 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json';
      case 'streets':
      default:
        return OSM_STYLE;
    }
  };

  const getMarkerColor = (type: string) => {
    switch (type) {
      case 'bus-stop':
        return '#1E88E5'; // Blue
      case 'metro-station':
        return '#D81B60'; // Pink
      case 'facility':
        return '#FFC107'; // Amber
      case 'point-of-interest':
        return '#FF9800'; // Orange
      case 'other':
        return '#9E9E9E'; // Grey
      case 'airport':
        return '#FF5722'; // Deep Orange
      case 'train-station':
        return '#3F51B5'; // Indigo
        case 'bus-terminal':
        return '#8BC34A'; // Light Green
        case 'ferry-terminal':  
        
        return '#FF5722'; // Deep Orange
      default:
        return '#4CAF50'; // Green

    }
  };

  // Handle map clicks to get coordinates
  const handleMapClick = (event: maplibregl.MapLayerMouseEvent) => {
    const { lngLat } = event;
    const longitude = lngLat.lng;
    const latitude = lngLat.lat;
    
    // Update state with clicked position
    setClickedPosition({ longitude, latitude });
    
    // If a callback was provided, call it with the coordinates
    if (onMapClick) {
      onMapClick(longitude, latitude);
    }
    
    console.log(`Clicked at: Longitude ${longitude.toFixed(6)}, Latitude ${latitude.toFixed(6)}`);
  };

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Map
        ref={mapRef}
        initialViewState={initialViewState}
        style={{ width: '100%', height: '100%' }}
        mapStyle={getMapStyle()}
        mapLib={maplibregl}
        attributionControl={true}
        onClick={handleMapClick}
        cursor="crosshair"
      >
        <NavigationControl position="bottom-right" />
        <ScaleControl />

        {locations.map((location) => (
          <Marker
            key={location.id}
            longitude={location.longitude}
            latitude={location.latitude}
            color={getMarkerColor(location.type)}
          />
        ))}

        {/* Show a marker and popup at the clicked location */}
        {clickedPosition && (
          <>
            <Marker
              longitude={clickedPosition.longitude}
              latitude={clickedPosition.latitude}
              color="#FF0000"
            />
            <Popup
              longitude={clickedPosition.longitude}
              latitude={clickedPosition.latitude}
              closeButton={true}
              closeOnClick={false}
              onClose={() => setClickedPosition(null)}
              anchor="bottom"
            >
              <div>
                <strong>Selected Coordinates</strong><br />
                Longitude: {clickedPosition.longitude.toFixed(6)}<br />
                Latitude: {clickedPosition.latitude.toFixed(6)}
              </div>
            </Popup>
          </>
        )}
      </Map>
    </div>
  );
};

export default TransportationMap;