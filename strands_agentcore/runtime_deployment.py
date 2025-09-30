from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import os, time, json, urllib3, ssl
#from IPython.display import Markdown, display

# Set environment variables for AWS credentials
#os.environ['AWS_PROFILE'] = 'Salman'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Disable SSL warnings and verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

#os.environ['AWS_PROFILE'] = 'Salman'
#os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['AWS_CA_BUNDLE'] = ''


#boto_session = Session(profile_name='Salman')
region = 'us-east-1'

agentcore_runtime = Runtime()
agent_name = "strands_external_api_agent"

response = agentcore_runtime.configure(
    entrypoint="external_api.py",
    auto_create_execution_role=True,
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    region=region,
    agent_name=agent_name
)
print("Configuration response:", response)

# Check if required files exist
import os
if not os.path.exists("basic_connection_check.py"):
    print("❌ basic_connection_check.py not found")
else:
    print("✅ basic_connection_check.py found")
    
if not os.path.exists("requirements.txt"):
    print("❌ requirements.txt not found")
else:
    print("✅ requirements.txt found")
    with open("requirements.txt", "r") as f:
        print("Requirements content:", f.read())

try:
    print("Starting launch process...")
    launch_result = agentcore_runtime.launch()
except Exception as e:
    print(f"Launch failed: {e}")
    print("Checking if agent was created despite timeout...")
    try:
        status_response = agentcore_runtime.status()
        if status_response:
            print("Agent may have been created, continuing...")
            launch_result = type('obj', (object,), {'agent_arn': 'timeout-but-continuing'})
        else:
            print("Agent creation failed")
            exit(1)
    except Exception:
        print("Agent creation failed")
        exit(1)

print("Agent_arn: ", launch_result.agent_arn)

status_response = agentcore_runtime.status()
if status_response and hasattr(status_response, 'endpoint') and status_response.endpoint:
    status = status_response.endpoint['status']
    end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
    while status not in end_status:
        time.sleep(10)
        status_response = agentcore_runtime.status()
        if status_response and status_response.endpoint:
            status = status_response.endpoint['status']
            print(status)
        else:
            print("Status check failed")
            break
    print("Final status:", status_response.endpoint if status_response else "None")
else:
    print("Agent endpoint not available - build may have failed")
    exit(1)

# Only try to invoke if agent is ready
if status_response and status_response.endpoint and status_response.endpoint.get('status') == 'READY':
    invoke_response = agentcore_runtime.invoke({"prompt": "Do a nuclear web search for the country India, On-site Physical Protection, Mandatory Physical Protection, Is physical protection a condition for licensing?"})
    print("invoke_response: ", invoke_response)
    
    if 'response' in invoke_response and invoke_response['response']:
        response_text = invoke_response['response'][0]
        print("Response:", response_text)
    else:
        print("No response received:", invoke_response)
else:
    print("Agent not ready for invocation - skipping test")