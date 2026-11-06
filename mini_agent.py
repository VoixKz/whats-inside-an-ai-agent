"""mini_agent.py - a tiny AI coding agent in ~50 lines of Python.

Connects to the LLM through llm.py. Put your key in the hidden file .env first.
    pip install openai
    python check_llm.py               # once: checks the key, the model and tool calling
    python mini_agent.py
"""
import json, subprocess, sys
from llm import client, MODEL  # llm.py connects to the LLM; the key stays hidden in .env

# ---------- STEP 1: tools are just ordinary Python functions ----------
def run_python(code):
    if input(f"\n--- agent wants to run ---\n{code}\n--- allow? [y/n] ") != "y":
        return "The user refused to run this code."
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
    return (r.stdout + r.stderr)[-2000:] or "(no output)"

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to {path}"

def read_file(path):
    with open(path) as f:
        return f.read()[-4000:]

TOOLS = {"run_python": run_python, "write_file": write_file, "read_file": read_file}

# ---------- STEP 2: describe the tools so the model knows they exist ----------
def schema(name, description, **params):
    props = {p: {"type": "string", "description": d} for p, d in params.items()}
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": props, "required": list(params)}}}

SCHEMAS = [schema("run_python", "Run Python code and return what it prints", code="Python source code"),
           schema("write_file", "Create or overwrite a file", path="file path", content="full file text"),
           schema("read_file", "Read a file", path="file path")]

# ---------- STEP 3: the agent loop - ask, act, observe, repeat ----------
def agent(task, max_steps=10):
    messages = [{"role": "system", "content": "You are a coding agent. Use the tools to do the task, "
                 "test it with plain Python (no pip, no venv), then reply with a short summary."},
                {"role": "user", "content": task}]
    for step in range(1, max_steps + 1):
        reply = client.chat.completions.create(model=MODEL, messages=messages, tools=SCHEMAS).choices[0].message
        messages.append(reply.model_dump(exclude_none=True))
        if not reply.tool_calls:                      # no tool requested -> the agent is done
            return reply.content
        for call in reply.tool_calls:                 # the model only ASKS; our code does the work
            args = json.loads(call.function.arguments)
            print(f"[step {step}] {call.function.name}({', '.join(args)})")
            try:
                result = TOOLS[call.function.name](**args)
            except Exception as e:
                result = f"Error: {e}"
            print("[result]", result[:300])
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    return "Stopped: too many steps."

if __name__ == "__main__":
    print(agent(input("Task: ")))
