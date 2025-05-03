import React, { ReactNode } from 'react';
import { Drawer, Box, Typography, Divider, Button } from '@mui/material';
import Dropdown from './Dropdown';

interface MapDrawerProps {
  // Content to be displayed in the drawer
  children?: ReactNode;
  // Title for the drawer
  title?: string;
  // Optional custom styling for the drawer
  drawerSx?: object;
  // Optional drawer height
  drawerHeight?: string | number;
  // Option to show filter dropdown
  showFilters?: boolean;
  // New props for route toggle
  showRoute?: boolean;
  onToggleRoute?: () => void;
}

const MapDrawer: React.FC<MapDrawerProps> = ({
  drawerSx = {},
  drawerHeight = "150px",
  showFilters = true,
  showRoute = true,
  onToggleRoute
}) => {
  // State to control drawer open/close
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [isHovering, setIsHovering] = React.useState(false);

  // Drawer hover handlers
  const handleMouseEnter = () => {
    setDrawerOpen(true);
    setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setDrawerOpen(false);
    setIsHovering(false);
  };

  return (
    <>
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '150px', // Small height for hover detection
          zIndex: 1200,
          cursor: 'pointer',
        }}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={() => setIsHovering(false)}
      />

      {/* Subtle indicator that appears on hover */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '5px', // Very thin line
          backgroundColor: 'primary.main',
          opacity: isHovering ? 0.8 : 0.1, // Nearly invisible when not hovering
          transition: 'opacity 0.3s ease',
          zIndex: 1201,
          borderRadius: '0 0 4px 4px',
        }}
      />

      {/* Drawer */}
      <Drawer
        anchor="top"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        variant="persistent"
        sx={{
          '& .MuiDrawer-paper': {
            height: drawerHeight,
            padding: 2,
            paddingTop: 2, // Extra space at top
            borderRadius: '0 0 8px 8px',
            boxShadow: 3,
            ...drawerSx
          }
        }}
        ModalProps={{
          keepMounted: true,
        }}
      >
        <Box
          sx={{ 
            width: '100%', 
            height: '100%',
            display: 'flex',
            flexDirection: showFilters ? 'row' : 'column'
          }}
          onMouseLeave={handleMouseLeave}
        >
          {/* Removed the route toggle button from here */}
          
          {showFilters && (
            <>
              <Box sx={{ flex: '1 1 auto', display: 'flex', alignItems: 'center', gap: 2 }}>
                <Dropdown />
                
                {/* Route toggle button next to dropdown */}
                {onToggleRoute && (
                  <Button 
                    variant="contained"
                    color="primary"
                    onClick={onToggleRoute}
                    className="route-toggle-btn"
                    sx={{ ml: 2 ,marginTop:5}}
                  >
                    {showRoute ? 'Hide Route' : 'Show Route'}
                  </Button>
                )}
              </Box>
            </>
          )}
        </Box>
      </Drawer>
    </>
  );
};

export default MapDrawer;