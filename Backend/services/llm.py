import json

from groq import AsyncGroq
from config import GROQ_API_KEY, GROQ_MODEL, SYSTEM_PROMPT

_client = AsyncGroq(api_key=GROQ_API_KEY)

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
          },
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
      },
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_current_time",
      "description": "Get the current time in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
          },
        },
        "required": ["location"],
      },
    }
  }
]

def get_current_time(location: str) -> str:
    """Get the current time in a given location"""

    print()
    print(f"[5] TOOL DEF | get_current_time() called with location='{location}'")
    print()

    result = f"The current time in {location} is 3:45 PM."

    print()
    print(f"[6] TOOL DEF → LLM SERVICE | Tool result: '{result}'")
    print()

    return result

def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location"""

    print()
    print(f"[5] TOOL DEF | get_current_weather() called with location='{location}', unit='{unit}'")
    print()

    result = f"The current weather in {location} is 72 degrees {unit}."

    print()
    print(f"[6] TOOL DEF → LLM SERVICE | Tool result: '{result}'")
    print()

    return result

async def chat_completion(message: str, history: list[dict]) -> str:
    """
    Send a message to the Groq LLM and return the assistant reply.

    Args:
        message:  The latest user message.
        history:  Previous turns as [{"role": "user"|"assistant", "content": "..."}].
    """

    print()
    print(f"[3] BACKEND → LLM SERVICE | chat_completion() called")
    print(f"    message  : '{message}'")
    print(f"    history  : {len(history)} previous turn(s)")
    print()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": message},
    ]

    print()
    print(f"[4] LLM SERVICE → GROQ API | Sending first request to Groq")
    print(f"    model      : {GROQ_MODEL}")
    print(f"    total msgs : {len(messages)}  (system + history + new user message)")
    print(f"    tools      : {[t['function']['name'] for t in tools]}")
    print()

    response = await _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
        tools=tools,
        tool_choice="auto",
    )
    
    print('This is the response before adding to the assistant:', response)

    assistant_message = response.choices[0].message

    print('This is the assistant message:', assistant_message)

    # ── Tool-call path ───────────────────────────────────────────────────────
    if assistant_message.tool_calls:

        print()
        print(f"[4b] GROQ API → LLM SERVICE | Model wants to call a tool (finish_reason=tool_calls)")
        print(f"     tool_calls : {[tc.function.name for tc in assistant_message.tool_calls]}")
        print()

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            args = json.loads(tool_call.function.arguments)

            print()
            print(f"[4c] LLM SERVICE | Dispatching tool '{tool_call.function.name}' with args: {args}")
            print()

            if tool_call.function.name == "get_current_weather":
                result = get_current_weather(
                    location=args["location"],
                    unit=args.get("unit", "fahrenheit"),
                )
            elif tool_call.function.name == "get_current_time":
                result = get_current_time(location=args["location"])
            else:
                result = f"Unknown tool: {tool_call.function.name}"
            print(result)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

        print()
        print(f"[7] LLM SERVICE → GROQ API | Sending second request with tool result")
        print(f"    total msgs now : {len(messages)}  (added assistant tool-call msg + tool result msg)")
        print()

        final = await _client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )

        final_content = final.choices[0].message.content

        print()
        print(f"[8] GROQ API → LLM SERVICE | Final text response received")
        print(f"    reply : '{final_content}'")
        print()

        return final_content

    # ── Direct reply path (no tool needed) ──────────────────────────────────
    print()
    print(f"[4b] GROQ API → LLM SERVICE | Direct reply (no tool call needed)")
    print(f"     reply : '{assistant_message.content}'")
    print()

    return assistant_message.content
