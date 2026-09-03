import { Card, CardTitle, CardAction, CardHeader, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { ItemsTable } from "@/components/items/table";

export function ItemsOverview() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of items</CardTitle>
                <CardDescription>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eius dignissimos nihil consequuntur eveniet blanditiis sunt sapiente dolorem laboriosam magni porro? Possimus impedit ad similique deleniti, veniam dolore nobis consequatur ea.</CardDescription>
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