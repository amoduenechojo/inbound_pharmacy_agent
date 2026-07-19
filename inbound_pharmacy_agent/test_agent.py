from unittest.mock import Mock, patch

from agent import ConversationAgent
from models import CallSession



def test_generate_reply_returns_text_for_a_plain_response():
    fake_client = Mock()
    fake_client.messages.create.return_value = _text_response("Hello there!")
    agent = ConversationAgent(client=fake_client)
    session = CallSession(caller_phone="+1-555-123-4567")

    reply = agent.generate_reply(session, "Hi")

    assert reply == "Hello there!"
    assert session.messages[0] == {"role": "user", "content": "Hi"}


@patch("agent.tools.schedule_callback")
def test_generate_reply_dispatches_tool_then_returns_final_text(mock_schedule):
    mock_schedule.return_value = {"action": "callback_scheduled"}
    fake_client = Mock()
    fake_client.messages.create.side_effect = [
        _tool_use_response(
            "schedule_callback",
            {"pharmacy_name": "HealthFirst", "preferred_time": "2pm"},
        ),
        _text_response("You're all set for 2pm!"),
    ]

    agent = ConversationAgent(client=fake_client)
    session = CallSession(caller_phone="+1-555-123-4567")

    reply = agent.generate_reply(session, "Can someone call me back at 2pm?")

    mock_schedule.assert_called_once_with(
        pharmacy_name="HealthFirst", preferred_time="2pm"
    )

    assert reply == "You're all set for 2pm!"
    assert fake_client.messages.create.call_count == 2


def test_system_prompt_includes_known_pharmacy_facts():
    from models import Pharmacy

    agent = ConversationAgent(client=Mock())
    session = CallSession(
        caller_phone="+1-555-123-4567",
        pharmacy=Pharmacy(
            id = "1", name = "HealthFirst Pharmacy", phone = "+1-555-123-4567",
            location = "New York, NY", rx_volume = 100, is_known=True,
        ),
    )

    prompt = agent._system_prompt(session)

    assert "HealthFirst Pharmacy" in prompt
    assert "New York, NY" in prompt


def test_system_prompt_asks_for_info_when_unrecognized():
    agent = ConversationAgent(client=Mock())
    session = CallSession(caller_phone="+1-555-000-0000", pharmacy=None)

    prompt = agent._system_prompt(session)

    assert "not found" in prompt
    assert "Rx" in prompt







def _text_response(text):
    block = Mock(type="text", text=text)
    return Mock(content=[block], stop_reason="end_turn")


def _tool_use_response(name, tool_input, tool_id="tool_1"):

    block = Mock(type="tool_use", input=tool_input, id=tool_id)
    block.name = name
    return Mock(content=[block], stop_reason="tool_use")
