import { Navigate } from "react-router-dom";
import { useAuth } from "@/context/auth/AuthContext";

interface Props {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: Props) {
    const { user, loading } = useAuth();
    if (loading) return null;
    if (!user || !user.login) return <Navigate to="/authenticate" replace />;
    return children;
}