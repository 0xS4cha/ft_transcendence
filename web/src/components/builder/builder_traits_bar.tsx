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

export default function BuilderTraitsBar() {
  return (
    <div className="flex h-full w-full flex-col rounded-xl border border-white/10 py-3 bg-[#202020]">
      <h3 className="mx-auto px-2 mb-4 text-xs font-semibold uppercase tracking-wider text-neutral-400">
        traits
      </h3>
      <ul className="flex flex-col gap-2 overflow-y-auto custom-scrollbar px-1">
        {FAKE_TRAITS.map((trait) => {
          const tier = calculateTier(trait.currentUnits, trait.breakpoints);
          
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