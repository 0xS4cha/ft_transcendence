import { createAsyncThunk, createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { initialState } from "@/constants/user";
import * as authService from "@/services/authService";
import { type SignupPayload, type UserPublic } from "@/types/user";
import { type ChatDataProps } from "@/types/chat";

function applyUser(state: typeof initialState, user: UserPublic) {
  state.id = user.id;
  state.email = user.email;
  state.username = user.username;
  state.picture = user.picture ? user.picture : undefined;
  state.isAuthenticated = true;
  state.chat = user.chat && user.chat.length > 0 ? user.chat : [];
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
    setChat: (state, action: PayloadAction<ChatDataProps[]>) => {
      state.chat = action.payload;
    },
    addChatContent: (state, action: PayloadAction<ChatDataProps>) => {
      if (!state.chat) return;
      if (state.chat.some((item) => item.date === action.payload.date)) return;
      state.chat.push(action.payload);
    },
    updateChatContent: (
      state,
      action: PayloadAction<{ id: number; message: ChatDataProps }>,
    ) => {
      if (!state.chat) return;
      const index = state.chat.findIndex((item) => item.id === action.payload.id);
      if (index !== -1) {
        state.chat[index] = action.payload.message;
      }
    },
    removeChatContent: (state, action: PayloadAction<number>) => {
      if (!state.chat) return;
      state.chat = state.chat.filter((item) => item.id !== action.payload);
    },
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
        username: "",
        isAuthenticated: false,
        chat: [],
        status: "ready" as const,
      }))
      .addCase(logoutUser.rejected, (state) => {
        state.status = "ready";
      })
  },
});

export const { clearUser, addChatContent, updateChatContent, removeChatContent, setChat } = userSlice.actions;

export default userSlice.reducer;
