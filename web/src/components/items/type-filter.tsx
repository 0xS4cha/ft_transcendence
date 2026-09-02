import { useState } from "react";
import { Coins } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const typeOptions = [
  { value: "all", label: "All items" },
  { value: "normal", label: "Normal items" },
  { value: "artifact", label: "Artifact items" },
  { value: "radiant", label: "Radiant items" },
  { value: "emblem", label: "Emblem" },
  { value: "trait", label: "Trait items" },
] as const;

export function ItemsTypeFilter() {
  const [typeFilter, setTypeFilter] = useState("all");

  return (
    <div className="flex items-center">
      <Select
        value={typeFilter}
        onValueChange={setTypeFilter}
      >
        <SelectTrigger size="sm" className="w-[110px]">
          <div className="flex items-center gap-1.5 truncate">
            <Coins className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <SelectValue />
          </div>
        </SelectTrigger>
        <SelectContent>
          {typeOptions.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
