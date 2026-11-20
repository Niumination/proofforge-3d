import { FileCode2, ShieldCheck, ShieldX } from "lucide-react";
import { useForgeStore } from "../store/forgeStore";
import type { AuditEvent, VerificationResult } from "../types/forge";

interface Props {
  events: AuditEvent[];
  result: VerificationResult | null;
}

export function AuditPanel({ events, result }: Props) {
  const { patchDiff, exportResponse, setDiffModalOpen } = useForgeStore();
  const isProven = result?.status === "UNSAT_PROVEN";

  return (
    <div className="space-y-3 text-xs">
      <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-3">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider">
            Z3 Verification Result
          </span>
          {result && (
            <span
              className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                isProven
                  ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/40"
                  : "bg-red-500/15 text-red-400 border border-red-500/40"
              }`}
            >
              {result.status}
            </span>
          )}
        </div>
        {result ? (
          <div className="mono text-[11px] space-y-1 text-zinc-300">
            <div>iteration: {result.iteration}</div>
            <div>hash_valid: {String(result.invariant_hash_valid)}</div>
            <div>solver_ms: {result.solver_duration_ms} ms</div>
            {result.violated_invariant && (
              <div className="text-red-300">violated: {result.violated_invariant}</div>
            )}
            {result.counterexample_inputs && (
              <pre className="bg-zinc-950 p-2 rounded border border-zinc-800 text-[10px] overflow-x-auto text-amber-300">
                {JSON.stringify(result.counterexample_inputs, null, 2)}
              </pre>
            )}
            {result.note && <div className="text-emerald-300 text-[10px]">{result.note}</div>}
          </div>
        ) : (
          <div className="text-zinc-500 text-[11px]">No verification run yet.</div>
        )}
      </div>

      {patchDiff && (
        <button
          type="button"
          onClick={() => setDiffModalOpen(true)}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg border border-cyan-500/40 bg-cyan-950/30 hover:bg-cyan-950/50 text-cyan-300 font-semibold cursor-pointer"
        >
          <FileCode2 className="w-3.5 h-3.5" />
          Inspect Surgical Patch Diff
        </button>
      )}

      {exportResponse && (
        <div className="rounded-lg border border-emerald-500/40 bg-emerald-950/20 p-3 space-y-1">
          <div className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">
            Credential Proxy Audit
          </div>
          <div className="mono text-[10px] text-zinc-300 break-all">
            target: {exportResponse.export_url}
          </div>
          <pre className="mono text-[10px] text-emerald-300 overflow-x-auto">
            {JSON.stringify(exportResponse.proxy_audit, null, 2)}
          </pre>
        </div>
      )}

      <div>
        <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider mb-1.5">
          SSE & Security Hooks Stream
        </div>
        <div className="space-y-1.5 max-h-72 overflow-y-auto pr-1">
          {events.map((e, i) => {
            const isBlocked = e.type === "HOOK_AUDIT" && e.payload.action === "BLOCKED";
            const isAllow = e.type === "HOOK_AUDIT" && e.payload.action === "ALLOW";
            return (
              <div
                key={i}
                className={`mono text-[10px] rounded border p-2 ${
                  isBlocked
                    ? "border-red-500/50 bg-red-950/30 text-red-200"
                    : isAllow
                    ? "border-emerald-500/40 bg-emerald-950/20 text-emerald-200"
                    : "border-zinc-800 bg-zinc-900/70 text-zinc-300"
                }`}
              >
                <div className="flex items-center gap-1.5 font-bold">
                  {isBlocked && <ShieldX className="w-3 h-3 text-red-400" />}
                  {isAllow && <ShieldCheck className="w-3 h-3 text-emerald-400" />}
                  <span className="text-cyan-400">{e.type}</span>
                  <span className="ml-auto text-zinc-500 font-normal">{e.timestamp}</span>
                </div>
                <div className="text-zinc-400 mt-0.5 break-words">
                  {e.type === "VERIFICATION_RESULT"
                    ? `phase=${String(e.payload.phase)} status=${String(
                        (e.payload.result as Record<string, unknown> | undefined)?.status
                      )}`
                    : JSON.stringify(e.payload)}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
