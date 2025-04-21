// Navigation.tsx
import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import TurnSharpRightRoundedIcon from '@mui/icons-material/TurnSharpRightRounded';
import { useNavigate } from 'react-router-dom';

interface NavigationProps {
  open: boolean;
}

const navItems = [
  { text: 'Home', icon: <HomeRoundedIcon />, path: '/home' },
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Network', icon: <TurnSharpRightRoundedIcon />, path: '/network' },
  
];

const Navigation: React.FC<NavigationProps> = ({ open }) => {
  const drawerWidth = open ? 240 : 65; // Smaller width when closed
  const navigate = useNavigate();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: 'border-box',
          overflowX: 'hidden',
          transition: 'width 0.3s ease-in-out',
        },
      }}
    >
      <Toolbar />
      <List>
        {navItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              onClick={() => navigate(item.path)}
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.text} 
                sx={{ 
                  opacity: open ? 1 : 0,
                  display: open ? 'block' : 'none'
                }} 
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Navigation;