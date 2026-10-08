import type { ColumnDef } from "@tanstack/react-table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { dataTableFeatures } from "@/lib/data-table-features";
import type { ItemRow } from "@/components/items/schema";

export const ItemsColumns: ColumnDef<typeof dataTableFeatures, ItemRow>[] = [
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
            </div>
          </div>
        </div>
      </div>
    ),
    enableHiding: false,
  },
  {
    accessorKey: "place",
    header: "Avg place",
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