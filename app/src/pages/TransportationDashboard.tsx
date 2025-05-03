import React, { useState } from 'react';
import TransportationMap from '../components/TransportationMap';
import ApiDebugger from '../components/ApiDebugger';
import Dropdown from '../components/Dropdown';
import '../style/transportation-map.css';
import { Box, Button, Typography } from '@mui/material';

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
  const [showDebugger, setShowDebugger] = useState(false);
  
  return (
    <div className="dashboard-container">
      <Box sx={{ width: '100%', p: 2 }}>
        <Dropdown />
        
        <Box sx={{ textAlign: 'center', my: 2 }}>
          <Button 
            variant="contained" 
            color="secondary" 
            onClick={() => setShowDebugger(!showDebugger)}
          >
            {showDebugger ? 'Hide API Debugger' : 'Show API Debugger'}
          </Button>
        </Box>
        
        {showDebugger && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 1 }}>API Debugging Tool</Typography>
            <ApiDebugger />
          </Box>
        )}
      </Box>
      
      <div className="map-container">
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
    </div>
  );
};

export default TransportationDashboard;