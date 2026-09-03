import os

from tools import validate_phone_call_config


def test_validate_phone_call_config_requires_trunk(monkeypatch):
    monkeypatch.delenv("LIVEKIT_SIP_OUTBOUND_TRUNK", raising=False)
    monkeypatch.delenv("SIP_OUTBOUND_TRUNK_ID", raising=False)
    assert "not configured" in validate_phone_call_config().lower()


def test_validate_phone_call_config_accepts_livekit_trunk(monkeypatch):
    monkeypatch.setenv("LIVEKIT_SIP_OUTBOUND_TRUNK", "test-trunk")
    monkeypatch.delenv("SIP_OUTBOUND_TRUNK_ID", raising=False)
    assert validate_phone_call_config() is None
