import { useEffect, useRef } from "react";
import { useForgeStore } from "../store/forgeStore";
import { useAuditStore } from "../store/auditStore";
import { apiClient } from "../lib/apiClient";
import { sseClient } from "../lib/sseClient";
import { SpecPanel } from "./SpecPanel";
import { Viewport3D } from "./Viewport3D";
import { TimeScrubber } from "./TimeScrubber";
import { AuditPanel } from "./AuditPanel";
import { PatchDiffModal } from "./PatchDiffModal";

export default function App() {
  const { state, setRunning, applyResult, reset } = useForgeStore();
  const { events, addEvent, clear } = useAuditStore();
  const streamRef = useRef<AsyncGenerator<{ event: string; data: unknown }> | null>(null);

  useEffect(() => {
    return () => {
      streamRef.current?.return?.();
    };
  }, []);

  const onRun = async () => {
    if (!state.request) return;
    setRunning(state.request);
    clear();
    const { runId } = await apiClient.runForge(state.request);
    const stream = sseClient.stream(runId);
    streamRef.current = stream;
    for await (const ev of stream) {
      addEvent(ev.event, ev.data as Record<string, unknown>);
      if (ev.event === "VERIFICATION_RESULT") {
        applyResult(ev.data as never, (ev.data as { frames?: unknown }).frames ?? []);
      }
    }
  };

  return (
    <div className="h-screen w-screen bg-zinc-950 text-zinc-200 flex flex-col font-sans">
      <header className="h-12 border-b border-zinc-800 flex items-center px-4 text-sm font-bold">
        <span>ProofForge 3D</span>
        <span className="ml-3 text-xs font-normal text-zinc-500">Phase 1 — deterministic</span>
        <span className="ml-auto text-xs font-normal text-zinc-500 mono">mode: {state.request?.mode ?? "deterministic"}</span>
      </header>
      <div className="flex-1 flex min-h-0">
        <aside className="w-72 border-r border-zinc-800 p-3 overflow-auto">
          <SpecPanel />
        </aside>
        <main className="flex-1 relative">
          <Viewport3D frames={state.frames} />
        </main>
        <aside className="w-72 border-l border-zinc-800 p-3 overflow-auto">
          <AuditPanel events={events} result={state.result} />
        </aside>
      </div>
      <footer className="border-t border-zinc-800 p-2">
        <TimeScrubber frames={state.frames} onRun={onRun} />
      </footer>
      <PatchDiffModal />
    </div>
  );
}
