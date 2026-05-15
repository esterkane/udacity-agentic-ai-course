# Do And Don't

## Do

- Keep each agent's responsibility narrow.
- Use stable route labels.
- Save representative outputs when they support the project submission.
- Validate output format before chaining to the next step.
- Document evaluator criteria.
- Log routing scores and selected agents.
- Preserve prior workflow context for later steps.

## Don't

- Do not let the evaluator replace human review of the product plan.
- Do not hardcode secrets or private endpoints.
- Do not mix generated project plans with source code without clear folder boundaries.
- Do not claim the workflow passed tests unless output evidence is committed.
- Do not rely on embedding similarity alone for short routing prompts.
- Do not let evaluator corrections remove valid existing content.

## Examples

- Use Product Manager only for user stories, not features or tasks.
- Use Program Manager for features derived from stories and the product spec.
- Use Development Engineer for engineering tasks with acceptance criteria, effort, and dependencies.
- Use capped keyword boosts for route terms such as `user story`, `feature`, and `engineering`.
