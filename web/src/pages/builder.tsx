import BuilderBoard from "@/components/builder/builder_boards"
import BuilderToolBar from "@/components/builder/builder_tool_bar";
import BuilderTraitsBar from "@/components/builder/builder_traits_bar";
import BuilderTraitsBarMobile from "@/components/builder/builder_traits_bar_mobile";

export default function Builder() {
  return (
    <div className="flex h-[calc(100vh-3.9rem)] flex-col gap-4 overflow-hidden">
      <BuilderToolBar />
      <div className="grid grid-cols-1 lg:grid-cols-[195px_1fr_195px] gap-4 min-h-0 flex-1">
        <div className="hidden lg:block min-w-0">
          <BuilderTraitsBar />
        </div>
        <div className="flex flex-col gap-4 min-w-0 min-h-0">
          <div className="flex items-center justify-center rounded-xl border border-white/10 bg-[#171717] min-w-0 min-h-0 flex-1">
              <BuilderBoard />
          </div>
          <div className="block lg:hidden">
            <BuilderTraitsBarMobile />
          </div>
        </div>
        <div className="hidden lg:flex flex-col rounded-xl border border-white/10 bg-[#171717] min-w-0 min-h-0">
        </div>
      </div>
      <div className="h-[28%] shrink-0 rounded-xl border border-white/10 bg-[#171717] min-h-0">
      </div>
    </div>
  );
}