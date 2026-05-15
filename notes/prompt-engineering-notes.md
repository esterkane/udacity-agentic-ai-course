# Prompt Engineering Notes

## Practical Prompt Template

```text
Role:
Task:
Input:
Constraints:
Output format:
Quality checks:
```

## Notes

- The output format should be strict when another tool or agent consumes the result.
- Constraints should be testable where possible.
- Examples help when the task has edge cases or route boundaries.
- Keep generation prompts separate from evaluation prompts.
- Do not mix JSON output and narrative output in the same model response when code must parse the result.

## Project Examples

- Project 1 uses an Expert Planner prompt with traveler data, weather, activities, constraints, and a required `TravelPlan` JSON shape.
- Project 2 uses role-specific prompts for Product Manager, Program Manager, and Development Engineer artifacts.
