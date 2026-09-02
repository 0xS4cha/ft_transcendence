import z from "zod";

const UnitRow = z.object({
  id: z.string(),
  unit: z.string(),
  count: z.string(),
  place: z.string(),
  avg: z.string(),
  pick: z.string(),
});

export type UnitRow = z.infer<typeof UnitRow>;