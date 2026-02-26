import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
SYSTEM_PROMPT: str = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful AI assistant. Be concise and clear.",
)

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY is not set. Add it to your .env file.")
