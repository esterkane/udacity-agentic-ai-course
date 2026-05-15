# Udacity Agentic AI Course

This repository documents my Udacity Agentic AI course work. It is organized as one folder per project plus shared notes, troubleshooting pages, checklists, and quiz questions.

The goal is not to present these projects as production systems. The goal is to preserve the implementation patterns, design decisions, limitations, and evidence needed to explain the work clearly.

## Project Index

| Project | Name | Main format | Focus | Location |
| --- | --- | --- | --- | --- |
| 01 | AgentsVille Trip Planner | Jupyter Notebook | Multi-stage travel assistant with validation, prompt chaining, evaluation, and ReAct-style revision | `projects/01-agentsville-trip-planner/` |
| 02 | AI-Powered Agentic Workflow for Project Management | Python package/workflow | Reusable agents, routing, evaluation, action planning, and project-plan generation | `projects/02-agentic-workflow-project-management/` |
| 03 | Reserved | TBD | Will be added when the course project is complete | Not created yet |
| 04 | Reserved | TBD | Will be added when the course project is complete | Not created yet |

## Repository Organization

```text
docs/       Course-level explanations, patterns, troubleshooting, and quiz bank
notes/      Topic notes for prompt engineering, ReAct, evaluation, and routing
projects/   One folder per Udacity project
```

Each project folder should contain:

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

## How To Run Locally

These are high-level steps. Use project-specific commands only when source files or notebooks are present in that project folder.

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

When evidence is missing, the docs should say so directly. Do not imply a notebook, script, or test ran unless the repository includes the relevant output artifact or command log.

## Current State

- Project 1 includes a sanitized notebook and support library in `projects/01-agentsville-trip-planner/src-or-notebooks/`.
- Project 2 includes source files, scripts, requirements, reflection notes, and output evidence in `projects/02-agentic-workflow-project-management/`.
- I did not rerun the notebook or scripts during the artifact upload.
- The Project 1 notebook was sanitized to replace a hardcoded API key with `OPENAI_API_KEY`.
- `.env` and `.env.example` files are not included.
