import json
import anthropic

import tools
from models import CallSession

MODEL = "claude-sonnet-5"
MAX_TOOL_ROUNDS = 5

TOOL_DEFINITIONS = [
    {
        "name": "schedule_callback",
        "description": "Schedule a callback for the pharmacy at a time they requested.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pharmacy_name": {"type": "string"},
                "preferred_time": {"type": "string"},
            },
            "required": ["pharmacy_name", "preferred_time"],
        },
    },

    {
        "name": "send_followup_email",
        "description": "Send a follow-up email summarizing what the pharmacy is interested in.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pharmacy_name": {"type": "string"},
                "summary": {"type": "string"},
            },
            "required": ["pharmacy_name", "summary"],
        },
    },
]

TOOL_NAMES = {"schedule_callback", "send_followup_email"}


class ConversationAgent:
    def __init__(self, client: anthropic.Anthropic = None):

        self.client = client or anthropic.Anthropic()

    def _system_prompt(self, session: CallSession):
        pharmacy = session.pharmacy
        if pharmacy and pharmacy.is_known:
            known_facts = (
                f"The caller has been identified as {pharmacy.name}, "
                f"located in {pharmacy.location or 'an unknown location'}, "
                f"with an estimated monthly Rx volume of "
                f"{pharmacy.rx_volume or 'an unknown amount'}."
            )
        else:
            known_facts = (
                "This caller's phone number was not found in our records. "
                "Early in the conversation, politely ask for their pharmacy "
                "name and their approximate monthly prescription (Rx) volume."
            )

        return f"""You are an inbound sales agent for TJM Labs, answering a call
from a pharmacy on our sales line.

{known_facts}

TJM Labs builds AI and automation tools that help high-Rx-volume pharmacies
handle repetitive, manual work, so their staff can process more
prescriptions with fewer errors and spend more time on patient care.

Rules:
- Only discuss TJM Labs, this pharmacy, and pharmacy operations. If asked
  about something outside that scope, say plainly that it's outside what
  you can help with on this call -- don't guess or make anything up.
- Once you know the caller's pharmacy name, use it naturally throughout
  the conversation.
- If the caller wants a callback or a follow-up email, use the matching
  tool rather than just saying you will."""

    def generate_reply(self, session: CallSession, user_input: str) -> str:
        session.add_message("user", user_input)

        for _ in range(MAX_TOOL_ROUNDS):
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=500,
                system=self._system_prompt(session),
                messages=session.messages,
                tools=TOOL_DEFINITIONS,
            )
            session.add_message("assistant", response.content)

            if response.stop_reason != "tool_use":
                return "".join(
                    block.text for block in response.content if block.type == "text"
                )

            tool_results = []
            for block in response.content:
                if block.type == "tool_use" and block.name in TOOL_NAMES:
                    func = getattr(tools, block.name)
                    result = func(**block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        }
                    )
            session.add_message("user", tool_results)

        return "Sorry, I'm having trouble completing that. Could you repeat what you need?"
