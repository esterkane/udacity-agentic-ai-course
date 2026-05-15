# Udacity Agentic AI Course

This repository documents my Udacity Agentic AI course work. It is organized as a practical learning archive: one folder per project, shared course notes, troubleshooting notes, do/don't guidance, and quiz questions for review.

The goal is not to present these projects as production systems. The goal is to preserve the implementation patterns, design decisions, limitations, and evidence needed to explain the work clearly.

## Project Index

| Project | Name | Main format | Focus | Location |
| --- | --- | --- | --- | --- |
| 01 | AgentsVille Trip Planner | Jupyter Notebook | Multi-stage travel assistant with validation, prompt chaining, evaluation, and ReAct-style revision | `projects/01-agentsville-trip-planner/` |
| 02 | AI-Powered Agentic Workflow for Project Management | Python package/workflow | Reusable agents, routing, evaluation, action planning, and project-plan generation | `projects/02-agentic-workflow-project-management/` |
| 03 | TBD | TBD | To be added later | TODO |
| 04 | TBD | TBD | To be added later | TODO |

## Repository Organization

```text
docs/       Course-level explanations, patterns, troubleshooting, and quiz bank
notes/      Topic notes for prompt engineering, ReAct, evaluation, and routing
projects/   One folder per Udacity project
```

Each project folder is expected to contain:

- A project README with purpose, setup notes, and evidence status.
- `docs/architecture.md` for workflow structure and agent responsibilities.
- `docs/lessons-learned.md` for implementation notes and tradeoffs.
- `docs/dos-and-donts.md` for practical guidance.
- `docs/troubleshooting.md` for observed failures and fixes.
- `docs/quiz.md` for difficult review questions.
- Source files, notebooks, and outputs only after review for secrets and submission hygiene.

## Project 1: AgentsVille Trip Planner

Project 1 is a Jupyter Notebook-based multi-stage AI assistant. It generates a structured day-by-day travel itinerary using:

- Pydantic validation.
- Weather and activity data.
- Prompt chaining.
- Evaluation functions.
- A ReAct-style itinerary revision agent with tools.

The important engineering focus is how the assistant moves from user intent to structured itinerary output while validating intermediate results and revising weak plans.

## Project 2: AI-Powered Agentic Workflow For Project Management

Project 2 is a Python package and workflow implementation.

Phase 1 builds reusable agents:

- `DirectPromptAgent`
- `AugmentedPromptAgent`
- `KnowledgeAugmentedPromptAgent`
- `RAGKnowledgePromptAgent`
- `EvaluationAgent`
- `RoutingAgent`
- `ActionPlanningAgent`

Phase 2 uses these agents to create an Email Router project plan with user stories, product features, and engineering tasks.

The important engineering focus is decomposition: each agent has a narrower responsibility, and the workflow turns a product request into structured planning artifacts.

## What I Learned

- Agentic workflows are easier to debug when each agent has a clear responsibility, input, and output.
- Prompt chaining needs structured intermediate artifacts; otherwise downstream steps can misread fluent but ambiguous text.
- Evaluation agents are useful for feedback loops, but they are not a replacement for human review or deterministic validation.
- Routing logic should be explicit and auditable. If a decision can be made deterministically, code may be safer than an LLM route decision.
- Outputs should be generated from actual script or notebook runs. They should not be fabricated or rewritten to look successful.

## How To Run Locally

These are high-level steps. Project-specific commands should be added only after the project files are reviewed and the commands are confirmed.

1. Clone the repository.
2. Create a Python virtual environment.
3. Install the dependencies listed by each project, if present.
4. Configure required environment variables locally. Do not commit `.env` files.
5. Run the notebook or Python scripts from the relevant project folder.
6. Save output evidence only when it comes from an actual run and is safe to include.

## Security / Submission Hygiene

- Real API keys, tokens, credentials, `.env` files, and private local paths are not included.
- `.gitignore` excludes common secret files, virtual environments, caches, logs, temporary files, and editor/OS clutter.
- Notebook outputs should be reviewed before commit because they can contain prompts, stack traces, raw model responses, or local execution details.
- Generated outputs must come from actual script or notebook runs. Do not fabricate outputs for submission.
- Do not claim a test, notebook, or workflow was run unless the repository contains supporting evidence.

## Evidence Policy

When evidence is missing, the docs should say so directly. Use `TODO: add test evidence` or equivalent wording instead of implying a successful run.

## TODO

- Review the provided project ZIP files and copy sanitized source artifacts into the project folders.
- Add project-specific run commands after confirming dependencies.
- Add evidence artifacts from real runs only.
