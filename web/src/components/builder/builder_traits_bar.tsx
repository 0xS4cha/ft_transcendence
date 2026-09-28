import { cn } from "@/lib/utils";
import { Hexagon } from "lucide-react";
import type { Unit } from "@/types/unit";
import type { Trait } from "@/types/trait";

function calculateTier(currentUnits: number, breakpoints: number[]): number {
  if (currentUnits === 0)
    return 10;
  for (let i = breakpoints.length - 1; i >= 0; i--) 
  {
    if (currentUnits >= breakpoints[i]) {
      return i;
    }
  }
  return 10; 
}

export default function BuilderTraitsBar({ boardState , champions, traits }: {boardState: Record<string, string>, champions: Unit[], traits: Trait[]}) {
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

  const uniqueTraitsMap = new Map<string, Trait>();
  traits.forEach((trait) => {
    const key = trait.name.toLowerCase();
    if (!uniqueTraitsMap.has(key)) {
      uniqueTraitsMap.set(key, trait);
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
    <div className="flex h-full w-full flex-col rounded-xl border border-white/10 py-3 bg-[#202020]">
      <h3 className="mx-auto px-2 mb-4 text-xs font-semibold uppercase tracking-wider text-neutral-400">
        traits
      </h3>
      <ul className="flex flex-col gap-2 overflow-y-auto custom-scrollbar px-1">
        {displayTraits.map((trait) => {
          const tier = calculateTier(trait.currentUnits, trait.breakpoints.map(Number));
          
          return (
            <li
              key={trait.id}
              className={cn(
                "flex items-center gap-1 overflow-hidden rounded-lg px-0.5 py-0.5 shadow-sm transition-all w-[75%] mx-auto",
                tier === 4 && "bg-linear-to-r from-[#4E80EE] to-[#38E1FF] text-black",
                tier === 3 && "bg-linear-to-r from-yellow-500 to-amber-400 text-black",
                tier === 2 && "bg-linear-to-r from-slate-200 to-white text-black",
                tier === 1 && "bg-linear-to-r from-amber-700 to-orange-500 text-white",
                tier === 10 && "border border-white/5 bg-white/2 text-neutral-400"
              )}
            >
              <Hexagon 
                className={cn(
                  "h-10 w-10 shrink-0 opacity-20",
                  tier === 10 ? "text-white opacity-5" : "fill-black stroke-black"
                )} 
              />
              <div className={cn(
                "relative z-10 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[9px] font-bold shadow-sm",
                tier === 10
                  ? "bg-neutral-800 text-neutral-400" 
                  : "bg-white text-black"
              )}>
                {trait.currentUnits}
              </div>
              <div className="relative z-10 flex min-w-0 flex-col overflow-hidden">
                <span className="truncate text-[9px] font-bold uppercase leading-tight tracking-wider">
                  {trait.name}
                </span>
                <span className={cn(
                  "truncate text-[9px] font-bold tracking-widest",
                  tier === 10 ? "opacity-50" : "opacity-75"
                )}>
                  {trait.breakpoints.join(' / ')}
                </span>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  )
}