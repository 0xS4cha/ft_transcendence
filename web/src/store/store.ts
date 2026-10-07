import { configureStore } from '@reduxjs/toolkit';
import userReducer from '@/store/reducers/userSlice'
import homeReducer from '@/store/reducers/homeSlice'

export const store = configureStore({
  reducer: {
    user: userReducer,
    home: homeReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;