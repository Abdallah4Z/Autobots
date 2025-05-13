import React, {useState} from 'react'
import {Link, useNavigate} from 'react-router-dom'
import {useGoogleLogin} from '@react-oauth/google'
import {jwtDecode} from 'jwt-decode'

import AuthHeader from '../components/Auth/AuthHeader'
import AuthInput from '../components/Auth/AuthInput'
import AuthError from '../components/Auth/AuthError'
import SocialAuthButtons from '../components/Auth/SocialAuthButtons'

import '../style/Auth.css' 

const Signup: React.FC = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')

  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!name || !email || !password || !confirmPassword) {
      setError('Please fill in all fields')
      return
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    // Simulate signup
    setTimeout(() => navigate('/dashboard'), 1000)
  }

  const signupWithGoogle = useGoogleLogin({
    onSuccess: tokenResponse => {
      try {
        const decoded = jwtDecode(tokenResponse.access_token)
        console.log(decoded)
        navigate('/dashboard')
      } catch (err) {
        setError('Google signup failed. Please try again.')
      }
    },
    onError: err => {
      setError('Google signup failed. Please try again.')
    },
  })

  return (
    <div className="login-container">
      <AuthHeader
        title="Create an account"
        subtitle="Start your journey with us!"
      />
      <AuthError message={error} />

      <form onSubmit={handleSubmit}>
        <AuthInput
          label="Full Name"
          type="text"
          id="name"
          placeholder="Enter your full name"
          value={name}
          onChange={e => setName(e.target.value)}
        />
        <AuthInput
          label="Email"
          type="email"
          id="email"
          placeholder="Enter your email"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <AuthInput
          label="Password"
          type="password"
          id="password"
          placeholder="Enter your password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <AuthInput
          label="Confirm Password"
          type="password"
          id="confirmPassword"
          placeholder="Confirm your password"
          value={confirmPassword}
          onChange={e => setConfirmPassword(e.target.value)}
        />
        <button type="submit" className="login-btn">
          Sign Up
        </button>
      </form>

      <div className="social-login">
        <div className="social-login-divider">or</div>
        <SocialAuthButtons onGoogleClick={signupWithGoogle} isLoading={false} />
      </div>

      <div className="account-prompt">
        Already have an account?{' '}
        <Link to="/login" className="account-link">
          Log in
        </Link>
      </div>
    </div>
  )
}

export default Signup
