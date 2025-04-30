import {ErrorLayout} from '../../components/ErrorLayout'

export const ForbiddenPage = () => {
  return (
    <ErrorLayout
      code={403}
      title="Access Denied"
      message="You don't have permission to view this page. Please check your account or contact support if you believe this is an error."
    />
  )
}
