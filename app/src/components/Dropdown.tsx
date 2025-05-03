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
  
      // Try to fetch with JSON headers
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries([...response.headers]));
      
      // Get the response text first
      const responseText = await response.text();
      console.log('Raw response (first 500 chars):', responseText.substring(0, 500));
      
      // Check for server error status
      if (response.status >= 500) {
        console.error('Server error response:', responseText);
        alert(`Server error (${response.status}). Check your backend logs for details.`);
        
        // Optional: Try extracting error message if it's in JSON format
        try {
          if (responseText.includes('{') && responseText.includes('}')) {
            const errorMatch = responseText.match(/\{.*"error":\s*"([^"]+)".*\}/);
            if (errorMatch && errorMatch[1]) {
              console.log('Extracted error message:', errorMatch[1]);
            }
          }
        } catch (e) {
          // Silent catch - just for extra error info
        }
        
        return null;
      }
      
      // For non-500 errors, still try to process
      if (!response.ok) {
        throw new Error(`Failed to fetch route: ${response.status} ${response.statusText}`);
      }
      
      // Try to parse as JSON
      let data;
      try {
        data = JSON.parse(responseText);
        console.log('Successfully parsed route data:', data);
      } catch (jsonError) {
        console.error('Failed to parse JSON:', jsonError);
        
        // Try extracting JSON from HTML if needed
        if (responseText.includes('{') && responseText.includes('edges')) {
          try {
            // Look for our specific JSON format with edges, total_distance and total_time
            const jsonMatch = responseText.match(/\{\s*"edges"\s*:\s*\[\s*\{.*?\}\s*\]\s*,\s*"total_distance"\s*:\s*[\d\.]+\s*,\s*"total_time"\s*:\s*[\d\.]+\s*\}/s);
            if (jsonMatch && jsonMatch[0]) {
              const jsonContent = jsonMatch[0];
              console.log('Found JSON content in response:', jsonContent);
              data = JSON.parse(jsonContent);
              console.log('Successfully extracted embedded JSON:', data);
            } else {
              throw new Error('Could not extract JSON from response');
            }
          } catch (extractError) {
            console.error('Failed to extract JSON:', extractError);
            throw new Error('Response is not valid JSON and extraction failed');
          }
        } else {
          throw new Error('Response is not valid JSON');
        }
      }
      
      // Optional: Pass route data to parent
      if (onFetchRoute && data) {
        onFetchRoute(data);
      }
  
      return data;
    } catch (error) {
      console.error('Error fetching route:', error);
      alert(`Failed to fetch route data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      return null;
    }
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
