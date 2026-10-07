import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { ItemsTable } from "@/components/items/table";
import { useRef, useState } from "react";
import { type exportRef } from "@/types/stats"
import { SelectContent, Select, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const FORMATS = [
  { value: "json", label: "JSON" },
  { value: "xml", label: "XML" },
] as const;

export function ItemsOverview() {
    const exportRef = useRef<exportRef>(null);
    const [exportFormat, setExportFormat] = useState<'json' | 'xml'>('json');
    
    const handleExport = () => {
    
        if (exportFormat === 'json') {
            exportRef.current?.exportJson();
        } else {
            exportRef.current?.exportXml();
        }
    };
    
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of items</CardTitle>
                <CardAction className="flex gap-2">
                    <Select value={exportFormat} onValueChange={(v) => v ? setExportFormat(v) : console.log("value is null")} >
                        <SelectTrigger
                        size="sm"
                        aria-label="Format d'export"
                        className="w-[100px] focus:z-10"
                        >
                        <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                        {FORMATS.map((f) => (
                            <SelectItem key={f.value} value={f.value}>{f.label}</SelectItem>
                        ))}
                        </SelectContent>
                    </Select>
                    <Button variant="outline" onClick={handleExport}><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <ItemsTable ref={exportRef}/>
            </CardContent>
        </Card>
    );
};