# Troubleshooting

This guide covers practical issues from the Udacity Agentic AI course projects: the AgentsVille Trip Planner notebook and the Agentic Workflow Project Management Python workflow.

## Python Was Not Found On Windows

Symptom:

- Running `python` returns a message that Python was not found.
- PowerShell opens the Microsoft Store or reports that `python` is not recognized.

Likely cause:

- Python is not installed.
- Python is installed but not on `PATH`.
- Windows app execution aliases are intercepting `python`.

Fix:

1. Run `py --version`.
2. If `py` works, use `py` instead of `python`.
3. If neither works, install Python from python.org or your approved course environment.
4. Reopen PowerShell after installation.
5. Confirm with `python --version` or `py --version`.

Prevention:

- Document whether the project uses `python`, `py`, or a notebook kernel.
- Verify the interpreter before running scripts.

## PowerShell Blocks .ps1 Script Execution

Symptom:

- Running a `.ps1` file fails with an execution-policy error.
- PowerShell says scripts are disabled on this system.

Likely cause:

- Windows PowerShell execution policy blocks local scripts.

Fix:

1. Run the commands manually if the script is short.
2. For the current PowerShell session only, use:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. Run the `.ps1` script again.

Prevention:

- Include both `.ps1` and `.sh` options only when needed.
- Document manual command equivalents for important scripts.
- Avoid asking users to change machine-wide execution policy for course work.

## Running A PowerShell Script With Python Causes SyntaxError

Symptom:

- Running `python run_all_tests.ps1` produces `SyntaxError`.
- Python points at PowerShell syntax such as `$env:` or `Write-Host`.

Likely cause:

- A PowerShell script was passed to the Python interpreter.

Fix:

1. Check the file extension.
2. Run PowerShell scripts with PowerShell:

   ```powershell
   .\run_all_tests.ps1
   ```

3. Run Python scripts with Python:

   ```powershell
   python script_name.py
   ```

Prevention:

- Keep run instructions explicit about the interpreter.
- Use filenames that make script type obvious.

## VS Code Says .env Injection Is Disabled

Symptom:

- VS Code reports that `.env` injection is disabled.
- Notebook or terminal sessions do not see expected environment variables.

Likely cause:

- VS Code settings or notebook environment handling are not loading `.env`.
- The active kernel was started before environment variables were set.

Fix:

1. Set the variable in the active terminal session.
2. Restart the notebook kernel.
3. Confirm the variable exists without printing the secret value.
4. If needed, configure VS Code Python environment settings for local development.

Prevention:

- Do not depend on editor-specific `.env` injection.
- Document required variable names.
- Keep secrets outside committed files.

## API Key Not Found

Symptom:

- The code fails before a model response is returned.
- Error text mentions a missing API key or missing `OPENAI_API_KEY`.

Likely cause:

- The key is not set in the current shell, notebook kernel, or environment.
- The notebook kernel was not restarted after setting the variable.

Fix:

1. Set the key locally in the shell or untracked local environment file.
2. Restart the notebook kernel or terminal session.
3. Confirm the variable is present without printing the full key.
4. Re-run the failing cell or script.

Prevention:

- Fail early with a clear message when the key is missing.
- Never commit `.env` files.
- Document required variable names only.

## Invalid Key / BadRequestError

Symptom:

- API calls fail with `BadRequestError`, authentication errors, or invalid-key messages.
- The code reaches the API client but the request is rejected.

Likely cause:

- The key is expired, malformed, copied incorrectly, or for the wrong environment.
- The base URL does not match the course provider environment.
- The model name is unsupported in the configured environment.

Fix:

1. Confirm the key was copied without spaces or quotes.
2. Confirm the correct base URL for the course environment.
3. Confirm the model name is available.
4. Replace the local key if it is expired.
5. Re-run a minimal API call before running the whole notebook.

Prevention:

- Keep provider-specific setup notes.
- Do not hardcode base URLs or keys unless the course environment explicitly requires a placeholder.
- Test credentials with a minimal call first.

## Outputs Contain Traceback

Symptom:

- Notebook or output files include Python `Traceback` sections.
- Submission artifacts show failed cells or stack traces.

Likely cause:

- A cell or script failed and its output was saved.
- The notebook was not rerun cleanly after fixing the issue.

Fix:

1. Read the traceback from the first error line to the root cause.
2. Fix the code, prompt, environment, or data issue.
3. Restart the kernel.
4. Run from top to bottom.
5. Save new output evidence only after the run is clean.

Prevention:

- Review outputs before committing or zipping.
- Keep failure traces only when they are intentionally documented for troubleshooting.

## Notebook Output Exceeds Size Limit

Symptom:

- The notebook is too large to upload.
- GitHub renders slowly or refuses to display the notebook.
- Course submission complains about file size.

Likely cause:

- Large model traces, dataframe renders, repeated observations, or images are stored in notebook output.

Fix:

1. Clear unnecessary notebook outputs.
2. Keep only concise evidence needed for review.
3. Save important output excerpts as text files in `outputs/`.
4. Re-run only if fresh evidence is needed.

Prevention:

- Avoid storing every intermediate trace in the notebook.
- Use separate output files for long logs.
- Review notebook size before submission.

## JSON Parsing Fails

Symptom:

- Parsing the model response raises a JSON error.
- The response includes markdown, extra prose, comments, or malformed quotes.

Likely cause:

- The model did not return strict JSON.
- The parser extracted the wrong block.
- The prompt allowed mixed prose and JSON.

Fix:

1. Print the raw response if safe.
2. Extract only the JSON block.
3. Tighten the prompt to require exactly one JSON object.
4. Re-run the model call.
5. Fail the run if parsing still fails.

Prevention:

- Include the schema in the prompt.
- Keep narrative summaries separate from JSON generation.
- Validate before downstream use.

## Pydantic Validation Fails

Symptom:

- JSON parses but Pydantic rejects it.
- Errors mention missing fields, wrong types, invalid dates, or nested object mismatch.

Likely cause:

- The model returned the wrong structure.
- Field names differ from the schema.
- The prompt did not include the schema or required fields.

Fix:

1. Read the Pydantic error path.
2. Compare the failing output to the model schema.
3. Add or clarify schema instructions in the prompt.
4. Re-run generation.
5. Do not loosen the schema unless the domain model is actually wrong.

Prevention:

- Use Pydantic schemas as prompt context.
- Validate immediately after generation.
- Add regression examples for common validation failures.

## ReAct Agent Does Not Produce ACTION

Symptom:

- The agent returns `THOUGHT` only.
- The agent gives prose instead of an `ACTION` JSON object.
- The tool loop cannot continue.

Likely cause:

- The prompt did not enforce the ReAct format strongly enough.
- The model tried to answer directly instead of using tools.

Fix:

1. Reject the response as malformed.
2. Return a formatting error observation if the loop supports it.
3. Tighten the prompt to require `THOUGHT` and `ACTION`.
4. Show the exact expected action JSON shape.

Prevention:

- Unit-test the action parser with malformed responses.
- Keep ReAct output format short and strict.
- Use a max step count.

## ReAct Agent Calls final_answer_tool Too Early

Symptom:

- The agent finalizes before running evals.
- The final itinerary still violates budget, weather, activity, or feedback constraints.

Likely cause:

- The prompt does not require evals before finalization.
- The controller does not track whether evals have passed.

Fix:

1. Reject `final_answer_tool` if evals have not run.
2. Return an observation telling the agent to call `run_evals_tool`.
3. Require passing evals before accepting final output.

Prevention:

- Add a controller-side flag for `evals_passed`.
- State the finalization rule in the system prompt.
- Run final evals after the loop completes.

## RoutingAgent Picks Wrong Agent

Symptom:

- A user-story task goes to the Program Manager or Development Engineer.
- A feature task goes to the wrong role.
- Logs show unexpected route selection.

Likely cause:

- Route descriptions overlap.
- The prompt is too short for embedding similarity.
- Keyword boosts are missing or too strong.

Fix:

1. Inspect routing logs: similarity, keyword boost, and final score.
2. Improve route descriptions.
3. Add route-specific keywords for short prompts.
4. Cap keyword boosts so they do not overpower semantic fit.
5. Add fallback behavior for ambiguous input.

Prevention:

- Test routing with short, long, and ambiguous prompts.
- Keep route responsibilities mutually exclusive.
- Log route decisions in output evidence.

## EvaluationAgent Over-Corrects And Removes Useful Content

Symptom:

- A revised response satisfies one criterion but drops useful detail.
- The output becomes shorter, less complete, or loses required context.

Likely cause:

- Correction instructions were too narrow.
- The evaluator focused only on the failed criterion.
- The worker agent was not told to preserve valid content.

Fix:

1. Add "preserve correct existing content" to correction prompts.
2. Re-run the full evaluation suite.
3. Compare before and after output.
4. Tighten evaluation criteria to include completeness.

Prevention:

- Use full-artifact evals after every correction.
- Limit correction iterations.
- Keep previous output available during revision.

## Generated Output Misses Rubric-Required Sections

Symptom:

- Project output lacks user stories, product features, engineering tasks, eval results, or required notebook sections.

Likely cause:

- The planner skipped a required workflow step.
- The prompt did not list required sections.
- The evaluator checked style but not rubric coverage.

Fix:

1. List rubric-required sections explicitly.
2. Normalize action-planning output against required steps.
3. Add an eval that checks required section names.
4. Regenerate missing sections only after preserving valid existing output.

Prevention:

- Convert rubric requirements into a checklist.
- Use structured output or fixed headings.
- Keep the rubric close to the workflow prompt.

## .env Accidentally Included In Zip

Symptom:

- A submission ZIP contains `.env` or `.env.*`.
- The ZIP includes credentials or local configuration.

Likely cause:

- The ZIP was created from the whole working directory without exclusions.
- `.gitignore` was treated as enough, but ZIP tools do not automatically follow `.gitignore`.

Fix:

1. Delete the ZIP.
2. Remove `.env` from the package directory.
3. Rotate any exposed credentials.
4. Recreate the ZIP from a clean export folder.
5. Inspect the ZIP contents before submission.

Prevention:

- Use a clean staging folder for submissions.
- Inspect ZIP contents.
- Keep `.env` outside project folders when possible.

## __pycache__ Included In Zip

Symptom:

- Submission ZIP contains `__pycache__/` folders or `.pyc` files.

Likely cause:

- Python cache files were generated during local runs and the entire folder was zipped.

Fix:

1. Delete `__pycache__/` folders and `.pyc` files from the submission folder.
2. Recreate the ZIP.
3. Inspect the ZIP contents.

Prevention:

- Add `__pycache__/` and `*.pyc` to `.gitignore`.
- Build submissions from a clean folder.
- Do not zip runtime caches.
