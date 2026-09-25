import { useEffect, useState } from "react";
import { 
  DndContext, 
  type DragEndEvent,
  type DragStartEvent,
  DragOverlay,
  useSensor, 
  useSensors, 
  MouseSensor,
  TouchSensor,
  pointerWithin
} from "@dnd-kit/core";
import { snapCenterToCursor } from '@dnd-kit/modifiers';

import { cn } from "@/lib/utils";
import type { Unit } from "@/types/unit";
import type { Item } from "@/types/item";
import type { Trait } from "@/types/trait";
import BuilderBoard from "@/components/builder/builder_boards"
import BuilderToolBar from "@/components/builder/builder_tool_bar";
import BuilderTraitsBar from "@/components/builder/builder_traits_bar";
import { getItemsStats, getUnitsStats } from "@/services/statsService";
import BuilderAugmentsBar from "@/components/builder/builder_augment_bar";
import BuilderChampionsBar from "@/components/builder/builder_champions_bar";
import BuilderTraitsBarMobile from "@/components/builder/builder_traits_bar_mobile";

export default function Builder() {

  const [boardState, setBoardState] = useState<Record<string, string>>({});
  const [activeDragId, setActiveDragId] = useState<string | null>(null);
  const [boardItems, setBoardItems] = useState<Record<string, string[]>>({});

  const [champions, setChampions] = useState<Unit[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [traits, setTraits] =useState<Trait[]>([]);

  useEffect(() => {
    const fetchChampions = async () => {
      try {
        const result = await getUnitsStats();
        setChampions(result);
      } catch (error) {
        console.error("Error while fetching champs", error);
      }
    };
    fetchChampions();
  }, []);

  useEffect(() => {
    const fetchChampions = async () => {
      try {
        const result = await getItemsStats();
        setItems(result);
      } catch (error) {
        console.error("Error while fetching champs", error);
      }
    };
    fetchChampions();
  }, []);

  useEffect(() => {
    const fetchTraits = async () => {
      try {
        const result = await getTraitsStats();
        setTraits(result);
      } catch (error) {
        console.error("Error while fetching traits", error);
      }
    };
    fetchTraits()
  }, []);

  const sensors = useSensors(
    useSensor(MouseSensor, {
      activationConstraint: {
        distance: 6,
      },
    }),
    useSensor(TouchSensor, {
      activationConstraint: {
        delay: 50,
        tolerance: 5,
      },
    })
  );

  const handleDragStart = (event: DragStartEvent) => {
    setActiveDragId(event.active.id as string );
  };

  const handleClearBoard = () => {
    setBoardState({});
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveDragId(null);
    const { active, over } = event;
    const sourceId = active.id as string;
    if (over) {
      const targetId = over.id as string;
      setBoardState((prev) => {
        const newState = { ...prev };
        
        const champId = sourceId.startsWith('hex-') ? prev[sourceId] : sourceId;
        if (sourceId.startsWith('hex-') && sourceId !== targetId) {
          if (newState[targetId]) {
            newState[sourceId] = newState[targetId];
          } else {
            delete newState[sourceId];
          }
        }
        newState[targetId] = champId;
        return newState;
      });
    } else {
      if (sourceId.startsWith('hex-')) {
        setBoardState((prev) => {
          const newState = { ...prev };
          delete newState[sourceId];
          return newState;
        });
      }
    }
  };

  const handleRemoveChampion = (hexId: string) => {
    setBoardState((prev) => {
      const newState = { ...prev };
      delete newState[hexId];
      return newState;
    });
  };

  const handleChampClick = (championId: string) => {
    for (let row = 0; row < 4; row++)
    {
      for (let col = 0; col < 7; col++)
      {
        const hexId = `hex-${row}-${col}`;
        if (!boardState[hexId])
        {
          setBoardState((prev) => ({
            ...prev,
            [hexId]: championId
        }));
        return;
        }
      }
    }
  };

  let draggingChampId = activeDragId;
  if (activeDragId?.startsWith('hex-')) {
    draggingChampId = boardState[activeDragId];
  }
  const activeChampion = draggingChampId ? champions.find(c => c.id === draggingChampId) : null;
  const activeItem = activeDragId ? items.find(i => i.id === activeDragId) : null
  return (
    <DndContext 
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      sensors={sensors}
      collisionDetection={pointerWithin}
    >
      <div className="flex  w-full max-w-375 mx-auto flex-col gap-3 overflow-hidden">
        <BuilderToolBar />
        <div className="grid grid-cols-1 lg:grid-cols-[0.8fr_3.3fr_0.8fr] gap-3 min-h-0 flex-1">
          <div className="hidden lg:block min-w-0">
            <BuilderTraitsBar boardState={boardState} champions={champions} traits={traits} />
          </div>
          <div className="flex flex-col gap-3 min-w-0 min-h-0">
            <div className="flex items-center justify-center rounded-xl border border-white/10 flex-1 bg-[#202020]">
                <BuilderBoard boardState={boardState} champions={champions} onRemoveChampion={handleRemoveChampion} boardStateItem={boardItems}/>
            </div>
            <div className="block lg:hidden ">
              <BuilderTraitsBarMobile boardState={boardState} champions={champions} traits={traits} />
            </div>
          </div>
          
          <div className="hidden lg:flex flex-col rounded-xl border border-white/10 min-w-0 min-h-0">
            <BuilderAugmentsBar handleClearBoard={handleClearBoard}/>
          </div>
        </div>
        <div className="flex rounded-xl border border-white/10">
          <BuilderChampionsBar champions={champions}  items={items} onAddChampionClick={handleChampClick}/>
        </div>
      </div>
      <DragOverlay modifiers={[snapCenterToCursor]} dropAnimation={null}>
        {activeChampion ? (
          <div
          className={cn(
              "cursor-pointer flex items-center justify-center overflow-hidden bg-neutral-800 rounded-md border-2",
              "w-[clamp(40px,8vw,100px)] h-[clamp(40px,8vw,100px)]",
              "border-slate-500"
              // activeChampion.cost === 1 && "border-slate-500",
              // activeChampion.cost === 2 && "border-emerald-500",
              // activeChampion.cost === 3 && "border-blue-500",
              // activeChampion.cost === 4 && "border-purple-500",
              // activeChampion.cost === 5 && "border-yellow-500"
            )}>
            <img
                src={activeChampion.icon}
                alt={activeChampion.name}
                className="h-full w-full object-cover"
              />
          </div>
        ) : null}
        {activeItem ? (
          <div className={cn(
            "w-[clamp(20px,8vw,35px)] h-[clamp(20px,8vw,35px)]",
            "cursor-pointer flex items-center justify-center overflow-hidden bg-neutral-800 rounded-md",
            activeItem.type === "Artifact" ? "border border-red-600" :
            activeItem.type === "Radiant"  ? "border border-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.5)]" :
            null
          )}>
            <img src={activeItem.icon} alt={activeItem.name} className="h-full w-full object-cover" />
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}