# Troubleshooting

## Model Returns Prose Instead Of JSON

Symptom: The planner returns paragraphs, bullets, or markdown instead of a `TravelPlan` JSON object.

Likely cause: The prompt did not make JSON mandatory or did not show the schema.

Fix:

- Require a single JSON object.
- Include the target schema.
- Tell the model not to include extra text inside the JSON block.
- Reject prose output instead of trying to use it.

## JSON Parse Error

Symptom: JSON extraction or parsing fails.

Likely cause: The response contains extra prose, trailing commas, comments, broken quoting, or multiple JSON blocks.

Fix:

- Extract only the JSON block.
- Print the failing text for review if safe.
- Tighten the prompt.
- Re-run the cell after correcting the prompt or parser.

## Schema Validation Fails

Symptom: Pydantic rejects the parsed JSON.

Likely cause: Missing fields, wrong types, invalid dates, or incorrect nested structure.

Fix:

- Compare the failing JSON to the Pydantic schema.
- Add the schema to the prompt.
- Make required field names explicit.
- Do not weaken the schema just to pass invalid output.

## Agent Invents Activities

Symptom: The itinerary includes an activity ID, name, price, location, or date that is not in the activity data.

Likely cause: The model filled gaps from imagination instead of copying from the provided activities.

Fix:

- Tell the planner to copy selected activity objects exactly.
- Add an eval that compares itinerary activity IDs against available activity IDs.
- Fail the run if invented activities are found.

## Total Cost Mismatch

Symptom: `total_cost` does not equal the sum of selected activity prices.

Likely cause: The model performed arithmetic incorrectly or changed activities without updating total cost.

Fix:

- Recalculate cost with `calculator_tool` or deterministic Python.
- Add an eval for total-cost accuracy.
- Require the revision agent to fix cost mismatches before final answer.

## Weather Compatibility Eval Fails

Symptom: An activity is flagged as incompatible with the day's weather.

Likely cause: The model selected an outdoor activity during rain or thunderstorm, or the evaluator did not recognize an indoor backup.

Fix:

- Check the activity description.
- Prefer indoor activities during bad weather.
- Allow outdoor activities only when the description explicitly says they can move indoors or have a weather-safe backup.
- Improve the eval criteria for conditional weather language.

## ReAct Agent Does Not Include ACTION

Symptom: The revision agent returns a thought or explanation but no parseable action.

Likely cause: The prompt did not enforce the ReAct response format strongly enough.

Fix:

- Require `THOUGHT` and `ACTION` sections.
- Require `ACTION` to be JSON.
- Return a formatting error as the observation if the loop supports it.
- Re-run with stricter prompt wording.

## final_answer_tool Called Too Early

Symptom: The agent finalizes before running evals or before fixing known failures.

Likely cause: The stop condition is too easy or the prompt does not require evals before finalization.

Fix:

- Require `run_evals_tool` before `final_answer_tool`.
- Track whether evals have run.
- Reject final answers if evals have not passed.

## Notebook Output Too Large

Symptom: The notebook becomes slow, difficult to review, or too noisy for submission.

Likely cause: Large traces, dataframe renders, repeated model outputs, or verbose tool observations are stored in the notebook.

Fix:

- Clear unnecessary outputs before committing.
- Save concise output evidence separately in `outputs/`.
- Keep only the traces needed to prove the workflow ran and passed evals.

## API Key Not Found

Symptom: Model calls fail before a response is returned.

Likely cause: Required environment variables are missing from the local session.

Fix:

- Set API credentials locally.
- Do not commit `.env` files.
- Use placeholder names in documentation only.
- Restart the notebook kernel after changing environment variables.
