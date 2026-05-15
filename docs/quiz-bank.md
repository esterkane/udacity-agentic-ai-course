# Quiz Bank

These questions test trade-offs, failure modes, and debugging decisions in agentic AI workflows. They are written for the Udacity Agentic AI course projects, especially the AgentsVille Trip Planner and the Agentic Workflow Project Management project.

## 1. Prompt Engineering

1. A travel-planning prompt says "create a good itinerary" and includes weather data, but the output schedules an outdoor picnic during a thunderstorm. What went wrong, and how should the prompt be improved?

   Answer: The prompt gave context but did not make weather compatibility an explicit constraint. The model optimized for a plausible itinerary rather than a checkable plan. Add concrete instructions: inspect each day's weather, avoid outdoor-only activities in rain or storms, allow outdoor activities only if an indoor backup is stated, and explain weather-related choices in the structured output.

2. A Product Manager agent returns features instead of user stories. The persona says "You are a Product Manager." Why did the persona fail?

   Answer: The persona described a role but did not constrain the artifact. Product managers can write stories, features, requirements, or strategy. The prompt needs the exact output type, required format, and negative instruction such as "only write user stories; do not define features or engineering tasks."

3. Compare a direct prompt with a knowledge-augmented prompt for generating Email Router user stories. What trade-off is introduced?

   Answer: Direct prompting is simpler but may use broad model assumptions. Knowledge augmentation grounds the answer in the product spec, but the prompt becomes more brittle if the knowledge block is incomplete or too broad. The fix is to provide concise relevant context and evaluate whether every story is supported by the spec.

4. A prompt includes role, task, context, and examples, but the answer still ignores the required output labels. What is a practical next step?

   Answer: Add a strict output contract and an evaluator that checks those labels. Examples help, but they do not guarantee compliance. The workflow should reject or revise outputs missing required labels.

5. What would go wrong if the same prompt asked for a JSON itinerary and a polished narrative summary in one answer?

   Answer: The model may mix prose with JSON, making parsing fragile. Separate machine-readable generation from presentation. First produce and validate JSON, then generate a summary from the validated object.

6. A model follows the output format but invents facts not in the source data. Is this a prompt engineering problem or an evaluation problem?

   Answer: Both. The prompt should say not to invent facts and to copy from source data. The evaluator should independently compare generated fields against source data because instructions alone are not enforcement.

7. A system prompt says "forget previous context" in an agent class. Why can this be useful in notebook or multi-agent workflows?

   Answer: It reduces accidental carryover from previous interactions or earlier prompt context. This matters when agents have narrow roles. It is not a security boundary, but it helps keep each call scoped to its current task.

8. When is chain-of-thought-style planning useful, and when can it be harmful?

   Answer: It is useful when the model must consider several constraints before output, such as dates, weather, interests, and cost. It can be harmful if verbose reasoning is mixed into the machine-readable output or if the workflow treats reasoning text as evidence. Keep planning separate from final JSON.

## 2. Structured Output And Validation

9. The planner returns valid JSON, but the workflow still produces a bad itinerary. What does this show about structured output?

   Answer: Structured output solves parsing and data shape, not correctness. A valid object can still contain invented activities, bad cost math, or poor weather choices. Add semantic evals after structural validation.

10. A downstream function expects `itinerary_days`, but the model returns `days`. What is the likely failure point and fix?

   Answer: Schema validation should fail before downstream code runs. The fix is to include the schema in the prompt, validate with Pydantic, and reject mismatched field names instead of adapting silently.

11. What would go wrong if a workflow accepted "mostly parseable" JSON after manual cleanup?

   Answer: Manual cleanup can hide model failures and make runs non-reproducible. If cleanup is required, document it or improve the prompt/parser. The safer path is to fail loudly, inspect the raw output, and rerun with stricter instructions.

12. Compare structured JSON output with markdown tables for an itinerary.

   Answer: JSON is better for validation and programmatic checks. Markdown tables are easier for humans but harder to parse reliably, especially with nested activity data. A good workflow can generate JSON first and render a human-friendly table later.

13. A model returns two JSON objects in one response. Why is this dangerous?

   Answer: The parser may extract the wrong object or fail entirely. The prompt should require exactly one object. The parser should reject multiple candidates unless the workflow explicitly supports arrays.

14. How should a workflow handle optional fields in structured output?

   Answer: Decide whether the field is truly optional. If downstream code depends on it, make it required. If it is optional, document the default behavior and make evals robust to `null` or missing values.

15. A JSON schema is included in the prompt, but the model omits a nested required field. What does this imply?

   Answer: Schema prompting reduces failures but does not guarantee compliance. Runtime validation is still required. The fix is to validate, return a targeted correction prompt, and rerun or revise.

16. Why is "valid JSON" a weaker acceptance criterion than "valid TravelPlan object"?

   Answer: Valid JSON only means syntax is correct. A valid `TravelPlan` object also satisfies expected field names, nested shape, and types defined by the model.

## 3. Pydantic And Schemas

17. A Pydantic model catches that `start_date` is malformed. What kind of bug did it prevent?

   Answer: It prevented invalid input from flowing into date range generation, weather lookup, activity lookup, and eval logic. Without validation, the failure might occur later in a less obvious place.

18. Pydantic accepts an itinerary where an activity exists but is scheduled on the wrong date. Why?

   Answer: Pydantic validates structure and types, not cross-field semantic consistency with source data. Add an eval that compares each selected activity ID and date against the activity dataset.

19. What is the trade-off between a strict schema and a flexible schema for LLM output?

   Answer: A strict schema catches errors early but may require more prompt tuning and retries. A flexible schema accepts more outputs but pushes ambiguity downstream. For agent workflows, strict schemas are usually better for intermediate artifacts.

20. A schema uses `int` for total cost, but activity prices can be decimals. What could go wrong?

   Answer: Valid decimal costs may fail validation or be rounded incorrectly. The schema should match the domain. Use `float`, `Decimal`, or cents as integers depending on precision needs.

21. Why should schemas be close to the code that consumes the model output?

   Answer: It reduces drift between the expected structure and the actual consumer logic. If the schema and consuming code diverge, valid model output can still break execution.

22. A developer loosens all Pydantic fields to `str` because validation keeps failing. Why is this a bad fix?

   Answer: It hides the problem instead of solving it. Downstream code loses type guarantees and must parse strings manually. The better fix is to improve the prompt, schema, or correction loop.

23. How can Pydantic improve prompt engineering?

   Answer: The schema can be shown to the model as the target output contract. It also provides concrete validation errors that can be fed into a refinement prompt.

## 4. ReAct Agents And Tool Use

24. A ReAct agent writes a good explanation but no `ACTION`. What should the controller do?

   Answer: It should not guess the intended tool call. Return a formatting error or fail the step, then tighten the prompt. Tool execution must depend on parseable action JSON.

25. The model calls `calculator_tool` with `"expression": "sum prices"`. Why is this a bad tool call?

   Answer: The arguments are not executable or precise. Tool schemas should require concrete inputs, such as a list of numeric prices or a valid expression. The controller should validate arguments before execution.

26. What would go wrong if the model were allowed to report tool results without Python execution?

   Answer: The model could invent observations. The workflow would lose the deterministic benefit of tools. Python should execute tools and append observations.

27. Why should a ReAct loop have a maximum step count?

   Answer: The model can repeat actions, fail to reach a final answer, or keep reacting to its own errors. A max step count prevents unbounded runs and makes failure visible.

28. A revision agent calls `final_answer_tool` before checking evals. What design guardrail should be added?

   Answer: Track whether `run_evals_tool` has run and passed. Reject finalization until required evals pass or return an observation telling the agent what remains.

29. Compare tool calling for cost calculation with asking the LLM to calculate total cost.

   Answer: Cost calculation is deterministic, so a tool or Python function is more reliable. The LLM may make arithmetic mistakes, especially after revisions. Use the model for judgment-heavy tasks, not exact arithmetic.

30. A tool returns a long observation with too much data. What failure can this cause?

   Answer: The model may miss the important part or exceed context limits. Return concise, structured observations that contain the data needed for the next action.

31. What is the risk of using `eval()` to parse tool arguments or stored embeddings?

   Answer: `eval()` can execute arbitrary code if input is untrusted. Prefer JSON parsing or safe literal parsing. In coursework this may be controlled, but production code should avoid it.

## 5. Evaluation Agents

32. An evaluator says "Yes, this is good" without explaining why. Why is this weak?

   Answer: It gives no debugging signal and may mask missed criteria. Evaluators should provide pass/fail plus reasons tied to specific requirements.

33. What would go wrong if an evaluator uses the same vague prompt as the generator?

   Answer: It may share the same blind spots and approve the same mistakes. Evaluation criteria should be more explicit than generation instructions.

34. Compare deterministic evals and LLM-based evals for weather compatibility.

   Answer: Deterministic evals are reproducible but may miss nuanced descriptions like indoor backups. LLM-based evals can interpret language but may be inconsistent. A practical design uses deterministic checks for clear rules and LLM evals for judgment-heavy comparisons.

35. A feedback loop fixes formatting but changes the content. What should happen next?

   Answer: Run the full eval suite again, not only the formatting check. Refinement can introduce regressions in budget, source grounding, or completeness.

36. Why is max interaction count important for an EvaluationAgent?

   Answer: It prevents endless correction loops. If the worker cannot satisfy criteria after several attempts, the workflow should fail visibly and preserve the failure for debugging.

37. A Product Manager evaluator checks only that each sentence starts with "As a". What can still be wrong?

   Answer: The stories may be unsupported by the product spec, omit value, duplicate each other, or include engineering tasks. Criteria should check structure and relevance.

38. Why should evaluator prompts avoid subjective words like "high quality" unless they define the metric?

   Answer: Subjective words produce inconsistent judgments. Define concrete requirements such as required labels, source support, budget limits, or exact story format.

39. What is the risk of treating evaluator approval as final truth?

   Answer: Evaluators are model outputs too. They can miss errors, especially if criteria or evidence are incomplete. Keep human review and deterministic checks for important requirements.

## 6. Routing Agents

40. A routing agent sends "define stories" to the Program Manager instead of Product Manager. What likely happened?

   Answer: The prompt was short and embedding similarity did not capture the intended route. Add route-specific keywords like `story` and `user story`, improve route descriptions, and log similarity/boost scores.

41. Compare embedding-based routing with keyword routing.

   Answer: Embedding routing handles semantic variation but can be weak on short prompts. Keyword routing is predictable for explicit terms but brittle with paraphrases. Combining embeddings with a capped keyword boost is practical.

42. Why should routing decisions be logged?

   Answer: Logs show similarity, keyword boost, final score, and selected route. Without logs, wrong routing is hard to debug because the failure appears later in the worker output.

43. What would go wrong if keyword boosts were too large?

   Answer: Incidental keyword matches could overpower semantic fit and route to the wrong agent. Keep boosts capped and treat them as guardrails, not the main signal.

44. A router has no fallback behavior. What is the risk?

   Answer: Ambiguous or unsupported prompts will still be forced into one route, producing misleading output. Add a fallback that asks for clarification or reports no suitable route.

45. Why should route descriptions say what an agent does not handle?

   Answer: Negative boundaries reduce overlap. For example, Product Manager handles user stories only and does not define features or tasks.

46. A route works in Phase 1 tests but fails in Phase 2. What changed?

   Answer: The route space changed. Phase 1 topic routing may be simple, while Phase 2 role routing has overlapping product-management language. Re-test with workflow-specific prompts.

## 7. RAG And Knowledge Grounding

47. A RAG agent retrieves the wrong chunk and answers confidently. What should be inspected first?

   Answer: Inspect the retrieved chunk, similarity score, chunk size, and query wording. The generator can only answer well if retrieval provides the right evidence.

48. What would go wrong if a RAG prompt says "answer using this chunk" but does not say "only this chunk"?

   Answer: The model may blend retrieved text with prior knowledge. If source grounding matters, require answers only from retrieved context and evaluate for unsupported claims.

49. Compare direct knowledge injection with RAG for a short product spec.

   Answer: Direct injection is simpler and often better for short specs because all context fits. RAG adds complexity and retrieval failure risk but helps when the source is too large for the prompt.

50. Why can chunk overlap matter?

   Answer: Important information can span chunk boundaries. Overlap reduces the chance that retrieval separates a question from its answer, but too much overlap increases redundancy.

51. A retrieved chunk is relevant but lacks one required detail. What is a good workflow response?

   Answer: Do not let the model invent the missing detail. Retrieve additional context, return "not found", or ask for more information depending on the task.

52. Why should generated answers cite or expose the grounding source during debugging?

   Answer: It lets reviewers verify whether the answer came from retrieved knowledge or model assumptions. Even simple chunk IDs can help.

## 8. Workflow Orchestration

53. Why is action planning separate from routing in the project-management workflow?

   Answer: Planning decides what steps are needed. Routing decides who should execute each step. Combining them makes it harder to debug whether a failure is a bad plan or bad route.

54. The ActionPlanningAgent returns two steps instead of the required three. What should the orchestrator do?

   Answer: If the rubric requires three artifacts, normalize or validate the plan against expected steps. Do not silently skip missing user stories, features, or tasks.

55. What would go wrong if each workflow step did not receive prior step context?

   Answer: Features might ignore user stories, and engineering tasks might ignore both stories and features. Later agents need previous outputs to maintain continuity.

56. Compare a single large prompt with an orchestrated workflow for the Email Router project plan.

   Answer: A single prompt is simpler but harder to inspect and repair. Orchestration adds complexity but gives separate agents, evals, routing logs, and intermediate artifacts.

57. Why should completed workflow steps be stored explicitly?

   Answer: Explicit state makes later context construction clear and supports debugging. Hidden state in a conversation can drift or be lost.

58. A workflow produces good user stories but weak engineering tasks. Where should debugging start?

   Answer: Check whether the engineering agent received the user stories and features, whether its knowledge is specific enough, and whether the evaluator criteria require detailed tasks with acceptance criteria and dependencies.

59. What is a workflow contract?

   Answer: It is the expected set of steps, inputs, outputs, and acceptance criteria for the workflow. It prevents agents from redefining the task mid-run.

## 9. Debugging And Reproducibility

60. A README says "tests passed", but there is no output file or command log. What is wrong?

   Answer: The claim lacks evidence. Documentation should say tests passed only when a command, notebook output, or saved artifact supports it.

61. A notebook output is huge and contains repeated traces. What should be kept?

   Answer: Keep enough evidence to show the run, final output, and eval result. Remove or move excessive traces if they make review harder, after ensuring no evidence is lost.

62. A workflow fails only sometimes. What should be logged?

   Answer: Model name, prompt version, inputs, route scores, tool calls, observations, eval results, and final output. Intermittent failures need enough context to compare runs.

63. Why is rerunning cells out of order dangerous in notebooks?

   Answer: Notebook state can become inconsistent with visible code. A variable may come from an earlier run that is no longer represented by the current cell order. Reproducibility requires top-to-bottom execution.

64. A saved output was edited manually to remove a failed eval. Why is this a serious issue?

   Answer: It misrepresents the actual run and hides a failure mode. Fix the workflow and save a new real output instead.

65. How can line-by-line logs help with routing failures?

   Answer: They reveal which route scored highest and why. Without score logs, the wrong worker output may look like a generation problem rather than a routing problem.

66. What should be done when an API call fails due to missing credentials?

   Answer: Stop and report missing local configuration. Do not add credentials to the repo. Document the variable name and set it locally.

## 10. Security And Submission Hygiene

67. Why should `.env` files be excluded even for course projects?

   Answer: They often contain real API keys or endpoints. Course repos are still repos; accidental pushes can expose credentials.

68. A notebook cell output contains a local file path. Is that always a secret?

   Answer: Not always, but it can expose username, directory structure, or private project context. Review and remove private paths before publishing.

69. What is safer: committing `.env.example` or documenting variable names in README?

   Answer: Both can be safe if placeholders are clean, but documentation avoids accidental real values in example files. If `.env.example` is used, review it carefully.

70. A generated output includes raw model prompts. What should be checked before committing?

   Answer: Check for secrets, private data, proprietary text, hidden endpoints, local paths, and any content that should not be public. Keep only what is needed as evidence.

71. Why should project source ZIPs not be copied blindly into the repo?

   Answer: ZIPs can contain `.env` files, notebook outputs, caches, credentials, or private paths. Inspect and sanitize before committing.

72. What would go wrong if fabricated outputs were submitted?

   Answer: They do not prove the workflow works and can hide real bugs. They also undermine reproducibility and course review integrity.

73. How should API keys be handled in local runs?

   Answer: Store them in local environment variables or local untracked files. Documentation should name required variables without showing real values.

74. Why is a security scan not enough by itself?

   Answer: Scans can miss secrets in unusual formats, screenshots, notebook metadata, or prose. Manual review is still needed for notebooks and generated outputs.

75. A repo is private. Does that remove the need for secret hygiene?

   Answer: No. Private repos can be shared, cloned, leaked, or made public later. Secrets should never be committed.
