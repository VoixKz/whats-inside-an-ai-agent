# Step 1 - give the LLM a tool. It can ASK to use it, but it never sees the result.
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
    "parameters": {
        "type": "object",
        "properties": {"code": {"type": "string"}},
        "required": ["code"]
    }
}}]

question = input("You: ")
response = client.chat.completions.create(model=MODEL, tools=TOOL_MENU,
                                          messages=[{"role": "user", "content": question}])
reply = response.choices[0].message
if reply.tool_calls:  # the LLM answered with a tool request instead of text
    call = reply.tool_calls[0]
    print("The LLM asks for:", call.function.name, call.function.arguments)
    print("Our code runs it and gets:", run_python(**json.loads(call.function.arguments)))
else:
    print("AI:", reply.content)
