import { Card, CardTitle, CardAction, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { ItemsTable } from "@/components/items/table";

export function ItemsOverview() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of items</CardTitle>
                <CardAction>
                    <Button variant="outline"><Download/>Export</Button>
                </CardAction>
            </CardHeader>
            <CardContent>
                <ItemsTable />
            </CardContent>
        </Card>
    );
};