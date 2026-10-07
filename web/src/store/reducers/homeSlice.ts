import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { type HomeDataProps } from "@/types/home";

export const initialHomeState: HomeDataProps = {
  visitsCount: 0,
  goldCount: 0,
  matchCount: 0,
  history: [],
};

export const homeSlice = createSlice({
  name: "home",
  initialState: initialHomeState,
  reducers: {
    setHomeStats: (_, action: PayloadAction<HomeDataProps>) => action.payload,
  },
});

export const { setHomeStats } = homeSlice.actions;

export default homeSlice.reducer;