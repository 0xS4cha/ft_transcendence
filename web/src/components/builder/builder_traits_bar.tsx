import { cn } from "@/lib/utils";
import { Hexagon } from "lucide-react";

interface Trait {
  id: string;
  name: string;
  currentUnits: number;
  breakpoints: number[];
}

const FAKE_TRAITS: Trait[] = [
  { id: '1', name: 'selunite', currentUnits: 10, breakpoints: [1, 3, 5, 8, 10] },
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

export default function BuilderTraitsBar()
{
	return (
		<div className="flex h-full flex-col rounded-xl border border-white/10 bg-[#171717] px-3 py-3">
			<h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-neutral-400">
       	traits
      </h3>
      <ul className="flex flex-col gap-3 overflow-y custom-scrollbar">
        {FAKE_TRAITS.map((trait) => (
          <li
            key={trait.id}
            className={cn(
              "relative flex items-center gap-3 overflow-hidden rounded-lg px-3 py-2 shadow-sm transition-all",
              calculateTier(trait.currentUnits, trait.breakpoints) === 4 && "bg-gradient-to-r from-[#4E80EE] to-[#38E1FF] text-black",
              calculateTier(trait.currentUnits, trait.breakpoints) === 3 && "bg-gradient-to-r from-yellow-500 to-amber-400 text-black",
              calculateTier(trait.currentUnits, trait.breakpoints) === 2 && "bg-gradient-to-r from-slate-200 to-white text-black",
              calculateTier(trait.currentUnits, trait.breakpoints) === 1 && "bg-gradient-to-r from-amber-700 to-orange-500 text-white",
              calculateTier(trait.currentUnits, trait.breakpoints) === 0 && "border border-white/5 bg-white/[0.02] text-neutral-400"
            )}
          >
            <Hexagon 
              className={cn(
                "h-12 w-12 opacity-20 shrink-0",
                calculateTier(trait.currentUnits, trait.breakpoints) === 10 ? "text-white opacity-5" : "fill-black stroke-black"
              )} 
            />

            <div className={cn(
              "relative z-10 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold shadow-sm",
              calculateTier(trait.currentUnits, trait.breakpoints) === 10
                ? "bg-neutral-800 text-neutral-400" 
                : "bg-white text-black"
            )}>
              {trait.currentUnits}
            </div>

            <div className="relative z-10 flex flex-col overflow-hidden">
              <span className="text-[11px] font-bold uppercase tracking-wider leading-tight">
                {trait.name}
              </span>
              <span className={cn(
                "text-[9px] font-bold tracking-widest",
                calculateTier(trait.currentUnits, trait.breakpoints) === 10 ? "opacity-50" : "opacity-75"
              )}>
                {trait.breakpoints.join(' / ')}
              </span>
            </div>
          </li>
        ))}
      </ul>
		</div>
	)
}