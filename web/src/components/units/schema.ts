import z from "zod";

const UnitRow = z.object({
  unit: z.string(),
  count: z.number(),
  place: z.number(),
  avg: z.number(),
  pick: z.number(),
  items: z.array(
    z.object({
      itemName: z.string(),
    })
  ),
});

export type UnitRow = z.infer<typeof UnitRow>;