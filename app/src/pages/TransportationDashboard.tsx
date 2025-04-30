import React, { useState } from 'react';
import TransportationMap from '../components/TransportationMap';
import '../style/transportation-map.css';

// Cairo facilities data from the CSV file
const CAIRO_FACILITIES = [
  {
    id: "F1",
    name: "Cairo International Airport",
    type: "airport" as const,
    latitude: 30.11,
    longitude: 31.41
  },
  {
    id: "F2",
    name: "Ramses Railway Station",
    type: "train-station" as const,
    latitude: 30.06,
    longitude: 31.25
  },
  {
    id: "F3",
    name: "Cairo University",
    type: "other" as const,
    latitude: 30.03,
    longitude: 31.21
  },
  {
    id: "F4",
    name: "Al-Azhar University",
    type: "facility" as const,
    latitude: 30.05,
    longitude: 31.26
  },
  {
    id: "F5",
    name: "Egyptian Museum",
    type: "bus-stop" as const,
    latitude: 30.05,
    longitude: 31.23
  },
  {
    id: "F6",
    name: "Cairo International Stadium",
    type: "metro-station" as const,
    latitude: 30.07,
    longitude: 31.3
  },
  {
    id: "F7",
    name: "Smart Village",
    type: "bus-terminal" as const,
    latitude: 30.07,
    longitude: 30.97
  },
  {
    id: "F8",
    name: "Cairo Festival City",
    type: "point-of-interest" as const,
    latitude: 30.03,
    longitude: 31.4
  },
  {
    id: "F9",
    name: "Qasr El Aini Hospital",
    type: "ferry-terminal" as const,
    latitude: 30.03,
    longitude: 31.23
  },
  {
    id: "F10",
    name: "Maadi Military Hospital",
    type: "facility" as const,
    latitude: 29.95,
    longitude: 31.25
  }
];

const TransportationDashboard: React.FC = () => {
  // Only keep the bare minimum state
  const [mapStyle] = useState<'streets' | 'satellite' | 'dark' | 'light'>('streets');
  const [coordinates, setCoordinates] = useState<{longitude: number, latitude: number} | null>(null);

  // Handle map click event
  const handleMapClick = (longitude: number, latitude: number) => {
    setCoordinates({ longitude, latitude });
    
    // You can perform additional actions with the coordinates here
    // For example, sending them to an API or storing them in a database
  };

  return (
    <div className="map-only-container">
      <TransportationMap
        locations={CAIRO_FACILITIES}
        initialViewState={{
          longitude: 31.23, // Centered on Cairo
          latitude: 30.05,
          zoom: 11
        }}
        mapStyle={mapStyle}
        onMapClick={handleMapClick}
      />
      
      {/* Optional: Display coordinates outside of map for copying/pasting */}
      {coordinates && (
        <div className="coordinates-display">
          <p>Longitude: {coordinates.longitude.toFixed(6)}, Latitude: {coordinates.latitude.toFixed(6)}</p>
        </div>
      )}
    </div>
  );
};

export default TransportationDashboard;