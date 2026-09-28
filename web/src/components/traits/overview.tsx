import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { TraitsTable } from "@/components/traits/table";

export function TraitsOverview() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of traits</CardTitle>
                <CardAction>
                    <Button variant="outline"><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <TraitsTable />
            </CardContent>
        </Card>
    );
};