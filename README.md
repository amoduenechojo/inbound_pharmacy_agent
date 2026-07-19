# Inbound Pharmacy Sales Agent

Text-based simulation of TJM Labs' inbound pharmacy sales line. See `DESIGN.md` for the design doc.

## Project structure

```
models.py                 Pharmacy and CallSession data classes
pharmacy_client.py        Identifies a pharmacy by phone via the mock API, normalizes both record shapes
tools.py                  Mocked follow-up actions (callback, email) -- log/print only, per the PRD
agent.py                  Builds the system prompt, calls the LLM, dispatches tools
main.py                   Text-based REPL that runs a simulated call
test_*.py                 Unit tests, flat in the project root -- the pharmacy API and the LLM are both mocked
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

Get a key at console.anthropic.com if you don't have one yet.

## Run a simulated call

```bash
python main.py
```

By default `MOCK_CALLER_PHONE` in `main.py` is set to a number that matches a known pharmacy in the API, so you'll see the "recognized caller" path. Change it to any number not in the API (e.g. `+1-555-000-0000`) to see the "unknown pharmacy" path instead, where the agent asks for the pharmacy's name and Rx volume.

Type `bye` (or `exit`, `quit`, `goodbye`, `hang up`) to end the call.

## Run the tests

```bash
pytest -v
```

All 15 tests pass. The pharmacy API call and the LLM call are both mocked, so the suite runs with no network connection and no API key needed.
