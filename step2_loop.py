# Step 2 - close the loop: send each result back and repeat. Now it is an agent!
import json, subprocess, sys
from llm import client, MODEL  # llm.py connects to the LLM; the key stays hidden in .env

def run_python(code):  # the tool: an ordinary Python function
    if input(f"\n--- run this code? ---\n{code}\n[y/n] ") != "y":
        return "The user said no."
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
    return r.stdout + r.stderr or "(no output)"

TOOL_MENU = [{"type": "function", "function": {  # the menu: name, what it does, what it needs
    "name": "run_python",
    "description": "Run Python code and return what it prints",
    "parameters": {"type": "object",
                   "properties": {"code": {"type": "string"}},
                   "required": ["code"]}}}]

messages = [{"role": "user", "content": input("You: ")}]  # the conversation so far
while True:
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_MENU)
    reply = response.choices[0].message
    messages.append(reply.model_dump(exclude_none=True))  # remember what the LLM said
    if not reply.tool_calls:  # no tool request -> this is the final answer
        print("AI:", reply.content)
        break
    for call in reply.tool_calls:  # run every tool it asked for...
        result = run_python(**json.loads(call.function.arguments))
        print("[result]", result)
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})  # ...show it
