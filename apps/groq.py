import httpx
from dotenv import load_dotenv
import os 

load_dotenv() 

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API = os.getenv("GROQ_API", "")

async def iliiz(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are Iliiz, a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
    except httpx.HTTPStatusError as e:
        return f"Groq API Error: Status {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        return f"Network Error: Could not connect to Groq server. {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"