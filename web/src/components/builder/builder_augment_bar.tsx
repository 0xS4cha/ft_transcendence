import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import type { AugmentRow } from "../augments/schema";

export default function BuilderAugmentsBar({ handleClearBoard, augments }: { handleClearBoard: () => void, augments: AugmentRow[] }) {
  const [selectedAugments, setSelectedAugments] = useState<(string | null)[]>([null, null, null]);
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null);

  const openModal = (index: number) => setSelectedSlot(index);
  const closeModal = () => setSelectedSlot(null);

  const handleSelectAugment = (augmentId: string) => {
    if (selectedSlot !== null) {
      setSelectedAugments((prev) => {
        const newAugments = [...prev];
        newAugments[selectedSlot] = augmentId;
        return newAugments;
      });
      closeModal();
    }
  };

  const handleClearAugments = () => {
    setSelectedAugments([null, null, null]);
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        closeModal();
      }
    };
    if (selectedSlot !== null) {
      window.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [selectedSlot]);

  const sortedAugments = [...augments].sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className="flex flex-col gap-4 py-4 px-4 h-full w-full rounded-xl border border-white/10">
      <button
        onClick={handleClearBoard}
        className="w-full rounded-md
         bg-gray-400/10 px-4 py-3 text-sm font-medium 
         text-white transition-colors hover:bg-gray-400/20 
         active:scale-95">
        Clear board
      </button>
      <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
        Augments
      </div>
      
      <div className="flex flex-row justify-between gap-2">
        {selectedAugments.map((augmentId, index) => {
          const augment = augmentId ? augments.find((a) => a.id === augmentId) : null;
          return (
            <button
              key={index}
              onClick={() => openModal(index)}
              className={cn(
                "group relative flex aspect-square flex-1 items-center justify-center overflow-hidden rounded-md border-2",
                augment
                  ? "border-neutral-500 bg-neutral-800"
                  : "border-dashed border-neutral-700 hover:border-neutral-500  hover:scale-95 transition-transform"
              )}>
              {augment ? (
              <>
                <img
                  src={augment.icon}
                  alt={augment.name}
                  className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-95 "
                />
                <span className="absolute bottom-1 w-[90%] rounded px-1 py-0.5 text-center text-[8px] leading-tight font-bold tracking-wider text-white">
                  {augment.name}
                </span>
              </> ) : (<span className="text-xl">+</span>)}
            </button>
          );
        })}
      </div>
      
      <button
        onClick={handleClearAugments}
        className="w-full rounded-md
         bg-gray-400/10 px-4 py-3 text-sm font-medium 
         text-white transition-colors  
         active:scale-95">
        Clear augments
      </button>

      {selectedSlot !== null && (
        <div className="fixed inset-0 z-9999 flex items-center justify-center p-4 backdrop-blur-sm"
        onClick={closeModal}>
          <div className="flex max-h-[80vh] w-full max-w-2xl flex-col rounded-xl border border-white/10 bg-white p-6 shadow-2xl"
          onClick={(e) => e.stopPropagation()}>
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">Choose an augment</h2>
              <button
                onClick={closeModal}
                className="flex h-8 w-8 items-center 
                justify-center rounded-full bg-white/10 
                text-white hover:bg-white/20">
                X
              </button>
            </div>
            <div className="grid flex-1 grid-cols-4 gap-4 overflow-y-auto custom-scrollbar pr-2 sm:grid-cols-5 md:grid-cols-6">
              {sortedAugments.map((aug) => (
                <button
                  key={aug.id}
                  onClick={() => handleSelectAugment(aug.id)}
                  className="group flex flex-col 
                  items-center gap-2 transition-transform 
                  hover:scale-95 active:scale-95"
                  title={aug.name}>
                  <img
                    src={aug.icon}
                    alt={aug.name}
                    className="aspect-square w-full
                    rounded-md border-2 border-transparent
                    object-cover transition-colors"/>
                    <span className="text-center text-xs font-semibold text-white transition-colors leading-tight">
                      {aug.name}
                    </span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}