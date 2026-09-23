import z from "zod";

const UnitRow = z.object({
  id: z.string(),
  avg_place: z.number(),
  winrate: z.number(),
  frequency: z.number(),
  name: z.string(),
  icon: z.string(),
  model: z.string()
});

export type UnitRow = z.infer<typeof UnitRow>;