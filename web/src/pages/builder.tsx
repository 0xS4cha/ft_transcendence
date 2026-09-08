import BuilderToolBar from "@/components/builder/builder_tool_bar";
import BuilderTraitsBar from "@/components/builder/builder_traits_bar";

export default function Builder() {
  return (
    <div className="flex flex-col gap-6 h-[calc(100vh-4rem)]">
      <BuilderToolBar />
      <div className="grid grid-cols-[220px_1fr_240px] gap-6 min-h-0 flex-1">
        <BuilderTraitsBar />
        <div className="flex items-center justify-center rounded-xl border border-white/10 bg-[#171717]">
            <span className="text-neutral-500">
              Le plus dur ici mdr
              </span>
        </div>
        <div className="flex flex-col rounded-xl border border-white/10 bg-[#171717]">
        </div>
      </div>
      <div className="h-128 shrink-0 rounded-xl border border-white/10 bg-[#171717]">
      </div>
    </div>
  );
}