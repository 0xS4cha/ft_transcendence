import {
  Layers,
  Swords,
  CalendarDays,
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

const setOptions = [
  { value: "all", label: "All Set" },
  { value: "S18", label: "Set 18" },
  { value: "S17", label: "Set 17" },
] as const;

const queueOptions = [
  { value: "ranked", label: "Ranked" },
  { value: "doubleup", label: "Double up" },
] as const;

const dateOptions = [
  { value: "1", label: "Last day" },
  { value: "2", label: "Last 2 days" },
  { value: "3", label: "Last 3 days" },
  { value: "4", label: "Last 4 days" },
  { value: "5", label: "Last 5 days" },
  { value: "6", label: "Last 6 days" },
  { value: "7", label: "Last 7 days" },
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
  set: "all",
  queue: "ranked",
  date: "1",
  ranked: "platinium",
  server: "euw",
} as const;

interface DataTableFilterProps {
  table: any;
}

export function DataTableFilter({ table }: DataTableFilterProps) {
  const setFilter =
    (table?.getColumn("set")?.getFilterValue() as string | undefined) ?? DEFAULTS.set;
  const queueFilter =
    (table?.getColumn("queue")?.getFilterValue() as string | undefined) ?? DEFAULTS.queue;
  const dateFilter =
    (table?.getColumn("date")?.getFilterValue() as string | undefined) ?? DEFAULTS.date;
  const rankFilter =
    (table?.getColumn("ranked")?.getFilterValue() as string | undefined) ?? DEFAULTS.ranked;
  const serverFilter =
    (table?.getColumn("server")?.getFilterValue() as string | undefined) ?? DEFAULTS.server;

  const updateFilter = (columnId: string, value: string, defaultValue: string) => {
    table?.getColumn(columnId)?.setFilterValue(value === defaultValue ? undefined : value);
    table?.setPageIndex(0);
  };

  const hasActiveFilters =
    setFilter !== DEFAULTS.set ||
    queueFilter !== DEFAULTS.queue ||
    dateFilter !== DEFAULTS.date ||
    rankFilter !== DEFAULTS.ranked ||
    serverFilter !== DEFAULTS.server;

  const resetFilters = () => {
    table?.getColumn("set")?.setFilterValue(undefined);
    table?.getColumn("queue")?.setFilterValue(undefined);
    table?.getColumn("date")?.setFilterValue(undefined);
    table?.getColumn("ranked")?.setFilterValue(undefined);
    table?.getColumn("server")?.setFilterValue(undefined);
    table?.setPageIndex(0);
  };

  return (
    <div className="flex flex-wrap items-center gap-2 rounded-lg">
      <Select
        value={setFilter}
        onValueChange={(value) => value ? updateFilter("set", value, DEFAULTS.set) : console.log("value is null")}
      >
        <SelectTrigger size="sm" className="w-[130px]">
          <div className="flex items-center gap-1.5 truncate">
            <Layers className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {setOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

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
        value={dateFilter}
        onValueChange={(value) => value ? updateFilter("date", value, DEFAULTS.date) : console.log("value is null")}
      >
        <SelectTrigger size="sm" className="w-[150px]">
          <div className="flex items-center gap-1.5 truncate">
            <CalendarDays className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {dateOptions.map((option) => (
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
