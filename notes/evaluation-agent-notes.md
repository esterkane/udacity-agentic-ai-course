# Evaluation Agent Notes

## Purpose

An evaluation agent checks a generated artifact against criteria. Use it for feedback loops, format checks, rubric checks, and coarse quality review. Do not treat evaluator approval as proof that the work is correct.

## Recommended Output

```json
{
  "passed": false,
  "issues": [],
  "evidence": [],
  "recommended_fix": ""
}
```

## Common Failure Modes

- The evaluator checks style but misses factual errors.
- The evaluator accepts unsupported claims.
- The evaluator gives vague feedback that cannot be turned into a code or prompt change.
- The evaluator over-corrects and removes useful content.

## Project Examples

- Project 1 uses eval functions for dates, cost, activity availability, weather compatibility, and traveler feedback.
- Project 2 uses `EvaluationAgent` to check Product Manager, Program Manager, and Development Engineer outputs against role-specific criteria.
