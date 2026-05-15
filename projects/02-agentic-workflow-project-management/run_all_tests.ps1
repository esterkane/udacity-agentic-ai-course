New-Item -ItemType Directory -Force outputs | Out-Null

$commands = @(
    @('phase_1/direct_prompt_agent.py', 'outputs/direct_prompt_agent_output.txt'),
    @('phase_1/augmented_prompt_agent.py', 'outputs/augmented_prompt_agent_output.txt'),
    @('phase_1/knowledge_augmented_prompt_agent.py', 'outputs/knowledge_augmented_prompt_agent_output.txt'),
    @('phase_1/rag_knowledge_prompt_agent.py', 'outputs/rag_knowledge_prompt_agent_output.txt'),
    @('phase_1/evaluation_agent.py', 'outputs/evaluation_agent_output.txt'),
    @('phase_1/routing_agent.py', 'outputs/routing_agent_output.txt'),
    @('phase_1/action_planning_agent.py', 'outputs/action_planning_agent_output.txt'),
    @('phase_2/agentic_workflow.py', 'outputs/agentic_workflow_output.txt')
)

foreach ($cmd in $commands) {
    $script = $cmd[0]
    $outfile = $cmd[1]
    Write-Host "Running $script"
    python $script 2>&1 | Out-File -Encoding utf8 $outfile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $script. Check $outfile" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

Write-Host "All scripts finished. Check outputs/ before submitting." -ForegroundColor Green
