"""Reusable agent classes for the project management agentic workflow.

The classes in this file stay intentionally small and explicit. The goal of the
project is to show the workflow pattern, not to hide everything behind a large
framework.
"""

from __future__ import annotations

import csv
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
from openai import OpenAI


DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"
DEFAULT_BASE_URL = "https://openai.vocareum.com/v1"


def _client(openai_api_key: str) -> OpenAI:
    """Create the OpenAI client used by the Udacity/Vocareum workspace."""
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file or environment.")
    return OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", DEFAULT_BASE_URL),
        api_key=openai_api_key,
    )


def _clean_step_line(line: str) -> str:
    """Remove numbering/bullets from one action-planning line."""
    line = line.strip()
    line = re.sub(r"^[-*•]\s*", "", line)
    line = re.sub(r"^\d+[\.)]\s*", "", line)
    return line.strip()


class DirectPromptAgent:
    """Send a prompt directly to the LLM without adding a system prompt."""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key

    def respond(self, prompt: str) -> str:
        client = _client(self.openai_api_key)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content or ""


class AugmentedPromptAgent:
    """Prompt agent that answers as a specific persona."""

    def __init__(self, openai_api_key: str, persona: str):
        self.openai_api_key = openai_api_key
        self.persona = persona

    def respond(self, input_text: str) -> str:
        client = _client(self.openai_api_key)
        system_prompt = (
            f"You are {self.persona}. Forget all previous conversational context. "
            "Answer the user's prompt while staying in this persona."
        )
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""


class KnowledgeAugmentedPromptAgent:
    """Prompt agent that answers only from provided knowledge."""

    def __init__(self, openai_api_key: str, persona: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.knowledge = knowledge

    def respond(self, input_text: str) -> str:
        client = _client(self.openai_api_key)
        system_prompt = (
            f"You are {self.persona} knowledge-based assistant. Forget all previous context.\n"
            f"Use only the following knowledge to answer, do not use your own knowledge: {self.knowledge}\n"
            "Answer the prompt based on this knowledge, not your own."
        )
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""


class RAGKnowledgePromptAgent:
    """Small RAG helper agent provided for the project.

    It chunks a knowledge text, embeds the chunks, retrieves the closest chunk for
    a prompt, and then asks the LLM to answer using only that retrieved chunk.
    """

    def __init__(self, openai_api_key: str, persona: str, chunk_size: int = 2000, chunk_overlap: int = 100):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.csv"
        self.chunks_file = Path(f"chunks-{self.unique_filename}")
        self.embeddings_file = Path(f"embeddings-{self.unique_filename}")
        self.chunks: list[dict[str, Any]] = []

    def get_embedding(self, text: str) -> list[float]:
        client = _client(self.openai_api_key)
        response = client.embeddings.create(
            model=DEFAULT_EMBEDDING_MODEL,
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    def calculate_similarity(self, vector_one: list[float], vector_two: list[float]) -> float:
        vec1, vec2 = np.array(vector_one), np.array(vector_two)
        denominator = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        if denominator == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / denominator)

    def chunk_text(self, text: str) -> list[dict[str, Any]]:
        text = re.sub(r"\s+", " ", text).strip()
        chunks: list[dict[str, Any]] = []

        if len(text) <= self.chunk_size:
            chunks = [{"chunk_id": 0, "text": text, "chunk_size": len(text)}]
        else:
            start, chunk_id = 0, 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                if end < len(text):
                    last_space = text.rfind(" ", start, end)
                    if last_space > start:
                        end = last_space
                chunk_text = text[start:end].strip()
                if chunk_text:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": chunk_text,
                        "chunk_size": len(chunk_text),
                        "start_char": start,
                        "end_char": end,
                    })
                    chunk_id += 1
                start = max(end - self.chunk_overlap, end)

        self.chunks = chunks
        with self.chunks_file.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["chunk_id", "text", "chunk_size"])
            writer.writeheader()
            for chunk in chunks:
                writer.writerow({"chunk_id": chunk["chunk_id"], "text": chunk["text"], "chunk_size": chunk["chunk_size"]})
        return chunks

    def calculate_embeddings(self) -> pd.DataFrame:
        if not self.chunks_file.exists():
            raise FileNotFoundError("Run chunk_text() before calculate_embeddings().")
        df = pd.read_csv(self.chunks_file, encoding="utf-8")
        df["embeddings"] = df["text"].apply(self.get_embedding)
        df.to_csv(self.embeddings_file, encoding="utf-8", index=False)
        return df

    def find_prompt_in_knowledge(self, prompt: str) -> str:
        if not self.embeddings_file.exists():
            raise FileNotFoundError("Run calculate_embeddings() before find_prompt_in_knowledge().")

        prompt_embedding = self.get_embedding(prompt)
        df = pd.read_csv(self.embeddings_file, encoding="utf-8")
        df["embeddings"] = df["embeddings"].apply(lambda x: np.array(eval(x)))
        df["similarity"] = df["embeddings"].apply(lambda emb: self.calculate_similarity(prompt_embedding, emb))
        best_chunk = df.loc[df["similarity"].idxmax(), "text"]

        client = _client(self.openai_api_key)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": f"You are {self.persona}, a knowledge-based assistant. Forget previous context."},
                {"role": "user", "content": f"Answer based only on this information: {best_chunk}\n\nPrompt: {prompt}"},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""


class EvaluationAgent:
    """Evaluate and optionally refine another agent's response."""

    def __init__(
        self,
        openai_api_key: str,
        persona: str,
        evaluation_criteria: str,
        worker_agent: Any | None = None,
        max_interactions: int = 3,
        agent_to_evaluate: Any | None = None,
    ):
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.worker_agent = worker_agent or agent_to_evaluate
        self.max_interactions = max_interactions

    def _evaluate_response(self, response_from_worker: str) -> str:
        client = _client(self.openai_api_key)
        eval_prompt = (
            f"Does the following answer meet the criteria?\n\n"
            f"ANSWER:\n{response_from_worker}\n\n"
            f"CRITERIA:\n{self.evaluation_criteria}\n\n"
            "Respond with Yes or No first, then give the reason."
        )
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": eval_prompt},
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()

    def _correction_instructions(self, response_from_worker: str, evaluation: str) -> str:
        client = _client(self.openai_api_key)
        correction_prompt = (
            "Create concise correction instructions for the worker agent.\n\n"
            f"Current response:\n{response_from_worker}\n\n"
            f"Evaluation result:\n{evaluation}\n\n"
            f"Criteria to satisfy:\n{self.evaluation_criteria}\n\n"
            "Only include the changes needed to meet the criteria."
        )
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": self.persona},
                {"role": "user", "content": correction_prompt},
            ],
            temperature=0,
        )
        return (response.choices[0].message.content or "").strip()

    def evaluate(self, initial_prompt: str, original_prompt: str | None = None, response_is_output: bool = False) -> dict[str, Any]:
        """Evaluate a worker result.

        By default `initial_prompt` is treated as a prompt for the worker agent.
        For the Phase 2 support functions, `response_is_output=True` allows the
        function to evaluate an already-generated worker response while still
        using the worker agent for corrections if needed.
        """
        if self.worker_agent is None:
            raise ValueError("EvaluationAgent needs a worker_agent or agent_to_evaluate.")

        prompt_to_worker = original_prompt or initial_prompt
        final_response = initial_prompt if response_is_output else ""
        evaluation = ""
        iterations = 0

        for i in range(self.max_interactions):
            iterations = i + 1
            print(f"\n--- Evaluation interaction {iterations} ---")

            if not response_is_output or i > 0:
                final_response = self.worker_agent.respond(prompt_to_worker)

            print(f"Worker response:\n{final_response}\n")
            evaluation = self._evaluate_response(final_response)
            print(f"Evaluation:\n{evaluation}\n")

            if evaluation.lower().startswith("yes"):
                break

            instructions = self._correction_instructions(final_response, evaluation)
            print(f"Correction instructions:\n{instructions}\n")
            prompt_to_worker = (
                f"Original prompt:\n{original_prompt or initial_prompt}\n\n"
                f"Previous response:\n{final_response}\n\n"
                f"Correction instructions:\n{instructions}\n\n"
                "Revise the response. Keep the same requested artifact type and satisfy the criteria exactly."
            )
            response_is_output = False

        return {
            "final_response": final_response,
            "evaluation": evaluation,
            "iterations": iterations,
            # Extra keys keep the return value easy to inspect in the Phase 1 script.
            "final_worker_response": final_response,
            "evaluation_result": evaluation,
            "iteration_count": iterations,
        }


class RoutingAgent:
    """Route a prompt to the best configured agent.

    The main routing signal is embedding similarity, as required for the project.
    A small keyword boost is also supported through an optional ``keywords`` field
    on each route. This keeps short, obvious prompts like "define user stories"
    from being routed to the wrong role because the sentence is too short for
    similarity alone to be reliable.
    """

    def __init__(self, openai_api_key: str, agents: list[dict[str, Any]] | None = None):
        self.openai_api_key = openai_api_key
        self.agents = agents or []

    def get_embedding(self, text: str) -> list[float]:
        client = _client(self.openai_api_key)
        response = client.embeddings.create(
            model=DEFAULT_EMBEDDING_MODEL,
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    @staticmethod
    def _keyword_boost(user_input: str, agent: dict[str, Any]) -> float:
        """Return a small routing boost for explicit words in the prompt."""
        keywords = agent.get("keywords", [])
        if not keywords:
            return 0.0

        text = user_input.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in text)
        # Keep the boost useful but not so large that it hides bad route config.
        return min(matches * 0.20, 0.60)

    def route(self, user_input: str) -> str:
        if not self.agents:
            return "No agents configured for routing."

        input_emb = np.array(self.get_embedding(user_input))
        best_agent: dict[str, Any] | None = None
        best_score = -1.0

        for agent in self.agents:
            agent_emb = np.array(self.get_embedding(agent["description"]))
            denominator = np.linalg.norm(input_emb) * np.linalg.norm(agent_emb)
            similarity = 0.0 if denominator == 0 else float(np.dot(input_emb, agent_emb) / denominator)
            boost = self._keyword_boost(user_input, agent)
            score = similarity + boost
            print(
                f"[Router] {agent['name']} similarity={similarity:.3f} "
                f"keyword_boost={boost:.3f} score={score:.3f}"
            )

            if score > best_score:
                best_score = score
                best_agent = agent

        if best_agent is None:
            return "Sorry, no suitable agent could be selected."

        print(f"[Router] Best agent: {best_agent['name']} (score={best_score:.3f})")
        func: Callable[[str], str] = best_agent["func"]
        return func(user_input)


class ActionPlanningAgent:
    """Extract a clean list of action steps from a high-level prompt."""

    def __init__(self, openai_api_key: str, knowledge: str):
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge

    def extract_steps_from_prompt(self, prompt: str) -> list[str]:
        client = _client(self.openai_api_key)
        system_prompt = (
            "You are an action planning agent. Using your knowledge, you extract from the user prompt "
            "the steps requested to complete the action the user is asking for. You return the steps as a list. "
            "Only return the steps in your knowledge. Forget any previous context. "
            f"This is your knowledge: {self.knowledge}"
        )
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        response_text = response.choices[0].message.content or ""
        steps = []
        for line in response_text.splitlines():
            cleaned = _clean_step_line(line)
            if not cleaned:
                continue
            # Avoid returning headers like "Steps:" as actual work items.
            if cleaned.lower() in {"steps", "steps:", "action steps", "action steps:"}:
                continue
            steps.append(cleaned)
        return steps
