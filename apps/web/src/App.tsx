import { useEffect, useRef } from "react";
import { useForgeStore } from "./store/forgeStore";
import { useAuditStore } from "./store/auditStore";
import { apiClient } from "./lib/apiClient";
import { sseClient } from "./lib/sseClient";
import { SpecPanel } from "./components/SpecPanel";
import { Viewport3D } from "./components/Viewport3D";
import { TimeScrubber } from "./components/TimeScrubber";
import { AuditPanel } from "./components/AuditPanel";
import { PatchDiffModal } from "./components/PatchDiffModal";
import type { SceneTimelineFrame, VerificationResult } from "./types/forge";

export default function App() {
  const {
    selectedScenario,
    injectInitialBug,
    enableAdversarialHookTest,
    stage,
    viewMode,
    beforeFrames,
    afterFrames,
    beforeResult,
    afterResult,
    errorMessage,
    startRun,
    setStage,
    applyVerification,
    setPatchDiff,
    setExportResponse,
    setError,
  } = useForgeStore();

  const { events, addEvent, clear } = useAuditStore();
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => {
      abortRef.current?.abort();
    };
  }, []);

  const onRun = async () => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    const req = {
      scenario_id: selectedScenario,
      mode: "deterministic" as const,
      inject_initial_bug: injectInitialBug,
      max_iterations: 5,
      enable_adversarial_hook_test: enableAdversarialHookTest,
    };

    startRun(req);
    clear();

    try {
      const { runId } = await apiClient.runForge(req);
      for await (const ev of sseClient.stream(runId, controller.signal)) {
        addEvent(ev.event, ev.data);
        if (ev.event === "STAGE_CHANGED") {
          setStage(String(ev.data.stage ?? "VERIFY"));
        } else if (ev.event === "PATCH_DIFF") {
          setPatchDiff(String(ev.data.diff ?? ""));
        } else if (ev.event === "VERIFICATION_RESULT") {
          const phase = ev.data.phase === "before" ? "before" : "after";
          const result = ev.data.result as VerificationResult;
          const frames = (ev.data.frames as SceneTimelineFrame[]) ?? [];
          applyVerification(phase, result, frames);
        }
      }
    } catch (err) {
      if (!controller.signal.aborted) {
        setError(err instanceof Error ? err.message : "Run failed");
      }
    }
  };

  const onExport = async () => {
    const proven = afterResult ?? beforeResult;
    if (!proven) return;
    try {
      const res = await apiClient.exportProof(selectedScenario, proven);
      setExportResponse(res);
      addEvent("PROXY_AUDIT", res.proxy_audit);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Export failed");
    }
  };

  const activeFrames = viewMode === "before" ? beforeFrames : afterFrames;
  const activeResult = viewMode === "before" ? beforeResult : afterResult;

  return (
    <div className="h-screen w-screen bg-zinc-950 text-zinc-200 flex flex-col overflow-hidden">
      <header className="h-12 shrink-0 border-b border-zinc-800 flex items-center px-4 text-sm font-bold bg-zinc-950/90">
        <span className="text-zinc-100">ProofForge 3D</span>
        <span className="ml-3 text-xs font-normal text-cyan-400">
          Self-Verifying Systems Compiler
        </span>
        <div className="ml-auto flex items-center gap-3 text-xs font-normal">
          <span className="mono px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">
            stage: {stage}
          </span>
          <span className="mono px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-emerald-400">
            mode: deterministic
          </span>
        </div>
      </header>

      {errorMessage && (
        <div className="px-4 py-2 bg-red-950/60 border-b border-red-500/40 text-xs text-red-200">
          Error: {errorMessage}
        </div>
      )}

      <div className="flex-1 flex min-h-0">
        <aside className="w-80 shrink-0 border-r border-zinc-800 p-3 overflow-y-auto bg-zinc-950/70">
          <SpecPanel onRun={onRun} onExport={onExport} />
        </aside>

        <main className="flex-1 relative min-w-0">
          <Viewport3D frames={activeFrames} />
        </main>

        <aside className="w-96 shrink-0 border-l border-zinc-800 p-3 overflow-y-auto bg-zinc-950/70">
          <AuditPanel events={events} result={activeResult} />
        </aside>
      </div>

      <footer className="shrink-0 border-t border-zinc-800 px-4 py-2.5 bg-zinc-950/90">
        <TimeScrubber frames={activeFrames} />
      </footer>

      <PatchDiffModal />
    </div>
  );
}
