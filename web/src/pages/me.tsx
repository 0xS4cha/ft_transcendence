
import { ProtectedRoute } from "@/context/auth/ProtectedRoute";
import { ProfileCard } from "@/components/profile/card"
import { FriendsCard } from "@/components/friends/card"
import { RequestsCard } from "@/components/friends/requests"

export default function Me() {
    return (
        <ProtectedRoute>
            <div className="relative w-full min-h-screen">
                <div className="flex flex-col gap-4 lg:gap-6">
                    <ProfileCard/>
                    <RequestsCard />
                    <FriendsCard />
                </div>
            </div>
        </ProtectedRoute>
    );
}
