import React, { useState } from 'react';
import { Box } from '@mui/material';
import Appbar from './Appbar';
import Navigation from './Navigation';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [open, setOpen] = useState(false);

  const toggleDrawer = () => {
    setOpen(!open);
  };
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', overflow: 'auto' }}>
      <Appbar onToggle={toggleDrawer} isOpen={open} />
      <Navigation open={open} />
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: '100%', overflowY: 'auto' }}>
        <Box sx={{ height: '64px' }} /> {/* Toolbar spacer */}
        {children}
      </Box>
    </Box>
  );
};

export default Layout;