import { useEffect, useState } from "react";
import { DataTable } from "@/components/data-table/data-table";
import { RankingColumns } from "./columns";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import type { rankingPlayer } from "@/types/ranking";

export function RankingTable() {
  const [players, setPlayers] = useState<rankingPlayer[]>([]);
  const [loading, setLoading] = useState(true);

  const [filter, setFilter] = useState({
    queue: "1100",
    server: "EUW1",
	ranked: "CHALLENGER"
  });

  useEffect(() => {
    const fetchRankings = async () => {
      try {
        const response = await fetch("/api/leaderboard/"); 
        const json = await response.json();
        setPlayers(json.data); 
      } catch (error) {
        console.error("Erreur fetch ranking:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRankings();
  }, []);

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
            hideQueueFilter={true}
          />
        )}
      </CardContent>
    </Card>
  );
}