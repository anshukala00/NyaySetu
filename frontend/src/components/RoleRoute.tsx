import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

interface RoleRouteProps {
  children: React.ReactNode;
  allowedRoles: ('CITIZEN' | 'JUDGE')[];
}

export const RoleRoute: React.FC<RoleRouteProps> = ({ children, allowedRoles }) => {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  if (!allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};
