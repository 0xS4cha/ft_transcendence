import { useState } from "react";
import { 
  DndContext, 
  type DragEndEvent,
  type DragStartEvent,
  DragOverlay,
  useSensor, 
  useSensors, 
  PointerSensor 
} from "@dnd-kit/core";
import { snapCenterToCursor } from '@dnd-kit/modifiers';

import BuilderBoard from "@/components/builder/builder_boards"
import BuilderChampionsBar from "@/components/builder/builder_champions_bar";
import BuilderToolBar from "@/components/builder/builder_tool_bar";
import BuilderTraitsBar from "@/components/builder/builder_traits_bar";
import BuilderTraitsBarMobile from "@/components/builder/builder_traits_bar_mobile";
import { CHAMPIONS_DB } from "@/lib/champion";

export default function Builder() {

  const [boardState, setBoardState] = useState<Record<string, string>>({});

  const [activeChampionId, setActiveChampionId] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 6,
      },
    })
  );
  const handleDragStart = (event: DragStartEvent) => {
    setActiveChampionId(event.active.id as string );
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveChampionId(null);
    const { active, over } = event;
    if (over){
      setBoardState((prev) => ({
        ...prev,
        [over.id]: active.id as string,
      }))
    }
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

  const activeChampion = activeChampionId 
    ? CHAMPIONS_DB.find(c => c.id === activeChampionId) 
    : null;
  return (
    <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd} sensors={sensors}>
    <div className="flex h-[calc(100vh-3.9rem)] flex-col gap-4 overflow-hidden">
      <BuilderToolBar />
      <div className="grid grid-cols-1 lg:grid-cols-[195px_1fr_195px] gap-4 min-h-0 flex-1">
        <div className="hidden lg:block min-w-0">
          <BuilderTraitsBar />
        </div>
        <div className="flex flex-col gap-4 min-w-0 min-h-0">
          <div className="flex items-center justify-center rounded-xl border border-white/10  min-w-0 min-h-0 flex-1">
              <BuilderBoard boardState={boardState}/>
          </div>
          <div className="block lg:hidden">
            <BuilderTraitsBarMobile />
          </div>
        </div>
        <div className="hidden lg:flex flex-col rounded-xl border border-white/10  min-w-0 min-h-0">
        </div>
      </div>
      <div className="h-[28%] shrink-0 rounded-xl border border-white/10  min-h-0">
        <BuilderChampionsBar onAddChampionClick={handleChampClick}/>
      </div>
    </div>
    <DragOverlay modifiers={[snapCenterToCursor]} dropAnimation={null}>
      {activeChampion ? (
        <div className="cursor-pointer flex h-14 w-14 items-center justify-center overflow-hidden bg-neutral-800 shadow-2xl opacity-90 scale-110">
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