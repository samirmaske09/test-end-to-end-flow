from strands import Agent, tool
from strands_tools import calculator
import json, requests
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@tool
def get_objects_api():
    """Fetch objects from the external REST API.
    
    Returns:
        dict: JSON response from the API containing objects data
    """
    try:
        response = requests.get("https://api.restful-api.dev/objects", verify=False, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

agent = Agent(
    name="strands_external_api_agent",
    model=BedrockModel(model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0"),
    tools=[calculator, get_objects_api],
    system_prompt="""You are a helpful assistant. You can do simple external api calls to get data about objects from a REST API and perform calculations using the calculator tool.""",
)

app = BedrockAgentCoreApp()

@app.entrypoint
def strands_agent_bedrock(payload):
    """Invoke the agent with a payload"""
    user_input = payload.get("prompt", "")
    if not user_input:
        return "No prompt provided"
    
    try:
        response = agent(user_input)
        return str(response)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()