import type { ColumnDef } from "@tanstack/react-table";
import type { rankingPlayer } from "./types/ranking";
import { Trophy } from "lucide-react";

export const RankingColumns: ColumnDef<rankingPlayer>[] = [
  {
    accessorKey: "rank",
    header: "Ranks",
    cell: ({ row }) => { 
      const rank = row.original.rank;
      return (
        <div className="flex items-center gap-2">
          {rank === 1 && <Trophy className="h-4 w-4 text-yellow-400" />}
          {rank === 2 && <Trophy className="h-4 w-4 text-slate-300" />}
          {rank === 3 && <Trophy className="h-4 w-4 text-amber-600" />}
          #{rank}
        </div>
      );
    },
  },
  {
    accessorKey: "riot_id",
    header: "Summoner",
    cell: ({ row }) => <span >{row.original.riot_id}</span>,
  },
  {
    accessorKey: "rating",
    header: "LP",
    cell: ({ row }) => (
      <div className="flex items-center gap-2">
        <img 
          src="https://cdn.teamfight.lol/riot/regalia/CHALLENGER.webp" 
          alt="Challenger" 
          className="h-6 w-6 object-contain" 
        />
        <span>{row.original.rating}</span>
      </div>
    ),
  },
  {
    id: "winrate",
    header: "Winrate",
    cell: ({ row }) => {
      const stats = row.original.stats;
      const winrate = ((stats.wins / stats.num_played) * 100).toFixed(1);
      return <span>{winrate}%</span>;
    },
  },
  {
    id: "avg_place",
    header: "Avg Place",
    cell: ({ row }) => {
      const stats = row.original.stats;
      const avgPlace = (stats.place_sum / stats.num_played).toFixed(2);
      return <span>{avgPlace}</span>;
    },
  },
  {
    accessorKey: "num_played",
    header: "Games",
  },
];