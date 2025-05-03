import React, { useState } from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Box,
  Typography,
  Grid
} from '@mui/material';

interface DropdownProps {
  className?: string;
}

const Dropdown: React.FC<DropdownProps> = ({ className }) => {
  // Set default values
  const [location, setLocation] = useState('1');
  const [category, setCategory] = useState('2');
  const [timeRange, setTimeRange] = useState('Morning');
  const [filterOption, setFilterOption] = useState('highest-rated');

  // Handlers
  const handleLocationChange = (event: SelectChangeEvent) => {
    setLocation(event.target.value);
  };

  const handleCategoryChange = (event: SelectChangeEvent) => {
    setCategory(event.target.value);
  };

  const handleTimeRangeChange = (event: SelectChangeEvent) => {
    setTimeRange(event.target.value);
  };

  const handleFilterOptionChange = (event: SelectChangeEvent) => {
    setFilterOption(event.target.value);
  };

  const selectStyle = {
    fontSize: '1.2rem',
    height: '3.5rem',
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
              value={location}
              label="Location"
              onChange={handleLocationChange}
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
              value={category}
              label="Category"
              onChange={handleCategoryChange}
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
              value={timeRange}
              label="Time Range"
              onChange={handleTimeRangeChange}
              sx={selectStyle}
            >
              <MenuItem value="Morning">Morning</MenuItem>
              <MenuItem value="Afternoon">Afternoon</MenuItem>
              <MenuItem value="Evening">Evening</MenuItem>
              <MenuItem value="Night">Night</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        {/* Filter Option */}
        
      </Grid>
    </Box>
  );
};

export default Dropdown;
