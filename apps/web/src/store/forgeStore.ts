import { create } from "zustand";
import type {
  ForgeRunRequest,
  ProofExportResponse,
  ScenarioId,
  SceneTimelineFrame,
  VerificationResult,
} from "../types/forge";

export interface ForgeState {
  selectedScenario: ScenarioId;
  injectInitialBug: boolean;
  enableAdversarialHookTest: boolean;
  status: "idle" | "running" | "complete" | "error";
  stage: string;
  viewMode: "before" | "after";
  beforeFrames: SceneTimelineFrame[];
  afterFrames: SceneTimelineFrame[];
  beforeResult: VerificationResult | null;
  afterResult: VerificationResult | null;
  activeTick: number;
  playing: boolean;
  speed: number;
  focusTrigger: number;
  patchDiff: string;
  diffModalOpen: boolean;
  exportResponse: ProofExportResponse | null;
  errorMessage: string | null;

  setScenario: (id: ScenarioId) => void;
  setInjectInitialBug: (v: boolean) => void;
  setAdversarialHookTest: (v: boolean) => void;
  startRun: (req: ForgeRunRequest) => void;
  setStage: (stage: string) => void;
  applyVerification: (
    phase: "before" | "after",
    result: VerificationResult,
    frames: SceneTimelineFrame[]
  ) => void;
  setPatchDiff: (diff: string) => void;
  setViewMode: (mode: "before" | "after") => void;
  setActiveTick: (tick: number) => void;
  setPlaying: (playing: boolean) => void;
  setSpeed: (speed: number) => void;
  triggerFocusViolation: () => void;
  setDiffModalOpen: (open: boolean) => void;
  setExportResponse: (res: ProofExportResponse | null) => void;
  setError: (msg: string) => void;
  reset: () => void;
}

export const useForgeStore = create<ForgeState>((set, get) => ({
  selectedScenario: "drone_swarm",
  injectInitialBug: true,
  enableAdversarialHookTest: true,
  status: "idle",
  stage: "IDLE",
  viewMode: "before",
  beforeFrames: [],
  afterFrames: [],
  beforeResult: null,
  afterResult: null,
  activeTick: 0,
  playing: false,
  speed: 1,
  focusTrigger: 0,
  patchDiff: "",
  diffModalOpen: false,
  exportResponse: null,
  errorMessage: null,

  setScenario: (selectedScenario) =>
    set({
      selectedScenario,
      beforeFrames: [],
      afterFrames: [],
      beforeResult: null,
      afterResult: null,
      activeTick: 0,
      playing: false,
      patchDiff: "",
      exportResponse: null,
      status: "idle",
      stage: "IDLE",
    }),
  setInjectInitialBug: (injectInitialBug) => set({ injectInitialBug }),
  setAdversarialHookTest: (enableAdversarialHookTest) => set({ enableAdversarialHookTest }),
  startRun: (req) =>
    set({
      status: "running",
      stage: "STARTING",
      viewMode: req.inject_initial_bug ? "before" : "after",
      beforeFrames: [],
      afterFrames: [],
      beforeResult: null,
      afterResult: null,
      activeTick: 0,
      playing: false,
      patchDiff: "",
      exportResponse: null,
      errorMessage: null,
    }),
  setStage: (stage) =>
    set({
      stage,
      status: stage === "COMPLETE" ? "complete" : "running",
    }),
  applyVerification: (phase, result, frames) => {
    if (phase === "before") {
      const targetTick = result.violated_tick ?? 0;
      set({
        beforeResult: result,
        beforeFrames: frames,
        viewMode: "before",
        activeTick: targetTick,
        playing: true,
      });
    } else {
      const current = get();
      set({
        afterResult: result,
        afterFrames: frames,
        viewMode: current.beforeFrames.length > 0 ? current.viewMode : "after",
      });
    }
  },
  setPatchDiff: (patchDiff) => set({ patchDiff }),
  setViewMode: (viewMode) => {
    const s = get();
    const frames = viewMode === "before" ? s.beforeFrames : s.afterFrames;
    const violated = frames.findIndex((f) => f.is_violation);
    set({
      viewMode,
      activeTick: violated >= 0 ? violated : 0,
    });
  },
  setActiveTick: (activeTick) => set({ activeTick }),
  setPlaying: (playing) => set({ playing }),
  setSpeed: (speed) => set({ speed }),
  triggerFocusViolation: () => {
    const s = get();
    const frames = s.viewMode === "before" ? s.beforeFrames : s.afterFrames;
    const vIdx = frames.findIndex((f) => f.is_violation);
    const fallback = s.beforeResult?.violated_tick ?? 0;
    set({
      activeTick: vIdx >= 0 ? vIdx : fallback,
      playing: false,
      focusTrigger: s.focusTrigger + 1,
    });
  },
  setDiffModalOpen: (diffModalOpen) => set({ diffModalOpen }),
  setExportResponse: (exportResponse) => set({ exportResponse }),
  setError: (errorMessage) => set({ status: "error", errorMessage }),
  reset: () =>
    set({
      status: "idle",
      stage: "IDLE",
      beforeFrames: [],
      afterFrames: [],
      beforeResult: null,
      afterResult: null,
      activeTick: 0,
      playing: false,
      patchDiff: "",
      exportResponse: null,
      errorMessage: null,
    }),
}));
