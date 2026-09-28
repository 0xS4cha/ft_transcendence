import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { UnitsTable } from "@/components/units/table";

export function UnitsOverview() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of units</CardTitle>
                <CardAction>
                    <Button variant="outline"><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <UnitsTable />
            </CardContent>
        </Card>
    );
};