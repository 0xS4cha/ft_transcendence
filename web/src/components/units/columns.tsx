import type { ColumnDef } from "@tanstack/react-table";
import { Button } from "@/components/ui/button"
import { Avatar, AvatarImage } from "@/components/ui/avatar";
import { dataTableFeatures } from "@/lib/data-table-features";
import type { UnitRow } from "@/components/units/schema";
import { ChevronRight } from "lucide-react";

export const UnitsColumns: ColumnDef<typeof dataTableFeatures, UnitRow>[] = [
  {
    id: "search",
    accessorFn: (row) => `${row.name} ${row.id}`,
    filterFn: "includesString",
    enableHiding: true,
  },
  {
    id: "expand",
    header: () => null,
    cell: ({ row }: any) => (
      row.original.model ? (
        <Button
          variant="ghost"
          size="sm"
          onClick={(event) => {
            event.stopPropagation();
            row.toggleExpanded();
          }}
          aria-label={row.getIsExpanded() ? "Collapse row" : "Expand row"}
          className="h-8 w-8 p-0">
          <ChevronRight
            className={`transition-transform ${row.getIsExpanded() ? "rotate-90" : ""}`}
          />
        </Button>
        ) : <></>
    ),
    enableSorting: false,
    enableHiding: false
  },
  {
    accessorKey: "unit",
    header: "Unit",
    cell: ({ row }: any) => (
      <div className="flex items-center gap-2 cursor-pointer">
        <Avatar>
          <AvatarImage src={row.original.icon}/>
        </Avatar>
        <div className="min-w-0 flex-1">
          <div className="flex items-end justify-between gap-3">
            <div className="grid min-w-0 gap-0.5">
              <span className="truncate font-medium text-sm leading-none">
                {row.original.name}
              </span>

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
  {
    accessorKey: "cost",
    header: "Cost",
    cell: ({ row }: any) => <span className="text-sm">{parseFloat(row.original.cost).toFixed(2)}</span>,
  },
  {
    id: "avg_place",
    accessorFn: (row) => row.avg_place,
    enableSorting: true,
  },
  {
    id: "name",
    accessorFn: (row) => row.name,
    enableSorting: true,
  }
];