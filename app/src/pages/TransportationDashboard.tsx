import React from 'react';
import TransportationMap from '../components/TransportationMap';
import '../style/transportation-map.css';

interface Waypoint {
  location: {
    lat: number;
    lng: number;
  };
  stopover: boolean;
}

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
];

// Sample origin and destination this is starting
const SAMPLE_ORIGIN = { lat: 30.03, lng: 31.4 }; // Cairo Airport
const SAMPLE_DESTINATION = { lat: 30.03, lng: 31.21}; // Maadi Military Hospital

const TransportationDashboard: React.FC = () => {
  return (
    <div className="map-only-container">
      <TransportationMap
        initialViewState={{
          longitude: 31.23, // Centered on Cairo
          latitude: 30.05,
          zoom: 11
        }}
        waypoints={SAMPLE_WAYPOINTS}
        origin={SAMPLE_ORIGIN}
        destination={SAMPLE_DESTINATION}
      />
    </div>
  );
};

export default TransportationDashboard;