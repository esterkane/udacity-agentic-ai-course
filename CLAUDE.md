# CLAUDE.md — udacity-agentic-ai-course

## What this repo is
Coursework for the Udacity Agentic AI course. It is **not** a production system. It is
a portfolio of four self-contained projects plus shared notes, docs, and quiz banks.
The README is explicit about this: the goal is to preserve implementation patterns,
design decisions, limitations, and evidence — not to ship an app. Treat every project
as exercise/submission code.

## Architecture in 5 lines
1. `projects/01-agentsville-trip-planner/` — Jupyter notebook + `project_lib.py`; ReAct itinerary planner with Pydantic validation and eval loop (mocked weather/activity data).
2. `projects/02-agentic-workflow-project-management/` — Python package; reusable agents (`workflow_agents/base_agents.py`) for direct/augmented/knowledge/RAG/eval/routing/action-planning, composed into a project-plan workflow across `phase_1/` and `phase_2/`.
3. `projects/03-udaplay-solution-project/` — starter + solution notebooks with a `lib/` package; offline RAG over `games/*.json` via a committed local ChromaDB, plus a stateful research agent with web-search fallback.
4. `projects/04-beavers-choice-submission/` — single-file multi-agent workflow (`beavers_choice_multi_agent.py`) using smolagents + a local SQLite DB; emits `test_results.csv` and a report.
5. `docs/` and `notes/` hold course-level explanations; each project also has its own `docs/` (architecture, lessons-learned, dos-and-donts, troubleshooting, quiz).

## Run / test commands
There is **no repo-wide test suite, linter, type-checker, or CI** — none of `pytest.ini`,
`pyproject.toml`, a Makefile, or `.github/workflows/` exist. Do not invent them. What
actually exists is per-project and ad-hoc:

- Each project pins its own deps in `projects/<n>/requirements.txt`. Create a venv per
  project and `pip install -r requirements.txt`.
- **Project 2** has the only scripted runner: `projects/02-agentic-workflow-project-management/run_all_tests.sh`
  (and `run_all_tests.ps1`). These *run each agent script live against the LLM* and tee
  stdout into `outputs/` — they are evidence-generators, not assertion-based tests, and
  require a valid API key.
- **Project 4**: running `python beavers_choice_multi_agent.py` executes sample scenarios
  and writes `test_results.csv`. It degrades to deterministic evaluation if `smolagents`
  is not installed.
- **Projects 1 and 3** are notebooks: run top-to-bottom in Jupyter.

If asked to "run tests/lint/typecheck" at the repo level, state plainly that none are
configured — this is coursework.

## External services & secrets/config
- **LLM**: OpenAI Python SDK against an OpenAI-compatible endpoint. Projects 2 and 4
  default to the Udacity Vocareum gateway (`https://openai.vocareum.com/v1`), overridable
  via `OPENAI_BASE_URL`. Project 3's `lib/llm.py` uses the default OpenAI base URL.
- **Keys**: `OPENAI_API_KEY` (project 4 also accepts `UDACITY_OPENAI_API_KEY`). Model id
  defaults to `gpt-4o-mini`, overridable via `UDACITY_OPENAI_MODEL`/`OPENAI_MODEL`.
  Loaded from a local `.env` via `python-dotenv` (`load_dotenv()`); **no `.env` or
  `.env.example` is committed**.
- **Vector store**: ChromaDB, committed as a local data folder in project 3.
- **Web search**: Tavily (`tavily-python`, needs `TAVILY_API_KEY`) in project 3.
- **Database**: local SQLite (`sqlite:///beavers_choice.db`) in project 4, gitignored.
- Project 1's notebook was sanitized: a previously hardcoded key was replaced with
  `os.getenv("OPENAI_API_KEY")`.

## Invariants I must never break
1. **No secrets in git.** API keys, tokens, `.env` files, and private local paths must
   never be committed. `.gitignore` already excludes `.env*`, `*.key`, `*.pem`, `*.token`,
   `secrets/`, `credentials/`. Before committing notebooks, scrub outputs that may leak
   keys, raw prompts, or stack traces. This is the load-bearing rule here.
2. **Evidence honesty.** Per the README's evidence policy: do not claim a notebook,
   script, or test ran unless a real output artifact / log backs it. Do not fabricate
   `outputs/*.txt`, `test_results.csv`, or report contents.
3. **Determinism of planner/pipeline** — *partially N/A*. There is no formal determinism
   gate. Where determinism matters it is local: project 4 falls back to deterministic
   evaluation without `smolagents`; the README notes routing decisions that can be made
   in code should not be delegated to an LLM. Preserve those deterministic fallbacks.
4. **Quality gates (pytest/ruff/mypy/CI)** — **N/A**: none are configured in this repo.
5. **Provenance on every chunk (RAG citations)** — applies only to project 3's RAG /
   project 2's `RAGKnowledgePromptAgent`; there is no repo-wide citation contract.
6. Keep each project self-contained: deps, data, and outputs live under its own folder.

## Definition of done
- Notebooks (projects 1, 3) run top-to-bottom without errors when a valid key is set.
- Live-run scripts (project 2, project 4) produce their evidence artifacts from an
  **actual** run, not hand-written.
- No secrets, `.env` files, or local absolute paths committed; notebook outputs scrubbed.
- Relevant project README / `docs/` updated when behavior or structure changes.
- Tests / type-checks / CI: **N/A** (none exist) — do not claim they passed.
