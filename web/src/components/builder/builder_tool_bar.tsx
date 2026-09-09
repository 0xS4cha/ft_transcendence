import { SelectDemo } from "./select_set";
import { Button } from "../ui/button";
import { Camera, Copy, Download } from "lucide-react";

export default function BuilderToolBar() {
  return (
    <div className="flex shrink-0 items-center justify-between gap-2 rounded-xl border border-white/10 px-3 py-2 bg-[#202020]">
      <div className="w-[120px] xl:w-[180px]">
        <SelectDemo/>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="secondary" className="text-white/55 px-2 xl:px-4">
          <span className="hidden xl:inline">Screenshot comp</span>
          <Camera className="h-4 w-4 xl:ml-2" />
        </Button>
        <Button variant="secondary" className="text-white/55 px-2 xl:px-4">
          <span className="hidden xl:inline">Copy code</span>
          <Copy className="h-4 w-4 xl:ml-2" />
        </Button>
        <Button variant="secondary" className="text-white/55 px-2 xl:px-4">
          <span className="hidden xl:inline">Import comp</span>
          <Download className="h-4 w-4 xl:ml-2" />
        </Button>
      </div>
    </div>
  )
}