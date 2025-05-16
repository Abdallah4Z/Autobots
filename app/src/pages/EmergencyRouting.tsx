import React, { useState } from 'react';
import { Box, Typography, Select, MenuItem, Button, FormControl, InputLabel } from '@mui/material';
import { useTransportationMap } from '../components/TransportationMap';

const EmergencyRouting: React.FC = () => {
    const [origin, setOrigin] = useState('');
    const [destination, setDestination] = useState('');
    const [emergencyType, setEmergencyType] = useState('ambulance');
    const [routeInfo, setRouteInfo] = useState<any>(null);
    const { updateRouteOnMap } = useTransportationMap();

    const handleFindRoute = async () => {
        try {
            const response = await fetch(
                `/emergency/route?origin=${origin}&dest=${destination}&type=${emergencyType}`
            );
            const data = await response.json();
            
            if (response.ok) {
                setRouteInfo(data);
                // Update route on map
                updateRouteOnMap(data.edges, true); // true indicates emergency route
            } else {
                console.error('Error:', data.error);
            }
        } catch (error) {
            console.error('Failed to fetch route:', error);
        }
    };

    const findNearestFacility = async () => {
        try {
            const response = await fetch(
                `/emergency/nearest-facility?location=${origin}&type=${
                    emergencyType === 'ambulance' ? 'hospital' :
                    emergencyType === 'fire_truck' ? 'fire_station' : 'police_station'
                }`
            );
            const data = await response.json();
            
            if (response.ok) {
                setDestination(data.facility_id);
            } else {
                console.error('Error:', data.error);
            }
        } catch (error) {
            console.error('Failed to find nearest facility:', error);
        }
    };

    return (
        <Box sx={{ p: 2 }}>
            <Typography variant="h5" gutterBottom>
                Emergency Response Routing
            </Typography>

            <Box sx={{ mb: 2 }}>
                <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Emergency Type</InputLabel>
                    <Select
                        value={emergencyType}
                        label="Emergency Type"
                        onChange={(e) => setEmergencyType(e.target.value)}
                    >
                        <MenuItem value="ambulance">Ambulance</MenuItem>
                        <MenuItem value="fire_truck">Fire Truck</MenuItem>
                        <MenuItem value="police">Police</MenuItem>
                    </Select>
                </FormControl>

                <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Origin Location</InputLabel>
                    <Select
                        value={origin}
                        label="Origin Location"
                        onChange={(e) => setOrigin(e.target.value)}
                    >
                        {/* Add your location options here */}
                    </Select>
                </FormControl>

                <Button 
                    variant="contained" 
                    color="secondary" 
                    onClick={findNearestFacility}
                    sx={{ mb: 2 }}
                >
                    Find Nearest Emergency Facility
                </Button>

                <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Destination</InputLabel>
                    <Select
                        value={destination}
                        label="Destination"
                        onChange={(e) => setDestination(e.target.value)}
                    >
                        {/* Add your location options here */}
                    </Select>
                </FormControl>

                <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleFindRoute}
                    fullWidth
                >
                    Find Emergency Route
                </Button>
            </Box>

            {routeInfo && (
                <Box sx={{ mt: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                    <Typography variant="h6">Route Information</Typography>
                    <Typography>
                        Estimated Response Time: {routeInfo.estimated_response_time.toFixed(1)} minutes
                    </Typography>
                    <Typography>
                        Emergency Type: {emergencyType}
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

export default EmergencyRouting;
