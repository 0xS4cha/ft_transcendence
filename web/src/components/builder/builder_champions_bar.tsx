import { cn } from '@/lib/utils';
import { useDraggable } from '@dnd-kit/core';

interface Champion {
  id: string;
  name: string;
  cost: number;
  imageUrl: string;
}

const CHAMPIONS_DB: Champion[] = [
  { id: "akali", name: "Akali", cost: 4, imageUrl: "https://raw.communitydragon.org/8.4/game/assets/characters/akali/skins/base/4x_akali.png" },
  { id: "jinx", name: "Jinx", cost: 1, imageUrl: "https://raw.communitydragon.org/8.4/game/assets/characters/akali/skins/base/4x_akali.png" },
  { id: "ahri", name: "Ahri", cost: 4, imageUrl: "https://raw.communitydragon.org/8.4/game/assets/characters/akali/skins/base/4x_akali.png" },
  { id: "kennen", name: "Kennen", cost: 1, imageUrl: "https://raw.communitydragon.org/8.4/game/assets/characters/akali/skins/base/4x_akali.png" },
  { id: "ekko", name: "Ekko", cost: 3, imageUrl: "https://raw.communitydragon.org/8.4/game/assets/characters/akali/skins/base/4x_akali.png" },
  { id: "neeko", name: "Neeko", cost: 3, imageUrl: "https://raw.communitydragon.org/8.4/game/assets/characters/akali/skins/base/4x_akali.png" },
];

function DraggableChampion({ champion }: { champion: Champion }) {
  const { attributes, listeners, setNodeRef, transform , isDragging } = useDraggable({ id: champion.id });

  const style = transform ? {
    transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
    zIndex: 10,
  } : undefined;

  return (
    <button
      ref={setNodeRef as any}
      style={style}
      {...listeners}
      {...attributes}
      title={champion.name}
      className={cn(
        "relative flex aspect-square items-center justify-center overflow-hidden rounded-md border-2 bg-neutral-800 transition-all",
        isDragging ? "scale-110 opacity-90 shadow-2xl cursor-grabbing" : "cursor-grab hover:scale-105",
        champion.cost === 1 && "border-slate-400 hover:border-slate-200",
        champion.cost === 2 && "border-emerald-600 hover:border-emerald-400",
        champion.cost === 3 && "border-blue-500 hover:border-blue-300",
        champion.cost === 4 && "border-purple-500 hover:border-purple-300",
        champion.cost === 5 && "border-yellow-500 hover:border-yellow-300"
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

export default function BuilderChampionsBar() {
  return (
    <div className="flex h-full w-full flex-col p-4 bg-[#202020]">
      <div className="mb-3 text-xs font-semibold uppercase tracking-wider text-neutral-400">
        Champions
      </div>

      <div className="flex-1 custom-scrollbar pr-2">
        <div className="grid grid-cols-[repeat(auto-fill,minmax(48px,1fr))] gap-2.5">
          {CHAMPIONS_DB.map((champ) => (
            <DraggableChampion key={champ.id} champion={champ} />
          ))}
        </div>
      </div>
    </div>
  );
}
