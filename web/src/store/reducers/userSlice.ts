import { createSlice, type PayloadAction } from '@reduxjs/toolkit';
import { initialState } from '@/constants/User';

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setEmail: (state, action: PayloadAction<string>) => {
      state.email = action.payload;
    },
    setId: (state, action: PayloadAction<number>) => {
      state.id = action.payload;
    },
    setLogin: (state, action: PayloadAction<boolean>) => {
      state.login = action.payload;
    }
  },
});

export const { setEmail, setId, setLogin } = userSlice.actions;

export default userSlice.reducer;