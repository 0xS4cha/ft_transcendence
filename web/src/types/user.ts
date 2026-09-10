export interface UserPublic {
  id: number;
  email: string;
  username: string;
  picture?: string;
}

export interface UserState {
  id: number;
  email: string;
  username: string;
  picture?: string;
  isAuthenticated: boolean;
  status: "idle" | "loading" | "ready";
}

export interface SignupPayload {
  email: string;
  password: string;
  confirm_password: string;
}
