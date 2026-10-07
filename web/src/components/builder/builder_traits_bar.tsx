import { cn } from "@/lib/utils";
import type { UnitRow } from "../units/schema";
import type { TraitRow } from "../traits/schema";

function calculateTier(currentUnits: number, breakpoints: number[]): number {
  if (currentUnits === 0 || breakpoints.length === 0) return 10;

  if (breakpoints.length === 1 && breakpoints[0] === 1) {
    return currentUnits >= 1 ? 5 : 10;
  }

  for (let i = breakpoints.length - 1; i >= 0; i--) {
    if (currentUnits >= breakpoints[i]) {
      return i + 1;
    }
  }
  return 10;
}

export default function BuilderTraitsBar({ boardState, champions, traits }: { boardState: Record<string, string>, champions: UnitRow[], traits: TraitRow[] }) {
  
  const uniqueChampIds = Array.from(new Set(Object.values(boardState)));
  const traitCounts: Record<string, number> = {};

  uniqueChampIds.forEach((champId) => {
    const champ = champions.find((c) => c.id === champId);
    if (champ && Array.isArray(champ.traits)) {
      champ.traits.forEach((traitRaw: any) => {
        if (!traitRaw) return;
        const traitName = typeof traitRaw === 'string' ? traitRaw : (traitRaw.name || traitRaw.id);
        
        if (traitName) {
          const key = String(traitName).toLowerCase(); 
          traitCounts[key] = (traitCounts[key] || 0) + 1;
        }
      });
    }
  });

  const uniqueTraitsMap = new Map<string, TraitRow>();
  if (Array.isArray(traits)) {
    traits.forEach((trait) => {
      if (!trait || !trait.name) return; 
      
      const key = String(trait.name).toLowerCase();
      if (!uniqueTraitsMap.has(key)) {
        uniqueTraitsMap.set(key, trait);
      }
    });
  }

  const displayTraits = Array.from(uniqueTraitsMap.values()).map((trait) => {
    const safeName = trait && trait.name ? String(trait.name).toLowerCase() : "";
    return {
      ...trait,
      currentUnits: traitCounts[safeName] || 0
    };
  }).filter((trait) => trait.currentUnits > 0);

  displayTraits.sort((a, b) => {
    const tierA = calculateTier(a.currentUnits, a.breakpoints.map(Number));
    const tierB = calculateTier(b.currentUnits, b.breakpoints.map(Number));
    
    const weightA = tierA === 10 ? -1 : tierA;
    const weightB = tierB === 10 ? -1 : tierB;
    if (weightA !== weightB) {
      return weightB - weightA;
    }
    return b.currentUnits - a.currentUnits;
  });

  return (
    <div className="flex h-full w-full flex-col rounded-xl border border-white/10 py-3">
      <h3 className="mx-auto px-2 mb-4 text-xs font-semibold uppercase tracking-wider text-neutral-400 shrink-0">
        traits
      </h3>
      <ul className="min-h-0 flex-col gap-2 overflow-y-auto custom-scrollbar px-1">
        {displayTraits.map((trait) => {
          const tier = calculateTier(trait.currentUnits, trait.breakpoints.map(Number));
          return (
            <li
              key={trait.id}
              className={cn(
                "flex items-center gap-2 overflow-hidden rounded-lg px-2 py-1 shadow-sm transition-all w-[80%] mx-auto mb-1.5",
               tier === 5 && "bg-linear-to-r from-[rgba(232,173,255,0.6)] to-[rgba(41,44,75,0)] white:text-black text-white",
                tier === 4 && trait.name != "Invoker" && "bg-linear-to-r from-[#4E80EE] to-[#38E1FF] white:text-black text-white",
                  tier === 4 && trait.name == "Invoker" && "bg-linear-to-r from-[rgba(252,179,74,0.6)] to-[rgba(252,179,74,0)] text-white white:text-black ",
                tier === 3 && trait.name != "Invoker" && "bg-linear-to-r from-[rgba(252,179,74,0.6)] to-[rgba(252,179,74,0)] text-white white:text-black",
                tier === 3 && trait.name == "Invoker" && "bg-linear-to-r from-slate-200 to-white/10 white:text-black text-white",
                tier === 2 && "bg-linear-to-r from-slate-300 to-slate-250 white:from-slate-300 white:to-slate-200 white:text-black text-white",
                tier === 1 && "bg-linear-to-r from-[rgba(179,123,102,0.6)] to-[rgba(179,123,102,0)] white:text-black text-white",
                tier === 10 && "bg-linear-to-r from-black/10 to-white/10  dark:from-white/10 dark:to-black/10 white:text-black text-white"
              )}
            >
              <img 
                src={trait.icon} 
                alt={trait.name} 
                className={cn(
                  "h-6 w-6 shrink-0 object-contain drop-shadow-sm",
                  (tier === 2 || tier === 3 || tier === 4) ? "brightness-0" : "brightness-0 invert",
                  tier === 10 && "opacity-40"
                )} 
              />
              <div className={cn(
                "relative z-10 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[9px] font-bold shadow-sm",
                tier === 10
                  ? "bg-neutral-800 text-neutral-400" 
                  : "bg-black/90 text-neutral-400"
              )}>
                {trait.currentUnits}
              </div>
              
              <div className="relative z-10 flex min-w-0 flex-col overflow-hidden ml-0.5">
                <span className="truncate text-[10px] font-bold uppercase leading-tight tracking-wider">
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