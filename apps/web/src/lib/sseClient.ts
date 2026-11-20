export const sseClient = {
  async * stream(runId: string): AsyncGenerator<{ event: string; data: unknown }> {
    // EventSource → GET /api/forge/stream/{runId}; Phase 1 deterministic mock
    const es = new EventSource(`/api/forge/stream/${runId}`);
    es.onmessage = (e: MessageEvent) => {
      const data = JSON.parse((e as MessageEvent).data);
      yield { event: (e as MessageEvent).data.event ?? "MESSAGE", data };
    };
    es.close();
  },
};
