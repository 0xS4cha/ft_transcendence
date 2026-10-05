import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { AugmentsTable } from "@/components/augments/table";
import { useRef } from "react";
import { type exportRef } from "@/types/stats"

export function AugmentsOverview() {
    const exportRef = useRef<exportRef>(null);
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of augments</CardTitle>
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