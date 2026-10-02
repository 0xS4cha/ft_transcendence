import { cn } from "@/lib/utils";
import type { TraitRow } from "../traits/schema";
import type { UnitRow } from "../units/schema";

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

export default function BuilderTraitsBarMobile({ boardState , champions, traits }: {boardState: Record<string, string>, champions: UnitRow[], traits: TraitRow[]}) {
  
  const uniqueChampIds = Array.from(new Set(Object.values(boardState)));
  const traitCounts: Record<string, number> = {};

  uniqueChampIds.forEach((champId) => {
    const champ = champions.find((c) => c.id === champId);
    if (champ && champ.traits) {
      champ.traits.forEach((traitRaw: any) => {
        if (!traitRaw) return;
        const traitName = typeof traitRaw === 'string' ? traitRaw : traitRaw.name || traitRaw.id;
        if (traitName && typeof traitName === 'string') {
          const key = traitName.toLowerCase(); 
          traitCounts[key] = (traitCounts[key] || 0) + 1;
        }
      });
    }
  });

  const uniqueTraitsMap = new Map<string, TraitRow>();
  traits.forEach((trait) => {
    const key = trait.name.toLowerCase();
    if (!uniqueTraitsMap.has(key)) {
      uniqueTraitsMap.set(key, trait);
    }
  });

  const displayTraits = Array.from(uniqueTraitsMap.values()).map((trait) => {
    return {
      ...trait,
      currentUnits: traitCounts[trait.name.toLowerCase()] || 0
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
    <div className="flex w-full items-center gap-2 overflow-x-auto custom-scrollbar rounded-xl border border-white/10 px-3 py-2.5 bg-[#202020]">
      <span className="shrink-0 mr-1 text-[10px] font-semibold uppercase tracking-wider text-neutral-400">
        Traits
      </span>
      {displayTraits.map((trait) => {
        const tier = calculateTier(trait.currentUnits, trait.breakpoints.map(Number));
        return (
          <div
            key={trait.id}
            className={cn(
              "flex shrink-0 items-center gap-1.5 rounded-md px-2 py-1 shadow-sm transition-all border border-white/5",
              tier === 5 && "bg-linear-to-r from-[rgba(239,198,255,0.6)] to-[rgba(41,44,75,0)] text-white border-[rgba(239,198,255,0.3)]",
              tier === 4 && trait.name !== "Invoker" && "bg-linear-to-r from-[#4E80EE] to-[#38E1FF] text-white",
              tier === 4 && trait.name === "Invoker" && "bg-linear-to-r from-[rgba(252,179,74,0.6)] to-[rgba(252,179,74,0)] text-white",
              tier === 3 && trait.name !== "Invoker" && "bg-linear-to-r from-[rgba(252,179,74,0.6)] to-[rgba(252,179,74,0)] text-white border-[rgba(252,179,74,0.3)]",
              tier === 3 && trait.name === "Invoker" && "bg-linear-to-r from-slate-200 to-white/10 text-white",
              tier === 2 && "bg-linear-to-r from-slate-200 to-white/10 text-white border-[rgba(191,192,225,0.3)]",
              tier === 1 && "bg-linear-to-r from-[rgba(179,123,102,0.6)] to-[rgba(179,123,102,0)] text-white border-[rgba(179,123,102,0.3)]",
              tier === 10 && "bg-linear-to-r from-white/10 to-white/1 text-white"
            )}
          >
            <img 
              src={trait.icon} 
              alt={trait.name} 
              className={cn(
                "h-3.5 w-3.5 shrink-0 object-contain",
                (tier === 2 || tier === 3 || tier === 4) ? "brightness-0" : "brightness-0 invert",
                tier === 10 && "opacity-50"
              )} 
            />
            
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