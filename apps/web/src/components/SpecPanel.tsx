import { useState } from "react";
import { Lock, Mic, Play, ShieldAlert, Skull, Sparkles, UploadCloud } from "lucide-react";
import { useForgeStore } from "../store/forgeStore";
import type { ScenarioId } from "../types/forge";

const SCENARIOS: Array<{
  id: ScenarioId;
  title: string;
  domain: string;
  invariant: string;
  desc: string;
}> = [
  {
    id: "drone_swarm",
    title: "Drone Swarm Collision",
    domain: "Robotics · Kinematics",
    invariant: "||p_A(t) - p_B(t)|| >= 1.50m",
    desc: "Head-on crossing with sensor/braking latency. Naive controller collides at t=4.2s.",
  },
  {
    id: "robot_arm",
    title: "3-DOF Robot Arm Torque",
    domain: "Robotics · QF_LIA Taylor",
    invariant: "|tau2| <= 8.0 N·m & y_eff >= 0.15m",
    desc: "Unclamped boundary target + 4.5 kg payload overloads elbow joint torque.",
  },
  {
    id: "spatial_tiling",
    title: "4×4×4 Spatial Deadlock",
    domain: "Concurrency · Int Grid",
    invariant: "Mutual Exclusion & Deadlock < 4 ticks",
    desc: "Two workers enter opposing cells without canonical lock order at tick 14..18.",
  },
];

interface Props {
  onRun: () => void;
  onExport: () => void;
  onRedTeam: () => void;
  onVoiceSubmit: (transcript: string) => void;
}

export function SpecPanel({ onRun, onExport, onRedTeam, onVoiceSubmit }: Props) {
  const {
    selectedScenario,
    mode,
    customSpec,
    voiceTranscript,
    injectInitialBug,
    enableAdversarialHookTest,
    status,
    afterResult,
    beforeResult,
    redTeamBusy,
    setScenario,
    setMode,
    setCustomSpec,
    setVoiceTranscript,
    setInjectInitialBug,
    setAdversarialHookTest,
  } = useForgeStore();

  const [listening, setListening] = useState(false);
  const activeMeta = SCENARIOS.find((s) => s.id === selectedScenario) ?? SCENARIOS[0];
  const canExport = (afterResult ?? beforeResult)?.status === "UNSAT_PROVEN";

  const handleMic = () => {
    const w = window as unknown as {
      SpeechRecognition?: new () => {
        lang: string;
        onresult: (e: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void;
        onend: () => void;
        start: () => void;
      };
      webkitSpeechRecognition?: new () => {
        lang: string;
        onresult: (e: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void;
        onend: () => void;
        start: () => void;
      };
    };
    const Rec = w.SpeechRecognition ?? w.webkitSpeechRecognition;
    if (!Rec) {
      const sample = "Limit robot arm payload to 3.0 kg";
      setVoiceTranscript(sample);
      onVoiceSubmit(sample);
      return;
    }
    const rec = new Rec();
    rec.lang = "en-US";
    setListening(true);
    rec.onresult = (ev) => {
      const text = ev.results[0]?.[0]?.transcript ?? "";
      setVoiceTranscript(text);
      if (text.trim()) onVoiceSubmit(text);
    };
    rec.onend = () => setListening(false);
    rec.start();
  };

  return (
    <div className="flex flex-col gap-3.5 text-xs">
      <div>
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-1.5">
          Execution Engine
        </div>
        <div className="grid grid-cols-2 gap-1.5">
          <button
            type="button"
            onClick={() => setMode("deterministic")}
            className={`py-1.5 px-2 rounded-md border text-[11px] font-semibold cursor-pointer ${
              mode === "deterministic"
                ? "border-emerald-500/60 bg-emerald-950/40 text-emerald-300"
                : "border-zinc-800 bg-zinc-900 text-zinc-400"
            }`}
          >
            Local Z3 Core
          </button>
          <button
            type="button"
            onClick={() => setMode("live_gemini")}
            className={`py-1.5 px-2 rounded-md border text-[11px] font-semibold flex items-center justify-center gap-1 cursor-pointer ${
              mode === "live_gemini"
                ? "border-cyan-500/60 bg-cyan-950/40 text-cyan-300"
                : "border-zinc-800 bg-zinc-900 text-zinc-400"
            }`}
          >
            <Sparkles className="w-3 h-3" />
            Gemini 4 Argon
          </button>
        </div>
      </div>

      <div>
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-1.5">
          1. Verification Scenario
        </div>
        <div className="space-y-1.5">
          {SCENARIOS.map((sc) => {
            const active = sc.id === selectedScenario;
            return (
              <button
                key={sc.id}
                type="button"
                onClick={() => setScenario(sc.id)}
                className={`w-full text-left rounded-lg border p-2 transition cursor-pointer ${
                  active
                    ? "border-cyan-500/60 bg-cyan-950/30 text-zinc-100"
                    : "border-zinc-800 bg-zinc-900/60 text-zinc-400 hover:border-zinc-700"
                }`}
              >
                <div className="font-bold text-xs">{sc.title}</div>
                <div className="text-[10px] text-cyan-400 mt-0.5">{sc.domain}</div>
                <div className="text-[11px] text-zinc-400 mt-0.5 leading-snug">{sc.desc}</div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="rounded-lg border border-emerald-500/30 bg-emerald-950/20 p-2.5">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-emerald-400 uppercase tracking-wider">
          <Lock className="w-3.5 h-3.5" />
          Locked Formal Invariant
        </div>
        <div className="mono text-[11px] text-zinc-200 mt-1 break-words">{activeMeta.invariant}</div>
      </div>

      <div className="space-y-1.5">
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400">
          Voice / Natural Constraint
        </div>
        <div className="flex gap-1.5">
          <input
            type="text"
            value={voiceTranscript}
            onChange={(e) => setVoiceTranscript(e.target.value)}
            placeholder="e.g. Set drone separation to 2.2 m"
            className="flex-1 rounded-md border border-zinc-800 bg-zinc-900 px-2 py-1.5 text-[11px] text-zinc-200"
          />
          <button
            type="button"
            onClick={handleMic}
            title="Speak constraint"
            className={`px-2 py-1.5 rounded-md border cursor-pointer ${
              listening
                ? "border-red-500 bg-red-950/50 text-red-300"
                : "border-zinc-700 bg-zinc-900 text-zinc-300 hover:bg-zinc-800"
            }`}
          >
            <Mic className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={() => voiceTranscript.trim() && onVoiceSubmit(voiceTranscript)}
            className="px-2.5 py-1.5 rounded-md bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-[11px] font-semibold cursor-pointer"
          >
            Apply
          </button>
        </div>
        <div className="flex flex-wrap gap-1">
          {[
            "Set drone separation to 2.2 m",
            "Limit robot arm payload to 3.0 kg",
            "Limit spatial deadlock wait to 2 ticks",
          ].map((preset) => (
            <button
              key={preset}
              type="button"
              onClick={() => {
                setVoiceTranscript(preset);
                onVoiceSubmit(preset);
              }}
              className="px-2 py-0.5 rounded bg-zinc-900 border border-zinc-800 hover:border-cyan-500/40 text-[10px] text-zinc-400 hover:text-cyan-300 cursor-pointer"
            >
              {preset}
            </button>
          ))}
        </div>
        <textarea
          rows={2}
          value={customSpec}
          onChange={(e) => setCustomSpec(e.target.value)}
          placeholder="Optional custom spec for Gemini 4 Argon co-generation..."
          className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-2 py-1.5 text-[11px] text-zinc-300"
        />
      </div>

      <div className="space-y-2 border-t border-zinc-800 pt-2.5">
        <label className="flex items-start gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={injectInitialBug}
            onChange={(e) => setInjectInitialBug(e.target.checked)}
            className="mt-0.5 accent-cyan-500"
          />
          <span>
            <span className="font-semibold text-zinc-200 block">Inject Initial Edge-Case Bug</span>
            <span className="text-[11px] text-zinc-400">
              Show Z3 SAT counterexample in 3D first, then surgical patch to UNSAT.
            </span>
          </span>
        </label>

        <label className="flex items-start gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={enableAdversarialHookTest}
            onChange={(e) => setAdversarialHookTest(e.target.checked)}
            className="mt-0.5 accent-amber-500"
          />
          <span className="flex-1">
            <span className="font-semibold text-amber-300 flex items-center gap-1">
              <ShieldAlert className="w-3.5 h-3.5" />
              Enable Protected Hook Audit
            </span>
          </span>
        </label>
      </div>

      <div className="space-y-2 pt-0.5">
        <button
          type="button"
          onClick={onRun}
          disabled={status === "running"}
          className="w-full flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white font-bold text-xs cursor-pointer"
        >
          <Play className="w-3.5 h-3.5" />
          {status === "running" ? "Verifying with Z3..." : "Run ProofForge Pipeline"}
        </button>

        <button
          type="button"
          onClick={onRedTeam}
          disabled={redTeamBusy}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg border border-red-500/40 bg-red-950/30 hover:bg-red-950/50 text-red-300 font-semibold text-xs cursor-pointer"
        >
          <Skull className="w-3.5 h-3.5" />
          {redTeamBusy ? "Simulating Attack..." : "Simulate Prompt Injection Attack"}
        </button>

        <button
          type="button"
          onClick={onExport}
          disabled={!canExport}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 disabled:opacity-40 text-zinc-200 font-semibold text-xs cursor-pointer"
        >
          <UploadCloud className="w-3.5 h-3.5 text-emerald-400" />
          Export Proof via Credential Proxy
        </button>
      </div>
    </div>
  );
}
