import { Download, FileText, X } from "lucide-react";
import { useForgeStore } from "../store/forgeStore";

export function ProofCertModal() {
  const { certModalOpen, certificate, setCertModalOpen } = useForgeStore();

  if (!certModalOpen || !certificate) return null;

  const downloadJson = () => {
    const blob = new Blob([JSON.stringify(certificate, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${certificate.certificate_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4">
      <div className="w-full max-w-2xl flex flex-col rounded-xl border border-emerald-500/40 bg-zinc-950 shadow-2xl">
        <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800">
          <span className="text-sm font-bold text-emerald-300">
            Signed UNSAT Proof Certificate · {certificate.certificate_id}
          </span>
          <div className="flex items-center gap-2">
            <a
              href={`/api/forge/report/${encodeURIComponent(certificate.certificate_id)}`}
              download={`${certificate.certificate_id}-audit.md`}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded border border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-zinc-200 text-xs font-semibold"
            >
              <FileText className="w-3.5 h-3.5 text-cyan-400" />
              Download Audit Report (.md)
            </a>
            <button
              type="button"
              onClick={downloadJson}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              Download JSON
            </button>
            <button
              type="button"
              onClick={() => setCertModalOpen(false)}
              className="p-1 rounded hover:bg-zinc-800 text-zinc-400 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
        <pre className="p-4 mono text-[11px] leading-relaxed text-emerald-200 overflow-auto max-h-[65vh]">
          {JSON.stringify(certificate, null, 2)}
        </pre>
      </div>
    </div>
  );
}
