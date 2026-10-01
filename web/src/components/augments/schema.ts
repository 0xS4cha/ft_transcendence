import z from "zod"

const AugmentRow = z.object({
  id: z.string(),
  name: z.string(),
  rarity: z.string(),
  rounds: z.array(z.string()),
  icon: z.string()
});

export type AugmentRow = z.infer<typeof AugmentRow>;