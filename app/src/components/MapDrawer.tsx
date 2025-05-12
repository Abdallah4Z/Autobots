import React, { ReactNode, useEffect, useRef, useState } from 'react';
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
  // Add route data handler
  onFetchRoute?: (data: any) => void;
}

const MapDrawer: React.FC<MapDrawerProps> = ({
  drawerSx = {},
  drawerHeight = "150px",
  showFilters = true,
  showRoute = true,
  onToggleRoute,
  onFetchRoute
}) => {
  // State to control drawer open/close with hover
  const [isOpen, setIsOpen] = useState(false);
  // State to track if user is hovering near the top
  const [isHovering, setIsHovering] = useState(false);
  // Reference to the drawer contents
  const hoverAreaRef = useRef<HTMLDivElement>(null);
  const drawerContentRef = useRef<HTMLDivElement>(null);
  // Track if drawer is currently in transition
  const isTransitioning = useRef(false);

  // Clear all timeouts to prevent conflicting state updates
  const clearAllTimeouts = () => {
    // Removed timeout clearing as we're no longer using timeouts
  };

  // Hover enter handler - simplified to open immediately
  const handleMouseEnter = () => {
    if (isTransitioning.current) return;
    
    setIsHovering(true);
    // Open drawer immediately on hover
    isTransitioning.current = true;
    setIsOpen(true);
    setTimeout(() => {
      isTransitioning.current = false;
    }, 300);
  };

  // Hover leave handler - simplified
  const handleMouseLeave = () => {
    // Don't trigger leave during transitions
    if (isTransitioning.current) return;
    
    setIsHovering(false);
    // Close immediately when mouse leaves
    isTransitioning.current = true;
    setIsOpen(false);
    setTimeout(() => {
      isTransitioning.current = false;
    }, 250);
  };
  
  // Check if mouse is inside either hover area or drawer content
  const handleMouseMoveOutside = (e: MouseEvent) => {
    if (!isOpen) return;
    
    const hoverArea = hoverAreaRef.current;
    const drawerContent = drawerContentRef.current;
    
    if (!hoverArea || !drawerContent) return;

    const targetElement = e.target as HTMLElement;

    // Check if the mouse is over a Material UI Select's dropdown menu (Popover)
    // or any element with role="listbox" which MUI uses for menus.
    // These menus are often portaled outside the main drawer DOM structure.
    const isInOpenDropdownMenu = targetElement.closest('.MuiPopover-paper, .MuiMenu-list, [role="listbox"]');
    if (isInOpenDropdownMenu) {
      // If over a dropdown, do not close the drawer
      return;
    }
    
    // Check if mouse is inside either element with a small buffer zone
    const hoverRect = hoverArea.getBoundingClientRect();
    const drawerRect = drawerContent.getBoundingClientRect();
    
    // Add buffer zone (5px) around elements to prevent erratic behavior
    const isInHoverArea = e.clientX >= hoverRect.left - 5 &&
                          e.clientX <= hoverRect.right + 5 &&
                          e.clientY >= hoverRect.top - 5 &&
                          e.clientY <= hoverRect.bottom + 5;
    
    const isInDrawerContent = e.clientX >= drawerRect.left - 5 &&
                              e.clientX <= drawerRect.right + 5 &&
                              e.clientY >= drawerRect.top - 5 &&
                              e.clientY <= drawerRect.bottom + 5;
    
    if (!isInHoverArea && !isInDrawerContent) {
      // Only call handleMouseLeave if not in hover area, not in drawer content,
      // AND (implicitly from the check above) not in an open dropdown menu.
      handleMouseLeave();
    }
  };
  // Set up global mouse move listener to detect when mouse leaves both areas
  useEffect(() => {
    document.addEventListener('mousemove', handleMouseMoveOutside);
    return () => {
      document.removeEventListener('mousemove', handleMouseMoveOutside);
    };
  }, [isOpen]);

  return (
    <>
      {/* Hover detection area - increased height for easier detection */}
      <Box
        ref={hoverAreaRef}
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '50px', // Increased from 30px for easier hover detection
          zIndex: 1200,
          cursor: isOpen || isHovering ? 'pointer' : 'default',
        }}
        onMouseEnter={handleMouseEnter}
      />

      {/* Subtle indicator that appears on hover */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '4px', // Very thin line
          backgroundColor: 'primary.main',
          opacity: isOpen ? 0.8 : isHovering ? 0.2 : 0, // Simplified - shows on any hover
          transition: 'opacity 0.2s ease-in-out', // Faster transition
          zIndex: 1201,
          borderRadius: '0 0 4px 4px',
          pointerEvents: 'none', // So it doesn't interfere with mouse events
        }}
      />

      {/* Drawer - uses temporary variant for better animations */}
      <Drawer
        anchor="top"
        open={isOpen}
        onClose={() => setIsOpen(false)}
        variant="temporary" // Changed from persistent for smoother animations
        transitionDuration={{ enter: 200, exit: 200 }} // Faster transitions
        sx={{
          '& .MuiDrawer-paper': {
            height: drawerHeight,
            padding: 2,
            paddingTop: 2,
            borderRadius: '0 0 12px 12px',
            boxShadow: 3,
            transition: 'transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)', // Faster transition
            ...drawerSx
          },
          // Add custom backdrop styling
          '& .MuiBackdrop-root': {
            backgroundColor: 'transparent',
          }
        }}
        BackdropProps={{
          invisible: true, // Hide the backdrop
        }}
        ModalProps={{
          keepMounted: true,
        }}
      >
        <Box
          ref={drawerContentRef}
          sx={{ 
            width: '100%', 
            height: '100%',
            display: 'flex',
            flexDirection: showFilters ? 'row' : 'column',
          }}
          // onMouseLeave={handleMouseLeave} // Added to detect when mouse leaves drawer
        >
          {showFilters && (
            <>
              <Box sx={{ 
                flex: '1 1 auto', 
                display: 'flex', 
                alignItems: 'center', 
                gap: 2,
                animation: 'fadeIn 0.2s ease-in-out', // Faster animation
                '@keyframes fadeIn': {
                  '0%': {
                    opacity: 0.5,
                    transform: 'translateY(-10px)'
                  },
                  '100%': {
                    opacity: 1,
                    transform: 'translateY(0)'
                  }
                }
              }}>
                {/* Pass the route data handler to Dropdown */}
                <Dropdown onFetchRoute={onFetchRoute} />
                
                {/* Route toggle button next to dropdown */}
                {onToggleRoute && (
                  <Button 
                    variant="contained"
                    color="primary"
                    onClick={onToggleRoute}
                    className="route-toggle-btn"
                    sx={{ 
                      ml: 2,
                      marginTop: 5,
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        transform: 'scale(1.05)'
                      }
                    }}
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