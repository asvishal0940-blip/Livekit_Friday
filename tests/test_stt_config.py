import os

from agent import build_stt


def test_build_stt_uses_speechmatics_when_key_present(monkeypatch):
    monkeypatch.setenv("SPEECHMATICS_API_KEY", "test-key")
    monkeypatch.delenv("STT_PROVIDER", raising=False)

    stt = build_stt()

    assert stt.model == "speechmatics/enhanced"


def test_build_stt_falls_back_to_deepgram_without_key(monkeypatch):
    monkeypatch.delenv("SPEECHMATICS_API_KEY", raising=False)
    monkeypatch.delenv("STT_PROVIDER", raising=False)

    stt = build_stt()

    assert stt.model == "deepgram/nova-3"
