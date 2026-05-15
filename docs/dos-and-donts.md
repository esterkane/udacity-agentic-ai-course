# Do And Don't

Use this as a practical checklist for future agentic AI projects.

## 1. API Keys And Environment Handling

Do:

- Keep API keys in local environment variables or untracked local files.
- Document required variable names without showing real values.
- Fail early when a required key is missing.
- Keep `.env` and `.env.*` ignored by Git.

Don't:

- Do not commit real `.env` files, tokens, credentials, or private endpoints.
- Do not paste keys into notebooks, README files, screenshots, or output logs.
- Do not rely on a private repository as a substitute for secret hygiene.

Why it matters:

Leaked credentials can be reused outside the course project. Notebooks and generated outputs can expose keys through traces or printed environment values.

Example from the projects:

Project 2 loads `OPENAI_API_KEY` from the environment. That value should exist only locally, not in the repository.

## 2. Prompt Design

Do:

- Include role, task, input context, constraints, and output format.
- State negative constraints explicitly, such as "do not invent activities."
- Keep each agent's responsibility narrow.
- Use examples when the output has a strict shape.

Don't:

- Do not ask for broad outcomes such as "make a good plan" without measurable constraints.
- Do not rely on persona alone to enforce task behavior.
- Do not mix unrelated artifacts in one prompt when they need separate validation.

Why it matters:

Vague prompts produce fluent but hard-to-check output. Agentic workflows need prompts that produce inspectable intermediate artifacts.

Example from the projects:

Project 1's Expert Planner prompt works because it includes traveler details, weather, activities, constraints, and a required JSON output format.

## 3. Structured Outputs

Do:

- Use JSON when Python code or another agent will consume the result.
- Require one object or one clearly defined array.
- Keep machine-readable output separate from narrative summaries.
- Reject output that cannot be parsed.

Don't:

- Do not accept prose when downstream code expects JSON.
- Do not manually rewrite model output to make it appear valid.
- Do not treat valid JSON as proof that the content is correct.

Why it matters:

Structured output makes parsing, validation, evals, and later workflow steps possible. It solves shape, not truth.

Example from the projects:

Project 1 requires the itinerary as `TravelPlan` JSON before running Pydantic validation and itinerary evals.

## 4. Pydantic Validation

Do:

- Define Pydantic models for important inputs and outputs.
- Validate LLM output before passing it to tools or evals.
- Use validation errors as debugging signal.
- Keep schemas aligned with the code that consumes them.

Don't:

- Do not weaken schemas just to make bad output pass.
- Do not use Pydantic as the only quality check.
- Do not ignore validation errors and continue the workflow.

Why it matters:

Pydantic catches malformed structure, wrong types, missing fields, and invalid nested objects before failures spread downstream.

Example from the projects:

Project 1 validates `VacationInfo` for input and `TravelPlan`-style models for generated itinerary output.

## 5. Tool Calling

Do:

- Keep a fixed registry of supported tools.
- Validate tool names and arguments before execution.
- Use deterministic tools for deterministic tasks such as cost calculation.
- Return tool results as observations, not as hidden state.

Don't:

- Do not let the model invent tool results.
- Do not execute unknown tool names.
- Do not pass unvalidated model-generated arguments into tools.

Why it matters:

Tools are useful because Python executes real operations. If the model can fake tool results, the workflow loses the reliability benefit.

Example from the projects:

Project 1 uses `calculator_tool`, `get_activities_by_date_tool`, `run_evals_tool`, and `final_answer_tool` inside the itinerary revision flow.

## 6. ReAct Loops

Do:

- Require `THOUGHT` and `ACTION`.
- Require `ACTION` to be parseable JSON.
- Set a maximum number of loop steps.
- Require evals before finalization.
- Log thoughts, actions, observations, and final answers.

Don't:

- Do not continue after malformed actions without surfacing the error.
- Do not assume the model will stop on its own.
- Do not allow `final_answer_tool` before required checks have passed.

Why it matters:

ReAct loops are powerful but fragile. Strict formatting and loop control prevent unbounded execution and unverified final answers.

Example from the projects:

Project 1's Resourceful Itinerary Revision Agent uses a THOUGHT -> ACTION -> OBSERVATION cycle and should run evals before calling `final_answer_tool`.

## 7. Evaluation Agents

Do:

- Write explicit criteria.
- Prefer pass/fail plus reasons.
- Combine model-based evaluation with deterministic checks.
- Re-run the full eval suite after revisions.
- Limit correction-loop iterations.

Don't:

- Do not ask vague questions such as "is this good?"
- Do not treat evaluator approval as absolute truth.
- Do not evaluate only the field that failed last time.

Why it matters:

Evaluation agents catch format and quality problems, but they only check what their criteria specify.

Example from the projects:

Project 2 uses `EvaluationAgent` to check Product Manager, Program Manager, and Development Engineer outputs against role-specific criteria.

## 8. Routing Agents

Do:

- Define route descriptions clearly.
- Add negative boundaries when routes overlap.
- Log similarity scores, keyword boosts, and selected route.
- Use fallback behavior for unsupported input.
- Test short prompts and ambiguous prompts.

Don't:

- Do not hide routing decisions inside a black-box prompt.
- Do not rely only on embeddings for very short route prompts.
- Do not let keyword boosts overpower bad route design.

Why it matters:

Wrong routing sends good prompts to the wrong specialist, producing output that can look plausible but answer the wrong task.

Example from the projects:

Project 2 uses embedding-based routing plus capped keyword boosts for Product Manager, Program Manager, and Development Engineer workflow steps.

## 9. Output Evidence

Do:

- Save outputs from actual notebook or script runs.
- Include enough logs to support claims such as evals passing.
- Keep generated artifacts separate from source code.
- Label outputs clearly.

Don't:

- Do not fabricate outputs.
- Do not claim tests passed without evidence.
- Do not overwrite failure evidence without saving the actual replacement run.

Why it matters:

Course submissions need reproducible evidence. Fabricated or edited outputs hide workflow failures and make debugging impossible.

Example from the projects:

Project 2 includes output text files such as workflow output, routing output, and static check output. These should represent real runs.

## 10. GitHub / Submission Hygiene

Do:

- Review notebooks, logs, and generated outputs before committing.
- Keep `.gitignore` current for `.env`, virtual environments, caches, logs, and OS/editor clutter.
- Commit focused changes with clear messages.
- Document known limitations directly.
- Keep project documentation close to the project folder.

Don't:

- Do not commit API keys, local paths, notebook checkpoints, caches, or oversized temporary output.
- Do not overstate production readiness.
- Do not mix unrelated project changes into a course submission commit.

Why it matters:

Clean submissions are easier to review, safer to publish, and easier to extend when later course projects are added.

Example from the projects:

The repository keeps Project 1 and Project 2 in separate folders and uses documentation pages for architecture, lessons learned, troubleshooting, and quiz material.
