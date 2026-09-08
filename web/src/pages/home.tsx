import { ChartSpline, Coins, User } from "lucide-react";
import { motion } from "motion/react";
import { Separator } from "@/components/ui/separator";
import { BreakdownCard } from "@/components/home/breakdowncard";
import { ChartAreaInteractive } from "@/components/home/chart_test";

const stats = [
  { Icon: User, title: "Visits", count: 1000 },
  { Icon: Coins, title: "Coins wasted", count: 1000 },
  { Icon: ChartSpline, title: "Matches analyzed", count: 1000 },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08, delayChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: "easeOut" },
  },
};

export default function Home() {
  return (
    <div className="relative w-full min-h-screen">
      <div className="w-full px-6 py-10 space-y-10">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="space-y-1"
        >
          <h1 className="text-3xl font-semibold tracking-tight">
            Welcome to Tactycs
          </h1>
          <p className="text-muted-foreground">
            Here's an overview of your TFT performance and analysis.
          </p>
        </motion.div>

        <Separator />

        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 gap-6 md:grid-cols-3"
        >
          {stats.map(({ Icon, title, count }) => (
            <motion.div key={title} variants={item}>
              <BreakdownCard Icon={Icon} title={title} count={count} />
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.35, ease: "easeOut" }}
        >
          <ChartAreaInteractive />
        </motion.div>
      </div>
    </div>
  );
}