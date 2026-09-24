import { cn } from '@/lib/utils';
import { useDraggable } from '@dnd-kit/core';
import type { Unit } from '@/types/unit';
import type { Item } from '@/types/item';

function DraggableChampion({ champion, onClick }: { champion: Unit, onClick: () => void }) {
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
        "border-slate-500",
        // cost === 2 && "border-emerald-500",
        // cost === 3 && "border-blue-500",
        // cost === 4 && "border-purple-500",
        // cost === 5 && "border-yellow-500"
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

function DraggableItem({ item, onClick }: { item: Item, onClick: () => void }) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({ id: item.id });

  return (
    <button
      ref={setNodeRef as any}
      {...listeners}
      {...attributes}
      onClick={onClick}
      title={item.name}
      className={cn(
        "relative flex aspect-square items-center justify-center overflow-hidden rounded-md border-2 bg-neutral-800 touch-pan-y",
        isDragging 
          ? "opacity-95" 
          : "cursor-pointer hover:scale-105",
        "border-slate-500",
        // cost === 2 && "border-emerald-500",
        // cost === 3 && "border-blue-500",
        // cost === 4 && "border-purple-500",
        // cost === 5 && "border-yellow-500"
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

export default function BuilderChampionsBar({ champions, items ,onAddChampionClick }: { champions: Unit[], items: Item[], onAddChampionClick: (id: string) => void }) {
  return (
    <div className="flex h-full w-full flex-row gap-6 p-4 bg-[#202020]">
      <div className="flex flex-1 flex-col min-w-0 overflow-hidden">
        <div className="mb-3 text-xs font-semibold uppercase tracking-wider text-neutral-400 shrink-0">
          Champions
        </div>
        <div className="flex-1 custom-scrollbar pr-2 overflow-y-auto min-h-0 p-1">
          <div className="grid grid-cols-[repeat(auto-fill,minmax(clamp(25px,8vw,45px),1fr))] gap-2.5">
            {champions.map((champ) => (
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
      <div className="flex flex-1 flex-col min-w-0 overflow-hidden">
        <div className="mb-3 text-xs font-semibold uppercase tracking-wider text-neutral-400 shrink-0">
          Items
        </div>
        <div className="flex-1 custom-scrollbar pr-2 overflow-y-auto min-h-0 p-1">
          <div className="grid grid-cols-[repeat(auto-fill,minmax(clamp(15px,8vw,40px),1fr))] gap-2.5">
            {items.map((item) => (
              <DraggableItem 
                key={item.id} 
                item={item} 
                onClick={() => onAddChampionClick(item.id)}
              />
            ))}
          </div>
        </div>
      </div>

    </div>
  );
}