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
    accessorKey: "name",
    header: "Item",
    cell: ({ row }: any) => (
      <div className="flex items-center gap-2">
        <Avatar>
          <AvatarImage src={row.original.icon}/>
          <AvatarFallback>{row.original.name}</AvatarFallback>
        </Avatar>
        <div className="min-w-0 flex-1">
          <div className="flex items-end justify-between gap-3">
            <div className="grid min-w-0 gap-0.5">
              <span className="truncate font-medium text-sm leading-none">{row.original.name}</span>
              <span className="truncate text-muted-foreground text-xs leading-none">#{row.original.id}</span>
            </div>
          </div>
        </div>
      </div>
    ),
    enableHiding: false,
  },
  {
    accessorKey: "place",
    header: "Place change (avg.)",
    filterFn: "equalsString",
    cell: ({ row }: any) => <span className="text-sm">{parseFloat(row.original.avg_place).toFixed(2)}</span>
  },
  {
    accessorKey: "wr",
    header: "WR",
    cell: ({ row }: any) => <span className="text-sm">{parseFloat(row.original.winrate).toFixed(2)}%</span>,
  },
  {
    accessorKey: "frequency",
    header: "Frequency",
    cell: ({ row }: any) => <span className="text-sm">{parseFloat(row.original.frequency).toFixed(2)}</span>,
  },
];