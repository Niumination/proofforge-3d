import { create } from "zustand";

export interface AuditEvent {
  type: string;
  payload: Record<string, unknown>;
}

export interface AuditState {
  events: AuditEvent[];
  addEvent: (type: string, payload: Record<string, unknown>) => void;
  clear: () => void;
}

export const useAuditStore = create<AuditState>((set) => ({
  events: [],
  addEvent: (type, payload) => set((s) => ({ events: [...s.events, { type, payload }].slice(-500) })),
  clear: () => set({ events: [] }),
}));
