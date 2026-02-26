from groq import AsyncGroq
from config import GROQ_API_KEY, GROQ_MODEL, SYSTEM_PROMPT

_client = AsyncGroq(api_key=GROQ_API_KEY)


async def chat_completion(message: str, history: list[dict]) -> str:
    """
    Send a message to the Groq LLM and return the assistant reply.

    Args:
        message:  The latest user message.
        history:  Previous turns as [{"role": "user"|"assistant", "content": "..."}].
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": message},
    ]

    response = await _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )

    return response.choices[0].message.content
