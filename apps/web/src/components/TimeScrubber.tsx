import { useEffect, useRef, useState } from "react";
import type { SceneTimelineFrame } from "../types/forge";

interface Props {
  frames: SceneTimelineFrame[];
  onRun: () => void;
}

export function TimeScrubber({ frames, onRun }: Props) {
  const [playing, setPlaying] = useState(false);
  const [tick, setTick] = useState(0);
  const last = frames[frames.length - 1];
  const tickRef = useRef<number>(0);

  useEffect(() => {
    if (frames.length) setTick(frames.length - 1);
  }, [frames.length]);

  useEffect(() => {
    if (!playing) return;
    const id = setInterval(() => {
      tickRef.current = (tickRef.current + 1) % Math.max(frames.length, 1);
      setTick(tickRef.current);
    }, 300);
    return () => clearInterval(id);
  }, [playing, frames.length]);

  const violated = last?.is_violation ?? false;

  return (
    <div className="flex items-center gap-3">
      <button onClick={onRun} className="px-3 py-1.5 rounded bg-cyan-600 text-white text-xs font-bold">
        ▶ RUN FORGE
      </button>
      <button
        onClick={() => setPlaying((p) => !p)}
        className="px-3 py-1.5 rounded bg-zinc-800 border border-zinc-700 text-xs"
      >
        {playing ? "❚❚ Pause" : "▶ Play"}
      </button>
      <input
        type="range"
        min={0}
        max={Math.max(frames.length - 1, 0)}
        value={tick}
        onChange={(e) => setTick(Number(e.target.value))}
        className="flex-1"
      />
      <span className="mono text-[11px] text-zinc-400">tick {String(tick).padStart(3, "0")}</span>
      <span className={`text-[11px] font-bold ${violated ? "text-red-400" : "text-emerald-400"}`}>
        {violated ? "⚠ SAT_VIOLATION" : "✓ UNSSAT / PROVEN_SAFE"}
      </span>
    </div>
  );
}
