import { type UserState } from "@/types/user";

export const initialState: UserState = {
  id: 0,
  email: "",
  isAuthenticated: false,
  status: "idle",
};
