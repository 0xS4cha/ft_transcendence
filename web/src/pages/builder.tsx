import { useState } from "react";
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

import BuilderBoard from "@/components/builder/builder_boards"
import BuilderChampionsBar from "@/components/builder/builder_champions_bar";
import BuilderToolBar from "@/components/builder/builder_tool_bar";
import BuilderTraitsBar from "@/components/builder/builder_traits_bar";
import BuilderTraitsBarMobile from "@/components/builder/builder_traits_bar_mobile";
import { CHAMPIONS_DB } from "@/lib/champion";
import { cn } from "@/lib/utils";
import BuilderAugmentsBar from "@/components/builder/builder_augment_bar";

export default function Builder() {

  const [boardState, setBoardState] = useState<Record<string, string>>({});
  const [activeChampionId, setActiveChampionId] = useState<string | null>(null);

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
    setActiveChampionId(event.active.id as string );
  };

  const handleClearBoard = () => {
    setBoardState({});
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveChampionId(null);
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

  let draggingChampId = activeChampionId;
  if (activeChampionId?.startsWith('hex-')) {
    draggingChampId = boardState[activeChampionId];
  }
  const activeChampion = draggingChampId ? CHAMPIONS_DB.find(c => c.id === draggingChampId) : null;

  return (
    <DndContext 
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      sensors={sensors}
      collisionDetection={pointerWithin}
    >
      <div className="flex h-[calc(100vh-3.9rem)] lg:h-[calc(100vh-3.9rem)] w-full max-w-375 mx-auto flex-col gap-3 overflow-hidden">
        <BuilderToolBar />
        <div className="grid grid-cols-1 lg:grid-cols-[0.8fr_3.3fr_0.8fr] gap-3 min-h-0 flex-1">
          <div className="hidden lg:block min-w-0">
            <BuilderTraitsBar />
          </div>
          <div className="flex flex-col gap-3 min-w-0 min-h-0">
            <div className="flex items-center justify-center rounded-xl border border-white/10 min-w-0 min-h-0 flex-1 bg-[#202020]">
                <BuilderBoard boardState={boardState} onRemoveChampion={handleRemoveChampion}/>
            </div>
            <div className="block lg:hidden">
              <BuilderTraitsBarMobile />
            </div>
          </div>
          
          <div className="hidden lg:flex flex-col rounded-xl border border-white/10 min-w-0 min-h-0">
            <BuilderAugmentsBar handleClearBoard={handleClearBoard}/>
          </div>
        </div>
        <div className="flex h-30 lg:h-110 shrink-0 rounded-xl border border-white/10 min-h-0">
          <BuilderChampionsBar onAddChampionClick={handleChampClick}/>
        </div>
      </div>
      <DragOverlay modifiers={[snapCenterToCursor]} dropAnimation={null}>
        {activeChampion ? (
          <div
          className={cn(
              "cursor-pointer flex items-center justify-center overflow-hidden bg-neutral-800 rounded-md border-2",
              "w-[clamp(35px,5vw,100px)] h-[clamp(35px,5vw,100px)]",
              activeChampion.cost === 1 && "border-slate-500",
              activeChampion.cost === 2 && "border-emerald-500",
              activeChampion.cost === 3 && "border-blue-500",
              activeChampion.cost === 4 && "border-purple-500",
              activeChampion.cost === 5 && "border-yellow-500"
            )}>
            <img
                src={activeChampion.imageUrl}
                alt={activeChampion.name}
                className="h-full w-full object-cover"
              />
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}