import {Link} from 'react-router-dom'
import {ErrorLayout} from '../../components/ErrorLayout'

export const UnauthorizedPage = () => {
  return (
    <ErrorLayout
      code={401}
      title="Login Required"
      message="You need to be logged in to access this page. Please sign in and try again."
    >
      <Link
        to="/login"
        className="error-button primary"
        style={{marginTop: '1rem'}}
      >
        Go to Login
      </Link>
      <br />
      <br />
    </ErrorLayout>
  )
}
