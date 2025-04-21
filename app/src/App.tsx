import { GoogleOAuthProvider } from "@react-oauth/google"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { BadRequestPage } from "./pages/errors/BadRequestPage"
import { ForbiddenPage } from "./pages/errors/ForbiddenPage"
import { NotFoundPage } from "./pages/errors/NotFoundPage"
import { ServerErrorPage } from "./pages/errors/ServerErrorPage"
import { UnauthorizedPage } from "./pages/errors/UnauthorizedPage"
import Login from "./pages/Login"
import Signup from "./pages/Signup"
import ContactPage from "./pages/ContactPage"

function App() {

  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
    <Router>

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/contact" element={<ContactPage />} />


        {/* Errors Routes */}
        <Route path="/400" element={<BadRequestPage />} />
        <Route path="/401" element={<UnauthorizedPage />} />
        <Route path="/403" element={<ForbiddenPage />} />
        <Route path="/500" element={<ServerErrorPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  </GoogleOAuthProvider>
  )
}

export default App
