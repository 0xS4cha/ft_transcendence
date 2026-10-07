import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { UnitsTable } from "@/components/units/table";
import { useRef } from "react";
import { type exportRef } from "@/types/stats"
import { useTranslation } from "react-i18next";

export function UnitsOverview() {
    const {t} = useTranslation();
    const exportRef = useRef<exportRef>(null);
    return (
        <Card>
            <CardHeader>
                <CardTitle>{t("table.listof", "List of units")}</CardTitle>
                <CardAction>
                    <Button variant="outline" onClick={() => exportRef.current?.export()}><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <UnitsTable ref={exportRef}/>
            </CardContent>
        </Card>
    );
};