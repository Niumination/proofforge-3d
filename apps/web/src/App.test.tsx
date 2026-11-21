import { act } from "react";
import { createRoot } from "react-dom/client";
import { describe, expect, it } from "vitest";
import { AuditPanel } from "./components/AuditPanel";
import { PatchDiffModal } from "./components/PatchDiffModal";
import { ProofCertModal } from "./components/ProofCertModal";
import { SpecPanel } from "./components/SpecPanel";
import { TimeScrubber } from "./components/TimeScrubber";
import { useAuditStore } from "./store/auditStore";
import { useForgeStore } from "./store/forgeStore";

describe("ProofForge stores & UI components", () => {
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
        solver_duration_ms: 4,
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
        solver_duration_ms: 3,
      },
      [{ tick: 0, time_sec: 0, is_violation: false, entities: [], constraints_overlay: [] }]
    );
    useForgeStore.getState().setViewMode("after");
    expect(useForgeStore.getState().viewMode).toBe("after");
    expect(useForgeStore.getState().activeTick).toBe(0);
  });

  it("supports mode toggle, customSpec, certificate, and auditStore", () => {
    const s = useForgeStore.getState();
    s.setMode("live_gemini");
    s.setCustomSpec("Keep drone separation >= 2.2m");
    s.setCertificate({
      certificate_id: "cert-123456",
      issued_at_utc: "2026-11-21T15:00:00Z",
      scenario_id: "drone_swarm",
      verification_status: "UNSAT_PROVEN",
      invariant_sha256: "abc",
      impl_sha256: "def",
      certificate_digest_sha256: "999",
      hooks_enforced: ["pre_verify_invariant_guard"],
      credential_exposed: false,
    });
    expect(useForgeStore.getState().mode).toBe("live_gemini");
    expect(useForgeStore.getState().customSpec).toContain("2.2m");
    expect(useForgeStore.getState().certificate?.certificate_id).toBe("cert-123456");

    useAuditStore.getState().clear();
    useAuditStore.getState().addEvent("HOOK_AUDIT", { action: "BLOCKED" });
    expect(useAuditStore.getState().events).toHaveLength(1);
    expect(useAuditStore.getState().events[0].payload.action).toBe("BLOCKED");
  });

  it("mounts Cockpit UI panels cleanly in jsdom without stray backlog markers", () => {
    (globalThis as unknown as { IS_REACT_ACT_ENVIRONMENT: boolean }).IS_REACT_ACT_ENVIRONMENT =
      true;
    const s = useForgeStore.getState();
    s.setPatchDiff("--- a\n+++ b\n@@ -1 +1 @@\n-bad\n+good");
    s.setDiffModalOpen(true);
    s.setCertModalOpen(true);

    const container = document.createElement("div");
    document.body.appendChild(container);
    const root = createRoot(container);

    act(() => {
      root.render(
        <div>
          <SpecPanel
            onRun={() => {}}
            onAutoDemo={() => {}}
            onExport={() => {}}
            onRedTeam={() => {}}
            onVoiceSubmit={() => {}}
          />
          <TimeScrubber frames={useForgeStore.getState().afterFrames} />
          <AuditPanel
            events={useAuditStore.getState().events}
            result={useForgeStore.getState().afterResult}
          />
          <PatchDiffModal />
          <ProofCertModal />
        </div>
      );
    });

    const html = container.innerHTML;
    expect(html).toContain("Run ProofForge Pipeline");
    expect(html).toContain("Simulate Prompt Injection Attack");
    expect(html).toContain("Export Proof via Credential Proxy");
    expect(html).toContain("Inspect Surgical Patch Diff");
    expect(html).toContain("Signed UNSAT Proof Certificate");
    expect(html).not.toContain("PF-026");

    act(() => {
      root.unmount();
    });
    container.remove();
  });
});
