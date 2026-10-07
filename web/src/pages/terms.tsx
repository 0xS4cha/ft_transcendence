import { Card, CardContent, CardTitle, CardHeader, CardDescription } from "@/components/ui/card";
import { terms } from "@/constants/terms";
import { motion } from "motion/react";
import { useTranslation } from "react-i18next";

export default function Terms() {
  const { t } = useTranslation();

  return (
    <div className="relative w-full min-h-screen">
      <Card>
        <CardHeader>
          <CardTitle>{t("terms.title")}</CardTitle>
          <CardDescription>{t("terms.description")}</CardDescription>
        </CardHeader>
        <CardContent>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-12 pb-24 text-foreground/80 dark:text-white/80"
          >
            {terms.map((u) => (
              <section key={u.id}>
                <div className="flex items-center gap-3 mb-4">
                  <h2 className="text-lg font-semibold text-foreground dark:text-white">{u.id}. {u.title}</h2>
                </div>
                <p className="text-xs leading-relaxed text-foreground/70 dark:text-white/60">{u.content}</p>
              </section>
            ))}
          </motion.div>
        </CardContent>
      </Card>
    </div>
  );
}
