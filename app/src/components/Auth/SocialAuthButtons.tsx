import React from 'react';
import googleLogo from '../../assets/google.svg';
import githubLogo from '../../assets/github.svg';

interface SocialAuthButtonsProps {
  onGoogleClick: () => void;
  isLoading: boolean;
}

const SocialAuthButtons: React.FC<SocialAuthButtonsProps> = ({
  onGoogleClick,
  isLoading,
}) => (
  <div className="social-buttons-container">
    <button className="social-btn" onClick={onGoogleClick} disabled={isLoading}>
      <img src={googleLogo} alt="google" />
      Continue with Google
    </button>
    <button className="social-btn" disabled={isLoading}>
      <img src={githubLogo} alt="github" />
      Continue with GitHub
    </button>
  </div>
);

export default SocialAuthButtons;
