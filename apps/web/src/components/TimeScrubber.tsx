import { useEffect } from "react";
import { Crosshair, GitCompareArrows } from "lucide-react";
import { useForgeStore } from "../store/forgeStore";
import type { SceneTimelineFrame } from "../types/forge";

export function TimeScrubber({ frames }: { frames: SceneTimelineFrame[] }) {
  const {
    activeTick,
    playing,
    speed,
    viewMode,
    beforeFrames,
    afterFrames,
    beforeResult,
    afterResult,
    setActiveTick,
    setPlaying,
    setSpeed,
    setViewMode,
    triggerFocusViolation,
  } = useForgeStore();

  const maxTick = Math.max(frames.length - 1, 0);
  const safeTick = Math.min(activeTick, maxTick);
  const activeFrame = frames[safeTick];

  useEffect(() => {
    if (!playing || frames.length <= 1) return;
    const intervalMs = Math.max(30, Math.round(100 / speed));
    const id = window.setInterval(() => {
      const current = useForgeStore.getState().activeTick;
      const next = (current + 1) % frames.length;
      setActiveTick(next);
    }, intervalMs);
    return () => window.clearInterval(id);
  }, [playing, speed, frames.length, setActiveTick]);

  const violationIndices = frames
    .map((f, idx) => (f.is_violation ? idx : -1))
    .filter((idx) => idx >= 0);

  const zoneLeftPct =
    violationIndices.length && maxTick > 0
      ? (Math.min(...violationIndices) / maxTick) * 100
      : 0;
  const zoneWidthPct =
    violationIndices.length && maxTick > 0
      ? ((Math.max(...violationIndices) - Math.min(...violationIndices) + 1) / (maxTick + 1)) * 100
      : 0;

  const activeResult = viewMode === "before" ? beforeResult : afterResult;
  const isViolated = activeFrame?.is_violation ?? false;

  return (
    <div className="space-y-1.5">
      <div className="flex flex-wrap items-center gap-2.5 text-xs">
        <button
          type="button"
          disabled={frames.length === 0}
          onClick={() => setPlaying(!playing)}
          className="px-3 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 text-white font-bold w-20 cursor-pointer"
        >
          {playing ? "❚❚ Pause" : "▶ Play"}
        </button>

        <select
          value={speed}
          onChange={(e) => setSpeed(Number(e.target.value))}
          className="bg-zinc-900 border border-zinc-700 rounded px-2 py-1.5 text-xs"
        >
          <option value={0.5}>0.5×</option>
          <option value={1}>1×</option>
          <option value={2}>2×</option>
        </select>

        <button
          type="button"
          disabled={violationIndices.length === 0}
          onClick={triggerFocusViolation}
          className="flex items-center gap-1 px-2.5 py-1.5 rounded bg-zinc-800 hover:bg-zinc-700 disabled:opacity-40 border border-zinc-700 font-semibold cursor-pointer"
        >
          <Crosshair className="w-3.5 h-3.5 text-red-400" />
          Focus Violation
        </button>

        {beforeFrames.length > 0 && afterFrames.length > 0 && (
          <button
            type="button"
            onClick={() => setViewMode(viewMode === "before" ? "after" : "before")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded border font-bold cursor-pointer ${
              viewMode === "before"
                ? "bg-red-500/15 border-red-500/40 text-red-300"
                : "bg-emerald-500/15 border-emerald-500/40 text-emerald-300"
            }`}
          >
            <GitCompareArrows className="w-3.5 h-3.5" />
            {viewMode === "before" ? "BEFORE · BUG (SAT) → Switch to Fix" : "AFTER · PATCHED (UNSAT) → Switch to Bug"}
          </button>
        )}

        <div className="ml-auto flex items-center gap-3">
          <span className="mono text-zinc-400">
            tick {String(safeTick).padStart(3, "0")} · t {(activeFrame?.time_sec ?? 0).toFixed(1)}s
          </span>
          {activeResult && (
            <span
              className={`font-bold ${
                activeResult.status === "UNSAT_PROVEN" ? "text-emerald-400" : "text-red-400"
              }`}
            >
              {activeResult.status === "UNSAT_PROVEN" ? "✓ UNSAT / PROVEN_SAFE" : "⚠ SAT_VIOLATION"}
            </span>
          )}
        </div>
      </div>

      <div className="relative pt-1">
        <input
          type="range"
          min={0}
          max={maxTick}
          value={safeTick}
          disabled={frames.length === 0}
          onChange={(e) => {
            setPlaying(false);
            setActiveTick(Number(e.target.value));
          }}
          className={`w-full cursor-pointer ${isViolated ? "accent-red-500" : "accent-cyan-500"}`}
        />
        <div className="relative h-1.5 rounded-full bg-zinc-800 overflow-hidden">
          {violationIndices.length > 0 && (
            <div
              className="absolute top-0 h-full bg-red-600/80"
              style={{ left: `${zoneLeftPct}%`, width: `${Math.max(zoneWidthPct, 2)}%` }}
            />
          )}
        </div>
      </div>
    </div>
  );
}
