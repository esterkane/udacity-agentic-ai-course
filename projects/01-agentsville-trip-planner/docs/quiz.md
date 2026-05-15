# Quiz

These questions are designed to test implementation understanding, not simple recall.

1. Why is Pydantic useful after the LLM returns JSON, but insufficient as the only validation layer?

   Answer: Pydantic checks structure and types, such as required fields and valid nested objects. It does not prove that selected activities are real, weather-compatible, within budget, or aligned with traveler preferences. Semantic evals are still required.

2. What problem is solved by including the travel-plan schema directly in the planner prompt?

   Answer: It reduces ambiguity about field names, nesting, required values, and output shape. Without the schema, the model may produce a readable itinerary that cannot be parsed into the expected Pydantic model.

3. Why should the planner be told to copy activity objects exactly from the provided activity data?

   Answer: Exact copying reduces hallucinated activity names, prices, IDs, locations, and dates. It also makes it possible to compare selected activities against the source activity list.

4. If the JSON parses successfully but `TravelPlan` validation fails, what should be checked first?

   Answer: Check whether required fields are missing, types are wrong, date formats are invalid, or nested objects do not match the schema.

5. Why is total-cost validation better as deterministic Python than as an LLM judgment?

   Answer: Cost summation is a fixed arithmetic task. Python can compute it exactly, while an LLM can make arithmetic mistakes or rationalize an incorrect total.

6. What is the risk of letting the ReAct agent call `final_answer_tool` before `run_evals_tool`?

   Answer: The agent can finalize a plan that still violates date, budget, activity availability, weather, or feedback constraints.

7. Why does the ReAct loop require both `THOUGHT` and `ACTION`?

   Answer: `THOUGHT` makes the agent's intent inspectable, while `ACTION` gives Python a parseable instruction for tool execution. The loop needs both traceability and machine-readable control.

8. What should Python do if the model emits an unknown tool name?

   Answer: Reject the action, return a clear error observation, and avoid executing anything outside the registered tool set.

9. Why can weather compatibility be hard to evaluate with simple keyword rules?

   Answer: Activity descriptions can include conditional language, such as outdoor events that can move indoors. A simple rain/outdoor keyword rule can reject valid activities or accept unsafe ones.

10. What does `get_activities_by_date_tool` protect against during revision?

    Answer: It lets the agent inspect available activities for a date instead of inventing replacements from memory or prior context.

11. Why should the final evaluation suite run after a successful-looking revision?

    Answer: A revision can fix one issue while introducing another, such as adding a second activity but exceeding budget or selecting a weather-incompatible event.

12. What failure can occur if the planner prompt asks for JSON but also asks for a long narrative in the same output?

    Answer: The model may mix prose and JSON, making parsing unreliable. Narrative generation should be separate from machine-readable itinerary generation.

13. Why is "at least two activities per day" better as an explicit eval than a note in the prompt?

    Answer: The prompt can be ignored or partially followed. An eval can inspect the final object and fail specific days that do not meet the requirement.

14. What is the difference between validating `VacationInfo` and validating `TravelPlan`?

    Answer: `VacationInfo` validates the user/trip input. `TravelPlan` validates the model-generated itinerary output. Both ends of the workflow need structure checks.

15. If the model returns an activity with a correct name but wrong price, which eval should catch it?

    Answer: An activity-source matching eval should compare the selected activity object against the source data, and the total-cost eval should catch downstream price inconsistencies.

16. Why should notebook outputs be reviewed before committing?

    Answer: Notebook outputs can contain API errors, raw model traces, environment details, private paths, credentials, and excessive generated text.

17. What makes a saved output artifact acceptable evidence?

    Answer: It must come from an actual notebook or script run, be safe to publish, and show enough context to support the claim being made.

18. Why is a maximum step count needed in the ReAct loop?

    Answer: The agent can repeat actions, fail to call the final tool, or get stuck reacting to errors. A max step count prevents unbounded execution.

19. What should happen if `final_answer_tool` receives a structurally valid but semantically failing travel plan?

    Answer: The workflow should reject it or continue revision because semantic evals have not passed, even though the object shape is valid.

20. Why is prompt chaining useful in this notebook?

    Answer: It separates vacation-data validation, context gathering, itinerary generation, evaluation, revision, and final narration. Each step can be inspected and fixed independently.

21. How can an LLM-based weather eval fail even when the prompt is clear?

    Answer: It can misread an activity description, overlook an indoor backup, or apply inconsistent judgment. That is why clear criteria and reviewable failure messages matter.

22. Why should fabricated outputs never be used for submission evidence?

    Answer: They do not prove the notebook or workflow ran. They also hide real failure modes that are important for debugging and course review.

23. If the model repeatedly emits invalid `ACTION` JSON, what is the most practical prompt-level fix?

    Answer: Tighten the ReAct format instructions, show the exact JSON shape, and state that no prose is allowed inside the `ACTION` block.

24. Why should generated itinerary JSON be kept separate from a human-friendly trip summary?

    Answer: The JSON is for validation and tool use. The summary is for presentation. Mixing them makes parsing fragile and can corrupt the machine-readable artifact.

25. What is the safest response when a required API key is missing?

    Answer: Stop the model call, report the missing local configuration, and instruct the user to set the environment variable locally without committing secrets.
