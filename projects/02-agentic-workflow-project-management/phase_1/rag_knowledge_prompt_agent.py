"""Smoke test for the provided RAGKnowledgePromptAgent."""

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import RAGKnowledgePromptAgent

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

persona = "You are a college professor, your answer always starts with: Dear students,"
rag_agent = RAGKnowledgePromptAgent(openai_api_key, persona, chunk_size=500, chunk_overlap=50)

knowledge_text = """
In the historic city of Boston, Clara, a marine biologist and science communicator, began each morning analyzing sonar data to track whale migration patterns along the Atlantic coast.
Inspired by her family and scientific work, Clara created a podcast called Crosscurrents, a show that explored the intersection of science, culture, and ethics.
Each week, she interviewed researchers, engineers, artists, and activists, covering topics from marine ecology and AI ethics to language preservation and retrieval-augmented generation.
"""

rag_agent.chunk_text(knowledge_text)
rag_agent.calculate_embeddings()

prompt = "What is the podcast that Clara hosts about?"
print(f"Prompt: {prompt}")
print("\nRAGKnowledgePromptAgent response:")
print(rag_agent.find_prompt_in_knowledge(prompt))
