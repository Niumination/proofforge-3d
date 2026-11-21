import { useState } from "react";
import { Check, Copy, X } from "lucide-react";
import { useForgeStore } from "../store/forgeStore";

export function PatchDiffModal() {
  const { diffModalOpen, patchDiff, setDiffModalOpen } = useForgeStore();
  const [copied, setCopied] = useState(false);

  if (!diffModalOpen) return null;

  const lines = patchDiff.split("\n");

  const copyDiff = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(patchDiff).catch(() => {});
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4">
      <div className="w-full max-w-3xl max-h-[80vh] flex flex-col rounded-xl border border-zinc-700 bg-zinc-950 shadow-2xl">
        <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
          <span className="text-sm font-bold text-zinc-100">Surgical Patch Diff (buggy → fixed)</span>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={copyDiff}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold cursor-pointer"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? "Copied!" : "Copy Diff"}
            </button>
            <button
              type="button"
              onClick={() => setDiffModalOpen(false)}
              className="p-1 rounded hover:bg-zinc-800 text-zinc-400 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
        <pre className="flex-1 overflow-auto p-4 mono text-[11px] leading-relaxed">
          {lines.map((ln, idx) => {
            const cls = ln.startsWith("+")
              ? "text-emerald-300 bg-emerald-950/30"
              : ln.startsWith("-")
              ? "text-red-300 bg-red-950/30"
              : ln.startsWith("@@")
              ? "text-cyan-400"
              : "text-zinc-400";
            return (
              <div key={idx} className={cls}>
                {ln}
              </div>
            );
          })}
        </pre>
      </div>
    </div>
  );
}
