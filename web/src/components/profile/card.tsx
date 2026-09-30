import { Card, CardContent } from "@/components/ui/card";
import { useAppSelector } from '@/store/hooks';
import { Avatar, AvatarImage } from "@/components/ui/avatar"

export function ProfileCard() {
    const { username, picture, email, id } = useAppSelector(state => state.user);

    return <Card>
        <CardContent>
            <div className="space-y-12">
                <div className="flex flex-col items-center space-y-4">
                    <Avatar>
                        <AvatarImage src={picture} alt={username} />
                    </Avatar>
                   <div className="text-center">
                        <h5 className="text-xl font-semibold">{username}</h5>
                        <div className="text-muted-foreground text-sm">{email}</div>
                    </div>
                </div>
                <div className="bg-muted grid grid-cols-3 divide-x rounded-md border text-center *:py-3">
                    <div>
                        <h5 className="text-lg font-semibold">{id}</h5>
                        <div className="text-muted-foreground text-sm">ID</div>
                    </div>
                </div>
            </div>
        </CardContent>
    </Card>
}