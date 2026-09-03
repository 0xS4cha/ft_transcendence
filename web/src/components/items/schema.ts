import z from "zod"

const ItemRow = z.object({
  itemName: z.string(),
  count: z.number(),
  place: z.number(),
  avg: z.number(),
  pick: z.number(),
  units: z
    .array(
      z.object({
        unit: z.string(),
      })
    )
});

export type ItemRow = z.infer<typeof ItemRow>;