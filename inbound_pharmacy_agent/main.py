
from models import CallSession, CallStage
from pharmacy_client import PharmacyClient
from agent import ConversationAgent

# Known pharmacy -- this exact number belongs to HealthFirst Pharmacy in
# the live API, so this exercises the "known" path (greeting uses real
# name/location/Rx volume).
MOCK_CALLER_PHONE = "+1-555-123-4567"

# Unknown pharmacy -- same format as the real records, but confirmed
# absent from the live API as of this writing(it's a shared sandbox
# other candidates also write test leads into, so this was checked
# against the full current list, not just the 5 seed records). Exercises
# the "unknown" path: the agent asks for name and Rx volume instead.
# MOCK_CALLER_PHONE = "+1-555-010-0000"

END_CALL_WORDS = {"bye", "goodbye", "hang up", "exit", "quit"}


def is_end_call(user_input: str) -> bool:
    text = user_input.lower()
    return any(word in text for word in END_CALL_WORDS)


def run_call(caller_phone: str = MOCK_CALLER_PHONE):

    session = CallSession(caller_phone = caller_phone)
    client = PharmacyClient()
    agent = ConversationAgent()

    print ("Call started")
    session.pharmacy = client.get_by_phone(caller_phone)
    session.stage = CallStage.IDENTIFIED

    if session.pharmacy:
        print(f" Identified caller as {session.pharmacy.name}")
    else:
        print(" Caller not recognized")

    opening = agent.generate_reply(session, "Hello, this is a pharmacy calling.")
    print(f"Agent: {opening}")

    session.stage = CallStage.CONVERSING


    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            session.stage = CallStage.ENDED
            print("\n[Call ended]")
            break

        if is_end_call(user_input):
            session.stage = CallStage.ENDED
            print("[Call ended]")
            break

        reply = agent.generate_reply(session, user_input)
        print(f"Agent: {reply}")

    return None


if __name__ == "__main__":
    run_call()