
import json
import requests

from key import OPENROUTER_KEY


def run_model(system_prompt: str, user_document: str) -> dict:
    """ Runs model as agent with system prompt and user documents """
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_document}
            ],
            "temperature": 0.0
        }
    )

    response.raise_for_status()

    raw_output = response.json()["choices"][0]["message"]["content"].strip()

    try:
        agent_output = json.loads(raw_output)
    except:
        print("RAW OUTPUT:", raw_output)
        raise
    return agent_output