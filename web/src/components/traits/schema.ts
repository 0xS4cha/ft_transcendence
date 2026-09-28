import z from "zod"

const TraitRow = z.object({
  id: z.string(),
  winrate: z.number(),
  avg_place: z.number(),
  frequency: z.number(),
  name: z.string(),
  breakpoint: z.string(),
  breakpoints: z.array(z.string()),
  icon: z.string(),
  background_icon: z.string()
});

export type TraitRow = z.infer<typeof TraitRow>;