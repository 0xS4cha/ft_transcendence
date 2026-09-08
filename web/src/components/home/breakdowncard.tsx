import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { CountUp } from "@/components/ui/countup";

interface BreakdownProps {
    Icon: any;
    title: string;
    count: number;
}

export function BreakdownCard({Icon, title, count}: BreakdownProps) {
    return (
        <Card>
            <CardHeader>
                <Icon />
                {title}
            </CardHeader>
            <CardContent>
                <CountUp
                    from={0}
                    to={count}
                    separator=","
                    direction="up"
                    duration={1}
                    className="count-up-text"
                    delay={0}
                />
            </CardContent>
        </Card>
    )
}