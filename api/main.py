from fastapi import FastAPI, Query
import requests
import json

app = FastAPI()

API_URL = "https://instantseek.org/api/chat"
SECRET = "pika"  # Secret to show conversation_id

@app.get("/")
async def chat(query: str, s: str = Query(None)):
    """
    Handles user queries and optionally includes conversation_id if secret is provided.
    
    - `query`: The user's message.
    - `s`: Secret or conversation_id (if s=pika, fetches new id).
    """

    # Check if `s` is a conversation ID or the secret key
    conversation_id = None
    if s and s != SECRET:
        conversation_id = s  # Use provided conversation_id

    payload = {
        "message": query,
        "conversationId": conversation_id
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 13; 220333QAG Build/TKQ1.221114.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.260 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'origin': "https://instantseek.org",
        'referer': "https://instantseek.org/chat.html"
    }

    response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
    data = response.json()

    # Prepare response
    result = {
        "response": data.get("response", "Try again with another query"),
        "Dev": "pikachufrombd.t.me"
    }

    # Show conversation_id only if s=pika
    if s == SECRET:
        result["conversation_id"] = data.get("conversation_id", None)

    return result
