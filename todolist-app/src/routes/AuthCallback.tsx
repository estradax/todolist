import { Navigate, useSearchParams } from "react-router-dom";

// save token to localstorage then redirect to dashboard
export default function AuthCallback() {
  const [searchParams, _] = useSearchParams();
  const token = searchParams.get('token');
  if (!token) {
    return <Navigate to="/login" replace />
  }

  let tokenParsed;
  try {
    tokenParsed = JSON.parse(token);
  } catch (error) {
    return <Navigate to="/login" replace />;
  }

  localStorage.setItem('access_token', tokenParsed.access_token);
  localStorage.setItem('refresh_token', tokenParsed.refresh_token);

  return <Navigate to="/" replace />;
}
