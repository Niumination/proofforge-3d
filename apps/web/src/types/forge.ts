export interface ForgeRunRequest {
  scenario_id: string;
  mode: "live_gemini" | "deterministic";
  custom_spec?: string;
  inject_initial_bug: boolean;
  max_iterations: number;
  enable_adversarial_hook_test: boolean;
}

export type VerificationStatus = "SAT_VIOLATION" | "UNSAT_PROVEN" | "ERROR";

export interface VerificationResult {
  iteration: number;
  status: VerificationStatus;
  invariant_hash_valid: boolean;
  violated_invariant: string | null;
  counterexample_inputs: Record<string, number> | null;
  violated_tick: number | null;
  violated_time_sec: number | null;
  solver_duration_ms: number;
}

export interface SceneEntity {
  id: string;
  kind: string;
  position: number[];
  rotation_euler: number[];
  velocity: number[];
  status: string;
}

export interface SceneTimelineFrame {
  tick: number;
  time_sec: number;
  is_violation: boolean;
  entities: SceneEntity[];
  constraints_overlay: Array<{ type: string; center: number[]; radius: number; breached: boolean }>;
}

export type SSEEventType =
  | "STAGE_CHANGED"
  | "AGENT_LOG"
  | "HOOK_AUDIT"
  | "PROXY_AUDIT"
  | "VERIFICATION_RESULT"
  | "PATCH_DIFF";
