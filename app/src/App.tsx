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
import TransportationDashboard from './pages/TransportationDashboard'
import { Box } from '@mui/material'
import MapContainer from './components/MapContainer'
import MapControls from './components/MapControls'
import SearchBar from './components/SearchBar'
import SearchWithDropdown from './components/SearchWithDropdown'
import CityMap from './pages/CityMap'
import GraphMap from './pages/GraphMap'


function App() {
  const handlePlaceSelect = (place: string) => {
    console.log('Selected:', place);
    // TODO: zoom to location or dispatch action
  };
  return (

    <CityMap />

  //   <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 1000 }}>
  //   <SearchBar onSelect={handlePlaceSelect} />
  //   <Box sx={{position: 'relative', width: '100vw', height: '100vh'}}>
  //     <MapContainer />
  //     <MapControls />
  //   </Box>
  // </div>

    //   <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
    //   <Router>

    //     <Routes>
    //       <Route path="/login" element={<Login />} />
    //       <Route path="/signup" element={<Signup />} />
    //       <Route path="/contact" element={<ContactPage />} />
    //       <Route path="/400" element={<BadRequestPage />} />
    //       <Route path="/401" element={<UnauthorizedPage />} />
    //       <Route path="/403" element={<ForbiddenPage />} />
    //       <Route path="/500" element={<ServerErrorPage />} />
    //       <Route path="*" element={<NotFoundPage />} />
    //       <Route path="/" element={<TransportationDashboard />} />
    //     </Routes>
    //   </Router>
    // </GoogleOAuthProvider>
  )
}

export default App
