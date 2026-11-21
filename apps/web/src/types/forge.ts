export type ScenarioId = "drone_swarm" | "robot_arm" | "spatial_tiling";

export interface ForgeRunRequest {
  scenario_id: ScenarioId;
  mode: "live_gemini" | "deterministic";
  custom_spec?: string;
  inject_initial_bug: boolean;
  max_iterations: number;
  enable_adversarial_hook_test: boolean;
  simulate_prompt_injection?: boolean;
}

export type VerificationStatus = "SAT_VIOLATION" | "UNSAT_PROVEN" | "ERROR";

export interface VerificationResult {
  iteration: number;
  status: VerificationStatus;
  invariant_hash_valid: boolean;
  invariant_sha256: string;
  violated_invariant: string | null;
  counterexample_inputs: Record<string, string | number> | null;
  violated_tick: number | null;
  violated_time_sec: number | null;
  solver_duration_ms: number;
  note?: string | null;
}

export interface SceneEntity {
  id: string;
  kind: string;
  position: number[];
  rotation_euler: number[];
  velocity: number[];
  status: string;
  meta?: Record<string, unknown>;
}

export interface ConstraintsOverlay {
  type: string;
  center: number[];
  radius: number;
  breached: boolean;
}

export interface SceneTimelineFrame {
  tick: number;
  time_sec: number;
  is_violation: boolean;
  entities: SceneEntity[];
  constraints_overlay: ConstraintsOverlay[];
}

export interface AuditEvent {
  type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

export interface ProofCertificate {
  certificate_id: string;
  issued_at_utc: string;
  scenario_id: string;
  verification_status: string;
  invariant_sha256: string;
  impl_sha256: string;
  certificate_digest_sha256: string;
  hooks_enforced: string[];
  credential_exposed: boolean;
}

export interface ProofExportResponse {
  export_url: string;
  certificate_id: string;
  certificate_digest: string;
  proxy_audit: Record<string, unknown>;
}

export interface RedTeamResponse {
  scenario_id: string;
  all_blocked: boolean;
  blocked_count: number;
  hook_events: Array<Record<string, unknown>>;
}

export interface VoiceConstraintResponse {
  scenario_id: ScenarioId;
  parameter: string;
  value: number | string;
  unit: string;
  summary: string;
  custom_spec_patch: string;
  source: string;
}
