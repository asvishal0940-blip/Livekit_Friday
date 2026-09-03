from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION


def test_friday_agent_prompt_contains_telephony_directives():
    assert "FRIDAY — PHONE CALLING & TELEPHONY AGENT MASTER PROMPT" in AGENT_INSTRUCTION
    assert "CALL_COMPLETED" in AGENT_INSTRUCTION
    assert "Before transfer:" in AGENT_INSTRUCTION
    assert "Transfer the call to the user" in AGENT_INSTRUCTION
    assert "Only do that if there is an open topic" not in SESSION_INSTRUCTION


def test_friday_session_prompt_uses_proper_persona():
    assert "Friday" in SESSION_INSTRUCTION
    assert "AI telephony and executive assistant" in SESSION_INSTRUCTION
    assert "Never claim a call or action succeeded" in SESSION_INSTRUCTION
