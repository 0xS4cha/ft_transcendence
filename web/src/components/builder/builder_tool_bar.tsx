import { SelectDemo } from "./select_set";
import { Button } from "../ui/button";
import { Camera, Copy, Download } from "lucide-react";

export default function BuilderToolBar()
{
	return (
		<div className="flex items-left rounded-xl border border-white/10 bg-[#171717] px-2 py-2">
      <div>
        <SelectDemo/>
      </div>

      <div className="px-3 flex items-center gap-3">
			  <Button variant="secondary" className="text-white/55">
				  Screenshot comp
				  <Camera/>
			  </Button>
			  <Button variant="secondary" className="text-white/55">
				  Copy code
				  <Copy/>
			  </Button>
			  <Button variant="secondary" className="text-white/55">
				  Import comp
				  <Download/>
			  </Button>
      </div>
		</div>
	)
}