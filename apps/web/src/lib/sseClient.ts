export interface ParsedSSEEvent {
  event: string;
  data: Record<string, unknown>;
}

const NAMED_EVENTS = [
  "STAGE_CHANGED",
  "AGENT_LOG",
  "HOOK_AUDIT",
  "PROXY_AUDIT",
  "VERIFICATION_RESULT",
  "PATCH_DIFF",
  "PROOF_CERTIFICATE",
  "ERROR",
] as const;

export const sseClient = {
  async *stream(runId: string, signal?: AbortSignal): AsyncGenerator<ParsedSSEEvent> {
    const es = new EventSource(`/api/forge/stream/${encodeURIComponent(runId)}`);
    const queue: ParsedSSEEvent[] = [];
    let wake: (() => void) | null = null;
    let done = false;

    const push = (event: string, raw: string) => {
      try {
        const parsed = JSON.parse(raw) as Record<string, unknown>;
        queue.push({ event, data: parsed });
        if (event === "STAGE_CHANGED" && parsed.stage === "COMPLETE") {
          done = true;
        }
      } catch {
        queue.push({ event, data: { raw } });
      }
      if (wake) {
        const fn = wake;
        wake = null;
        fn();
      }
    };

    for (const evName of NAMED_EVENTS) {
      es.addEventListener(evName, (e: Event) => {
        const msg = e as MessageEvent<string>;
        push(evName, msg.data);
      });
    }

    es.onerror = () => {
      done = true;
      es.close();
      if (wake) {
        const fn = wake;
        wake = null;
        fn();
      }
    };

    const onAbort = () => {
      done = true;
      es.close();
      if (wake) {
        const fn = wake;
        wake = null;
        fn();
      }
    };
    signal?.addEventListener("abort", onAbort);

    try {
      while (!done || queue.length > 0) {
        if (queue.length > 0) {
          yield queue.shift()!;
        } else if (!done) {
          await new Promise<void>((resolve) => {
            wake = resolve;
          });
        }
      }
    } finally {
      signal?.removeEventListener("abort", onAbort);
      es.close();
    }
  },
};
