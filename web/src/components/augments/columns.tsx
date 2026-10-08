import type { ColumnDef } from "@tanstack/react-table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { dataTableFeatures } from "@/lib/data-table-features";
import type { AugmentRow } from "@/components/augments/schema";

export const AugmentsColumns: ColumnDef<typeof dataTableFeatures, AugmentRow>[] = [
  {
    id: "search",
    accessorFn: (row) => `${row.name} ${row.id}`,
    filterFn: "includesString",
    enableHiding: true,
  },
  {
    accessorKey: "name",
    header: "Augment",
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
    accessorKey: "rarity",
    header: "Rarity",
    filterFn: "equalsString",
    cell: ({ row }: any) => <span className="text-sm">{row.original.rarity}</span>
  },
];