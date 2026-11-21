import type {
  ForgeRunRequest,
  ProofCertificate,
  ProofExportResponse,
  RedTeamResponse,
  ScenarioId,
  VerificationResult,
  VoiceConstraintResponse,
} from "../types/forge";

export class ApiClient {
  private baseUrl = "/api";

  async health(): Promise<{ status: string; mode: string; static_ui_ready?: boolean }> {
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

  async runRedTeam(scenarioId: ScenarioId): Promise<RedTeamResponse> {
    const res = await fetch(`${this.baseUrl}/forge/redteam`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario_id: scenarioId }),
    });
    if (!res.ok) throw new Error(`POST /api/forge/redteam failed: ${res.status}`);
    return res.json();
  }

  async parseVoiceConstraint(
    transcript: string,
    scenarioId: ScenarioId
  ): Promise<VoiceConstraintResponse> {
    const res = await fetch(`${this.baseUrl}/forge/voice-constraint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript, scenario_id: scenarioId }),
    });
    if (!res.ok) throw new Error(`POST /api/forge/voice-constraint failed: ${res.status}`);
    return res.json();
  }

  async fetchCertificate(certId: string): Promise<ProofCertificate> {
    const res = await fetch(`${this.baseUrl}/forge/certificate/${encodeURIComponent(certId)}`);
    if (!res.ok) throw new Error(`GET /api/forge/certificate failed: ${res.status}`);
    return res.json();
  }
}

export const apiClient = new ApiClient();
