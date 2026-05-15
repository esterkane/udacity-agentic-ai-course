# ReAct Agent Notes

## Working Definition

ReAct-style workflows alternate between reasoning about the next step and taking an action. In implementation, the important parts are tool boundaries, action logging, and verification of results.

## Do

- Keep tool outputs visible enough for debugging.
- Validate tool results before continuing.
- Stop when the next action is unsupported.

## Don't

- Let the model invent tool results.
- Continue after a failed action without recording the failure.
- Let the agent finalize before required evals pass.

## Project Example

- Project 1 uses a Resourceful Itinerary Revision Agent with a THOUGHT -> ACTION -> OBSERVATION loop.
- Python parses the `ACTION` JSON, executes tools, and returns `OBSERVATION`.
- The revision agent should run evals before calling `final_answer_tool`.
