import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/auth';

export default function Unauthenticated({ children }: { children: React.ReactNode }) {
  const { loading, error } = useAuth();

  if (loading) {
    return <p>Loading...</p>;
  }

  if (!error) {
    return <Navigate to="/" replace />;
  }

  return children;
}
