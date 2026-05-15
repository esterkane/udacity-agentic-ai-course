# Project 01: AgentsVille Trip Planner

## Project Summary

AgentsVille Trip Planner is a Jupyter Notebook-based AI assistant for building and revising a day-by-day travel itinerary. The project has two major stages:

1. An Expert Planner generates an initial structured itinerary from validated vacation details, weather data, and available activity data.
2. A Resourceful Itinerary Revision Agent uses a ReAct loop to inspect, evaluate, and revise the itinerary before returning the final plan.

The project is not a production travel planner. It is a course project that demonstrates prompt chaining, structured JSON output, Pydantic validation, simulated tool calling, ReAct-style control flow, and evaluation-driven refinement.

## Architecture Overview

The notebook flow is:

1. Define vacation details with Pydantic models.
2. Collect mocked weather and activity data for each travel date.
3. Prompt an Expert Planner LLM to generate a `TravelPlan` JSON object.
4. Parse and validate the JSON into Pydantic objects.
5. Run itinerary evaluation functions.
6. Pass the itinerary and traveler feedback to a ReAct revision agent.
7. Parse the agent's `ACTION` JSON, execute tools, return `OBSERVATION`, and continue until `final_answer_tool` is called.
8. Run final evals before accepting the revised plan.

## Main Files

| Path | Purpose |
| --- | --- |
| `src-or-notebooks/project_final.ipynb` | Sanitized project notebook. A hardcoded API key was replaced with `os.getenv("OPENAI_API_KEY")`. |
| `src-or-notebooks/project_lib.py` | Support library used by the notebook for mocked weather/activity data and display helpers. |
| `outputs/` | Reserved for separate output evidence files if the notebook is rerun later. |
| `docs/architecture.md` | Detailed flow of models, prompts, tools, evals, and failure handling. |
| `docs/lessons-learned.md` | Notes from the implementation patterns and tradeoffs. |
| `docs/dos-and-donts.md` | Practical guidance for prompts, validation, tools, ReAct, evals, and submission hygiene. |
| `docs/troubleshooting.md` | Common failure modes and fixes. |
| `docs/quiz.md` | Difficult review questions with answers. |

## How To Run

High-level local flow:

1. Create and activate a Python virtual environment.
2. Install the notebook dependencies from the project notebook or exported requirements.
3. Set required API credentials in the local shell or a local `.env` file outside Git.
4. Open the notebook in Jupyter.
5. Run cells from top to bottom.
6. Review generated JSON, Pydantic validation output, ReAct traces, and final eval output.
7. Save output evidence only if it was produced by an actual run and does not contain secrets.

Do not claim the notebook ran successfully unless the output evidence is present and reviewable.

This repository update copied the completed notebook and support file. I did not rerun the notebook during the upload.

## Expected Final Outcome

The expected final artifact is a validated AgentsVille travel plan that:

- Covers the requested destination and travel dates.
- Uses only available activities from the provided activity data.
- Includes weather-aware activity choices.
- Stays within the traveler budget.
- Incorporates traveler interests and feedback.
- Includes at least two activities per day when that feedback is required.
- Passes the evaluation functions before final acceptance.

## Known Limitations

- Mocked weather and activity tools do not represent live travel data.
- Pydantic validates structure and types, not factual truth.
- Weather compatibility can require judgment that simple rules do not capture.
- The ReAct agent can stall if it does not emit valid `ACTION` JSON.
- LLM-based evaluation can miss issues if the criteria are incomplete.
- Notebook outputs can become large and noisy if every intermediate trace is kept.

## Security Notes

- Do not commit real API keys, `.env` files, tokens, or credentials.
- Review notebook metadata and outputs before committing.
- Do not commit private local paths or raw error traces that expose local environment details.
- Generated outputs must come from real notebook runs. Do not fabricate output evidence.
