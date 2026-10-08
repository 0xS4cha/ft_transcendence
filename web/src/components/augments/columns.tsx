import type { ColumnDef } from "@tanstack/react-table";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { dataTableFeatures } from "@/lib/data-table-features";
import type { AugmentRow } from "@/components/augments/schema";

const getAugmentStyle = (tier?: number | string) => {
  const t = String(tier ?? "").toLowerCase();

  if (t === "1" || t === "silver") {
    return {
      fill: "linear-gradient(180deg, #AABACE 20%, #9FB4CE 50%, #6886A5 80%)",
      glow: "#477DCB",
    };
  }
  if (t === "2" || t === "gold") {
    return {
      fill: "linear-gradient(180deg, #DEBA31 20%, #E7BA1E 50%, #D69C31 80%)",
      glow: "#A18E21",
    };
  }
  if (t === "3" || t === "prismatic") {
    return {
      fill: "linear-gradient(180deg, #A887FF 10%, #8352FF 40%, #6800FF 90%)",
      glow: "#6838FF",
    };
  }

  return {
    fill: "linear-gradient(180deg, #737373 20%, #a3a3a3 50%, #404040 80%)",
    glow: "#737373",
  };
};

export const AugmentsColumns: ColumnDef<typeof dataTableFeatures, AugmentRow>[] = [
  {
    id: "search",
    accessorFn: (row) => `${row.name} ${row.id}`,
    filterFn: "includesString",
    enableHiding: true,
  },
  {
    accessorKey: "augment",
    header: () => (
      <>
        <svg width="0" height="0" className="absolute pointer-events-none" aria-hidden="true">
          <filter id="s18-augment-tier-key" colorInterpolationFilters="sRGB" x="-25%" y="-25%" width="150%" height="150%">
            <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0.75 0.75 0.75 0 0" />
          </filter>
          <filter id="s18-augment-tier-glyph" colorInterpolationFilters="sRGB" x="-25%" y="-25%" width="150%" height="150%">
            <feColorMatrix type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" />
          </filter>
        </svg>
        <span>Augment</span>
      </>
    ),
    cell: ({ row }: any) => {
      const activeStyle = getAugmentStyle(row.original.rarity);
      return (
        <div className="flex items-center gap-2">
          {row.original.icon ? (
            <div className="relative flex size-9 shrink-0 items-center justify-center">
              <span
                className="block aspect-square w-full opacity-80"
                style={{
                  backgroundImage: activeStyle.fill,
                  filter: `url(#s18-augment-tier-key) drop-shadow(0 0 3px ${activeStyle.glow})`,
                }}
              >
                <img
                  src={row.original.icon}
                  alt={row.original.name}
                  draggable={false}
                  className="block h-full w-full mix-blend-multiply"
                  style={{ filter: "url(#s18-augment-tier-glyph)" }}
                />
              </span>
            </div>
          ) : (
            <Avatar>
              <AvatarFallback>{row.original.name}</AvatarFallback>
            </Avatar>
          )}
          <div className="min-w-0 flex-1">
            <div className="flex items-end justify-between gap-3">
              <div className="grid min-w-0 gap-0.5">
                <span className="truncate font-medium text-sm leading-none">{row.original.name}</span>
              </div>
            </div>
          </div>
        </div>
      );
    },
    enableHiding: false,
  },
  {
    id: "name",
    accessorFn: (row) => row.name,
    enableSorting: true,
    enableHiding: true,
  }
];