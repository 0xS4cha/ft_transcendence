import {
  Swords,
  Trophy,
  Globe,
} from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { useMemo } from "react"

import { type FilterType } from "@/types/stats";

const queueOptions = [
  { value: "1100", label: "Ranked" },
  { value: "1160", label: "Double up" },
] as const;

const rankOptions = [
  { value: "RANKUNKNOWN", label: "Unknown" },
  { value: "IRON", label: "Iron" },
  { value: "BRONZE", label: "Bronze" },
  { value: "SILVER", label: "Silver" },
  { value: "GOLD", label: "Gold" },
  { value: "PLATINUM", label: "Platinium" },
  { value: "EMERALD", label: "Emerald" },
  { value: "DIAMOND", label: "Diamond" },
  { value: "MASTER", label: "Master" },
  { value: "GRANDMASTER", label: "Grand Master" },
  { value: "CHALLENGER", label: "Challenger" },
] as const;

const SERVER_OPTIONS = [
  { value: "BR1", label: "BR" },
  { value: "EUN1", label: "EUE" },
  { value: "EUW1", label: "EUW" },
  { value: "JP1", label: "JP" },
  { value: "KR", label: "KR" },
  { value: "LA1", label: "LAN" },
  { value: "LA2", label: "LAS" },
  { value: "ME1", label: "ME" },
  { value: "NA1", label: "NA" },
  { value: "OC1", label: "OCE" },
  { value: "RU", label: "RU" },
  { value: "SG2", label: "SEA" },
  { value: "TR1", label: "TR" },
  { value: "TW2", label: "TW" },
  { value: "VN2", label: "VN" },
] as const;

const GLOBAL_OPTION = { value: "GLOBAL", label: "GLOBAL" } as const;


interface DataTableFilterProps {
  filter: FilterType;
  setFilter: any;
  hideRankFilter?: boolean;
  hideQueueFilter?: boolean;
  addGlobalServerFilter?: boolean;
}

export function DataTableFilter({ filter, setFilter, hideRankFilter, hideQueueFilter, addGlobalServerFilter }: DataTableFilterProps) {
  const updateFilter = (columnId: string, value: string) => {
    setFilter((prev: FilterType) => ({
      ...prev,
      [columnId]: value,
    }));
  };

  const serverOptions = useMemo(
    () => (addGlobalServerFilter ? [...SERVER_OPTIONS, GLOBAL_OPTION] : SERVER_OPTIONS),
    [addGlobalServerFilter]
  );

  return (
    <div className="flex flex-wrap items-center gap-2 rounded-lg">

    {!hideQueueFilter && (
      <Select
        value={filter.queue}
        onValueChange={(value) => value ? updateFilter("queue", value) : console.log("value is null")}
      >
        <SelectTrigger size="sm" className="w-[130px]">
          <div className="flex items-center gap-1.5 truncate">
            <Swords className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {queueOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select> )}

      {!hideRankFilter && (
      <Select
        value={filter.ranked}
        onValueChange={(value) => value ? updateFilter("ranked", value) : console.log("value is null")}
      >
        <SelectTrigger size="sm" className="w-[140px]">
          <div className="flex items-center gap-1.5 truncate">
            <Trophy className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {rankOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select> )}

      <Select
        value={filter.server}
        onValueChange={(value) => value ? updateFilter("server", value) : console.log("value is null")}
      >
        <SelectTrigger size="sm" className="w-[100px]">
          <div className="flex items-center gap-1.5 truncate">
            <Globe className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {serverOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
