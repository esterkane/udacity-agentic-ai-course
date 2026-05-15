# Key Concepts

These notes use the two completed projects as the reference context:

- Project 1: AgentsVille Trip Planner notebook.
- Project 2: AI-Powered Agentic Workflow for Project Management.

## 1. Direct Prompting

What it means: Sending a user prompt directly to the model without adding a persona, private knowledge block, retrieval step, evaluator, or tool loop.

Where it appears: Project 2 Phase 1 implements `DirectPromptAgent` in `workflow_agents/base_agents.py` and smoke-tests it in `phase_1/direct_prompt_agent.py`.

Why it matters: It is the baseline pattern. It shows what the model can do before extra structure is added.

Common failure mode: The response can be generic, underspecified, or based on the model's broad prior knowledge instead of project-specific context.

Practical fix: Use direct prompting only for narrow tasks. Add output-format instructions, a persona, knowledge context, or validation when the task needs controlled behavior.

## 2. Persona/System-Prompt Augmentation

What it means: Adding a system prompt or persona that changes how the model should answer.

Where it appears: Project 1 uses an expert travel-planner system prompt for itinerary generation. Project 2 uses `AugmentedPromptAgent` and role personas such as Product Manager, Program Manager, and Development Engineer.

Why it matters: Persona prompts make the model optimize for a role-specific responsibility instead of a generic answer.

Common failure mode: The persona can become style-only and fail to enforce actual task constraints.

Practical fix: Pair the persona with concrete instructions, required fields, and evaluation criteria.

## 3. Knowledge-Augmented Prompting

What it means: Supplying a curated knowledge block directly in the prompt and instructing the model to answer only from that block.

Where it appears: Project 2 implements `KnowledgeAugmentedPromptAgent`. Phase 2 gives each role knowledge from the Email Router product spec and role-specific instructions.

Why it matters: It limits the model's answer space to project facts, which is useful for user stories, product features, and engineering tasks.

Common failure mode: The model can still add unsupported details if the prompt does not clearly restrict it.

Practical fix: State "use only this knowledge" and add an evaluator that checks required structure and relevance.

## 4. Retrieval-Augmented Generation At A Basic Level

What it means: Splitting a knowledge source into chunks, embedding those chunks, retrieving the closest chunk for a prompt, and answering from the retrieved text.

Where it appears: Project 2 Phase 1 implements `RAGKnowledgePromptAgent` with chunking, embedding generation, cosine similarity, and answer generation from the best chunk.

Why it matters: RAG keeps prompts smaller and makes the model answer from the most relevant part of a larger knowledge source.

Common failure mode: Retrieval can select the wrong chunk, especially when chunks are too large, too small, or semantically similar.

Practical fix: Tune chunk size and overlap, inspect retrieved chunks during debugging, and add evaluator checks for missing source support.

## 5. Prompt Chaining

What it means: Breaking a task into ordered model calls where each step produces input for the next step.

Where it appears: Project 1 chains vacation details, weather/activity context, itinerary generation, evaluation, and itinerary revision. Project 2 chains user stories -> product features -> engineering tasks.

Why it matters: Chaining makes complex work inspectable and reduces the burden on one prompt.

Common failure mode: A weak intermediate output contaminates later steps.

Practical fix: Validate each intermediate artifact before passing it forward. Store enough output evidence to debug the chain.

## 6. Structured JSON Output

What it means: Requiring the model to return machine-readable JSON instead of free-form prose.

Where it appears: Project 1 instructs the itinerary agent to return a `TravelPlan` JSON object and parses JSON from the model response.

Why it matters: Structured output can be validated, tested, transformed, and reused by later code.

Common failure mode: The model wraps JSON in extra prose, emits invalid JSON, or omits required fields.

Practical fix: Provide the target schema, isolate the JSON block, parse it strictly, and show the failing text when validation fails.

## 7. Pydantic Validation

What it means: Using Pydantic models to define and validate data structures at runtime.

Where it appears: Project 1 defines `Traveler`, `VacationInfo`, `Weather`, `Activity`, `ActivityRecommendation`, `ItineraryDay`, `TravelPlan`, and `EvaluationResults`.

Why it matters: It turns model output into typed Python objects and catches missing fields, wrong types, and malformed JSON.

Common failure mode: Validation only checks structure, not whether the content is true or appropriate.

Practical fix: Use Pydantic for schema validation and separate eval functions for semantic checks such as budget, dates, weather fit, and valid activity IDs.

## 8. Tool Calling With Simulated Tools

What it means: Letting the model request tool actions while Python code executes the actual function and returns the result.

Where it appears: Project 1 defines simulated tools such as `calculator_tool`, `get_activities_by_date_tool`, `run_evals_tool`, and `final_answer_tool`.

Why it matters: Tools give the workflow deterministic operations for cost calculation, activity lookup, evaluation, and stopping the loop.

Common failure mode: The model emits malformed tool-call JSON or asks for a tool that does not exist.

Practical fix: Parse tool calls defensively, maintain an explicit tool registry, validate arguments, and return clear errors as observations.

## 9. ReAct Loop: THOUGHT -> ACTION -> OBSERVATION

What it means: A loop where the model states its next reasoning step, calls a tool, receives an observation, and continues until it calls a final-answer tool.

Where it appears: Project 1 implements an itinerary revision agent that runs a THOUGHT -> ACTION -> OBSERVATION cycle to refine the itinerary.

Why it matters: It makes revision behavior inspectable and allows the model to use evaluation and lookup tools before finalizing.

Common failure mode: The loop can get stuck repeating actions or never call the final-answer tool.

Practical fix: Set a maximum step count, log traces, require a final-answer tool, and inspect observations when the loop stalls.

## 10. Evaluation Agents

What it means: A model-based reviewer that checks another agent's output against criteria.

Where it appears: Project 2 implements `EvaluationAgent` and uses it for Product Manager, Program Manager, and Development Engineer outputs. Project 1 uses evaluation functions and LLM-based checks for itinerary quality.

Why it matters: Evaluation catches format and quality problems before later workflow steps consume the output.

Common failure mode: The evaluator can approve fluent but incomplete work if the criteria are weak.

Practical fix: Make criteria explicit, require pass/fail plus reason, and combine model evaluation with deterministic checks where possible.

## 11. Feedback/Refinement Loops

What it means: Using evaluation feedback to revise a previous output.

Where it appears: Project 1 revises the itinerary based on traveler feedback requiring at least two activities per day. Project 2's `EvaluationAgent` can produce correction instructions and rerun the worker agent.

Why it matters: First outputs are often close but not compliant. Refinement loops give the workflow a controlled repair path.

Common failure mode: The revised output fixes one issue while breaking another.

Practical fix: Re-run the full evaluation set after revision, not only the failed check.

## 12. Routing Agents

What it means: An agent or component that selects which specialized path should handle a prompt.

Where it appears: Project 2 implements `RoutingAgent`. Phase 1 routes between Texas, Europe, and Math agents. Phase 2 routes workflow steps to Product Manager, Program Manager, or Development Engineer functions.

Why it matters: Routing lets one workflow use specialized agents without hardcoding every prompt to one model call.

Common failure mode: Ambiguous or short prompts can route to the wrong agent.

Practical fix: Use clear route descriptions, route-specific keywords, logging, and fallback behavior.

## 13. Embedding-Based Routing

What it means: Comparing the embedding of a user prompt with embeddings of route descriptions and selecting the highest similarity.

Where it appears: Project 2 `RoutingAgent` uses `text-embedding-3-large`, cosine similarity, and route descriptions.

Why it matters: It supports semantic routing when the user wording does not exactly match a keyword.

Common failure mode: Similarity alone can be unreliable for short prompts such as "define stories" or "create tasks".

Practical fix: Log similarity scores, test representative prompts, and add controlled keyword boosts for short high-signal terms.

## 14. Keyword Boosting As A Guardrail For Short Routing Prompts

What it means: Adding a small score boost when explicit route keywords appear in the input.

Where it appears: Project 2 `RoutingAgent._keyword_boost()` adds up to a capped boost for configured route keywords. Phase 2 uses keywords such as `user story`, `feature`, and `engineering`.

Why it matters: Short prompts often lack enough semantic context for embeddings to separate routes cleanly.

Common failure mode: Overweighting keywords can hide bad route descriptions or misroute prompts with incidental word matches.

Practical fix: Keep the boost capped, log both similarity and boost, and treat keyword boosting as a guardrail, not the main router.

## 15. Action Planning Agents

What it means: An agent that converts a high-level request into ordered work steps.

Where it appears: Project 2 implements `ActionPlanningAgent`. Phase 2 uses it to plan the Email Router workflow steps, then normalizes the result to the required three artifacts.

Why it matters: Planning separates "what work needs to happen" from "which agent executes each step."

Common failure mode: The planner may omit a required step or phrase steps in a way that breaks routing.

Practical fix: Normalize planner output against expected required steps when the rubric or workflow contract is known.

## 16. Workflow Orchestration

What it means: Coordinating planning, routing, worker agents, evaluation, context passing, and final output assembly.

Where it appears: Project 2 Phase 2 `agentic_workflow.py` orchestrates ActionPlanningAgent, RoutingAgent, role-specific KnowledgeAugmentedPromptAgents, EvaluationAgents, and completed-step context.

Why it matters: Orchestration is where isolated agent demos become a multi-step workflow.

Common failure mode: Later agents lack context from earlier outputs, or the workflow silently skips a step.

Practical fix: Maintain explicit completed-step state, print workflow progress, and define required workflow steps.

## 17. Output Evidence And Reproducibility

What it means: Keeping outputs traceable to actual script or notebook runs.

Where it appears: Project 1 notebook includes generated itinerary traces and final evaluation output. Project 2 includes output text files such as `agentic_workflow_output.txt`, routing output, and static check output.

Why it matters: Course submissions need evidence. Fabricated or manually rewritten outputs do not prove the workflow ran.

Common failure mode: Documentation says a workflow passed, but there is no command output, notebook run, or saved artifact.

Practical fix: Save outputs from real runs, label them clearly, avoid editing them into success states, and do not claim tests passed without evidence.
