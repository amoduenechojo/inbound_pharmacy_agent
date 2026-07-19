"""Mocked follow-up actions.

Per the PRD, these don't need to actually send an email or book a real
callback -- logging what *would* happen is sufficient. Each one returns
a dict so the caller (agent.py) has something concrete to report back
to the LLM as a tool result.
"""

from datetime import datetime


def schedule_callback(pharmacy_name: str, preferred_time: str) -> dict:
    result = {
        "action": "callback_scheduled",
        "pharmacy": pharmacy_name,
        "time": preferred_time,
        "logged_at": datetime.now().isoformat(timespec="seconds"),
    }
    print(f"[MOCK] Callback scheduled for {pharmacy_name} at {preferred_time}")
    return result


def send_followup_email(pharmacy_name: str, summary: str) -> dict:
    result = {
        "action": "email_sent",
        "pharmacy": pharmacy_name,
        "summary": summary,
        "logged_at": datetime.now().isoformat(timespec="seconds"),
    }
    print(f"[MOCK] Follow-up email sent to {pharmacy_name}: {summary}")
    return result
