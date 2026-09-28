import {
  Swords,
  Trophy,
  Globe,
  RotateCcw,
} from "lucide-react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { Button } from "@/components/ui/button";

const queueOptions = [
  { value: "ranked", label: "Ranked" },
  { value: "doubleup", label: "Double up" },
] as const;

const rankOptions = [
  { value: "unknown", label: "Unknown" },
  { value: "iron", label: "Iron" },
  { value: "bronze", label: "Bronze" },
  { value: "silver", label: "Silver" },
  { value: "gold", label: "Gold" },
  { value: "platinium", label: "Platinium" },
  { value: "emerald", label: "Emerald" },
  { value: "diamond", label: "Diamond" },
  { value: "master", label: "Master" },
  { value: "grandmaster", label: "Grand Master" },
  { value: "challenger", label: "Challenger" },
] as const;

const serverOptions = [
  { value: "br", label: "BR" },
  { value: "eue", label: "EUE" },
  { value: "euw", label: "EUW" },
  { value: "jp", label: "JP" },
  { value: "kr", label: "KR" },
  { value: "lan", label: "LAN" },
  { value: "las", label: "LAS" },
  { value: "me", label: "ME" },
  { value: "na", label: "NA" },
  { value: "oce", label: "OCE" },
  { value: "ru", label: "RU" },
  { value: "sea", label: "SEA" },
  { value: "tr", label: "TR" },
  { value: "tw", label: "TW" },
  { value: "vn", label: "VN" },
] as const;

const DEFAULTS = {
  queue: "ranked",
  ranked: "platinium",
  server: "euw",
} as const;

interface DataTableFilterProps {
  table: any;
}

export function DataTableFilter({ table }: DataTableFilterProps) {
  const queueFilter =
    (table?.getColumn("queue")?.getFilterValue() as string | undefined) ?? DEFAULTS.queue;
  const rankFilter =
    (table?.getColumn("ranked")?.getFilterValue() as string | undefined) ?? DEFAULTS.ranked;
  const serverFilter =
    (table?.getColumn("server")?.getFilterValue() as string | undefined) ?? DEFAULTS.server;

  const updateFilter = (columnId: string, value: string, defaultValue: string) => {
    table?.getColumn(columnId)?.setFilterValue(value === defaultValue ? undefined : value);
    table?.setPageIndex(0);
  };

  const hasActiveFilters =
    queueFilter !== DEFAULTS.queue ||
    rankFilter !== DEFAULTS.ranked ||
    serverFilter !== DEFAULTS.server;

  const resetFilters = () => {
    table?.getColumn("queue")?.setFilterValue(undefined);
    table?.getColumn("ranked")?.setFilterValue(undefined);
    table?.getColumn("server")?.setFilterValue(undefined);
    table?.setPageIndex(0);
  };

  return (
    <div className="flex flex-wrap items-center gap-2 rounded-lg">

      <Select
        value={queueFilter}
        onValueChange={(value) => value ? updateFilter("queue", value, DEFAULTS.queue) : console.log("value is null")}
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
      </Select>

      <Select
        value={rankFilter}
        onValueChange={(value) => value ? updateFilter("ranked", value, DEFAULTS.ranked) : console.log("value is null")}
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
      </Select>

      <Select
        value={serverFilter}
        onValueChange={(value) => value ? updateFilter("server", value, DEFAULTS.server) : console.log("value is null")}
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

      {hasActiveFilters && (
        <Button
          variant="ghost"
          size="sm"
          onClick={resetFilters}
          className="ml-auto h-8 text-muted-foreground hover:text-foreground"
        >
          <RotateCcw className="mr-1 h-3.5 w-3.5" />
          Reset
        </Button>
      )}
    </div>
  );
}
