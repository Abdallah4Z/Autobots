import React from 'react'
import {GoogleOAuthProvider} from '@react-oauth/google'
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import {BadRequestPage} from './pages/errors/BadRequestPage'
import {ForbiddenPage} from './pages/errors/ForbiddenPage'
import {NotFoundPage} from './pages/errors/NotFoundPage'
import {ServerErrorPage} from './pages/errors/ServerErrorPage'
import {UnauthorizedPage} from './pages/errors/UnauthorizedPage'
import Login from './pages/Login'
import Signup from './pages/Signup'
import ContactPage from './pages/ContactPage'
import FAQsPage from './pages/FAQsPage'
import TransportationDashboard from './pages/TransportationDashboard'
import ConditionalHelpButton from './components/ConditionalHelpButton'

function App() {
  // Set a default document title for the application
  React.useEffect(() => {
    document.title = "Transportation Network"
  }, [])

  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
      <Router>
        {/* Conditional Help Button - only appears on specific pages */}
        <ConditionalHelpButton />
        
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/faqs" element={<FAQsPage />} />
          <Route path="/400" element={<BadRequestPage />} />
          <Route path="/401" element={<UnauthorizedPage />} />
          <Route path="/403" element={<ForbiddenPage />} />
          <Route path="/500" element={<ServerErrorPage />} />
          <Route path="*" element={<NotFoundPage />} />
          <Route path="/" element={<TransportationDashboard />} />
        </Routes>
      </Router>
    </GoogleOAuthProvider>
  )
}

export default App
