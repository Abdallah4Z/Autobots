import React, { useState } from 'react';
import TransportationMap from '../components/TransportationMap';
import '../style/transportation-map.css';

// Define the Waypoint interface to match what our map component expects
interface Waypoint {
  location: {
    lat: number;
    lng: number;
  };
  stopover: boolean;
}

// Cairo facilities data from the CSV file


// Example waypoints for a route
const SAMPLE_WAYPOINTS: Waypoint[] = [
  {
    location: { lat: 30.03, lng: 31.47 }, // Near Ramses Railway Station
    stopover: true
  },
  {
    location: { lat: 30.06, lng: 31.34 }, // Near Cairo University
    stopover: true
  },
  {
    location: { lat: 30.04, lng: 31.24 }, // Near Cairo International Stadium
    stopover: true
  },
  // {
  //   location: { lat: 30.07, lng: 30.97 }, // Near Smart Village
  //   stopover: true
  // },
  // {
  //   location: { lat: 30.03, lng: 31.4 }, // Near Cairo Festival City
  //   stopover: true
  // },
  // {
  //   location: { lat: 30.03, lng: 31.23 }, // Near Qasr El Aini Hospital
  //   stopover: true
  // },
  // {
  //   location: { lat: 30.05, lng: 31.28 }, // Near Al-Azhar Park
  //   stopover: true
  // },
  // {
  //   location: { lat: 30.04, lng: 31.22 }, // Near Tahrir Square
  //   stopover: true
  // },
  // {
  //   location: { lat: 30.00, lng: 31.23 }, // Near Maadi
  //   stopover: true
  // }
];

// Sample origin and destination
const SAMPLE_ORIGIN = { lat: 30.03, lng: 31.4 }; // Cairo Airport
const SAMPLE_DESTINATION = { lat: 30.03, lng: 31.21}; // Maadi Military Hospital

const TransportationDashboard: React.FC = () => {
  const [coordinates, setCoordinates] = useState<{longitude: number, latitude: number} | null>(null);
  const [showRoute, setShowRoute] = useState<boolean>(false);

  // Handle map click event
  const handleMapClick = (longitude: number, latitude: number) => {
    setCoordinates({ longitude, latitude });
    
    // You can perform additional actions with the coordinates here
    // For example, sending them to an API or storing them in a database
  };

  return (
    <div className="map-only-container">
      <div className="map-controls">
        <button 
          className="route-toggle-btn"
          onClick={() => setShowRoute(!showRoute)}
        >
          {showRoute ? 'Hide Route' : 'Show Route'}
        </button>
      </div>
      
      <TransportationMap
        initialViewState={{
          longitude: 31.23, // Centered on Cairo
          latitude: 30.05,
          zoom: 11
        }}
        onMapClick={handleMapClick}
        waypoints={showRoute ? SAMPLE_WAYPOINTS : []}
        origin={showRoute ? SAMPLE_ORIGIN : undefined}
        destination={showRoute ? SAMPLE_DESTINATION : undefined}
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