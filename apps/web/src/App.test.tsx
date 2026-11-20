import { describe, expect, it } from "vitest";
import { useForgeStore } from "./store/forgeStore";
import { useAuditStore } from "./store/auditStore";

describe("ProofForge stores", () => {
  it("switches scenarios, tracks activeTick, and toggles before/after frames", () => {
    const s = useForgeStore.getState();
    s.setScenario("robot_arm");
    expect(useForgeStore.getState().selectedScenario).toBe("robot_arm");

    s.applyVerification(
      "before",
      {
        iteration: 1,
        status: "SAT_VIOLATION",
        invariant_hash_valid: true,
        invariant_sha256: "abc",
        violated_invariant: "tau2",
        counterexample_inputs: { payload_kg: 4.5 },
        violated_tick: 28,
        violated_time_sec: 2.8,
        solver_duration_ms: 4.2,
      },
      [
        { tick: 0, time_sec: 0, is_violation: false, entities: [], constraints_overlay: [] },
        { tick: 1, time_sec: 0.1, is_violation: true, entities: [], constraints_overlay: [] },
      ]
    );
    expect(useForgeStore.getState().activeTick).toBe(28);
    expect(useForgeStore.getState().beforeResult?.status).toBe("SAT_VIOLATION");

    s.applyVerification(
      "after",
      {
        iteration: 2,
        status: "UNSAT_PROVEN",
        invariant_hash_valid: true,
        invariant_sha256: "abc",
        violated_invariant: null,
        counterexample_inputs: null,
        violated_tick: null,
        violated_time_sec: null,
        solver_duration_ms: 3.1,
      },
      [{ tick: 0, time_sec: 0, is_violation: false, entities: [], constraints_overlay: [] }]
    );
    useForgeStore.getState().setViewMode("after");
    expect(useForgeStore.getState().viewMode).toBe("after");
    expect(useForgeStore.getState().activeTick).toBe(0);
  });

  it("logs audit events in auditStore", () => {
    useAuditStore.getState().clear();
    useAuditStore.getState().addEvent("HOOK_AUDIT", { action: "BLOCKED" });
    expect(useAuditStore.getState().events).toHaveLength(1);
    expect(useAuditStore.getState().events[0].payload.action).toBe("BLOCKED");
  });
});
