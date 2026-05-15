# Routing Agent Notes

## Purpose

A routing agent chooses which path should handle a request. It is useful when the same input channel can receive different task types.

## Design Checklist

- Define each route in one sentence.
- Include a fallback route.
- Record the selected route and reason.
- Keep route labels stable so downstream code can rely on them.
- Log similarity score, keyword boost, and final score when using embedding routing.
- Test short prompts separately.

## Project Examples

- Project 2 routes workflow steps to Product Manager, Program Manager, or Development Engineer support functions.
- The router uses embedding similarity plus capped keyword boosts for route terms such as `user story`, `feature`, and `engineering`.
