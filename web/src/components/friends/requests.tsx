import { useEffect, useState, useCallback } from "react";
import { CheckIcon, XIcon } from "lucide-react";
import { useTranslation } from "react-i18next";

import { Card, CardHeader, CardTitle, CardAction, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { toast } from "@/components/ui/toast";
import { cn, initialsOf, errorMessage, resolvePictureUrl } from "@/lib/utils";
import {
  getFriendsRequestList,
  acceptFriendRequest,
  refuseFriendRequest,
} from "@/services/friendsService";
import { type UserProfile } from "@/types/user";

export function RequestsCard({ onAccepted }: { onAccepted?: () => void }) {
  const [requests, setRequests] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState<Set<string>>(new Set());
  const { t } = useTranslation();

  const loadRequests = useCallback(() =>
    getFriendsRequestList()
      .then(setRequests)
      .catch((error: unknown) => {
        toast.add({
          type: "error",
          title: t("friends.loadRequestsFailed"),
          description: errorMessage(error),
        });
      })
      .finally(() => setLoading(false)),
  [t]);

  useEffect(() => {
    void loadRequests();
  }, [loadRequests]);

  async function handleAnswer(username: string, action: "accept" | "refuse") {
    setPending((current) => new Set(current).add(username));
    try {
      if (action === "accept") {
        await acceptFriendRequest(username);
        toast.add({
          type: "success",
          title: t("friends.requestAcceptSuccess", { username }),
        });
        onAccepted?.();
      } else {
        await refuseFriendRequest(username);
      }
      setRequests((current) => current.filter((request) => request.username !== username));
    } catch (error) {
      toast.add({
        type: "error",
        title:
          action === "accept"
            ? t("friends.requestAcceptFailed")
            : t("friends.requestDeclineFailed"),
        description: errorMessage(error),
      });
    } finally {
      setPending((current) => {
        const next = new Set(current);
        next.delete(username);
        return next;
      });
    }
  }

  if (loading || requests.length === 0) return null;

  return (
    <Card className="w-full overflow-hidden">
      <CardHeader className="border-b">
        <CardTitle>{t("friends.friendRequests")}</CardTitle>
        <CardAction>
          <Badge variant="secondary">{requests.length}</Badge>
        </CardAction>
      </CardHeader>

      <CardContent className="flex max-h-64 flex-col gap-1 overflow-y-auto p-4" role="list">
        {requests.map((request) => {
          const busy = pending.has(request.username);
          return (
            <div
              key={request.username}
              role="listitem"
              className={cn(
                "flex items-center gap-3 rounded-xl px-2 py-2 transition-opacity",
                busy && "opacity-60",
              )}
            >
              <Avatar className="size-8 shrink-0">
                <AvatarImage src={resolvePictureUrl(request.picture)} />
                <AvatarFallback className="text-xs">{initialsOf(request.username)}</AvatarFallback>
              </Avatar>

              <span className="min-w-0 flex-1 truncate text-sm font-medium">
                {request.username}
              </span>

              <Tooltip>
                <TooltipTrigger
                  render={
                    <Button
                      variant="ghost"
                      size="icon"
                      disabled={busy}
                      onClick={() => void handleAnswer(request.username, "refuse")}
                      className="text-muted-foreground hover:text-destructive"
                      aria-label={t("friends.decline")} 
                    >
                      <XIcon />
                    </Button>
                  }
                />
                <TooltipContent side="top">{t("friends.decline")}</TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger
                  render={
                    <Button
                      variant="default"
                      size="icon"
                      disabled={busy}
                      onClick={() => void handleAnswer(request.username, "accept")}
                      aria-label={t("friends.accept")}
                    >
                      {busy ? <Spinner /> : <CheckIcon />}
                    </Button>
                  }
                />
                <TooltipContent side="top">{t("friends.accept")}</TooltipContent>
              </Tooltip>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}