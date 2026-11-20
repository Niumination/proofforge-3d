import { create } from "zustand";
import type { ForgeRunRequest, SceneTimelineFrame, VerificationResult } from "../types/forge";

export interface ForgeState {
  runId: string | null;
  status: "idle" | "running" | "satisfied" | "error";
  request: ForgeRunRequest | null;
  frames: SceneTimelineFrame[];
  result: VerificationResult | null;
}

export const useForgeStore = create<ForgeState>((set) => ({
  runId: null,
  status: "idle",
  request: null,
  frames: [],
  result: null,
  reset: () => set({ runId: null, status: "idle", request: null, frames: [], result: null }),
  setRunning: (request) =>
    set({ status: "running", request, frames: [], result: null }),
  applyResult: (result, frames) =>
    set({ status: result.status === "UNSAT_PROVEN" ? "satisfied" : "running", result, frames }),
  setError: () => set({ status: "error" }),
}));
