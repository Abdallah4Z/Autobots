import React from 'react';
import { AppBar,Toolbar, IconButton, Typography} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';

interface AppbarProps {
  onToggle: () => void;
  isOpen?: boolean;
}

const Appbar: React.FC<AppbarProps> = ({ onToggle, isOpen = false }) => {
  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="toggle drawer"
          edge="start"
          onClick={onToggle}
          sx={{ mr: 2 }}
        >
          {isOpen ? <MenuOpenIcon /> : <MenuIcon />}
        </IconButton>
        <Typography variant="h6" noWrap>
          STS
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Appbar;