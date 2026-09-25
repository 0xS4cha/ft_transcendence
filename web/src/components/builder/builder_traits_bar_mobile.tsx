import { cn } from "@/lib/utils";
import type { Unit } from "@/types/unit";
import { Hexagon } from "lucide-react";
import type { Trait } from "@/types/trait";

function calculateTier(currentUnits: number, breakpoints: number[]): number {
  if (currentUnits === 0) return 10;
  for (let i = breakpoints.length - 1; i >= 0; i--) {
    if (currentUnits >= breakpoints[i]) return i;
  }
  return 10; 
}

export default function BuilderTraitsBarMobile({ boardState , champions, traits }: {boardState: Record<string, string>, champions: Unit[], traits: Trait[]}) {
  
  const uniqueChampIds = Array.from(new Set(Object.values(boardState)));
  const traitCounts: Record<string, number> = {};

  uniqueChampIds.forEach((champId) => {
    const champ = champions.find((c) => c.id === champId);
    if (champ && champ.traits) {
      champ.traits.forEach((traitIdOrName) => {
        const key = traitIdOrName.toLowerCase(); 
        traitCounts[key] = (traitCounts[key] || 0) + 1;
      });
    }
  });

  const displayTraits = traits.map((trait) => {
    return {
      ...trait,
      currentUnits: traitCounts[trait.name.toLowerCase()] || 0
    };
  }).filter((trait) => trait.currentUnits > 0);

  displayTraits.sort((a, b) => b.currentUnits - a.currentUnits);
  return (
    <div className="flex w-full items-center gap-2 overflow-x-auto custom-scrollbar rounded-xl border border-white/10 px-3 py-2.5 bg-[#202020]">
      <span className="shrink-0 mr-2 text-[10px] font-semibold uppercase tracking-wider text-neutral-400 ">
        Traits
      </span>
      {displayTraits.map((trait) => {
        const tier = calculateTier(trait.currentUnits, trait.breakpoints);
        if (tier === 10) return null; 
        return (
          <div
            key={trait.id}
            className={cn(
              "flex shrink-0 items-center gap-1.5 rounded-md px-2 py-1 shadow-sm ",
              tier === 4 && "bg-linear-to-r from-[#4E80EE] to-[#38E1FF] text-black",
              tier === 3 && "bg-linear-to-r from-yellow-500 to-amber-400 text-black",
              tier === 2 && "bg-linear-to-r from-slate-200 to-white text-black",
              tier === 1 && "bg-linear-to-r from-amber-700 to-orange-500 text-white"
            )}
          >
            <Hexagon className="h-3 w-3 shrink-0 fill-black stroke-black" />
            <span className="text-[10px] font-bold">{trait.currentUnits}</span>
            <span className="text-[10px] font-bold uppercase tracking-wider truncate max-w-20">
              {trait.name}
            </span>
          </div>
        );
      })}
    </div>
  );
}