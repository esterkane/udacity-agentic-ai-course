# Architecture

## Workflow Summary

The workflow turns an Email Router product spec into three planning artifacts:

1. User stories.
2. Product features.
3. Engineering tasks.

The design separates planning, routing, generation, and evaluation. This makes it easier to see whether a failure came from the action planner, the router, a worker agent, or the evaluator.

## Components

| Component | Responsibility | Input | Output |
| --- | --- | --- | --- |
| Direct prompt agent | Baseline model call with no extra context | Prompt | Text response |
| Augmented prompt agent | Adds a persona/system prompt | Prompt plus persona | Role-shaped response |
| Knowledge-augmented prompt agent | Answers from provided project knowledge | Prompt plus product spec or role knowledge | Grounded project artifact |
| RAG knowledge prompt agent | Retrieves relevant text chunk before answering | Prompt plus chunked knowledge | Answer from selected chunk |
| Evaluation agent | Checks worker output against criteria and can request revision | Generated artifact and criteria | Final response, evaluation text, iteration count |
| Routing agent | Selects the role/function for a workflow step | Step text | Selected route output |
| Action planning agent | Extracts ordered workflow steps | High-level project-plan request | Step list |
| Workflow orchestrator | Runs planning, routing, generation, evaluation, and context passing | Product spec and workflow prompt | User stories, features, and tasks |

## Data Flow

1. The product spec is loaded.
2. The action planner proposes steps for a complete project plan.
3. The workflow normalizes the required steps so user stories, features, and engineering tasks are not skipped.
4. Each step is routed to Product Manager, Program Manager, or Development Engineer support functions.
5. The selected knowledge-augmented agent generates the artifact.
6. The matching evaluation agent checks format and criteria.
7. Accepted output is stored in completed-step context for later steps.
8. Final output combines the completed planning artifacts.

## External Dependencies

- Python runtime.
- OpenAI-compatible chat completions API.
- OpenAI-compatible embeddings API for routing and RAG examples.
- Environment variable for API credentials.
- Local product spec text file.

## Risks

- Agent outputs can drift from the requested schema.
- Evaluator prompts can miss product-management quality issues.
- Generated outputs can look plausible without being implementation-ready.
- Embedding routing can fail on short prompts without keyword guardrails.
- Action planning can omit required artifacts unless the workflow checks required steps.
