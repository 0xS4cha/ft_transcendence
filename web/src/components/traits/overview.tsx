import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { TraitsTable } from "@/components/traits/table";
import { useRef } from "react";
import { type exportRef } from "@/types/stats"
import { useTranslation } from "react-i18next";

export function TraitsOverview() {
    const exportRef = useRef<exportRef>(null);
    const {t} = useTranslation();
    return (
        <Card>
            <CardHeader>
                <CardTitle>{t("table.listoftrait", "list of traits")}</CardTitle>
                <CardAction>
                    <Button variant="outline" onClick={() => exportRef.current?.export()}><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <TraitsTable ref={exportRef}/>
            </CardContent>
        </Card>
    );
};