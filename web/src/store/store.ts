import { configureStore } from '@reduxjs/toolkit';
// import inputReducer from '@/store/features/inputSlice'

export const store = configureStore({
  reducer: {
    // user_input: inputReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;