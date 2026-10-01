import { useEffect, useMemo, useState } from "react";
import { motion } from "motion/react";
import { useLocation, useSearchParams } from "react-router-dom";
import { Copy, Globe, Trophy, UserRound } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "@/components/ui/toast";
import { initialsOf, errorMessage } from "@/lib/utils";
import { getSearchFromQuery } from "@/services/searchService";
import { type UserSearch } from "@/types/search";

type LocationState = {
  user?: UserSearch;
};

function formatPercent(value: number) {
  return `${(value * 100).toFixed(1)}%`;
}

export default function UserSearchPage() {
  const location = useLocation();
  const state = (location.state as LocationState | null) ?? null;
  const [searchParams] = useSearchParams();

  const query = searchParams.get("q")?.trim() ?? "";

  const [user, setUser] = useState<UserSearch | null>(state?.user ?? null);
  const [loading, setLoading] = useState(Boolean(query) && !state?.user);

  useEffect(() => {
    if (!query) {
      setUser(null);
      setLoading(false);
      return;
    }

    if (state?.user?.username?.toLowerCase() === query.toLowerCase()) {
      setUser(state.user);
      setLoading(false);
      return;
    }

    let cancelled = false;

    async function load() {
      setLoading(true);
      try {
        const result = await getSearchFromQuery(query);
        const exactMatch =
          result.user.find((entry) => entry.username.toLowerCase() === query.toLowerCase()) ??
          result.user[0] ??
          null;

        if (!cancelled) setUser(exactMatch);
      } catch (error) {
        if (!cancelled) {
          setUser(null);
          toast.add({
            type: "error",
            title: "Failed to load user",
            description: errorMessage(error),
          });
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();

    return () => {
      cancelled = true;
    };
  }, [query, state?.user]);

  const totalGames = (user?.wins ?? 0) + (user?.losses ?? 0);
  const winrate = totalGames > 0 ? (user?.wins ?? 0) / totalGames : null;

  const rankLabel = useMemo(
    () => [user?.tier, user?.rank].filter(Boolean).join(" ").trim(),
    [user?.tier, user?.rank],
  );

  async function copyUsername() {
    if (!user?.username) return;

    try {
      await navigator.clipboard.writeText(user.username);
      toast.add({
        type: "success",
        title: "Riot ID copied",
        description: `${user.username} copied to clipboard`,
      });
    } catch {
      toast.add({
        type: "error",
        title: "Copy failed",
        description: "Unable to access clipboard.",
      });
    }
  }

  return (
    <div className="relative min-h-screen w-full">
      <div className="space-y-6 px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="space-y-1"
        >
          <h1 className="text-3xl font-semibold tracking-tight">User search</h1>
          <p className="text-muted-foreground">
            {query ? `Results for “${query}”.` : "Select a user from search results."}
          </p>
        </motion.div>

        <Separator />

        {loading && (
          <Card>
            <CardHeader>
              <CardTitle>Loading user…</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-3">
                <Skeleton className="size-14 rounded-full" />
                <div className="space-y-2">
                  <Skeleton className="h-5 w-44" />
                  <Skeleton className="h-4 w-28" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
                {Array.from({ length: 4 }).map((_, index) => (
                  <Skeleton key={index} className="h-20 rounded-xl" />
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {!loading && !user && (
          <Card>
            <CardContent>
              <Empty className="py-8">
                <EmptyHeader>
                  <EmptyMedia variant="icon">
                    <UserRound />
                  </EmptyMedia>
                  <EmptyTitle>No user found</EmptyTitle>
                  <EmptyDescription>
                    Try searching with a Riot ID format like Name#TAG.
                  </EmptyDescription>
                </EmptyHeader>
              </Empty>
            </CardContent>
          </Card>
        )}

        {!loading && user && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease: "easeOut" }}
            className="space-y-4"
          >
            <Card>
              <CardContent className="flex flex-col gap-4 pt-6 md:flex-row md:items-center md:justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="size-14">
                    <AvatarImage src={user.picture ?? user.icon} alt={user.username} />
                    <AvatarFallback>{initialsOf(user.username)}</AvatarFallback>
                  </Avatar>
                  <div className="space-y-1">
                    <div className="text-xl font-semibold leading-none">{user.username}</div>
                    <div className="text-muted-foreground flex flex-wrap items-center gap-2 text-xs">
                      <Badge variant="outline">{user.source === "riot" ? "Riot" : "Local"}</Badge>
                      {user.region && (
                        <Badge variant="secondary">
                          <Globe />
                          {user.region.toUpperCase()}
                        </Badge>
                      )}
                      {rankLabel && (
                        <Badge>
                          <Trophy />
                          {rankLabel}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>

                <Button variant="outline" onClick={() => void copyUsername()}>
                  <Copy />
                  Copy Riot ID
                </Button>
              </CardContent>
            </Card>

            <div className="grid grid-cols-2 gap-3 lg:grid-cols-5">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Level</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{user.summonerLevel ?? "-"}</CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">LP</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{user.leaguePoints ?? "-"}</CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Wins</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{user.wins ?? "-"}</CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Losses</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">{user.losses ?? "-"}</CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Winrate</CardTitle>
                </CardHeader>
                <CardContent className="text-2xl font-semibold">
                  {winrate == null ? "-" : formatPercent(winrate)}
                </CardContent>
              </Card>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
