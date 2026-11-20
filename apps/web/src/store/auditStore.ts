import { create } from "zustand";
import type { AuditEvent } from "../types/forge";

export interface AuditState {
  events: AuditEvent[];
  addEvent: (type: string, payload: Record<string, unknown>) => void;
  clear: () => void;
}

export const useAuditStore = create<AuditState>((set) => ({
  events: [],
  addEvent: (type, payload) =>
    set((s) => ({
      events: [
        ...s.events,
        {
          type,
          payload,
          timestamp: new Date().toLocaleTimeString("en-US", { hour12: false }),
        },
      ].slice(-500),
    })),
  clear: () => set({ events: [] }),
}));
