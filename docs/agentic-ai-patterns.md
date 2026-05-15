# Agentic AI Patterns

This file groups the project concepts into implementation patterns. It is not a production architecture guide; it is a practical reference for the two Udacity projects in this repository.

## Prompt Construction Patterns

### Direct Prompting

What it means: A single user message goes to the model with no extra system role or private context.

Where it appears in the projects: Project 2 Phase 1 `DirectPromptAgent`.

Why it matters: Establishes the baseline behavior before adding more control.

Common failure mode: Generic answers and unsupported assumptions.

Practical fix: Use it only for simple prompts, then move to persona, knowledge, or validation when the output must follow project rules.

### Persona/System-Prompt Augmentation

What it means: A system message defines the role, behavior, or task frame.

Where it appears in the projects: Project 1's travel-planner prompt and Project 2's Product Manager, Program Manager, and Development Engineer personas.

Why it matters: Role framing narrows the output toward the responsibility of the agent.

Common failure mode: The model follows the voice of the persona but misses required fields.

Practical fix: Combine persona with explicit task instructions, examples, and evaluator criteria.

### Knowledge-Augmented Prompting

What it means: The prompt includes a specific knowledge block and tells the model to answer from that block.

Where it appears in the projects: Project 2 `KnowledgeAugmentedPromptAgent`; Phase 2 role agents receive the Email Router product spec and role-specific knowledge.

Why it matters: Keeps generation grounded in the project brief.

Common failure mode: The model adds facts that are plausible but absent from the knowledge block.

Practical fix: Add "use only this knowledge" constraints and evaluate for unsupported content.

### Retrieval-Augmented Generation At A Basic Level

What it means: Retrieve the most relevant chunk from a larger text before generating an answer.

Where it appears in the projects: Project 2 `RAGKnowledgePromptAgent` chunks text, embeds chunks, computes similarity, and answers from the best chunk.

Why it matters: Avoids sending all knowledge into every prompt.

Common failure mode: Retrieval picks a weak chunk, causing a weak answer.

Practical fix: Inspect retrieved chunks, tune chunk size/overlap, and add source-support checks.

## Structured Output And Validation Patterns

### Structured JSON Output

What it means: The model returns a defined JSON object instead of free-form prose.

Where it appears in the projects: Project 1 asks for a `TravelPlan` JSON object inside a JSON code fence.

Why it matters: JSON can be parsed, validated, and passed to tools or evals.

Common failure mode: Extra prose or invalid JSON breaks parsing.

Practical fix: Provide the schema, strip code fences carefully, and fail loudly on invalid JSON.

### Pydantic Validation

What it means: Python models define valid fields and types for input and output data.

Where it appears in the projects: Project 1 validates vacation details, itinerary objects, and evaluation results with Pydantic models.

Why it matters: It converts model output into typed objects and catches structural errors early.

Common failure mode: Structurally valid data can still be semantically wrong.

Practical fix: Add deterministic and model-based evals for content correctness.

### Output Evidence And Reproducibility

What it means: Outputs are saved because they were produced by real notebook or script runs.

Where it appears in the projects: Project 1 notebook traces and final evaluation output; Project 2 output text files for agents, routing, workflow, and static checks.

Why it matters: Evidence lets a reviewer distinguish a real run from hand-written success text.

Common failure mode: Docs claim success without a saved command, notebook run, or output artifact.

Practical fix: Save outputs from actual runs and do not fabricate or manually rewrite evidence.

## Tool And ReAct Patterns

### Tool Calling With Simulated Tools

What it means: The model requests named tools, while Python code executes local functions and returns the result.

Where it appears in the projects: Project 1 uses `calculator_tool`, `get_activities_by_date_tool`, `run_evals_tool`, and `final_answer_tool`.

Why it matters: Tool functions provide deterministic operations inside an LLM-driven loop.

Common failure mode: Tool-call arguments are malformed or the requested tool is unsupported.

Practical fix: Use a tool registry, validate arguments, and return errors as observations.

### ReAct Loop: THOUGHT -> ACTION -> OBSERVATION

What it means: The model decides what to do, calls a tool, receives an observation, and repeats until final answer.

Where it appears in the projects: Project 1's itinerary revision agent.

Why it matters: The trace shows why the agent revised the itinerary and which tools it used.

Common failure mode: The agent loops without reaching final answer.

Practical fix: Set `max_steps`, require a final-answer tool, and inspect the trace when it stalls.

### Feedback/Refinement Loops

What it means: Evaluate an output, generate correction instructions or tool observations, and revise the output.

Where it appears in the projects: Project 1 revises the itinerary to satisfy traveler feedback. Project 2 `EvaluationAgent` can ask worker agents to revise responses.

Why it matters: It gives the workflow a repair mechanism after initial generation.

Common failure mode: The repair fixes one criterion and breaks another.

Practical fix: Run the complete evaluation set after every revision.

## Evaluation Patterns

### Evaluation Agents

What it means: An LLM or evaluator component checks a worker output against criteria.

Where it appears in the projects: Project 2 role-specific `EvaluationAgent` instances; Project 1 itinerary eval functions and LLM-based weather/feedback checks.

Why it matters: Evaluation catches format drift and missing requirements before downstream use.

Common failure mode: Vague criteria lead to vague approval.

Practical fix: Use exact criteria, require reasons, and combine with deterministic checks.

### Prompt Chaining

What it means: The workflow uses multiple ordered prompts instead of one large prompt.

Where it appears in the projects: Project 1 moves from validated vacation data to itinerary to evals to revision. Project 2 moves from product spec to user stories, features, and engineering tasks.

Why it matters: Each step has a narrower job and can be inspected independently.

Common failure mode: One bad intermediate output propagates downstream.

Practical fix: Validate and record intermediate outputs before the next step consumes them.

## Routing And Planning Patterns

### Routing Agents

What it means: A component chooses which specialized agent or function handles a prompt.

Where it appears in the projects: Project 2 `RoutingAgent` routes to topic agents in Phase 1 and project roles in Phase 2.

Why it matters: Routing allows specialization without one overloaded prompt.

Common failure mode: Ambiguous prompts pick the wrong route.

Practical fix: Use clear descriptions, log scores, and include fallback handling.

### Embedding-Based Routing

What it means: Route selection is based on cosine similarity between prompt embeddings and route-description embeddings.

Where it appears in the projects: Project 2 `RoutingAgent` uses `text-embedding-3-large` and cosine similarity.

Why it matters: It catches semantic matches that do not share exact keywords.

Common failure mode: Short prompts do not contain enough semantic signal.

Practical fix: Test representative route prompts and inspect similarity scores.

### Keyword Boosting As A Guardrail For Short Routing Prompts

What it means: Explicit keywords add a small capped score to the embedding similarity result.

Where it appears in the projects: Project 2 route configs include keywords like `user story`, `feature`, `task`, and `engineering`.

Why it matters: It stabilizes obvious short routing prompts.

Common failure mode: A keyword match can overpower a better semantic route if the boost is too high.

Practical fix: Cap the boost and log `similarity`, `keyword_boost`, and final `score`.

### Action Planning Agents

What it means: An agent extracts ordered steps from a high-level request.

Where it appears in the projects: Project 2 `ActionPlanningAgent` plans the Email Router workflow.

Why it matters: It separates planning from execution and routing.

Common failure mode: The planner omits required artifacts or returns vague steps.

Practical fix: Normalize planned steps against known required artifacts when the assignment has a fixed rubric.

### Workflow Orchestration

What it means: The code coordinates planning, routing, worker agents, evaluation, context passing, and final output.

Where it appears in the projects: Project 2 `agentic_workflow.py` orchestrates the Email Router project plan.

Why it matters: Orchestration turns standalone agents into a complete workflow.

Common failure mode: Later steps lose context or the workflow silently skips required work.

Practical fix: Maintain completed-step state, print progress, and define required workflow steps explicitly.
