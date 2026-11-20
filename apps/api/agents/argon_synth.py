"""Argon synthesizer — Phase 3: Gemini 4 Argon co-generator & patcher (dibangun nanti)."""


class ArgonSynth:
    def __init__(self, model: str) -> None:
        self.model = model

    def synthesize(self, *args, **kwargs):
        raise NotImplementedError("Phase 3: co-generation via Gemini 4 Argon")
