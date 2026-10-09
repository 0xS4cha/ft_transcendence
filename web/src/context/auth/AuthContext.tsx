import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { initializeSession, logoutUser } from "@/store/reducers/userSlice";
import { AuthContext } from "@/context/auth/auth-context";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();
  const { id, email, username, picture, isAuthenticated, status, chat, isDark } = useAppSelector((state) => state.user);

  useEffect(() => {
    dispatch(initializeSession());
  }, [dispatch]);

  const user = isAuthenticated ? { id, email, username, picture, chat, isDark } : null;
  const loading = status !== "ready";

  const login = async () => {
    window.location.href = "/api/auth/login_with_42";
    return false;
  };

  const logout = async () => {
    await dispatch(logoutUser()).unwrap();
  };

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

