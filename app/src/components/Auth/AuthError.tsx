import React from 'react';

interface AuthErrorProps {
  message: string;
}

const AuthError: React.FC<AuthErrorProps> = ({ message }) => {
  if (!message) return null;
  return <div className="error-message">{message}</div>;
};

export default AuthError;
