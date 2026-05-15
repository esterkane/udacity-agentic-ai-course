# Course Overview

## Purpose

This course work focuses on practical agentic AI workflows: decomposing tasks, routing work between specialized agents, evaluating outputs, and keeping generated artifacts auditable.

## Project Map

| Project | Main Pattern | Current Evidence |
| --- | --- | --- |
| 01 AgentsVille Trip Planner | Pydantic-validated itinerary generation plus ReAct revision loop | Sanitized notebook and support library are committed. Notebook outputs are from the provided completed notebook; this repo update did not rerun it. |
| 02 Agentic Workflow Project Management | Agent classes, evaluation loops, embedding routing, action planning, and workflow orchestration | Source files, scripts, requirements, reflection notes, and output evidence are committed. This repo update did not rerun the scripts. |
| 03 Reserved | Not started in this repo | No files yet. |
| 04 Reserved | Not started in this repo | No files yet. |

## Working Standards

- Keep prompts, agent roles, inputs, outputs, and evaluation criteria close together.
- Separate source artifacts from generated outputs.
- Preserve enough output evidence to explain what happened, but do not preserve sensitive data.
- Record failure modes and fixes in troubleshooting notes.

## Current Gaps

- Add projects 03 and 04 when they are complete.
- Add fresh run logs if the committed notebook or scripts are rerun after future edits.
- Keep output evidence separate from source files.
