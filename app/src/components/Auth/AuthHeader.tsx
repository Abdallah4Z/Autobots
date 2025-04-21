import React from 'react';

interface AuthHeaderProps {
  title: string;
  subtitle: string;
}

const AuthHeader: React.FC<AuthHeaderProps> = ({ title, subtitle }) => (
  <div className="auth-header">
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
);

export default AuthHeader;
