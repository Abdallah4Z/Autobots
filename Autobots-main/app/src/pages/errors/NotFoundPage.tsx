import {ErrorLayout} from '../../components/ErrorLayout'

export const NotFoundPage = () => {
  return (
    <ErrorLayout
      code={404}
      title="Page Not Found"
      message="The page you're looking for doesn't exist or has been moved."
    />
  )
}
