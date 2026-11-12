import { create } from "zustand";

interface UIState {
  route: string;
  setRoute: (r: string) => void;
}
export const useUI = create<UIState>((set) => ({
  route: "/home",
  setRoute: (route) => set({ route }),
}));
