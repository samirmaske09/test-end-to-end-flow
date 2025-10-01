from bedrock_agentcore_starter_toolkit.notebook.runtime import bedrock_agentcore

agentcore_runtime = bedrock_agentcore.BedrockAgentCore()

def configure_runtime(non_interactive: bool = True):
    """Configure Bedrock AgentCore safely."""
    response = agentcore_runtime.configure(
        entrypoint="strands_agentcore/external_api.py",
        auto_create_execution_role=True,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        region="us-east-1",
        agent_name="strands_external_api_agent",
        interactive=not non_interactive,  # 👈 prevent prompt in CI
    )
    print("Configuration response:", response)
    return response


if __name__ == "__main__":
    # Only runs if you execute: python strands_agentcore/runtime_deployment.py
    configure_runtime(non_interactive=False)
    agentcore_runtime.launch()
