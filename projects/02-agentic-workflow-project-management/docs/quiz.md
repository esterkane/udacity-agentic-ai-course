# Quiz

1. Why is a routing agent useful in a multi-agent project-management workflow?

   Answer: It selects the correct specialized agent or workflow path based on the request, reducing the need for one broad prompt to handle every task.

2. What is the main limitation of using an evaluation agent to approve generated user stories?

   Answer: It can check rubric compliance, but it may miss business context, feasibility, or hidden stakeholder requirements.

3. Why should intermediate project artifacts use structured formats?

   Answer: Structured formats make validation, routing, diffing, and downstream processing more reliable.

4. What should be recorded when a workflow produces a final output?

   Answer: Input, route or agent path, relevant intermediate artifacts, final output, and any evaluation result that supports acceptance.

5. When is prompt chaining weaker than deterministic code?

   Answer: When the step is a fixed transformation, validation, or rule-based decision that can be implemented exactly in code.

6. Why does the workflow normalize the ActionPlanningAgent output instead of trusting every returned step?

   Answer: The project requires user stories, features, and engineering tasks. If the planner omits or rephrases a step, the workflow can skip required artifacts or route incorrectly. Normalization keeps the required contract explicit.

7. What problem does keyword boosting solve in the RoutingAgent, and what risk does it introduce?

   Answer: It helps short prompts such as "define user stories" route correctly when embedding similarity is weak. If the boost is too high, incidental keyword matches can overpower the better semantic route.

8. Why is an EvaluationAgent not enough to prove the project plan is implementation-ready?

   Answer: It checks against stated criteria, usually format and completeness. It may miss feasibility, hidden dependencies, product trade-offs, or engineering risks not listed in the criteria.

9. What should be logged when debugging a wrong route?

   Answer: The input step, each route description, similarity score, keyword boost, final score, and selected route.

10. Why should later workflow steps receive prior completed-step context?

   Answer: Features should be based on user stories, and engineering tasks should be based on both stories and features. Without context, each agent may produce isolated artifacts that do not line up.
