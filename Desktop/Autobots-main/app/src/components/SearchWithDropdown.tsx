import React, { useState } from 'react';
import { TextField, Autocomplete, Typography, ListItemIcon, Box } from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';

const recentSearches = [
  'Maadi', 'Nasr City', 'Downtown Cairo', 'New Cairo', 'Heliopolis', 
  'Zamalek', '6th October City', 'Giza', 'Mohandessin', 'Dokki', 
  'Shubra', 'Helwan', 'New Administrative Capital', 'Al Rehab', 'Sheikh Zayed', 
  'Cairo International Airport', 'Ramses Railway Station', 'Cairo University', 
  'Al-Azhar University', 'Egyptian Museum', 'Cairo International Stadium', 
  'Smart Village', 'Cairo Festival City', 'Qasr El Aini Hospital', 'Maadi Military Hospital'
];

interface SearchWithDropdownProps {
  label: string;
}

const SearchWithDropdown: React.FC<SearchWithDropdownProps> = ({ label }) => {
  const [inputValue, setInputValue] = useState('');

  return (
    <Box sx={{ width: '100%', display: 'flex', justifyContent: 'flex-start' }}>
      <Autocomplete
        freeSolo
        options={recentSearches}
        inputValue={inputValue}
        onInputChange={(e, value) => setInputValue(value)}
        renderInput={(params) => (
          <TextField
            {...params}
            label={label}
            placeholder="البحث في الخرائط"
            variant="standard"
            sx={{
              width: '350px', // Ensure the input takes up the full width
              '& .MuiInputLabel-root': { textAlign: 'left' }, // Align label to the left
              '& .MuiInputBase-root': { textAlign: 'left' }, // Align input text to the left
              '& .MuiFormLabel-root': { left: 0 }, // Adjust label position
            }}
            InputProps={{
              ...params.InputProps,
              startAdornment: <LocationOnIcon sx={{ mr: 1 }} />,
            }}
          />
        )}
        renderOption={(props, option) => (
          <li {...props}>
            <ListItemIcon>
              <LocationOnIcon fontSize="small" />
            </ListItemIcon>
            <Typography>{option}</Typography>
          </li>
        )}
      />
    </Box>
  );
};

export default SearchWithDropdown;
