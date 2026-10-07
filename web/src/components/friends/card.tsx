import { useState, useEffect, useCallback } from "react";
import { UserPlusIcon, UsersIcon, RefreshCwIcon, TrashIcon } from "lucide-react";
import { useTranslation } from "react-i18next";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
  InputGroupText,
} from "@/components/ui/input-group";
import { Avatar, AvatarFallback, AvatarImage, AvatarBadge } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Kbd, KbdGroup } from "@/components/ui/kbd";
import {
  Empty,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
  EmptyDescription,
} from "@/components/ui/empty";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { toast } from "@/components/ui/toast";
import { cn } from "@/lib/utils";
import { getFriendsList, sendFriendsRequest, removeFriend } from "@/services/friendsService";
import { type FriendState } from "@/types/user";
import { initialsOf, errorMessage } from "@/lib/utils";

const MAX_USERNAME_LENGTH = 32;

function FriendRow({
  friend,
  removing,
  onRemove,
  deleteLabel,
  deleteTooltip,
}: {
  friend: FriendState;
  removing: boolean;
  onRemove: (username: string) => void;
  deleteLabel: string;
  deleteTooltip: string;
}) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-xl px-2 py-2 transition-opacity",
        removing && "opacity-60",
      )}
    >
      <Avatar className="size-8 shrink-0">
        <AvatarImage src={friend.picture} />
        <AvatarFallback className="text-xs">{initialsOf(friend.username)}</AvatarFallback>
        <AvatarBadge className={friend.online ? 'bg-green-600 dark:bg-green-800' : 'bg-red-600 dark:bg-red-800' }/>
      </Avatar>

      <span className="min-w-0 flex-1 truncate text-sm font-medium">{friend.username}</span>

      <Tooltip>
        <TooltipTrigger
          render={
            <Button
              variant="ghost"
              size="icon"
              className="text-muted-foreground hover:text-destructive"
              onClick={() => onRemove(friend.username)}
              disabled={removing}
              aria-label={deleteLabel}
            >
              {removing ? <Spinner /> : <TrashIcon />}
            </Button>
          }
        />
        <TooltipContent side="left">{deleteTooltip}</TooltipContent>
      </Tooltip>
    </div>
  );
}

function FriendsSkeleton() {
  return (
    <div className="flex flex-col gap-4" aria-hidden>
      {["w-32", "w-44", "w-28"].map((width) => (
        <div key={width} className="flex items-center gap-3 px-2">
          <Skeleton className="size-8 shrink-0 rounded-full" />
          <Skeleton className={cn("h-4", width)} />
        </div>
      ))}
    </div>
  );
}

export function FriendsCard() {
  const [friends, setFriends] = useState<FriendState[]>([]);
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [removingIds, setRemovingIds] = useState<Set<string>>(new Set());
  const { t } = useTranslation();

  const loadFriends = useCallback(async () => {
    setLoading(true);
    try {
      setFriends(await getFriendsList());
    } catch (error) {
      toast.add({
        type: "error",
        title: t("friends.loadFailed"),
        description: errorMessage(error),
      });
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    const interval = setInterval(() => {
      void loadFriends();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const trimmed = username.trim();
  const canSend = trimmed.length > 0 && !sending;

  async function handleSend() {
    if (!canSend) return;

    setSending(true);
    try {
      await sendFriendsRequest(trimmed);
      setUsername("");
      toast.add({
        type: "success",
        title: t("friends.requestSent"),
        description: t("friends.requestSentDescription", { username: trimmed }),
      });
    } catch (error) {
      toast.add({
        type: "error",
        title: t("friends.requestNotSent"),
        description: errorMessage(error),
      });
    } finally {
      setSending(false);
    }
  }

  async function handleRemove(target: string) {
    setRemovingIds((current) => new Set(current).add(target));
    try {
      await removeFriend(target);
      setFriends((current) => current.filter((friend) => friend.username !== target));
    } catch (error) {
      toast.add({
        type: "error",
        title: t("friends.deleteImpossible"),
        description: errorMessage(error),
      });
    } finally {
      setRemovingIds((current) => {
        const next = new Set(current);
        next.delete(target);
        return next;
      });
    }
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Enter") {
      event.preventDefault();
      void handleSend();
    }
  }

  return (
    <Card className="flex h-[36rem] w-full flex-col overflow-hidden">
      <CardHeader className="border-b">
        <CardTitle>{t("friends.title")}</CardTitle>
        <CardDescription>{t("friends.subtitle")}</CardDescription>
        <CardAction className="flex items-center gap-2">
          <Badge variant="secondary">
            {friends.length} {t("friends.badgeFriend", { count: friends.length })}
          </Badge>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => void loadFriends()}
            disabled={loading}
            aria-label={t("common.reload")}
          >
            <RefreshCwIcon className={cn(loading && "animate-spin")} />
          </Button>
        </CardAction>
      </CardHeader>

      <CardContent className="min-h-0 flex-1 p-0">
        <ScrollArea className="h-full">
          <div className="flex flex-col gap-1 p-4" role="list" aria-busy={loading}>
            {loading ? (
              <FriendsSkeleton />
            ) : friends.length === 0 ? (
              <Empty>
                <EmptyHeader>
                  <EmptyMedia variant="icon">
                    <UsersIcon />
                  </EmptyMedia>
                  <EmptyTitle>{t("friends.noFriends")}</EmptyTitle>
                  <EmptyDescription>{t("friends.noFriendsDescription")}</EmptyDescription>
                </EmptyHeader>
              </Empty>
            ) : (
              friends.map((friend) => (
                <FriendRow
                  key={friend.username}
                  friend={friend}
                  removing={removingIds.has(friend.username)}
                  onRemove={(name) => void handleRemove(name)}
                  deleteLabel={t("friends.deleteAria", { username: friend.username })}
                  deleteTooltip={t("friends.deleteTooltip")}
                />
              ))
            )}
          </div>
        </ScrollArea>
      </CardContent>

      <CardFooter className="border-t pt-6">
        <InputGroup>
          <InputGroupInput
            id="friend-username"
            placeholder={t("friends.inputPlaceholder")}
            value={username}
            maxLength={MAX_USERNAME_LENGTH}
            disabled={sending}
            autoComplete="off"
            onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
              setUsername(event.target.value)
            }
            onKeyDown={handleKeyDown}
          />
          <InputGroupAddon align="inline-end" className="gap-2">
            <InputGroupText className="hidden text-xs sm:flex">
              <KbdGroup>
                <Kbd>Enter</Kbd>
              </KbdGroup>
              {t("chat.toSend")}
            </InputGroupText>
            <InputGroupButton
              variant="default"
              size="sm"
              disabled={!canSend}
              onClick={() => void handleSend()}
            >
              {sending ? <Spinner /> : <UserPlusIcon />}
              {t("friends.add")}
            </InputGroupButton>
          </InputGroupAddon>
        </InputGroup>
      </CardFooter>
    </Card>
  );
}