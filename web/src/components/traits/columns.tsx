import type { ColumnDef } from "@tanstack/react-table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { dataTableFeatures } from "@/lib/data-table-features";
import type { TraitRow } from "@/components/traits/schema";

export const TraitsColumns: ColumnDef<typeof dataTableFeatures, TraitRow>[] = [
  {
    id: "search",
    accessorFn: (row) => `${row.name} ${row.id}`,
    filterFn: "includesString",
    enableHiding: true,
  },
  {
    accessorKey: "trait",
    header: "Trait",
    cell: ({ row }) => (
      <div className="flex items-center gap-2">
        <Avatar>
          <AvatarImage src={row.original.icon}/>
          <AvatarFallback>{row.original.name}</AvatarFallback>
        </Avatar>
        <div className="min-w-0 flex-1">
          <div className="flex items-end justify-between gap-3">
            <div className="grid min-w-0 gap-0.5">
              <span className="truncate font-medium text-sm leading-none">{row.original.name}</span>
            </div>
          </div>
        </div>
      </div>
    ),
    enableHiding: false,
  },
  {
    accessorKey: "place",
    header: "Average Place",
    filterFn: "equalsString",
    cell: ({ row }) => <span className="text-sm">{Number(row.original.avg_place).toFixed(2)}</span>
  },
  {
    accessorKey: "wr",
    header: "Win rate",
    cell: ({ row }) => <span className="text-sm">{Number(row.original.winrate).toFixed(2)}%</span>,
  },
  {
    accessorKey: "frequency",
    header: "Frequency",
    cell: ({ row }) => <span className="text-sm">{Number(row.original.frequency).toFixed(2)}</span>,
  },
  {
    id: "avg_place",
    accessorFn: (row) => row.avg_place,
    enableSorting: true,
    enableHiding: true,
  },
  {
    id: "name",
    accessorFn: (row) => row.name,
    enableSorting: true,
    enableHiding: true,
  }
];