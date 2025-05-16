import React from 'react';
import { Fab, Tooltip, useTheme } from '@mui/material';
import HelpIcon from '@mui/icons-material/Help';
import { useNavigate, useLocation } from 'react-router-dom';

interface FloatingHelpButtonProps {
  position?: {
    bottom?: string | number;
    right?: string | number;
    top?: string | number;
    left?: string | number;
  };
}

const FloatingHelpButton: React.FC<FloatingHelpButtonProps> = ({ 
  position = { bottom: 20, left: 20 } 
}) => {
  const navigate = useNavigate();
  const theme = useTheme();
  const location = useLocation();
  
  // Don't render the button if the current path is '/faqs'
  if (location.pathname === '/faqs') {
    return null;
  }
  
  return (
    <Tooltip title="FAQs & Help" arrow placement="right">
      <Fab
        color="secondary"
        aria-label="help"
        size="medium"
        onClick={() => navigate('/faqs')}
        sx={{
          position: 'fixed',
          zIndex: 1000,
          ...position,
          boxShadow: 3,
          '&:hover': {
            backgroundColor: theme.palette.secondary.dark,
          },
        }}
      >
        <HelpIcon />
      </Fab>
    </Tooltip>
  );
};

export default FloatingHelpButton;
