import type { ForgeRunRequest, ProofExportResponse, ScenarioId, VerificationResult } from "../types/forge";

export class ApiClient {
  private baseUrl = "/api";

  async health(): Promise<{ status: string; mode: string }> {
    const res = await fetch(`${this.baseUrl}/health`);
    if (!res.ok) throw new Error(`GET /api/health failed: ${res.status}`);
    return res.json();
  }

  async runForge(request: ForgeRunRequest): Promise<{ runId: string }> {
    const res = await fetch(`${this.baseUrl}/forge/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!res.ok) throw new Error(`POST /api/forge/run failed: ${res.status}`);
    return res.json();
  }

  async exportProof(scenarioId: ScenarioId, result: VerificationResult): Promise<ProofExportResponse> {
    const res = await fetch(`${this.baseUrl}/forge/export`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario_id: scenarioId, result }),
    });
    if (!res.ok) throw new Error(`POST /api/forge/export failed: ${res.status}`);
    return res.json();
  }
}

export const apiClient = new ApiClient();
