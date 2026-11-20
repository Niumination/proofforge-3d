import { X } from "lucide-react";
import { useForgeStore } from "../store/forgeStore";

export function PatchDiffModal() {
  const { diffModalOpen, patchDiff, setDiffModalOpen } = useForgeStore();

  if (!diffModalOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4">
      <div className="w-full max-w-3xl max-h-[80vh] flex flex-col rounded-xl border border-zinc-700 bg-zinc-950 shadow-2xl">
        <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
          <span className="text-sm font-bold text-zinc-100">Surgical Patch Diff (buggy → fixed)</span>
          <button
            type="button"
            onClick={() => setDiffModalOpen(false)}
            className="p-1 rounded hover:bg-zinc-800 text-zinc-400 cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
        <pre className="flex-1 overflow-auto p-4 mono text-[11px] leading-relaxed text-zinc-300">
          {patchDiff}
        </pre>
      </div>
    </div>
  );
}
