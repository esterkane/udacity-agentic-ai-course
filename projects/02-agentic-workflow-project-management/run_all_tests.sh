#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs

echo "Running Phase 1 agent tests..."
cd phase_1
for script in direct_prompt_agent.py augmented_prompt_agent.py knowledge_augmented_prompt_agent.py rag_knowledge_prompt_agent.py evaluation_agent.py routing_agent.py action_planning_agent.py; do
  echo "Running $script"
  python "$script" | tee "../outputs/${script%.py}_output.txt"
done

cd ../phase_2
echo "Running Phase 2 workflow..."
python agentic_workflow.py | tee "../outputs/agentic_workflow_output.txt"
