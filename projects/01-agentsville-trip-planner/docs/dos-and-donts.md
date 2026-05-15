# Do And Don't

## Prompt Design

Do:

- State the agent role clearly.
- Include traveler details, dates, budget, interests, weather, and available activities.
- Tell the model not to invent activities, prices, dates, locations, or weather.
- Separate initial planning instructions from revision-agent instructions.

Don't:

- Ask for a "good itinerary" without specific constraints.
- Hide required business rules in notebook comments instead of the prompt.
- Let one prompt handle generation, evaluation, revision, and finalization with no structure.

## Structured Output

Do:

- Require JSON for machine-consumed output.
- Include the target schema in the prompt.
- Parse the JSON before using it.
- Print or log invalid output for debugging after checking it is safe.

Don't:

- Accept prose when downstream code expects JSON.
- Manually repair model JSON without noting the failure.
- Treat parseable JSON as proof that the itinerary is correct.

## Pydantic Validation

Do:

- Use Pydantic for vacation input and travel-plan output.
- Validate model output before running evals.
- Keep schema models close to the code that consumes them.

Don't:

- Use Pydantic as the only quality check.
- Ignore validation errors.
- Loosen schemas just to make invalid model output pass.

## Tool Calling

Do:

- Keep an explicit registry of supported tools.
- Validate tool-call JSON before execution.
- Return tool results as observations.
- Use deterministic tools for cost calculation and data lookup.

Don't:

- Let the model invent tool results.
- Execute unknown tool names.
- Trust tool arguments without validation.

## ReAct Loop

Do:

- Require `THOUGHT` and `ACTION`.
- Require `ACTION` to be JSON.
- Set a maximum number of loop steps.
- Require `run_evals_tool` before `final_answer_tool`.

Don't:

- Continue the loop after malformed actions without surfacing the error.
- Let the agent finalize before it has checked the itinerary.
- Assume the model will stop on its own.

## Evaluation

Do:

- Evaluate dates, budget, total cost, activity availability, traveler interests, weather compatibility, and feedback incorporation.
- Re-run all evals after a revision.
- Keep failure messages actionable.

Don't:

- Use vague evals such as "looks good".
- Treat LLM-based evals as deterministic truth.
- Claim the final plan passed without saved evidence.

## Notebook Submission Hygiene

Do:

- Clear or review notebook outputs before publishing.
- Keep output evidence only when it comes from an actual run.
- Check for API keys, private paths, stack traces, and raw secrets.
- Keep the notebook reproducible from top to bottom.

Don't:

- Commit `.env` files.
- Commit oversized notebook output when a smaller text artifact would be clearer.
- Fabricate successful outputs for submission.
