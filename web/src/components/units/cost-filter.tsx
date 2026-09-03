import { useState } from "react";
import { Coins } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const costOptions = [
  { value: "all", label: "All Costs" },
  { value: "1", label: "1 Cost" },
  { value: "2", label: "2 Cost" },
  { value: "3", label: "3 Cost" },
  { value: "4", label: "4 Cost" },
  { value: "5", label: "5 Cost" },
] as const;

export function UnitsCostFilter() {
  const [costFilter, setCostFilter] = useState("all");

  return (
    <div className="flex items-center">
      <Select
        value={costFilter}
        onValueChange={(value) => value ? setCostFilter(value) : console.log("value is null")}
      >
        <SelectTrigger size="sm" className="w-[110px]">
          <div className="flex items-center gap-1.5 truncate">
            <Coins className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {costOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
