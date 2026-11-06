"""offline_demo.py - backup demo: no internet and no API key needed.

The LLM's replies are pre-recorded (a fake LLM), but the harness, the tools and the
loop are the real ones from mini_agent.py: files really get written, code really runs.
    python offline_demo.py
"""
import json, os
os.environ.setdefault("LLM_API_KEY", "offline")  # llm.py needs some key to start

try:
    import httpx
except ImportError:  # newer openai versions install httpx2 instead of httpx
    import httpx2 as httpx
from openai import OpenAI
import mini_agent

BUGGY = ("def is_prime(n):\n    for d in range(2, n):\n        if n % d == 0:\n"
         "            return False\n    return True\n")
FIXED = "def is_prime(n):\n    if n < 2:\n        return False\n" + BUGGY.split("\n", 1)[1]
TEST = "from primes import is_prime\nprint([n for n in range(12) if is_prime(n)])"

def ask(n, name, **args):  # a pre-recorded tool request
    return {"role": "assistant", "content": None, "tool_calls": [{"id": f"call_{n}", "type": "function",
            "function": {"name": name, "arguments": json.dumps(args)}}]}

RECORDED = [ask(1, "write_file", path="primes.py", content=BUGGY),
            ask(2, "run_python", code=TEST),
            ask(3, "write_file", path="primes.py", content=FIXED),
            ask(4, "run_python", code=TEST),
            {"role": "assistant", "content": "Done. My first version said 0 and 1 are prime, which is "
             "wrong. I added a check for n < 2, ran the test again, and now it prints [2, 3, 5, 7, 11]."}]

def fake_llm(request):  # answers like a real OpenAI-compatible server would
    reply = RECORDED.pop(0)
    return httpx.Response(200, json={"id": "offline", "object": "chat.completion", "created": 0,
        "model": "pre-recorded", "choices": [{"index": 0, "message": reply,
        "finish_reason": "tool_calls" if reply.get("tool_calls") else "stop"}]})

mini_agent.client = OpenAI(api_key="offline", base_url="http://offline.invalid/v1",
                           http_client=httpx.Client(transport=httpx.MockTransport(fake_llm)))

task = "Write is_prime in primes.py and test it"
print("Task:", task, "   (offline demo: the LLM's replies are pre-recorded)")
print("\nAgent:", mini_agent.agent(task))
