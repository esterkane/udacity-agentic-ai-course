# Troubleshooting

## Missing Credentials

Symptom: Scripts fail before a model response is returned.

Likely cause: API credentials are not set in the active shell or notebook environment.

Resolution:
- Set required environment variables locally.
- Do not commit `.env` files.
- Keep only placeholder examples if needed.

## Agent Output Fails Evaluation

Symptom: The evaluation agent reports missing fields or weak quality.

Likely cause: The worker prompt did not require the exact artifact shape, or evaluator criteria are stricter than the generation prompt.

Resolution:
- Inspect the generated artifact.
- Tighten the generator prompt.
- Make the evaluator criteria explicit and measurable.
- Preserve correct content when asking for revisions.

## Routing Failure

Symptom: The routing agent selects the wrong specialized agent.

Likely cause: Route descriptions overlap, the input is short, or keyword boosts are missing/misweighted.

Resolution:
- Add route examples.
- Make route definitions mutually exclusive.
- Add fallback behavior for ambiguous tasks.
- Log similarity, keyword boost, and final route score.

## Missing Rubric Sections

Symptom: Final output lacks user stories, product features, or engineering tasks.

Likely cause: The action planner omitted a required step or the workflow accepted a partial plan.

Resolution:
- Define required workflow steps in code.
- Normalize planned steps against the required artifact list.
- Add evaluator checks for required sections.

## Evaluator Over-Correction

Symptom: A revised response meets format criteria but loses useful details from the first answer.

Likely cause: Correction instructions focused only on the failed criterion.

Resolution:
- Tell the worker to preserve correct existing content.
- Re-run the full evaluation criteria after revision.
- Compare the before/after output.
