// filepath: c:\Users\ahmed\Documents\GitHub\Autobots\app\src\components\SearchBar.tsx
// Author: Ahmed
import React, { useState } from 'react';
import { TextField, Autocomplete } from '@mui/material';

const mockPlaces = [
  'Cairo University',
  'Tahrir Square',
  'Giza Pyramids',
  'Alexandria Library',
  'Hurghada Marina',
  'Luxor Temple',
];

interface SearchBarProps {
  onSelect: (place: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSelect }) => {
  const [inputValue, setInputValue] = useState('');

  return (
    <Autocomplete
      freeSolo
      options={mockPlaces}
      inputValue={inputValue}
      onInputChange={(_, newInputValue) => setInputValue(newInputValue)}
      onChange={(_, value) => value && onSelect(value)}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Search places..."
          variant="outlined"
          sx={{ width: 300, backgroundColor: 'white', borderRadius: 1 }}
        />
      )}
    />
  );
};

export default SearchBar;
