import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { initialState } from "@/constants/User";
import * as authService from "@/services/authService";
import { type SignupPayload, type UserPublic } from "@/types/user";

function applyUser(state: typeof initialState, user: UserPublic) {
  state.id = user.id;
  state.email = user.email;
  state.isAuthenticated = true;
}

export const initializeSession = createAsyncThunk(
  "user/initializeSession",
  async (_, { rejectWithValue }) => {
    try {
      return await authService.getCurrentUser();
    } catch {
      return rejectWithValue(null);
    }
  },
);

export const loginUser = createAsyncThunk(
  "user/loginUser",
  async ({ email, password }: { email: string; password: string }) => {
    return authService.login(email, password);
  },
);

export const signupUser = createAsyncThunk(
  "user/signupUser",
  async (data: SignupPayload) => {
    await authService.signup(data);
    return authService.login(data.email, data.password);
  },
);

export const logoutUser = createAsyncThunk(
  "user/logoutUser",
  async () => {
    await authService.logout();
  },
);

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    clearUser: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      .addCase(initializeSession.pending, (state) => {
        state.status = "loading";
      })
      .addCase(initializeSession.fulfilled, (state, action) => {
        applyUser(state, action.payload);
        state.status = "ready";
      })
      .addCase(initializeSession.rejected, (state) => {
        state.isAuthenticated = false;
        state.status = "ready";
      })
      .addCase(loginUser.pending, (state) => {
        state.status = "loading";
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        applyUser(state, action.payload);
        state.status = "ready";
      })
      .addCase(loginUser.rejected, (state) => {
        state.status = "ready";
      })
      .addCase(signupUser.pending, (state) => {
        state.status = "loading";
      })
      .addCase(signupUser.fulfilled, (state, action) => {
        applyUser(state, action.payload);
        state.status = "ready";
      })
      .addCase(signupUser.rejected, (state) => {
        state.status = "ready";
      })
      .addCase(logoutUser.pending, (state) => {
        state.status = "loading";
      })
      .addCase(logoutUser.fulfilled, () => ({
        id: 0,
        email: "",
        isAuthenticated: false,
        status: "ready" as const,
      }))
      .addCase(logoutUser.rejected, (state) => {
        state.status = "ready";
      });
  },
});

export const { clearUser } = userSlice.actions;

export default userSlice.reducer;
