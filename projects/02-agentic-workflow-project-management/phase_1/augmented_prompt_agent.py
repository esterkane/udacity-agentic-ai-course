"""Smoke test for AugmentedPromptAgent."""

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import AugmentedPromptAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: Dear students,"

augmented_agent = AugmentedPromptAgent(openai_api_key, persona)
augmented_agent_response = augmented_agent.respond(prompt)

print(f"Prompt: {prompt}")
print("\nAugmentedPromptAgent response:")
print(augmented_agent_response)

# The agent still uses the LLM's general knowledge for the factual answer.
# The persona changes how the answer is phrased, so the response should sound like a college professor and start with the requested wording.
print("\nComment: the factual knowledge comes from the LLM, while the system prompt changes the style/persona of the answer.")
