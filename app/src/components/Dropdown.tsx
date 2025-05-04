import React, { useState, useEffect } from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Box,
  Typography,
  Grid,
  Button
} from '@mui/material';

interface DropdownProps {
  className?: string;
  onValuesChange?: (values: {
    origin: string;
    destination: string;
    timeOfDay: string;
  }) => void;
  onFetchRoute?: (data?: any) => void;
}

const Dropdown: React.FC<DropdownProps> = ({ 
  className,
  onValuesChange,
  onFetchRoute 
}) => {
  // Set default values
  const [Origin, setOrigin] = useState('1');
  const [Destination, setDestination] = useState('2');
  const [Time, setTime] = useState('Morning');

  // Notify parent component when values change
  useEffect(() => {
    if (onValuesChange) {
      onValuesChange({
        origin: Origin,
        destination: Destination,
        timeOfDay: Time
      });
    }
  }, [Origin, Destination, Time, onValuesChange]);

  // Handlers
  const handleOriginChange = (event: SelectChangeEvent) => {
    setOrigin(event.target.value);
  };

  const handleDestinationChange = (event: SelectChangeEvent) => {
    setDestination(event.target.value);
  };

  const handleTimeChange = (event: SelectChangeEvent) => {
    setTime(event.target.value);
  };

  const selectStyle = {
    fontSize: '1.2rem',
    height: '3.5rem',
  };
  
  const fetchRouteData = async () => {
    try {
      console.log('Fetching route data with parameters:', {
        origin: Origin,
        destination: Destination,
        timeOfDay: Time
      });
      
      const url = `/api/flow/route/astar?origin=${encodeURIComponent(Origin)}&dest=${encodeURIComponent(Destination)}`;
      console.log('Request URL:', url);
  
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries([...response.headers]));
      
      if (!response.ok) {
        throw new Error(`Failed to fetch route: ${response.status} ${response.statusText}`);
      }
      
      // Get the response text and parse it
      const responseText = await response.text();
      console.log('Raw response (first 500 chars):', responseText.substring(0, 500));
      
      // Parse the JSON response
      let data;
      try {
        data = JSON.parse(responseText);
        console.log('Successfully parsed route data:', data);
      } catch (jsonError) {
        console.error('Failed to parse JSON:', jsonError);
        throw new Error('Response is not valid JSON');
      }

      // Extract route nodes in order
      if (data && data.edges && Array.isArray(data.edges)) {
        // Create ordered list of nodes (from origin to destination)
        const orderedNodes = extractOrderedNodes(data.edges);
        console.log('Ordered route nodes:', orderedNodes);
        
        // Additional route information
        const routeInfo = {
          nodes: orderedNodes,
          totalDistance: data.total_distance,
          totalTime: data.total_time
        };
        
        console.log('Processed route information:', routeInfo);
        
        // Pass the processed route data to parent component
        if (onFetchRoute) {
          onFetchRoute(routeInfo);
        }
        
        return routeInfo;
      } else {
        throw new Error('Invalid route data format: missing edges array');
      }
    } catch (error) {
      console.error('Error fetching route:', error);
      alert(`Failed to fetch route data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      return null;
    }
  };

  // Helper function to extract ordered list of nodes from edges
  const extractOrderedNodes = (edges: Array<{from: string, to: string}>): string[] => {
    if (!edges || edges.length === 0) {
      return [];
    }

    // Start with the first "from" node (origin)
    const orderedNodes: string[] = [edges[0].from];
    
    // Add each edge's "to" node in order
    edges.forEach(edge => {
      orderedNodes.push(edge.to);
    });
    
    return orderedNodes;
  };
  
  return (
    <Box className={className} sx={{ p: 1 }}>
      <Typography variant="h5" sx={{ mb: 1, ml: 1 }}>Map Filters</Typography>

      <Grid container spacing={4}>
        {/* Location */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel id="location-label" sx={{ fontSize: '1.2rem' }}>Origin</InputLabel>
            <Select
              labelId="location-label"
              id="location-select"
              value={Origin}
              label="Location"
              onChange={handleOriginChange}
              sx={selectStyle}
            >
                <MenuItem value="1">Maadi</MenuItem>
                <MenuItem value="2">Nasr City</MenuItem>
                <MenuItem value="3">Downtown Cairo</MenuItem>
                <MenuItem value="4">New Cairo</MenuItem>
                <MenuItem value="5">Heliopolis</MenuItem>
                <MenuItem value="6">Zamalek</MenuItem>
                <MenuItem value="7">6th October City</MenuItem>
                <MenuItem value="8">Giza</MenuItem>
                <MenuItem value="9">Mohandessin</MenuItem>
                <MenuItem value="10">Dokki</MenuItem>
                <MenuItem value="11">Shubra</MenuItem>
                <MenuItem value="12">Helwan</MenuItem>
                <MenuItem value="13">New Administrative Capital</MenuItem>
                <MenuItem value="14">Al Rehab</MenuItem>
                <MenuItem value="15">Sheikh Zayed</MenuItem>
                <MenuItem value="F1">Cairo International Airport</MenuItem>
                <MenuItem value="F2">Ramses Railway Station</MenuItem>
                <MenuItem value="F3">Cairo University</MenuItem>
                <MenuItem value="F4">Al-Azhar University</MenuItem>
                <MenuItem value="F5">Egyptian Museum</MenuItem>
                <MenuItem value="F6">Cairo International Stadium</MenuItem>
                <MenuItem value="F7">Smart Village</MenuItem>
                <MenuItem value="F8">Cairo Festival City</MenuItem>
                <MenuItem value="F9">Qasr El Aini Hospital</MenuItem>
                <MenuItem value="F10">Maadi Military Hospital</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Category */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel id="category-label" sx={{ fontSize: '1.2rem' }}>Destination</InputLabel>
            <Select
              labelId="category-label"
              id="category-select"
              value={Destination}
              label="Category"
              onChange={handleDestinationChange}
              sx={selectStyle}
            >
                <MenuItem value="1">Maadi</MenuItem>
                <MenuItem value="2">Nasr City</MenuItem>
                <MenuItem value="3">Downtown Cairo</MenuItem>
                <MenuItem value="4">New Cairo</MenuItem>
                <MenuItem value="5">Heliopolis</MenuItem>
                <MenuItem value="6">Zamalek</MenuItem>
                <MenuItem value="7">6th October City</MenuItem>
                <MenuItem value="8">Giza</MenuItem>
                <MenuItem value="9">Mohandessin</MenuItem>
                <MenuItem value="10">Dokki</MenuItem>
                <MenuItem value="11">Shubra</MenuItem>
                <MenuItem value="12">Helwan</MenuItem>
                <MenuItem value="13">New Administrative Capital</MenuItem>
                <MenuItem value="14">Al Rehab</MenuItem>
                <MenuItem value="15">Sheikh Zayed</MenuItem>
                <MenuItem value="F1">Cairo International Airport</MenuItem>
                <MenuItem value="F2">Ramses Railway Station</MenuItem>
                <MenuItem value="F3">Cairo University</MenuItem>
                <MenuItem value="F4">Al-Azhar University</MenuItem>
                <MenuItem value="F5">Egyptian Museum</MenuItem>
                <MenuItem value="F6">Cairo International Stadium</MenuItem>
                <MenuItem value="F7">Smart Village</MenuItem>
                <MenuItem value="F8">Cairo Festival City</MenuItem>
                <MenuItem value="F9">Qasr El Aini Hospital</MenuItem>
                <MenuItem value="F10">Maadi Military Hospital</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Time Range */}
        <Grid item xs={12} sm={6} md={3}>
          <FormControl fullWidth>
            <InputLabel id="time-range-label" sx={{ fontSize: '1.2rem' }}>TimeOFday</InputLabel>
            <Select
              labelId="time-range-label"
              id="time-range-select"
              value={Time}
              label="Time Range"
              onChange={handleTimeChange}
              sx={selectStyle}
            >
              <MenuItem value="Morning">Morning</MenuItem>
              <MenuItem value="Afternoon">Afternoon</MenuItem>
              <MenuItem value="Evening">Evening</MenuItem>
              <MenuItem value="Night">Night</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Fetch Route Button */}
        <Grid item xs={12} sm={6} md={3} sx={{ display: 'flex', alignItems: 'center' }}>
          <Button 
            variant="contained" 
            color="primary" 
            fullWidth 
            onClick={fetchRouteData}
            sx={{ height: '3.5rem' }}
          >
            Fetch Route
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dropdown;
