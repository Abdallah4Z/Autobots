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
// Import icons for buttons
import MapIcon from '@mui/icons-material/Map';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import TrafficIcon from '@mui/icons-material/Traffic';
import FilterListIcon from '@mui/icons-material/FilterList';

interface DropdownProps {
  className?: string;
  onValuesChange?: (values: {
    origin: string;
    destination: string;
    timeOfDay: string;
    route: string;
    lines: string;
    algo: string;
    Emergency: string;
  }) => void;
  onFetchRoute?: (data?: any) => void;
  currentRouteData?: any;  // To store current route data if available
  // Added props for route toggle
  showRoute?: boolean;
  onToggleRoute?: () => void;
  // Added props for traffic toggle
  showTraffic?: boolean;
  onToggleTraffic?: () => void;
}

const Dropdown: React.FC<DropdownProps> = ({ 
  className,
  onValuesChange,
  onFetchRoute,
  currentRouteData,
  // Added route toggle props
  showRoute = true,
  onToggleRoute,
  // Added traffic toggle props
  showTraffic = false,
  onToggleTraffic
}) => {
  // Set default values
  const [Origin, setOrigin] = useState('1');
  const [Destination, setDestination] = useState('2');
  const [Time, setTime] = useState('morning');
  const [Routes, setRoute] = useState('MST');
  const [Lines, setLine] = useState('Roads');
  const [Em, setEm] = useState('None');
  // Cached route data for redrawing with different styles
  const [cachedRouteData, setCachedRouteData] = useState<any>(null);
  const [Algo, setAlgo] = useState('ASTAR');
  // Notify parent component when values change
  useEffect(() => {
    if (onValuesChange) {
      onValuesChange({
        origin: Origin,
        destination: Destination,
        timeOfDay: Time,
        route: Routes,
        lines: Lines,
        algo: Algo,
        Emergency:Em
      });
    }
  }, [Origin, Destination, Time, Routes, Lines, Algo,Em,onValuesChange]);

  // Update cached route data when received from parent
  useEffect(() => {
    if (currentRouteData) {
      setCachedRouteData(currentRouteData);
    }
  }, [currentRouteData]);

  // Handlers
  const handleOriginChange = (event: SelectChangeEvent) => {
    setOrigin(event.target.value);
  };

  const handleDestinationChange = (event: SelectChangeEvent) => {
    setDestination(event.target.value);
  };
  const handleEmergencyChange = (event: SelectChangeEvent) => {
    setEm(event.target.value);
  };  const handleTimeChange = (event: SelectChangeEvent) => {
    const newTimeOfDay = event.target.value;
    setTime(newTimeOfDay);
    
    // If we have cached route data, update the visualization immediately with the new time of day
    if (cachedRouteData && onFetchRoute) {
      const updatedRouteData = {
        ...cachedRouteData,
        timeOfDay: newTimeOfDay
      };
      
      // Pass the updated route data to update the map theme
      onFetchRoute(updatedRouteData);
    }
  };
  
  const handleRouteChange = (event: SelectChangeEvent) => {
    setRoute(event.target.value);
  };
  const handleAlgoChange = (event: SelectChangeEvent) => {
    setAlgo(event.target.value);
  }
  const handleLineChange = (event: SelectChangeEvent) => {
    const newLineStyle = event.target.value;
    setLine(newLineStyle);
    
    // If we have cached route data, update the visualization immediately
    if (cachedRouteData && onFetchRoute) {
      // Add the line style to the route data
      const updatedRouteData = {
        ...cachedRouteData,
        lineStyle: newLineStyle
      };
      
      // Pass the updated route data back to parent component to redraw
      onFetchRoute(updatedRouteData);
    }
  };
  const selectStyle = {
    fontSize: '1.2rem',
    height: '3.5rem',
    width: '130px',        // Fixed width for all dropdowns
    "& .MuiSelect-select": {
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  };
    // Controls the dropdown menu size
  const menuProps = {
    PaperProps: {
      style: {
        maxHeight: 300,
        overflow: 'auto',
        width: '220px',  // Match the dropdown width
      },
    },
    // Ensure proper text handling in the dropdown
    SelectDisplayProps: {
      style: {
        overflow: 'hidden',
        textOverflow: 'ellipsis'
      }
    }
  };
  
  const fetchRouteData = async () => {
    try {
      console.log('Fetching route data with parameters:', {
        origin: Origin,
        destination: Destination,
        timeOfDay: Time,
        routeType: Routes,
        lineStyle: Lines,
        algorithm: Algo,
        emergency: Em
      });
      
      // Convert time period to lowercase to match backend expectations
      const lowerCasePeriod = Time.toLowerCase();
      
      let url, response;

      // Use different API endpoints based on the route type and emergency status
      
      if (Em !== 'None') {
        // For emergency routes, use the emergency API
        const emType = Em.toLowerCase(); // Convert to lowercase for the API
        url = `http://localhost:5000/emergency/route?origin=${encodeURIComponent(Origin)}&dest=${encodeURIComponent(Destination)}&type=${emType}`;
        console.log('Emergency route request URL:', url);
        
        response = await fetch(url, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries([...response.headers]));
        
        if (!response.ok) {
          throw new Error(`Failed to fetch emergency route: ${response.status} ${response.statusText}`);
        }
        
        // Get the response text and parse it
        const responseText = await response.text();
        console.log('Raw emergency response (first 500 chars):', responseText.substring(0, 500));
        
        // Parse the JSON response
        let data;
        try {
          data = JSON.parse(responseText);
          console.log('Successfully parsed emergency route data:', data);
        } catch (jsonError) {
          console.error('Failed to parse JSON:', jsonError);
          throw new Error('Response is not valid JSON');
        }
        
        // Process the emergency route data
        if (data && data.edges && Array.isArray(data.edges)) {          const orderedNodes = extractOrderedNodes(data.edges);
          console.log('Ordered emergency route nodes:', orderedNodes);
          
          // Extract the estimated time properly from the API response
          const estimatedTime = data.estimated_response_time || data.total_time || data.estimated_time || data.time;

          console.log('Emergency response estimated time:', estimatedTime);
          
          const routeInfo = {
            nodes: orderedNodes,
            totalDistance: data.total_distance,
            totalTime: estimatedTime,
            edges: data.edges,
            lineStyle: Lines,
            isEmergencyRoute: true,
            emergencyType: Em
          };
          
          console.log('Processed emergency route information:', routeInfo);
          
          // Cache the route data for future style changes
          setCachedRouteData(routeInfo);
          
          // Pass the processed route data to parent component
          if (onFetchRoute) {
            onFetchRoute(routeInfo);
          }
          
          return routeInfo;
        } else {
          throw new Error('Invalid emergency route data format');
        }
      } else if (Routes === 'Public') {
        // For public transportation, use the transportation API
        url = `/api/transportation/itinerary?origin=${encodeURIComponent(Origin)}&dest=${encodeURIComponent(Destination)}`;
        console.log('Public transportation request URL:', url);
        
        response = await fetch(url, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        });

        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries([...response.headers]));
        
        if (!response.ok) {
          throw new Error(`Failed to fetch public transportation route: ${response.status} ${response.statusText}`);
        }

        // Get the response text and parse it
        const responseText = await response.text();
        console.log('Raw response (first 500 chars):', responseText.substring(0, 500));

        // Parse the JSON response
        let data;
        try {
          data = JSON.parse(responseText);
          console.log('Successfully parsed public transportation data:', data);
        } catch (jsonError) {
          console.error('Failed to parse JSON:', jsonError);
          throw new Error('Response is not valid JSON');
        }

        // Public transportation API returns a different format, so we need to convert it
        if (data && data.steps && Array.isArray(data.steps)) {
          // Extract route information from the steps
          const edges = [];
          const orderedNodes = [];
          let totalDistance = 0;
          let totalTime = 0; // Estimate based on stops
          
          // Process each leg of the journey
          data.steps.forEach((step, index) => {
            // Add the path nodes from each step
            if (step.path && Array.isArray(step.path)) {
              // First node of first step is already the origin
              if (index === 0) {
                orderedNodes.push(step.path[0]);
              }
              
              // Add the remaining nodes and create edges
              for (let i = (index === 0 ? 1 : 0); i < step.path.length; i++) {
                const from = step.path[i - 1];
                const to = step.path[i];
                orderedNodes.push(to);
                edges.push({ from, to, mode: step.mode, route: step.route });
              }
              
              // Estimate distance and time based on number of stops
              // (This is a simplification; real data would be better)
              totalDistance += step.stops * 2; // Rough estimate: 2km per stop
              totalTime += step.stops * 5;     // Rough estimate: 5 minutes per stop
            }
          });
          
          // Create route information object
          const routeInfo = {
            nodes: orderedNodes,
            totalDistance: totalDistance,
            totalTime: totalTime,
            edges: edges,
            lineStyle: Lines,
            isPublicTransport: true,
            steps: data.steps // Keep original steps for detailed display
          };
          
          console.log('Processed public transport information:', routeInfo);
          
          // Cache the route data for future style changes
          setCachedRouteData(routeInfo);
          
          // Pass the processed route data to parent component
          if (onFetchRoute) {
            onFetchRoute(routeInfo);
          }
          
          return routeInfo;
        } else {
          throw new Error('Invalid public transport data format');
        }
      } else if (Routes === 'MST') {
        // For MST routes, use the infrastructure API
        url = `/api/planner/period/${encodeURIComponent(lowerCasePeriod)}`;
        console.log('MST infrastructure request URL:', url);
        
        response = await fetch(url, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries([...response.headers]));
        
        if (!response.ok) {
          throw new Error(`Failed to fetch MST route: ${response.status} ${response.statusText}`);
        }
        
        // Get the response text and parse it
        const responseText = await response.text();
        console.log('Raw response (first 500 chars):', responseText.substring(0, 500));
        
        // Parse the JSON response
        let data;
        try {
          data = JSON.parse(responseText);
          console.log('Successfully parsed MST data:', data);
        } catch (jsonError) {
          console.error('Failed to parse JSON:', jsonError);
          throw new Error('Response is not valid JSON');
        }

        // For MST, we just directly use the edges from the JSON response
        if (data && data.edges && Array.isArray(data.edges)) {
          // Extract all unique nodes from the edges
          const uniqueNodes = new Set<string>();
          data.edges.forEach(edge => {
            uniqueNodes.add(edge.from);
            uniqueNodes.add(edge.to);
          });
          
          // Additional route information with line style preference
          const routeInfo = {
            // All unique nodes in the MST
            nodes: Array.from(uniqueNodes),
            totalDistance: data.total_distance || 0,
            totalTime: data.total_time || 0,
            // Pass the raw edges directly without modification
            edges: data.edges,
            lineStyle: Lines,
            // Special flag to indicate this is an MST, not a path
            isMST: true,
            // Include raw data to ensure we're using exactly what came from the API
            rawData: data
          };
          
          console.log('Processed MST information:', routeInfo);
          
          // Cache the route data for future style changes
          setCachedRouteData(routeInfo);
          
          // Pass the processed route data to parent component
          if (onFetchRoute) {
            onFetchRoute(routeInfo);
          }
          
          return routeInfo;
        } else {
          throw new Error('Invalid MST data format: missing edges array');
        }
      } else {
        // For road-based routes (Private, Emergency), use the flow API with the selected algorithm
        // Map the dropdown value to the correct backend API endpoint
        let algorithmEndpoint;
        if (Algo === 'dijkstra') {
          algorithmEndpoint = 'dijkstra';  // Map "DJ" to "dijkstra" for backend API
        } else {
          algorithmEndpoint = Algo.toLowerCase();  // For other algorithms like "ASTAR"
        }
        
        console.log(`Using algorithm: ${Algo} (endpoint: ${algorithmEndpoint})`);
        
        // Use the full backend URL instead of relative URL
        url = `http://127.0.0.1:5000/flow/route/${algorithmEndpoint}?origin=${encodeURIComponent(Origin)}&dest=${encodeURIComponent(Destination)}&period=${encodeURIComponent(lowerCasePeriod)}`;
        console.log('Road route request URL:', url);
      
        response = await fetch(url, {
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
          
          // Additional route information with line style preference
          const routeInfo = {
            nodes: orderedNodes,
            totalDistance: data.total_distance,
            totalTime: data.total_time,
            edges: data.edges,
            lineStyle: Lines,
            isPublicTransport: false
          };
          
          console.log('Processed route information with line style:', routeInfo);
          
          // Cache the route data for future style changes
          setCachedRouteData(routeInfo);
          
          // Pass the processed route data to parent component
          if (onFetchRoute) {
            onFetchRoute(routeInfo);
          }
          
          return routeInfo;
        } else {
          throw new Error('Invalid route data format: missing edges array');
        }
      }
    } catch (error) {
      console.error('Error fetching route:', error);
      alert(`Failed to fetch route data: ${error instanceof Error ? error.message : 'Unknown error'}`);
      return null;
    }
  };

  // Helper function to extract ordered list of nodes from edges
  const extractOrderedNodes = (edges: Array<{ from: string; to: string }>): string[] => {
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
      <Typography variant="h5" sx={{ mb: 1, ml: 1, display: 'flex', alignItems: 'center' }}>
        <FilterListIcon sx={{ mr: 1 }} /> Map Filters
      </Typography>

      <Grid container spacing={2}>
        {/* Location */}
        <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="location-label" sx={{ fontSize: '1.2rem' }}>Origin</InputLabel>            <Select
              labelId="location-label"
              id="location-select"
              value={Origin}
              label="Location"
              onChange={handleOriginChange}
              sx={selectStyle}
              MenuProps={menuProps}
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
        <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="category-label" sx={{ fontSize: '1.2rem' }}>Destination</InputLabel>            <Select
              labelId="category-label"
              id="category-select"
              value={Destination}
              label="Category"
              onChange={handleDestinationChange}
              sx={selectStyle}
              MenuProps={menuProps}
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
        <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="time-range-label" sx={{ fontSize: '1.2rem' }}>TimeOFday</InputLabel>            <Select
              labelId="time-range-label"
              id="time-range-select"
              value={Time}
              label="Time Range"
              onChange={handleTimeChange}
              sx={selectStyle}
              MenuProps={menuProps}
            >
              <MenuItem value="morning">morning</MenuItem>
              <MenuItem value="afternoon">afternoon</MenuItem>
              <MenuItem value="evening">evening</MenuItem>
              <MenuItem value="night">night</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="Route-label" sx={{ fontSize: '1.2rem' }}>Route</InputLabel>            <Select
              labelId="Route-label"
              id="Route-select"
              value={Routes}
              label="Route"
              onChange={handleRouteChange}
              sx={selectStyle}
              MenuProps={menuProps}
            >
              <MenuItem value="MST">MST</MenuItem>
              <MenuItem value="Private">Private</MenuItem>
              <MenuItem value="Public">Public</MenuItem>
              <MenuItem value="Emergency">Emergency</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="Line-label" sx={{ fontSize: '1.2rem' }}>Line</InputLabel>            <Select
              labelId="Line-label"
              id="Line-select"
              value={Lines}
              label="Line"
              onChange={handleLineChange}
              sx={selectStyle}
              MenuProps={menuProps}
            >
              <MenuItem value="StraightLine">
                Straight Line 
                <Typography variant="caption" display="block" color="text.secondary">
                  Draw direct lines
                </Typography>
              </MenuItem>
              <MenuItem value="Roads">
                Roads 
                <Typography variant="caption" display="block" color="text.secondary">
                  Follow actual road
                </Typography>
              </MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="Algo-label" sx={{ fontSize: '1.2rem' }}>Algorithm</InputLabel>            <Select
              labelId="Algo-label"
              id="Algo-select"
              value={Algo}
              label="Algo"
              onChange={handleAlgoChange}
              sx={selectStyle}
              MenuProps={menuProps}
            >
              <MenuItem value="ASTAR">ASTAR</MenuItem>
              <MenuItem value="dijkstra">dijkstra</MenuItem>
              
            </Select>
          </FormControl>
               </Grid>
               <Grid item xs={18} sm={8} md={4}>
          <FormControl fullWidth>
            <InputLabel id="EM-label" sx={{ fontSize: '1.2rem' }}>Emergency</InputLabel>            <Select
              labelId="EM-label"
              id="EM-select"
              value={Em}
              label="EM"
              onChange={handleEmergencyChange}
              sx={selectStyle}
              MenuProps={menuProps}
            >
              <MenuItem value="None">None</MenuItem>
              <MenuItem value="Ambulance">Ambulance</MenuItem>
              <MenuItem value="police">police</MenuItem>
              <MenuItem value="fire_truck">fire_truck</MenuItem>
            </Select>
          </FormControl>
               </Grid>
        {/* Fetch Route Button */}
        <Grid item xs={18} sm={8} md={4} sx={{ display: 'flex', alignItems: 'center' }}>          <Button 
            variant="contained" 
            color="primary" 
            fullWidth 
            onClick={fetchRouteData}
            startIcon={<MapIcon />}
            sx={{ height: '3.5rem' }}
          >
            Fetch Route
          </Button>
        </Grid>

        {/* Route toggle button */}
        {onToggleRoute && (
          <Grid item xs={18} sm={8} md={4} sx={{ display: 'flex', alignItems: 'center' }}>            <Button 
              variant="contained"
              color="primary"
              onClick={onToggleRoute}
              className="route-toggle-btn"
              fullWidth
              startIcon={showRoute ? <VisibilityOffIcon /> : <VisibilityIcon />}
              sx={{ 
                height: '3.5rem',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'scale(1.05)'
                },
                ...(Time === 'night' && {
                  backgroundColor: '#38414e',
                  color: '#9ca5b3',
                  '&:hover': {
                    backgroundColor: '#515c6d',
                    transform: 'scale(1.05)'
                  }
                })
              }}
            >
              {showRoute ? 'Hide Route' : 'Show Route'}
            </Button>
          </Grid>
        )}

        {/* Traffic toggle button */}
        {onToggleTraffic && (
          <Grid item xs={18} sm={8} md={4} sx={{ display: 'flex', alignItems: 'center' }}>            <Button 
              variant="contained"
              color={showTraffic ? "secondary" : "primary"}
              onClick={onToggleTraffic}
              className="traffic-toggle-btn"
              fullWidth
              startIcon={<TrafficIcon />}
              sx={{ 
                height: '3.5rem',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'scale(1.05)'
                },
                ...(Time === 'night' && {
                  backgroundColor: showTraffic ? '#ac4646' : '#38414e',
                })
              }}
            >
              {showTraffic ? 'Hide Traffic' : 'Show Traffic'}
            </Button>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default Dropdown;
