import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import type { AugmentRow } from "@/components/augments/schema";
import { useTranslation } from "react-i18next";

const getAugmentStyle = (tier?: number | string) => {
  const t = String(tier).toLowerCase();
  
  if (t === "1" || t === "silver") {
    return {
      fill: "linear-gradient(180deg, #AABACE 20%, #9FB4CE 50%, #6886A5 80%)",
      glow: "#477DCB",
    };
  }
  if (t === "2" || t === "gold") {
    return {
      fill: "linear-gradient(180deg, #DEBA31 20%, #E7BA1E 50%, #D69C31 80%)",
      glow: "#A18E21",
    };
  }
  if (t === "3" || t === "prismatic") {
    return {
      fill: "linear-gradient(180deg, #A887FF 10%, #8352FF 40%, #6800FF 70%)",
      glow: "#6838FF",
    };
  }
  
  return {
    fill: "linear-gradient(180deg, #737373 20%, #a3a3a3 50%, #404040 80%)",
    glow: "#737373",
  };
};

export default function BuilderAugmentsBar({ handleClearBoard, augments }: { handleClearBoard: () => void, augments: AugmentRow[] }) {
  const [selectedAugments, setSelectedAugments] = useState<(string | null)[]>([null, null, null]);
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null);
  const {t} = useTranslation();

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
    <>
      <svg width="0" height="0" className="absolute" aria-hidden="true">
        <filter id="s18-augment-tier-key" colorInterpolationFilters="sRGB" x="-25%" y="-25%" width="150%" height="150%">
          <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0.75 0.75 0.75 0 0" />
        </filter>
        <filter id="s18-augment-tier-glyph" colorInterpolationFilters="sRGB" x="-25%" y="-25%" width="150%" height="150%">
          <feColorMatrix type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" />
        </filter>
      </svg>

      <div className="flex flex-col gap-4 py-4 px-4 h-full w-full rounded-xl">
        <button
          onClick={handleClearBoard}
          className="w-full rounded-md bg-gray-400/10 px-4 py-3 text-sm font-medium text-white transition-colors hover:bg-gray-400/20 active:scale-95">
          {t("builder.board", "Clear the board")}
        </button>
        <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
          Augments
        </div>
        
        <div className="flex flex-row justify-between gap-2">
          {selectedAugments.map((augmentId, index) => {
            const augment = augmentId ? augments.find((a) => a.id === augmentId) : null;
            const activeStyle = augment ? getAugmentStyle(augment.rarity) : null;

            return (
              <button
                key={index}
                onClick={() => openModal(index)}
                className={cn(
                  "group relative flex aspect-square flex-1 items-center justify-center overflow-hidden rounded-md border-2",
                  augment
                    ? "border-neutral-500 bg-neutral-800"
                    : "border-dashed border-neutral-700 hover:border-neutral-500 hover:scale-95 transition-transform"
                )}>
                {augment && activeStyle ? (
                  <span
                    className="block aspect-square w-4/5 opacity-80 transition-transform duration-300 group-hover:scale-105"
                    style={{
                      backgroundImage: activeStyle.fill,
                      filter: `url(#s18-augment-tier-key) drop-shadow(0 0 4px ${activeStyle.glow})`,
                    }}
                  >
                    <img
                      src={augment.icon}
                      alt={augment.name}
                      draggable={false}
                      className="block h-full w-full mix-blend-multiply"
                      style={{ filter: "url(#s18-augment-tier-glyph)" }}
                    />
                  </span>
                ) : (
                  <span className="text-xl">+</span>
                )}
              </button>
            );
          })}
        </div>
        
        <button
          onClick={handleClearAugments}
          className="w-full rounded-md bg-gray-400/10 px-4 py-3 text-sm font-medium text-white transition-colors active:scale-95">
          {t("builder.clear", "Clear augments")}
        </button>
        {selectedSlot !== null && (
          <div className="fixed inset-0 z-9999 flex items-center justify-center p-4 backdrop-blur-sm bg-black/50" onClick={closeModal}>
            <div className="flex max-h-[80vh] w-full max-w-2xl flex-col rounded-xl border border-white/10 dark:bg-[#202020] bg-white p-6 shadow-2xl" onClick={(e) => e.stopPropagation()}>
              <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">Choose an augment</h2>
                <button onClick={closeModal} className="flex h-8 w-8 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20">
                  X
                </button>
              </div>

              <div className="grid flex-1 grid-cols-4 gap-4 overflow-y-auto custom-scrollbar pr-2 sm:grid-cols-5 md:grid-cols-6">
                {sortedAugments.map((aug) => {
                  const modalStyle = getAugmentStyle(aug.rarity);
                  return (
                    <button
                      key={aug.id}
                      onClick={() => handleSelectAugment(aug.id)}
                      className="group flex flex-col items-center gap-2 transition-transform hover:scale-95 active:scale-95"
                      title={aug.name}
                    >
                      <span
                        className="block aspect-square w-full opacity-80"
                        style={{
                          backgroundImage: modalStyle.fill,
                          filter: `url(#s18-augment-tier-key) drop-shadow(0 0 2px ${modalStyle.glow})`,
                        }}
                      >
                        <img
                          src={aug.icon}
                          alt={aug.name}
                          draggable={false}
                          className="block h-full w-full mix-blend-multiply"
                          style={{ filter: "url(#s18-augment-tier-glyph)" }}
                        />
                      </span>
                      <span className="text-center text-xs font-semibold text-neutral-800 dark:text-white leading-tight">
                        {aug.name}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}