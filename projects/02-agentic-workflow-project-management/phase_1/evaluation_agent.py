"""Smoke test for EvaluationAgent."""

import os
from pprint import pprint
from dotenv import load_dotenv
from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

worker_persona = "You are a college professor, your answer always starts with: Dear students,"
worker_knowledge = "The capitol of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, worker_persona, worker_knowledge)

evaluator_persona = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=evaluator_persona,
    evaluation_criteria=evaluation_criteria,
    worker_agent=knowledge_agent,
    max_interactions=10,
)

print(f"Prompt: {prompt}")
print("\nEvaluationAgent result:")
result = evaluation_agent.evaluate(prompt)
pprint(result)
