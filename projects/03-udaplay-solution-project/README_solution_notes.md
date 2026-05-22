# UdaPlay Solution Notes

This folder contains completed solution notebooks for the UdaPlay AI Research Agent project.

## Files to submit

- `Udaplay_01_solution_project.ipynb` — builds the persistent ChromaDB RAG collection from `games/*.json`.
- `Udaplay_02_solution_project.ipynb` — implements the stateful agent with local retrieval, evaluation, Tavily fallback, persistent long-term memory, and structured reports.
- `games/*.json` — local video game dataset.
- `lib/` — provided helper abstractions used by the notebooks.

## Environment

Create `.env` or `config.env` in the same folder as the notebooks:

```text
OPENAI_API_KEY="your-openai-key"
CHROMA_OPENAI_API_KEY="your-openai-key"  # optional; falls back to OPENAI_API_KEY
TAVILY_API_KEY="your-tavily-key"
```

## Rubric coverage

- Part 1 loads and formats the JSON game files.
- Part 1 creates a persistent ChromaDB collection named `udaplay`.
- Part 1 demonstrates semantic search.
- Part 2 implements three tools: `retrieve_game`, `evaluate_retrieval`, and `game_web_search`.
- Part 2 uses a stateful `UdaPlayResearchAgent` with an explicit state-machine workflow.
- Part 2 stores web fallback results in `udaplay_long_term_memory.json`.
- Part 2 prints tool usage, reasoning summary, confidence, citations, and structured JSON for multiple example queries.

## Do not submit

Do not submit `.env`, `config.env`, API keys, `.venv`, `__pycache__`, or generated ChromaDB data unless the project instructions explicitly require the generated database folder.
