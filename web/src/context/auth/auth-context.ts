import { createContext } from "react";
import { type UserPublic } from "@/types/user";

export interface AuthContextType {
  user: UserPublic | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: () => Promise<boolean>;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | null>(null);
