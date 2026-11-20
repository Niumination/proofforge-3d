export class ApiClient {
  private baseUrl = "/api";

  async runForge(request: unknown): Promise<{ runId: string }> {
    const res = await fetch(`${this.baseUrl}/forge/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!res.ok) throw new Error(`POST /api/forge/run failed: ${res.status}`);
    return res.json();
  }

  async exportProof(result: unknown): Promise<{ url: string }> {
    const res = await fetch(`${this.baseUrl}/forge/export`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ result }),
    });
    if (!res.ok) throw new Error(`POST /api/forge/export failed: ${res.status}`);
    return res.json();
  }
}

export const apiClient = new ApiClient();
