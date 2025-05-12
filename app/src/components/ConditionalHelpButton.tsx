import React from 'react';
import { useLocation } from 'react-router-dom';
import FloatingHelpButton from './FloatingHelpButton';

const ConditionalHelpButton: React.FC = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  
  // Only show button on the home page (map page) and not on FAQs or other pages
  const showOnPaths = ['/', '/dashboard']; // Add any paths where you want the button to appear
  const shouldShowButton = showOnPaths.includes(currentPath);
  
  return shouldShowButton ? <FloatingHelpButton /> : null;
};

export default ConditionalHelpButton;
