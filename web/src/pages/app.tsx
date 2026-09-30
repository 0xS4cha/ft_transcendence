import { useEffect } from "react";
import { RouterProvider } from "react-router-dom";
import { router } from "@/lib/router";
import { Toaster } from "@/components/ui/toast";
import { AuthProvider } from "@/context/auth/AuthContext";
import { useWSConnection } from "@/lib/websocket"
import { useAppSelector } from "@/store/hooks";

export default function App() {
  const { isActive, startConnection } = useWSConnection("/api/websocket/ws");
  const { isAuthenticated } = useAppSelector(state => state.user);

  useEffect(() => {
    if (!isActive && isAuthenticated) {
      startConnection();
    }
  })
  return (
  <>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
    <Toaster />
  </>)
}