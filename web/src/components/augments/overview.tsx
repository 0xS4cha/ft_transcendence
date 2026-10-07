import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { AugmentsTable } from "@/components/augments/table";
import { useRef } from "react";
import { type exportRef } from "@/types/stats"
import { useTranslation } from "react-i18next";

export function AugmentsOverview() {
    const exportRef = useRef<exportRef>(null);
    const {t} = useTranslation();
    return (
        <Card>
            <CardHeader>
                <CardTitle>{t("table.listofaug", "List of augments")}</CardTitle>
                <CardAction>
                    <Button variant="outline" onClick={() => exportRef.current?.export()}><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <AugmentsTable ref={exportRef}/>
            </CardContent>
        </Card>
    );
};