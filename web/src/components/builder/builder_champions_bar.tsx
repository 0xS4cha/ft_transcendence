import { cn } from '@/lib/utils';
import { useDraggable } from '@dnd-kit/core';
import type { UnitRow } from '../units/schema';
import type { ItemRow } from '../items/schema';

function DraggableChampion({ champion, onClick }: { champion: UnitRow, onClick: () => void }) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({ id: champion.id });

  return (
    <button
      ref={setNodeRef as any}
      {...listeners}
      {...attributes}
      onClick={onClick}
      title={champion.name}
      className={cn(
        "relative flex aspect-square items-center justify-center overflow-hidden rounded-md border-2 bg-neutral-800 touch-pan-y",
        isDragging 
          ? "opacity-95" 
          : "cursor-pointer hover:scale-105",
        champion.cost === 1 && "border-slate-500",
        champion.cost === 2 && "border-emerald-500",
        champion.cost === 3 && "border-blue-500",
        champion.cost === 4 && "border-purple-500",
        champion.cost === 5 && "border-yellow-500"
      )}
    >
      <img
        src={champion.icon}
        alt={champion.name}
        loading="lazy"
        decoding="async"
        className="h-full w-full object-cover"
        onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
        }}
      />
    </button>
  );
}

function DraggableItem({ item}: { item: ItemRow}) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({ id: item.id });

  return (
    <button
      ref={setNodeRef as any}
      {...listeners}
      {...attributes}
      title={item.name}
      className={cn(
        "relative flex aspect-square items-center justify-center overflow-hidden rounded-md bg-neutral-800 touch-pan-y",
        isDragging 
          ? "opacity-95" 
          : "cursor-pointer hover:scale-105",
        item.type === "Artifact" ? "border border-red-600" :
        item.type === "Radiant"  ? "border border-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.5)]" :
        null
      )}
    >
      <img
        src={item.icon}
        alt={item.name}
        loading="lazy"
        decoding="async"
        className="h-full w-full object-cover"
        onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
        }}
      />
    </button>
  );
}

export default function BuilderChampionsBar({ champions, items ,onAddChampionClick }: { champions: UnitRow[], items: ItemRow[], onAddChampionClick: (id: string) => void }) {
  
  const groupedItems = [
    { 
      title: "Items", 
      items: items.filter(i => i.type?.toLowerCase() === "normal" || i.type?.toLowerCase() === "normal-component") 
    },
    { 
      title: "Artifacts", 
      items: items.filter(i => i.type?.toLowerCase() === "artifact") 
    },
    { 
      title: "Radiants", 
      items: items.filter(i => i.type?.toLowerCase() === "radiant") 
    },
    { 
      title: "Emblems", 
      items: items.filter(i => i.type?.toLowerCase() === "emblem") 
    },
    { 
      title: "Components", 
      items: items.filter(i => i.type?.toLowerCase() === "component") 
    }
  ];
  groupedItems.forEach(group => {
    group.items.sort((a, b) => a.name.localeCompare(b.name));
  });
  const displayItemGroups = groupedItems.filter(group => group.items.length > 0);
  
  const groupedChampions = [
    { title: "Cost 1", champions: champions.filter(c => c.cost === 1) },
    { title: "Cost 2", champions: champions.filter(c => c.cost === 2) },
    { title: "Cost 3", champions: champions.filter(c => c.cost === 3) },
    { title: "Cost 4", champions: champions.filter(c => c.cost === 4) },
    { title: "Cost 5", champions: champions.filter(c => c.cost === 5) }
  ];

  groupedChampions.forEach(group => {
    group.champions.sort((a, b) => a.name.localeCompare(b.name));
  });

  const sortedChampions = [...champions].sort((a, b) => {
    if (a.cost !== b.cost) {
      return a.cost - b.cost;
    }
    return a.name.localeCompare(b.name);
  })

  return (
    <div className="flex h-full w-full flex-row gap-6 p-4 bg-[#202020]">
      <div className="flex flex-1 flex-col min-w-0 overflow-hidden">
        <div className="mb-3 text-xs font-semibold uppercase tracking-wider text-neutral-400 shrink-0">
          Champions
        </div>
        <div className="flex-1 custom-scrollbar pr-2 overflow-y-auto min-h-0 p-1">
          <div className="grid grid-cols-[repeat(auto-fill,minmax(clamp(25px,8vw,45px),1fr))] gap-2.5 pb-2">
            {sortedChampions.map((champ) => (
              <DraggableChampion 
                key={`champ-${champ.id}`} 
                champion={champ} 
                onClick={() => onAddChampionClick(champ.id)}
              />
            ))}
            
          </div>
          
        </div>
      </div>
      <div className="w-0.5 shrink-0 bg-white/10 hidden md:block"></div>
        <div className="flex-1 custom-scrollbar pr-3 overflow-y-auto min-h-0">
          <div className="flex flex-col gap-4 pb-2 pr-1">
            {displayItemGroups.map((group) => (
              <div key={group.title} className="flex flex-col gap-2 p-1">
                <div className="text-[10px] font-bold uppercase tracking-widest text-neutral-400 pb-1">
                  {group.title}
                </div>
                <div className="grid grid-cols-[repeat(auto-fill,minmax(clamp(15px,8vw,30px),1fr))] gap-2.5">
                  {group.items.map((item) => (
                    <DraggableItem
                      key={`item-${item.id}`} 
                      item={item} 
                    />
                  ))}
                </div>
                
              </div>
            ))}
        </div>
      </div>

    </div>
  );
}