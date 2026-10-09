import z from "zod";

const TraitRow = z.object({
  name: z.string(),
  breakpoints: z.array(z.string()),
  icon: z.string(),
  winrate: z.number(),
});

const UnitRow = z.object({
  id: z.string(),
  avg_place: z.number(),
  winrate: z.number(),
  frequency: z.number(),
  name: z.string(),
  icon: z.string(),
  model: z.string().nullable(),
  cost: z.number(),
  traits: z.array(TraitRow),
});

export type UnitRow = z.infer<typeof UnitRow>;
export type TraitRow = z.infer<typeof TraitRow>;