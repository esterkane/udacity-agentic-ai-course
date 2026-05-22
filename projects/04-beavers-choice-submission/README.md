# Project 04: Beaver's Choice Multi-Agent Quote Workflow

## Purpose

This project implements a multi-agent workflow for Beaver's Choice, a paper-products business that needs to answer customer quote requests while checking stock, supplier lead times, pricing history, cash, and transaction impact.

The workflow combines deterministic business logic with optional `smolagents` worker shells. When `smolagents` or an OpenAI-compatible API key is unavailable, the script still uses its deterministic orchestration path.

## Main Artifacts

- `beavers_choice_multi_agent.py`: main workflow, business rules, tools, orchestrator, and test runner.
- `beavers_choice_workflow_diagram.png`: workflow diagram for the multi-agent design.
- `beavers_choice_report.docx`: submitted project report.
- `test_results.csv`: saved output evidence from a completed test run.
- `requirements.txt`: Python dependencies used by the project.

## Required Local Inputs

The submitted zip did not include the external CSV inputs that the script reads at runtime:

- `quote_requests.csv`
- `quotes.csv`
- `quote_requests_sample.csv`

Place those files in this project folder before running `beavers_choice_multi_agent.py`. Without them, database initialization and the sample scenario runner will stop at file loading.

## How To Run

1. Create and activate a Python virtual environment.
2. Install dependencies from `requirements.txt`.
3. Add the required CSV input files to this folder.
4. Optional: set `OPENAI_API_KEY` or `UDACITY_OPENAI_API_KEY` to enable the `smolagents` worker shells.
5. Run `python beavers_choice_multi_agent.py`.

The script writes a local SQLite database named `beavers_choice.db` and refreshes `test_results.csv` when the sample scenario runner completes.

## Evidence

`test_results.csv` is committed as submitted output evidence. I did not rerun the script during this repository update because the source CSV inputs were not present in the submitted archive.

## Security Notes

- Do not commit `.env` or local API credentials.
- Do not commit generated SQLite databases.
- Review regenerated CSV output before committing because it can contain customer request text and model responses.
