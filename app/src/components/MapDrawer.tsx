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
  // Time of day for theming
  timeOfDay?: string;
  // Traffic layer toggle
  showTraffic?: boolean;
  onToggleTraffic?: () => void;
}

const MapDrawer: React.FC<MapDrawerProps> = ({
  drawerSx = {},
  drawerHeight = "150px",
  showFilters = true,
  showRoute = true,
  onToggleRoute,
  onFetchRoute,
  timeOfDay = 'morning',
  showTraffic = false,
  onToggleTraffic
}) => {
  // State to control drawer open/close with hover
  const [isOpen, setIsOpen] = useState(false);
  // State to track if user is hovering near the top
  const [isHovering, setIsHovering] = useState(false);  // Reference to the drawer contents
  const hoverAreaRef = useRef<HTMLDivElement>(null);
  const drawerContentRef = useRef<HTMLDivElement>(null);
  // Track if drawer is currently in transition
  const isTransitioning = useRef(false);
  // Store the close timeout ID
  const closeTimeoutRef = useRef<number | null>(null);

  // Determine if we're in dark mode based on timeOfDay
  const isDarkMode = timeOfDay === 'night';
  
  // Theme styles based on dark/light mode
  const themeStyles = {
    drawerPaper: {
      backgroundColor: isDarkMode ? '#242f3e' : '#ffffff',
      color: isDarkMode ? '#9ca5b3' : 'inherit',
    },
    formControl: {
      color: isDarkMode ? '#9ca5b3' : 'inherit',
    },
    indicator: {
      backgroundColor: isDarkMode ? '#38414e' : 'primary.main',
      opacity: isOpen ? 0.8 : isHovering ? 0.2 : 0,
    },
  };

  // Clear all timeouts to prevent conflicting state updates
  const clearAllTimeouts = () => {
    if (closeTimeoutRef.current !== null) {
      window.clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
  };
  // Hover enter handler - simplified to open immediately
  const handleMouseEnter = () => {
    if (isTransitioning.current) return;
    
    // Clear any pending close timeout
    clearAllTimeouts();
    
    setIsHovering(true);
    // Open drawer immediately on hover
    isTransitioning.current = true;
    setIsOpen(true);
    setTimeout(() => {
      isTransitioning.current = false;
    }, 300);
  };

  // Hover leave handler - with 3-second delay
  const handleMouseLeave = () => {
    // Don't trigger leave during transitions
    if (isTransitioning.current) return;
    
    setIsHovering(false);
    
    // Set a 3-second delay before closing
    clearAllTimeouts(); // Clear any existing timeout
    closeTimeoutRef.current = window.setTimeout(() => {
      isTransitioning.current = true;
      setIsOpen(false);
      setTimeout(() => {
        isTransitioning.current = false;
      }, 250);
    }, 1000); // 1.5-second delay
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
      clearAllTimeouts(); // Clear any close timeout
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
    
    if (isInHoverArea || isInDrawerContent) {
      // If mouse re-enters the area, cancel any pending close
      clearAllTimeouts();
    } else if (!isInHoverArea && !isInDrawerContent) {
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
      clearAllTimeouts(); // Clean up timeouts when component unmounts
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
          backgroundColor: themeStyles.indicator.backgroundColor,
          opacity: themeStyles.indicator.opacity, // Simplified - shows on any hover
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
            ...drawerSx,
            ...themeStyles.drawerPaper
          },          // Add custom backdrop styling
          '& .MuiBackdrop-root': {
            backgroundColor: 'transparent',
          },
          // Apply dark mode styles to form controls when in night mode
          ...(isDarkMode && {
            '& .MuiInputLabel-root': {
              color: '#9ca5b3',
            },
            '& .MuiOutlinedInput-root': {
              color: '#9ca5b3',
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: '#38414e',
              },
              '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: '#515c6d',
              },
              '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: '#6b7a8f',
              }
            },
            '& .MuiSelect-icon': {
              color: '#9ca5b3',
            },
            '& .MuiMenuItem-root': {
              color: '#9ca5b3',
            },
            '& .MuiSelect-select': {
              color: '#9ca5b3',
            }
          })
        }}
        BackdropProps={{
          invisible: true, // Hide the backdrop
        }}
        ModalProps={{
          keepMounted: true,
        }}
      >
        <Box
          ref={drawerContentRef}          sx={{ 
            width: '100%', 
            height: '100%',
            display: 'flex',
            flexDirection: showFilters ? 'row' : 'column',
            // Add dark mode theming to container elements
            ...(isDarkMode && {
              '& .MuiTypography-root': {
                color: '#9ca5b3',
              }
            })
          }}
          // onMouseLeave={handleMouseLeave} // Added to detect when mouse leaves drawer
        >
          {showFilters && (
            <>              <Box sx={{ 
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
                {/* Pass all required props to Dropdown */}
                <Dropdown 
                  onFetchRoute={onFetchRoute} 
                  currentRouteData={{ timeOfDay }}
                  showRoute={showRoute}
                  onToggleRoute={onToggleRoute}
                  showTraffic={showTraffic}
                  onToggleTraffic={onToggleTraffic}
                />
              </Box>
            </>
          )}
        </Box>
      </Drawer>
    </>
  );
};

export default MapDrawer;