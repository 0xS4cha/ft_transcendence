import { ProtectedRoute } from "@/context/auth/ProtectedRoute"
export default function Me() {
    return (
        <ProtectedRoute>
            test
        </ProtectedRoute>
    )
}
