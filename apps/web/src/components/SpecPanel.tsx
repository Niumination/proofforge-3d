import { Lock, Play, ShieldAlert, UploadCloud } from "lucide-react";
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
}

export function SpecPanel({ onRun, onExport }: Props) {
  const {
    selectedScenario,
    injectInitialBug,
    enableAdversarialHookTest,
    status,
    afterResult,
    beforeResult,
    setScenario,
    setInjectInitialBug,
    setAdversarialHookTest,
  } = useForgeStore();

  const activeMeta = SCENARIOS.find((s) => s.id === selectedScenario) ?? SCENARIOS[0];
  const canExport = (afterResult ?? beforeResult)?.status === "UNSAT_PROVEN";

  return (
    <div className="flex flex-col gap-4 text-xs">
      <div>
        <div className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 mb-2">
          1. Select Verification Scenario
        </div>
        <div className="space-y-2">
          {SCENARIOS.map((sc) => {
            const active = sc.id === selectedScenario;
            return (
              <button
                key={sc.id}
                type="button"
                onClick={() => setScenario(sc.id)}
                className={`w-full text-left rounded-lg border p-2.5 transition ${
                  active
                    ? "border-cyan-500/60 bg-cyan-950/30 text-zinc-100"
                    : "border-zinc-800 bg-zinc-900/60 text-zinc-400 hover:border-zinc-700"
                }`}
              >
                <div className="font-bold text-xs">{sc.title}</div>
                <div className="text-[10px] text-cyan-400 mt-0.5">{sc.domain}</div>
                <div className="text-[11px] text-zinc-400 mt-1 leading-snug">{sc.desc}</div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="rounded-lg border border-emerald-500/30 bg-emerald-950/20 p-3">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-emerald-400 uppercase tracking-wider">
          <Lock className="w-3.5 h-3.5" />
          Locked Formal Invariant
        </div>
        <div className="mono text-[11px] text-zinc-200 mt-1.5 break-words">{activeMeta.invariant}</div>
        <div className="text-[10px] text-zinc-400 mt-1">
          Guarded by SHA-256 Protected Hook (`invariants_locked.py`).
        </div>
      </div>

      <div className="space-y-2.5 border-t border-zinc-800 pt-3">
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
              Simulate Reward-Hacking Attack
            </span>
            <span className="text-[11px] text-zinc-400">
              Test Protected Hook blocking an attempt to relax Z3 safety bounds.
            </span>
          </span>
        </label>
      </div>

      <div className="space-y-2 pt-1">
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
