import { cn } from '@/lib/utils';
import { useDraggable } from '@dnd-kit/core';
import { CHAMPIONS_DB, type Champion } from '@/lib/champion';


function DraggableChampion({ champion, onClick }: { champion: Champion, onClick: () => void }) {
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
      src={champion.imageUrl}
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

export default function BuilderChampionsBar({ onAddChampionClick }: { onAddChampionClick: (id: string) => void }) {
  return (
    <div className="flex h-full w-full flex-col p-4 bg-[#202020]">
      <div className="mb-3 text-xs font-semibold uppercase tracking-wider text-neutral-400">
        Champions
      </div>

      <div className="flex-1 custom-scrollbar pr-2">
        <div className="grid grid-cols-[repeat(auto-fill,minmax(clamp(30px,8vw,70px),1fr))] gap-2.5">
          {CHAMPIONS_DB.map((champ) => (
            <DraggableChampion key={champ.id} champion={champ} onClick={() => onAddChampionClick(champ.id)}/>
          ))}
        </div>
      </div>
    </div>
  );
}
