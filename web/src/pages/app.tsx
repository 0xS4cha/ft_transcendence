import { RouterProvider } from "react-router-dom";
import { router } from "@/lib/router";
import { Toaster } from "@/components/ui/toast";
import { AuthProvider } from "@/context/auth/AuthContext";

export default function App() {
  return (
  <>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
    <Toaster />
  </>)
}