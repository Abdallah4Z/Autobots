import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useGoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import AuthHeader from '../components/Auth/AuthHeader';
import AuthInput from '../components/Auth/AuthInput';
import AuthError from '../components/Auth/AuthError';
import SocialAuthButtons from '../components/Auth/SocialAuthButtons';
import '../style/Auth.css';
const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    // Simulate login
    setTimeout(() => navigate('/dashboard'), 1000);
  };

  const loginWithGoogle = useGoogleLogin({
    onSuccess: tokenResponse => {
      try {
        const decoded = jwtDecode(tokenResponse.access_token);
        console.log(decoded);
        navigate('/dashboard');
      } catch (err) {
        setError('Google login failed. Please try again.');
      }
    },
    onError: err => {
      setError('Google login failed. Please try again.');
    }
  });

  return (
    
    <div className="login-container">
      <AuthHeader title="Log in to your account" subtitle="Welcome back! Please enter your details" />
      <AuthError message={error} />
      
      <form onSubmit={handleSubmit}>
        <AuthInput
          label="Email"
          type="email"
          id="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <AuthInput
          label="Password"
          type="password"
          id="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="login-btn">Log In</button>
      </form>

      <div className="social-login">
        <div className="social-login-divider">or</div>
        <SocialAuthButtons onGoogleClick={loginWithGoogle} isLoading={false} />
      </div>

      <div className="account-prompt">
        Don't have an account? <Link to="/signup" className="account-link">Sign up</Link>
      </div>
    </div>
  );
};

export default Login;
