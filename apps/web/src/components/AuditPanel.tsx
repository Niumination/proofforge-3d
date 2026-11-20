import type { AuditEvent, VerificationResult } from "../types/forge";

interface Props {
  events: AuditEvent[];
  result: VerificationResult | null;
}

export function AuditPanel({ events, result }: Props) {
  return (
    <div className="space-y-3">
      <div className="rounded border border-zinc-700 bg-zinc-900 p-3">
        <div className="text-[11px] font-bold text-zinc-500 uppercase tracking-wider mb-1">VerificationResult</div>
        <div className="mono text-[11px]">{JSON.stringify(result ?? null, null, 1)}</div>
      </div>
      <div className="space-y-1">
        {events.map((e, i) => (
          <div key={i} className="mono text-[11px] border-b border-zinc-800 pb-1">
            <span className="text-cyan-400">{e.type}</span>{" "}
            <span className="text-zinc-400">{JSON.stringify(e.data)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
