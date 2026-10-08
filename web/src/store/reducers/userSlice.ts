import { createAsyncThunk, createSlice, type PayloadAction } from "@reduxjs/toolkit";
import { initialState } from "@/constants/user";
import * as authService from "@/services/authService";
import { type SignupPayload, type UserPublic } from "@/types/user";
import { type ChatDataProps } from "@/types/chat";

function resolvePictureUrl(picture?: string | null): string | undefined {
  if (!picture) return undefined;
  if (picture.startsWith("http://") || picture.startsWith("https://") || picture.startsWith("/api/public/")) {
    return picture;
  }
  if (picture.startsWith("profile_pictures/")) {
    return `/api/public/${picture}`;
  }
  return picture;
}

function applyUser(state: typeof initialState, user: UserPublic) {
  state.id = user.id;
  state.email = user.email;
  state.username = user.username;
  state.picture = resolvePictureUrl(user.picture);
  state.isAuthenticated = true;
  state.chat = user.chat && user.chat.length > 0 ? user.chat : [];
  state.isDark = user.isDark ? user.isDark : typeof window !== 'undefined' ? (localStorage.getItem("isDark") == "true" || false) : true;
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

export const deleteUser = createAsyncThunk(
  "user/deleteUser",
  async () => {
    await authService.delete_rgpd();
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
    setTheme: (state, action: PayloadAction<boolean>) => {
      state.isDark = action.payload;
    },
    setUsername: (state, action: PayloadAction<string>) => {
      state.username = action.payload;
    },
    setPicture: (state, action: PayloadAction<string>) => {
      state.picture = resolvePictureUrl(action.payload);
    }
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
        isDark: true,
        status: "ready" as const,
      }))
      .addCase(logoutUser.rejected, (state) => {
        state.status = "ready";
      })
      .addCase(deleteUser.pending, (state) => {
        state.status = "loading";
      })
      .addCase(deleteUser.fulfilled, () => ({
        id: 0,
        email: "",
        username: "",
        isAuthenticated: false,
        chat: [],
        isDark: true,
        status: "ready" as const,
      }))
      .addCase(deleteUser.rejected, (state) => {
        state.status = "ready";
      })
  },
});

export const { clearUser, addChatContent, updateChatContent, removeChatContent, setChat, setTheme, setUsername , setPicture} = userSlice.actions;

export default userSlice.reducer;
