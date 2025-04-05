from langflow.load import run_flow_from_json
import requests
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6d6e7223-56b9-4f20-b1da-6b99fbbb0bbf"
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
# ENDPOINT = "nutrition" # The endpoint name of the flow

def askAi(profile,question):
  TWEAKS = {
    "TextInput-sBUdF": {
      "input_value": question
    },
    "TextInput-tLIH3": {
      "input_value": profile
    }
  }

  result = run_flow_from_json(flow="AskAI-1.0.json",
                              input_value="message",
                              session_id="", # provide a session id if you want to use session state
                              fallback_to_env_vars=True, # False by default
                               tweaks=TWEAKS)
  
  return result[0].outputs[0].results["text"].data["text"]



def get_macros(profile,goals):
  TWEAKS = {
      "TextInput-0xWcf": {
        "input_value": goals
      },
      "TextInput-PXcMS": {
        "input_value": profile
      }
    }

  return run_flow("",tweaks=TWEAKS, application_token=APPLICATION_TOKEN)

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/nutrition"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    
    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]


result = get_macros("name: Atul, age: 21, height: 172cm, weight: 80kg, activity level: moderate","fat loss")
print(result)