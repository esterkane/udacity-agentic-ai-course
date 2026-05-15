"""Smoke test for DirectPromptAgent."""

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import DirectPromptAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the Capital of France?"
print(f"Prompt: {prompt}")

direct_agent = DirectPromptAgent(openai_api_key)
direct_agent_response = direct_agent.respond(prompt)

print("\nDirectPromptAgent response:")
print(direct_agent_response)
print("\nKnowledge source: this agent used the general knowledge already available in the selected LLM model. No extra project knowledge or persona was provided.")
