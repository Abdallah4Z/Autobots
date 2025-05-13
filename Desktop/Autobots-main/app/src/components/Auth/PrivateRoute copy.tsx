import { Navigate, Outlet } from 'react-router-dom'

interface PrivateRouteProps {
  isAuthenticated: boolean
  redirectPath?: string
  children?: React.ReactNode
}

export const PrivateRoute = ({
  isAuthenticated,
  redirectPath = '/login',
  children,
}: PrivateRouteProps) => {
  if (!isAuthenticated) {
    return <Navigate to={redirectPath} replace />
  }

  return children ? <>{children}</> : <Outlet />
}