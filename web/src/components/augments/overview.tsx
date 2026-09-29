import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { AugmentsTable } from "@/components/augments/table";

export function AugmentsOverview() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of augments</CardTitle>
                <CardAction>
                    <Button variant="outline"><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <AugmentsTable />
            </CardContent>
        </Card>
    );
};