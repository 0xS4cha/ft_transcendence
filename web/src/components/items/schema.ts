import z from "zod"

const ItemRow = z.object({
  id: z.string(),
  winrate: z.number(),
  avg_place: z.number(),
  frequency: z.number(),
  name: z.string(),
  type: z.string(),
  icon: z.string()
});

export type ItemRow = z.infer<typeof ItemRow>;