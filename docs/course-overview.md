# Course Overview

## Purpose

This course work focuses on practical agentic AI workflows: decomposing tasks, routing work between specialized agents, evaluating outputs, and keeping generated artifacts auditable.

## Project Map

| Project | Main Pattern | Current Evidence |
| --- | --- | --- |
| 01 AgentsVille Trip Planner | Pydantic-validated itinerary generation plus ReAct revision loop | Documentation is present. Source notebook and run outputs are not committed in this repo yet. |
| 02 Agentic Workflow Project Management | Agent classes, evaluation loops, embedding routing, action planning, and workflow orchestration | Documentation is present. Source package and run outputs are not committed in this repo yet. |
| 03 Reserved | Not started in this repo | No files yet. |
| 04 Reserved | Not started in this repo | No files yet. |

## Working Standards

- Keep prompts, agent roles, inputs, outputs, and evaluation criteria close together.
- Separate source artifacts from generated outputs.
- Preserve enough output evidence to explain what happened, but do not preserve sensitive data.
- Record failure modes and fixes in troubleshooting notes.

## Current Gaps

- Add sanitized source artifacts for Project 1 and Project 2.
- Add run logs only after rerunning notebooks or scripts from committed source files.
- Add dependency details beside each project when source files are committed.
