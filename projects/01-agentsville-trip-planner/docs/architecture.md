# Architecture

## High-Level Flow

The project has two main stages.

Stage 1: Expert Planner

1. Vacation details are represented with Pydantic.
2. Mocked weather and activity data are collected for the requested date range.
3. The Expert Planner prompt includes traveler details, weather data, activity data, output instructions, and the target schema.
4. The LLM returns a structured itinerary.
5. Python extracts the JSON and validates it as a travel plan.

Stage 2: Resourceful Itinerary Revision Agent

1. The initial itinerary and traveler feedback are passed to a ReAct-style revision agent.
2. The agent responds with `THOUGHT` and `ACTION`.
3. Python parses the `ACTION` JSON.
4. Python executes the requested tool.
5. The tool result is returned as an `OBSERVATION`.
6. The loop repeats until the agent calls `final_answer_tool`.
7. The revised plan is evaluated before final acceptance.

## Data Model Flow

Input data starts as vacation details:

- Travelers.
- Destination.
- Start and end dates.
- Budget.
- Interests and preferences.

The notebook uses Pydantic models to make this input explicit. `VacationInfo` is the main input object. The planner output is represented by travel-plan models such as weather, activity, day-level itinerary items, and the full travel plan.

Data flow:

1. Raw vacation details are encoded as structured data.
2. `VacationInfo` validates the input structure.
3. Weather and activity records are collected for each date.
4. The LLM receives the validated vacation object plus contextual weather/activity data.
5. The LLM returns JSON.
6. Pydantic validates the returned JSON against the travel-plan schema.
7. Evaluation functions inspect the validated object.

Pydantic catches malformed structure, but separate evals are needed for semantic checks such as invented activities, budget errors, and weather mismatch.

## Prompt Flow

The Expert Planner prompt has several jobs:

- Set the role: expert travel planner for AgentsVille.
- Provide task instructions: build a realistic day-by-day itinerary.
- Provide context: traveler details, weather data, and available activities.
- Provide constraints: do not invent activities, dates, weather, prices, or locations.
- Provide output format: return a JSON object matching the travel-plan schema.
- Provide planning guidance: check dates, interests, weather, activity availability, and cost.

The revision prompt has a different job. It must force the agent into a strict ReAct protocol:

```text
THOUGHT:
...
ACTION:
{"tool_name": "...", "arguments": {...}}
```

The model does not execute tools. Python owns tool execution and returns observations.

## Tool Loop Flow

The ReAct loop uses simulated tools:

| Tool | Purpose |
| --- | --- |
| `calculator_tool` | Calculate totals reliably instead of trusting mental arithmetic from the model. |
| `get_activities_by_date_tool` | Retrieve available activities for a specific date. |
| `run_evals_tool` | Run itinerary checks before finalization. |
| `final_answer_tool` | Signal that the loop is complete and return the final structured plan. |

Loop control:

1. Model emits `THOUGHT` and `ACTION`.
2. Python parses the action JSON.
3. Python validates the tool name and arguments.
4. Python executes the tool.
5. Python appends the tool result as `OBSERVATION`.
6. The model decides the next action.
7. The loop stops only when `final_answer_tool` is called or a maximum step limit is reached.

## Evaluation Flow

Evaluation checks should happen before the final plan is accepted.

Typical checks:

- Start and end dates match the vacation request.
- Destination is correct.
- Total cost equals the sum of selected activity prices.
- Total cost is within budget.
- Activities exist in the available activity data.
- Selected activities match traveler interests.
- Activities are compatible with the weather.
- Traveler feedback is incorporated, such as at least two activities per day.

Some checks are deterministic, such as cost summation and date matching. Other checks, such as weather compatibility, may require LLM judgment because activity descriptions can include indoor backups or conditional weather handling.

## Failure Handling

Important failure cases:

- Invalid JSON from the planner.
- JSON that parses but fails Pydantic validation.
- Activities invented by the model.
- Weather/activity mismatch.
- Cost mismatch.
- ReAct response missing `ACTION`.
- Tool name not recognized.
- Tool arguments fail validation.
- Agent calls `final_answer_tool` before running evals.
- Loop reaches max steps without a final answer.

Practical handling:

- Fail loudly on parse and schema errors.
- Print the invalid JSON for debugging after checking it does not contain secrets.
- Keep a tool registry and reject unknown tools.
- Require `run_evals_tool` before `final_answer_tool`.
- Use max loop steps.
- Run the complete eval suite after revision.
