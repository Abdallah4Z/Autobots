import {ErrorLayout} from '../../components/ErrorLayout'

export const BadRequestPage = () => {
  return (
    <ErrorLayout
      code={400}
      title="Bad Request"
      message="The server couldn't understand your request. Please check the URL or parameters and try again."
    />
  )
}
