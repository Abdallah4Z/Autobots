import {Link} from 'react-router-dom'
import '../style/ErrorLayout.css'

type ErrorLayoutProps = {
  code: number
  title: string
  message: string
  children?: React.ReactNode
}

export const ErrorLayout = ({
  code,
  title,
  message,
  children,
}: ErrorLayoutProps) => {
  return (
    <div className="error-container">
      <div className="error-content">
        <div className="error-code" style={{color: '#d32f2f'}}>
          {code}
        </div>
        <h1 className="error-title">{title}</h1>
        <p className="error-message">{message}</p>
        {children}
        <div className="error-actions">
          <Link to="/" className="error-button primary">
            Return Home
          </Link>
          <Link to="/contact" className="error-button secondary">
            Contact Support
          </Link>
        </div>
      </div>
    </div>
  )
}
