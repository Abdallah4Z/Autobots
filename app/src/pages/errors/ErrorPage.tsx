import { ErrorLayout } from '../../components/ErrorLayout';
import { useRouteError } from 'react-router-dom';

export const ErrorPage = () => {
  const error = useRouteError() as { status?: number; data?: string };
  const errorMap: Record<number, { title: string; message: string }> = {
    400: {
      title: "Bad Request",
      message: "The server couldn't understand your request."
    },
    401: {
      title: "Unauthorized",
      message: "Please log in to access this page."
    },
    403: {
      title: "Forbidden",
      message: "You don't have permission to view this content."
    },
    404: {
      title: "Not Found",
      message: "The requested page doesn't exist."
    },
    500: {
      title: "Server Error",
      message: "Something went wrong on our end."
    }
  };

  const status = error?.status || 404;
  const { title, message } = errorMap[status] || errorMap[404];

  return (
    <ErrorLayout
      code={status}
      title={title}
      message={message}
    />
  );
};