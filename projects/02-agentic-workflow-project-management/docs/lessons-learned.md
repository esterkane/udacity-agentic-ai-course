# Lessons Learned

## What Worked

- Narrow role agents made the workflow easier to debug. Product Manager, Program Manager, and Development Engineer outputs have different acceptance criteria.
- Evaluation agents helped catch missing structure, such as user stories that did not follow the expected format or tasks without required labels.
- Routing logs are useful because they show similarity, keyword boost, final score, and selected agent.
- Normalizing planned steps against required project artifacts prevents the action planner from accidentally skipping user stories, features, or tasks.

## What Was Difficult

- Short routing prompts are hard for embedding similarity alone. A phrase like "define stories" needs keyword support.
- Evaluators can over-focus on one criterion and remove useful detail during correction.
- Product planning artifacts are prose-heavy, so a fluent response can still miss required sections.
- Without structured intermediate outputs, later agents depend on loose text context.

## Improvements For A Next Pass

- Store intermediate artifacts as JSON.
- Validate agent outputs with schemas before passing them downstream.
- Add deterministic checks for required sections.
- Preserve command output for run evidence.
- Keep route test cases for short prompts, ambiguous prompts, and rubric-specific prompts.
