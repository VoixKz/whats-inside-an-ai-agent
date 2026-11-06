"""check_llm.py - run this BEFORE the talk. It never prints your key.

Checks that the key works, lists the models on the server, and tests a tool call.
    python check_llm.py
"""
import time
from llm import client, MODEL

print("Server:", client.base_url, "| model in .env:", MODEL)

try:
    ids = [m.id for m in client.models.list()]
    print("Models on this server:", ", ".join(ids) or "(none listed)")
    if ids and MODEL not in ids:
        print(f"!! '{MODEL}' is not in that list: copy one of the names above into LLM_MODEL= in .env")
except Exception as e:
    print("(could not list models:", type(e).__name__, str(e)[:150], ")")

try:
    t = time.time()
    r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": "Say hi in 3 words."}])
    print(f"OK  chat works ({time.time() - t:.1f}s):", r.choices[0].message.content)
except Exception as e:
    print("FAIL chat:", type(e).__name__, str(e)[:300])
    raise SystemExit(1)

menu = [{"type": "function", "function": {"name": "run_python", "description": "Run Python code",
         "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}}]
try:
    t = time.time()
    r = client.chat.completions.create(model=MODEL, tools=menu,
                                       messages=[{"role": "user", "content": "Use Python to compute 2**200."}])
    calls = r.choices[0].message.tool_calls
    if calls:
        print(f"OK  tool calling works ({time.time() - t:.1f}s):", calls[0].function.name, calls[0].function.arguments)
        print("Ready for the demo.")
    else:
        print("!! The model answered with text, not a tool call. Try another model in .env:", r.choices[0].message.content)
except Exception as e:
    print("FAIL tool calling:", type(e).__name__, str(e)[:300])
