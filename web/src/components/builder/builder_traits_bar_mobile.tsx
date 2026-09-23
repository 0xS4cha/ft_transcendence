import { cn } from "@/lib/utils";
import { Hexagon } from "lucide-react";

interface Trait {
  id: string;
  name: string;
  currentUnits: number;
  breakpoints: number[];
}

const FAKE_TRAITS: Trait[] = [
  { id: '1', name: 'selunite', currentUnits: 9, breakpoints: [1, 3, 5, 8, 10] },
  { id: '2', name: 'avatar', currentUnits: 7, breakpoints: [1, 3, 5, 7] },
  { id: '3', name: 'fleur spirituel', currentUnits: 5, breakpoints: [1, 3, 5, 7, 9] },
  { id: '4', name: 'chasseur', currentUnits: 3, breakpoints: [1, 3, 6] },
  { id: '5', name: 'caustique', currentUnits: 1, breakpoints: [1, 3, 5, 7] },
  { id: '6', name: 'caca', currentUnits: 0, breakpoints: [3] },
];

function calculateTier(currentUnits: number, breakpoints: number[]): number {
  if (currentUnits === 0) return 10;
  for (let i = breakpoints.length - 1; i >= 0; i--) {
    if (currentUnits >= breakpoints[i]) return i;
  }
  return 10; 
}

export default function BuilderTraitsBarMobile() {
  return (
    <div className="flex w-full items-center gap-2 overflow-x-auto custom-scrollbar rounded-xl border border-white/10 px-3 py-2.5 bg-[#202020]">
      <span className="shrink-0 mr-2 text-[10px] font-semibold uppercase tracking-wider text-neutral-400 ">
        Traits
      </span>
      {FAKE_TRAITS.map((trait) => {
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