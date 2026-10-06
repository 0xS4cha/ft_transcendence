import { SelectDemo } from "./select_set";
import { Button } from "../ui/button";
import { Copy, Download } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function BuilderToolBar({ onCopyCode, onImportCode }: {onCopyCode?: () => void, onImportCode?: () => void}) {
  const { t } = useTranslation();

  return (
    <div className="flex shrink-0 items-center justify-between gap-2 rounded-xl border border-white/10 px-3 py-2 bg-[#202020]">
      <div className="w-30 xl:w-45">
        <SelectDemo/>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="secondary" className="text-white/55 px-2 xl:px-4" onClick={onCopyCode}>
          <span className="hidden xl:inline">{t('builder.copyCode')}</span>
          <Copy className="h-4 w-4 xl:ml-2" />
        </Button>
        <Button variant="secondary" className="text-white/55 px-2 xl:px-4" onClick={onImportCode}>
          <span className="hidden xl:inline">{t('builder.importComp')}</span>
          <Download className="h-4 w-4 xl:ml-2" />
        </Button>
      </div>
    </div>
  )
}