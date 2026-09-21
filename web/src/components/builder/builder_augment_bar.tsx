import { useState } from "react";
import { AUGMENTS_DB } from "@/lib/champion";
import { cn } from "@/lib/utils";

export default function BuilderAugmentsBar({ handleClearBoard }: { handleClearBoard: () => void }) {
  const [augments, setAugments] = useState<(string | null)[]>([null, null, null]);
  
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null);

  const openModal = (index: number) => setSelectedSlot(index);
  const closeModal = () => setSelectedSlot(null);

  const handleSelectAugment = (augmentId: string) => {
    if (selectedSlot !== null) {
      setAugments((prev) => {
        const newAugments = [...prev];
        newAugments[selectedSlot] = augmentId;
        return newAugments;
      });
      closeModal();
    }
  };

  return (
    <div className="flex flex-col gap-4 py-4 px-4 bg-[#202020] h-full w-full rounded-xl border border-white/10">
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
        {augments.map((augmentId, index) => {
          const augment = augmentId ? AUGMENTS_DB.find((a) => a.id === augmentId) : null;
          return (
            <button
              key={index}
              onClick={() => openModal(index)}
              className={cn(
                "relative flex aspect-square flex-1 items-center justify-center rounded-md border-2",
                augment
                  ? "border-neutral-500 bg-neutral-800"
                  : "border-dashed border-neutral-700 bg-neutral-800/50 hover:border-neutral-500 hover:bg-neutral-800"
              )}>
              {augment ? (<img
                  src={augment.imageUrl}
                  alt={augment.name}
                  className="h-full w-full object-cover p-1"/>) : (<span className="text-xl text-neutral-600">+</span>)}
            </button>
          );
        })}
      </div>
      {selectedSlot !== null && (
        <div className="fixed inset-0 z-9999 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div className="flex max-h-[80vh] w-full max-w-2xl flex-col rounded-xl border border-white/10 bg-[#202020] p-6 shadow-2xl">
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
              {AUGMENTS_DB.map((aug) => (
                <button
                  key={aug.id}
                  onClick={() => handleSelectAugment(aug.id)}
                  className="group flex flex-col 
                  items-center gap-2 transition-transform 
                  hover:scale-95 active:scale-95"
                  title={aug.name}>
                  <img
                    src={aug.imageUrl}
                    alt={aug.name}
                    className="aspect-square w-full
                    rounded-md border-2 border-transparent
                    object-cover transition-colors
                    group-hover:border-blue-500"/>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}