"""Smoke test for RoutingAgent."""

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent, RoutingAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

texas_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key,
    "You are a college professor",
    "You know about Texas history, Texas cities, and local Texas context. Rome, Texas is a small community in Texas.",
)

europe_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key,
    "You are a college professor",
    "You know about European history, Italian cities, and the history of Rome, Italy.",
)

math_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key,
    "You are a college math professor",
    "You know how to extract simple arithmetic from prompts and return the formula and answer without extra explanation.",
)

routing_agent = RoutingAgent(openai_api_key)
routing_agent.agents = [
    {
        "name": "Texas Agent",
        "description": "Answer questions about Texas places, Texas history, Texas towns, and Rome Texas local context.",
        "keywords": ["texas", "rome, texas", "rome texas"],
        "func": lambda x: texas_agent.respond(x),
    },
    {
        "name": "Europe Agent",
        "description": "Answer questions about Europe, Italy, Italian history, European history, and Rome Italy.",
        "keywords": ["italy", "italian", "europe", "rome, italy", "rome italy"],
        "func": lambda x: europe_agent.respond(x),
    },
    {
        "name": "Math Agent",
        "description": "Answer arithmetic, calculation, multiplication, totals, estimates, days, story points, and numeric planning questions.",
        "keywords": ["takes", "days", "story", "stories", "how many", "calculate", "total", "number", "plus", "minus", "times", "multiply"],
        "func": lambda x: math_agent.respond(x),
    },
]

prompts = [
    "Tell me about the history of Rome, Texas",
    "Tell me about the history of Rome, Italy",
    "One story takes 2 days, and there are 20 stories",
]

for prompt in prompts:
    print("\n" + "=" * 80)
    print(f"Prompt: {prompt}")
    print("RoutingAgent response:")
    print(routing_agent.route(prompt))
