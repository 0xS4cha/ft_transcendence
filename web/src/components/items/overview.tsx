import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { ItemsTable } from "@/components/items/table";
import { useRef } from "react";
import { type exportRef } from "@/types/stats"
import { useTranslation } from "react-i18next";

export function ItemsOverview() {
    const {t} = useTranslation();
    const exportRef = useRef<exportRef>(null);
    return (
        <Card>
            <CardHeader>
                <CardTitle>{t("table.list", "List of items")}</CardTitle>
                <CardAction>
                    <Button variant="outline" onClick={() => exportRef.current?.export()}><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <ItemsTable ref={exportRef}/>
            </CardContent>
        </Card>
    );
};