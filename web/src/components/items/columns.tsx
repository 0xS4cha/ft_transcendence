import type { ColumnDef } from "@tanstack/react-table";
import { Subscribe } from "@tanstack/react-table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import type { DataTableFeatures } from "@/lib/data-table-features";
import type { ItemRow } from "@/components/items/schema";

export const ItemsColumns: ColumnDef<DataTableFeatures, ItemRow>[] = [
  {
    id: "search",
    accessorFn: (row) => `${row.itemName}`,
    filterFn: "includesString",
    enableHiding: true,
  },
  {
    id: "select",
    header: ({ table }) => (
      <div className="flex items-center justify-center">
        <Subscribe
          source={table.atoms.rowSelection}
          selector={() =>
            table.getIsAllPageRowsSelected() ||
            (table.getIsSomePageRowsSelected() && !table.getIsAllPageRowsSelected() && "indeterminate")
          }
        >
          {(checked) => (
            <Checkbox
              checked={Boolean(checked)}
              onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
              aria-label="Select all units on this page"
            />
          )}
        </Subscribe>
      </div>
    ),
    cell: ({ row }) => (
      <div className="flex items-center justify-center">
        <Subscribe source={row.table.atoms.rowSelection} selector={(selection) => Boolean(selection?.[row.id])}>
          {(checked) => (
            <Checkbox
              checked={checked}
              onCheckedChange={(value) => row.toggleSelected(!!value)}
              aria-label={`Select ${row.original.itemName}`}
            />
          )}
        </Subscribe>
      </div>
    ),
    enableHiding: false,
  },
  {
    accessorKey: "itemName",
    header: "Item",
    cell: ({ row }) => (
      <div className="flex items-center gap-2">
          <Avatar>
            <AvatarImage src="https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/items/icons2d/096_eye_of_the_observer.png"/>
            <AvatarFallback>{row.original.itemName}</AvatarFallback>
          </Avatar>
        <div className="min-w-0 flex-1">
          <div className="flex items-end justify-between gap-3">
            <div className="grid min-w-0 gap-0.5">
              <span className="truncate font-medium text-sm leading-none">{row.original.itemName}</span>
              <span className="truncate text-muted-foreground text-xs leading-none">#{row.original.count}</span>
            </div>
          </div>
        </div>
      </div>
    ),
    enableHiding: false,
  },
  {
    accessorKey: "tier",
    header: "Tier",
    filterFn: "equalsString",
    cell: () => (
      <Badge className="bg-red-50 text-red-700 dark:bg-red-950 dark:text-red-300">
        S
      </Badge>
    ),
  },
  {
    accessorKey: "place",
    header: "Place change (avg.)",
    filterFn: "equalsString",
    cell: ({ row }) => <span className="text-sm">{row.original.avg}</span>
  },
  {
    accessorKey: "wr",
    header: "WR",
    cell: ({ row }) => <span className="text-sm">{row.original.avg}%</span>,
  },
  {
    accessorKey: "frequency",
    header: "Frequency",
    cell: ({ row }) => <span className="text-sm">{row.original.pick}</span>,
  },
  {
    accessorKey: "units",
    header: "Popular units",
    cell: () => {},
  },
];