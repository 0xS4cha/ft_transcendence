import { useEffect, useState } from "react";
import { DataTable } from "@/components/data-table/data-table";
import { RankingColumns } from "./columns";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import type { rankingPlayer } from "@/types/ranking";
import { getLeaderboardStats } from "@/services/statsService";

export function RankingTable() {
  const [players, setPlayers] = useState<rankingPlayer[]>([]);
  const [loading, setLoading] = useState(true);

  const [filter, setFilter] = useState({
    queue: "Ranked",
    server: "GLOBAL",
	  ranked: "CHALLENGER"
  });

  useEffect(() => {
    const fetchRankings = async () => {
      try {
        const response = await getLeaderboardStats(filter.server) 
        setPlayers(response.data); 
      } catch (error) {
        console.log("Erreur fetch ranking:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRankings();
  }, [filter]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Top 50 leaderboard</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div>loading players...</div>
        ) : (
          <DataTable
            columns={RankingColumns}
            data={players}
            getRowId={(row) => row.player_id}
            defaultSortId="rank"
            searchPlaceholder="Search player by Riot ID..."
            filter={filter}
            setFilter={setFilter}
            hideRankFilter={true}
            addGlobalServerFilter={true}
            hideQueueFilter={true}
          />
        )}
      </CardContent>
    </Card>
  );
}
