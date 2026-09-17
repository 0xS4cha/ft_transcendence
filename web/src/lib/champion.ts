// src/lib/champions.ts

export interface Champion {
  id: string;
  name: string;
  cost: number;
  imageUrl: string;
}

export const CHAMPIONS_DB: Champion[] = [
  { id: "akali", name: "Akali", cost: 4, imageUrl: "https://raw.communitydragon.org/latest/game/assets/characters/akali/hud/akali_square.png" },
  { id: "jinx", name: "Jinx", cost: 1, imageUrl: "https://raw.communitydragon.org/latest/game/assets/characters/jinx/hud/jinx_square.png" },
  { id: "ahri", name: "Ahri", cost: 4, imageUrl: "https://raw.communitydragon.org/latest/game/assets/characters/ahri/hud/ahri_square_0.png" },
  { id: "kennen", name: "Kennen", cost: 1, imageUrl: "https://raw.communitydragon.org/latest/game/assets/characters/kennen/hud/kennen_square.png" },
];

// Petite fonction utilitaire pour trouver un champion facilement
export const getChampionById = (id: string) => {
  return CHAMPIONS_DB.find((champ) => champ.id === id);
};