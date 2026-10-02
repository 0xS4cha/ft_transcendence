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
import { useRef } from 'react';
import { toPng } from 'html-to-image'
import type { ItemRow } from "@/components/items/schema";
import type { UnitRow } from "@/components/units/schema";
import type { TraitRow } from "@/components/traits/schema";
import BuilderBoard from "@/components/builder/builder_boards"
import BuilderToolBar from "@/components/builder/builder_tool_bar";
import BuilderTraitsBar from "@/components/builder/builder_traits_bar";
import BuilderAugmentsBar from "@/components/builder/builder_augment_bar";
import BuilderChampionsBar from "@/components/builder/builder_champions_bar";
import BuilderTraitsBarMobile from "@/components/builder/builder_traits_bar_mobile";
import { getItemsStats, getTraitsStats, getUnitsStats } from "@/services/statsService";

export default function Builder() {

  const [boardState, setBoardState] = useState<Record<string, string>>({});
  const [activeDragId, setActiveDragId] = useState<string | null>(null);
  const [boardItems, setBoardItems] = useState<Record<string, string[]>>({});

  const [champions, setChampions] = useState<UnitRow[]>([]);
  const [items, setItems] = useState<ItemRow[]>([]);
  const [traits, setTraits] =useState<TraitRow[]>([]);

  const builderRef = useRef<HTMLDivElement>(null);

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
        delay: 100,
        tolerance: 5,
      },
    })
  );

  const handleDragStart = (event: DragStartEvent) => {
    setActiveDragId(event.active.id as string );
  };

  const handleClearBoard = () => {
    setBoardState({});
    setBoardItems({});
  };

  const handleDragEnd = (event: DragEndEvent) => {
    setActiveDragId(null);
    const { active, over } = event;
    const sourceId = active.id as string;
    
    const isItem = items.find(i => i.id === sourceId);
    if (isItem) {
      if (over) {
        const targetHex = over.id as string;
        if (boardState[targetHex]) {
          setBoardItems(prev => {
            const currentItems = prev[targetHex] || [];
            if (currentItems.length < 3) {
              return { ...prev, [targetHex]: [...currentItems, sourceId] };
            }
            return prev;
          });
        }
      }
      return;
    }
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
      if (sourceId.startsWith('hex-') && sourceId !== targetId) {
        setBoardItems((prev) => {
          const newItems = { ...prev };
          const sourceItems = newItems[sourceId];
          const targetItems = newItems[targetId];
          if (targetItems) {
            newItems[sourceId] = targetItems;
          } else {
            delete newItems[sourceId];
          }
          if (sourceItems) {
            newItems[targetId] = sourceItems;
          } else {
            delete newItems[targetId];
          }
          return newItems;
        });
      }

    } else {
      if (sourceId.startsWith('hex-')) {
        setBoardState((prev) => {
          const newState = { ...prev };
          delete newState[sourceId];
          return newState;
        });
        setBoardItems((prev) => {
          const newItems = { ...prev };
          delete newItems[sourceId];
          return newItems;
        });
      }
    }}

  const handleRemoveChampion = (hexId: string) => {
    setBoardState((prev) => {
      const newState = { ...prev };
      delete newState[hexId];
      return newState;
    });
    setBoardItems((prev) => {
      const newItems = { ...prev };
      delete newItems[hexId];
      return newItems;
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

  const handleCopycode = async () => {
    try {
      const compData = { boardState, boardItems};
      const jsonString = JSON.stringify(compData);
      const encodedCode = btoa(jsonString);
      await navigator.clipboard.writeText(encodedCode);
      alert("Code copied to clipboard !\n\n" + encodedCode)
    } catch (error)
    {
      console.error("Error while copying :", error);
      alert("Error: failed to copy the board\n");
    }
  }

  const handleImportCode = () => {
    const code = window.prompt("Paste the team here :");
    if (!code)
        return ;
    try {
      const JsonString = atob(code);
      const compData = JSON.parse(JsonString);
      if (compData.boardState)
      {
        setBoardState(compData.boardState);
        if (compData.boardItems)
          setBoardItems(compData.boardItems);
      }
      else {
        alert("Format is invalid.");
      }
    } catch (error)
    {
      console.error("Error while importing the comp :", error);
      alert("Format is invalid or we encountered an error, retry.");
    }
  }

  const handleScreenshot = async () => {
    if (builderRef.current === null)
      return ;
    try {
      const dataUrl =  await toPng(builderRef.current, { cacheBust: true, backgroundColor: '#202020'});
      const link = document.createElement('a');
      link.download = 'tft-comp-tactyx.png';
      link.href = dataUrl;
      link.click();
    } catch (error)
    {
      console.error("Can't create the screenshot", error);
      alert("failed to create the screnshot, retry");
    }
  }

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
        <BuilderToolBar onCopyCode={handleCopycode} onImportCode={handleImportCode} onScreenshot={handleScreenshot}/>
        <div className="grid grid-cols-1 lg:grid-cols-[0.8fr_3.3fr_0.8fr] gap-3 min-h-0 flex-1">
          <div className="hidden lg:flex flex-col min-w-0 min-h-0 max-h-125">
            <BuilderTraitsBar boardState={boardState} champions={champions} traits={traits} />
          </div>
          <div className="flex flex-col gap-3 min-w-0 min-h-0">
            <div className="flex items-center justify-center rounded-xl border border-white/10 flex-1 bg-[#202020]">
                <BuilderBoard boardState={boardState} champions={champions} onRemoveChampion={handleRemoveChampion} boardItems={boardItems} items={items}/>
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
              activeChampion.cost === 1 && "border-slate-500",
              activeChampion.cost === 2 && "border-emerald-500",
              activeChampion.cost === 3 && "border-blue-500",
              activeChampion.cost === 4 && "border-purple-500",
              activeChampion.cost === 5 && "border-yellow-500"
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