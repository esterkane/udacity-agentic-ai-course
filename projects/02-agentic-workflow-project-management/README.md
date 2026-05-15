# Project 02: Agentic Workflow Project Management

## Purpose

This project demonstrates an agentic workflow for turning an Email Router product spec into project-planning artifacts.

Phase 1 builds reusable agent classes:

- `DirectPromptAgent`
- `AugmentedPromptAgent`
- `KnowledgeAugmentedPromptAgent`
- `RAGKnowledgePromptAgent`
- `EvaluationAgent`
- `RoutingAgent`
- `ActionPlanningAgent`

Phase 2 uses the workflow agents to generate user stories, product features, and engineering tasks. The implementation uses an action planner to define workflow steps, a routing agent to select the correct role agent, knowledge-augmented agents to generate artifacts, and evaluation agents to check output structure.

## Main Artifacts

- `phase_1/`: reusable agent classes and Phase 1 smoke-test scripts.
- `phase_2/`: Email Router workflow implementation and product spec.
- `outputs/`: output evidence copied from the completed project.
- `requirements.txt`: Python dependencies used by the project.
- `run_all_tests.ps1` / `run_all_tests.sh`: local scripts for running checks and output generation.
- `reflection.md`: short project reflection from the completed submission.
- `docs/`: architecture, lessons learned, do/don't, troubleshooting, and quiz.

## How To Run

The local project used Python, environment variables for API access, and the dependencies in `requirements.txt`.

High-level flow:

1. Create a Python virtual environment.
2. Install project dependencies.
3. Set API credentials locally.
4. Run Phase 1 scripts to check individual agents.
5. Run the Phase 2 workflow script.
6. Save generated output only when it comes from an actual run.

## Evidence

Output evidence is committed under `outputs/`. I copied these artifacts from the completed project; I did not rerun the scripts during this repository update.

## Security Notes

- Do not commit `.env` files.
- Review `.env.example` files before committing, even if values look like placeholders.
- Check generated outputs for private prompts, local paths, or sensitive data.
