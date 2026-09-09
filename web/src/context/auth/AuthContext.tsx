import { createContext, useContext, useState, useEffect } from "react";
import { toast } from "@/components/ui/toast";
import { useAppSelector } from '@/store/hooks';
import { type User } from "@/types/user";
import { useDispatch } from "react-redux";
import { setEmail, setId, setLogin } from "@/store/reducers/userSlice";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const user = useAppSelector((state) => state.user);
//   const [loading, setLoading] = useState(true);
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    const checkUser = async () => {
      try {
        const response = await fetch("/api/auth/login/users/me", { method: "GET" });

        if (!response.ok) {
            // setLoading(true);
          toast.add({
            type: "error",
            title: "Failed to fetch you",
          });
          return;
        }

        const result = await response.json();
        dispatch(setEmail(result.email));
        dispatch(setId(result.id));
        dispatch(setLogin(true));
        setLoading(false);
      } catch (error) {
        // setLoading(true);
        toast.add({
          type: "error",
          title: `Fetch failed: ${error}`,
        });
      }
    };

    checkUser();
  }, []);

  const login = async () => {
    window.location.href=import.meta.env.VITE_AUTH42;
    return false;
  };

  return (
    <AuthContext.Provider value={{ user, loading, login }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}