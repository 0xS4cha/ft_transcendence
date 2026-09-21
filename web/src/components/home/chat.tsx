import { Fragment, useState, useRef, useCallback, useEffect } from "react";
import { SendHorizontalIcon, MessagesSquareIcon, RefreshCwIcon } from "lucide-react";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Bubble, BubbleContent, BubbleGroup } from "@/components/ui/bubble";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupText,
  InputGroupTextarea,
} from "@/components/ui/input-group";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
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

import { type ChatDataProps } from "@/types/chat";
import { getChatHistory, sendChatMessage } from "@/services/chatService";

const MAX_LENGTH = 2000;

const timeFormatter = new Intl.DateTimeFormat(undefined, {
  hour: "2-digit",
  minute: "2-digit",
});

const dayFormatter = new Intl.DateTimeFormat(undefined, {
  weekday: "long",
  day: "numeric",
  month: "long",
});

function formatTime(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : timeFormatter.format(date);
}

function formatDay(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "" : dayFormatter.format(date);
}

function initialsOf(username: string) {
  return username.slice(0, 2).toUpperCase();
}


function groupMessages(messages: ChatDataProps[]) {
  return messages.reduce<ChatDataProps[][]>((groups, message) => {
    const last = groups.at(-1);
    if (last && last[0].username === message.username) {
      last.push(message);
      return groups;
    }
    groups.push([message]);
    return groups;
  }, []);
}

function MessageGroup({
  messages,
  mine,
  pendingIds,
}: {
  messages: ChatDataProps[];
  mine: boolean;
  pendingIds: Set<number>;
}) {
  const [first] = messages;

  return (
    <div className={cn("flex items-end gap-2", mine ? "flex-row-reverse" : "flex-row")}>
      <Avatar className="size-8 shrink-0">
        <AvatarFallback className="text-xs">{initialsOf(first.username)}</AvatarFallback>
      </Avatar>

      <div className={cn("flex min-w-0 flex-col gap-1", mine && "items-end")}>
        {!mine && (
          <span className="text-muted-foreground px-1 text-xs font-medium">
            {first.username}
          </span>
        )}

        <BubbleGroup>
          {messages.map((message) => (
            <Tooltip key={message.id}>
              <TooltipTrigger render={
                <Bubble
                  align={mine ? "end" : "start"}
                  variant={mine ? "default" : "muted"}
                  className={cn(
                    "transition-opacity",
                    pendingIds.has(message.id) && "opacity-60",
                  )}
                >
                  <BubbleContent className="whitespace-pre-wrap break-words">
                    {message.content}
                  </BubbleContent>
                </Bubble>
              } />
              <TooltipContent side={mine ? "left" : "right"}>
                {pendingIds.has(message.id) ? "Sending…" : formatTime(message.date)}
              </TooltipContent>
            </Tooltip>
          ))}
        </BubbleGroup>
      </div>
    </div>
  );
}

function MessagesSkeleton() {
  return (
    <div className="flex flex-col gap-6" aria-hidden>
      {["w-48", "w-64", "w-40"].map((width, index) => (
        <div
          key={width}
          className={cn("flex items-end gap-2", index % 2 === 1 && "flex-row-reverse")}
        >
          <Skeleton className="size-8 shrink-0 rounded-full" />
          <Skeleton className={cn("h-10 rounded-2xl", width)} />
        </div>
      ))}
    </div>
  );
}

export function Chat({ currentUser }: { currentUser: string }) {
  const [messages, setMessages] = useState<ChatDataProps[]>([]);
  const [pendingIds, setPendingIds] = useState<Set<number>>(new Set());
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);

  const viewportRef = useRef<HTMLDivElement>(null);

  const loadHistory = useCallback(async () => {
    setLoading(true);
    try {
      setMessages(await getChatHistory());
    } catch (error) {
      toast.add({
        type: "error",
        title: "Couldn't load the chat history",
        description: error instanceof Error ? error.message : String(error),
      });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadHistory();
  }, [loadHistory]);


  useEffect(() => {
    viewportRef.current?.scrollTo({
      top: viewportRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  const trimmed = message.trim();
  const canSend = trimmed.length > 0 && trimmed.length <= MAX_LENGTH && !sending;

  async function handleSubmit() {
    if (!canSend) return;

    const draft = trimmed;

    const tempId = -Date.now();

    setMessage("");
    setSending(true);
    setPendingIds((current) => new Set(current).add(tempId));
    setMessages((current) => [
      ...current,
      { id: tempId, date: new Date().toISOString(), content: draft, username: currentUser },
    ]);

    try {
      const saved = await sendChatMessage(draft);
      setMessages((current) => current.map((item) => (item.id === tempId ? saved : item)));
    } catch (error) {
      setMessages((current) => current.filter((item) => item.id !== tempId));
      setMessage(draft);
      toast.add({
        type: "error",
        title: "Message not sent",
        description: error instanceof Error ? error.message : String(error),
      });
    } finally {
      setPendingIds((current) => {
        const next = new Set(current);
        next.delete(tempId);
        return next;
      });
      setSending(false);
    }
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSubmit();
    }
  }

  const groups = groupMessages(messages);

  return (
    <Card className="flex h-[36rem] w-full max-w-2xl flex-col overflow-hidden">
      <CardHeader className="border-b">
        <CardTitle>Global chat</CardTitle>
        <CardDescription>Everyone in the workspace can read this.</CardDescription>
        <CardAction className="flex items-center gap-2">
          <Badge variant="secondary">{messages.length} messages</Badge>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => void loadHistory()}
            disabled={loading}
            aria-label="Reload messages"
          >
            <RefreshCwIcon className={cn(loading && "animate-spin")} />
          </Button>
        </CardAction>
      </CardHeader>

      <CardContent className="min-h-0 flex-1 p-0">
        <ScrollArea className="h-full" viewportRef={viewportRef}>
          <div
            className="flex flex-col gap-6 p-6"
            role="log"
            aria-live="polite"
            aria-busy={loading}
          >
            {loading ? (
              <MessagesSkeleton />
            ) : groups.length === 0 ? (
              <Empty>
                <EmptyHeader>
                  <EmptyMedia variant="icon">
                    <MessagesSquareIcon />
                  </EmptyMedia>
                  <EmptyTitle>No messages yet</EmptyTitle>
                  <EmptyDescription>
                    Say hello and start the conversation.
                  </EmptyDescription>
                </EmptyHeader>
              </Empty>
            ) : (
              groups.map((group, index) => {
                const previous = groups[index - 1];
                const showDay =
                  !previous ||
                  formatDay(previous[0].date) !== formatDay(group[0].date);

                return (
                  <Fragment key={`${group[0].username}-${group[0].id}`}>
                    {showDay && formatDay(group[0].date) && (
                      <div className="flex items-center justify-center">
                        <Badge variant="outline" className="bg-card">
                          {formatDay(group[0].date)}
                        </Badge>
                      </div>
                    )}
                    <MessageGroup
                      messages={group}
                      mine={group[0].username === currentUser}
                      pendingIds={pendingIds}
                    />
                  </Fragment>
                );
              })
            )}
          </div>
        </ScrollArea>
      </CardContent>

      <CardFooter className="border-t pt-6">
        <InputGroup>
          <InputGroupTextarea
            id="chat-message"
            placeholder="Write a message…"
            value={message}
            maxLength={MAX_LENGTH}
            disabled={loading}
            onChange={(event: React.ChangeEvent<HTMLTextAreaElement>) =>
              setMessage(event.target.value)
            }
            onKeyDown={handleKeyDown}
          />
          <InputGroupAddon align="block-end">
            <InputGroupText className="text-xs">
              <KbdGroup>
                <Kbd>Enter</Kbd>
              </KbdGroup>
              to send
            </InputGroupText>
            <InputGroupText
              className={cn(
                "ml-auto text-xs tabular-nums",
                message.length > MAX_LENGTH * 0.9 && "text-destructive",
              )}
            >
              {message.length}/{MAX_LENGTH}
            </InputGroupText>
            <InputGroupButton
              variant="default"
              size="sm"
              disabled={!canSend}
              onClick={() => void handleSubmit()}
            >
              {sending ? <Spinner /> : <SendHorizontalIcon />}
              Post
            </InputGroupButton>
          </InputGroupAddon>
        </InputGroup>
      </CardFooter>
    </Card>
  );
}