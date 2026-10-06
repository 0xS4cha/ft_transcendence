import { createContext, useContext, useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { initializeSession, logoutUser } from "@/store/reducers/userSlice";
import { type UserPublic } from "@/types/user";

interface AuthContextType {
  user: UserPublic | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: () => Promise<boolean>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();
  const { id, email, username, picture, isAuthenticated, status, chat, isDark } = useAppSelector((state) => state.user);

  useEffect(() => {
    dispatch(initializeSession());
  }, [dispatch]);

  const user = isAuthenticated ? { id, email, username, picture, chat, isDark } : null;
  const loading = status !== "ready";

  const login = async () => {
    window.location.href = import.meta.env.VITE_AUTH42;
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

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
