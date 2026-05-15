"""Smoke test for KnowledgeAugmentedPromptAgent."""

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"

knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
response = knowledge_agent.respond(prompt)

print(f"Prompt: {prompt}")
print("\nKnowledgeAugmentedPromptAgent response:")
print(response)
print("\nConfirmation: this response should follow the provided knowledge, even though the model's own general knowledge would normally say Paris.")
