from tools import schedule_callback, send_followup_email


def test_schedule_callback_returns_expected_fields():
    result = schedule_callback("HealthFirst Pharmacy", "tomorrow 2pm")

    assert result["action"] == "callback_scheduled"
    assert result["pharmacy"] == "HealthFirst Pharmacy"
    assert result["time"] == "tomorrow 2pm"
    assert "logged_at" in result


def test_send_followup_email_returns_expected_fields():
    result = send_followup_email("HealthFirst Pharmacy", "interested in bulk pricing")

    assert result["action"] == "email_sent"
    assert result["pharmacy"] == "HealthFirst Pharmacy"
    assert result["summary"] == "interested in bulk pricing"
    assert "logged_at" in result
