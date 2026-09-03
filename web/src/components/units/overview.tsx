import { Card, CardTitle, CardAction, CardHeader, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { UnitsTable } from "@/components/units/table";

export function UnitsOverview() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List of units</CardTitle>
                <CardDescription>Lorem ipsum dolor sit amet consectetur adipisicing elit. Eius dignissimos nihil consequuntur eveniet blanditiis sunt sapiente dolorem laboriosam magni porro? Possimus impedit ad similique deleniti, veniam dolore nobis consequatur ea.</CardDescription>
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