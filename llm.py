# llm.py - the ONE place that connects to the LLM (CityU's DeepSeek server by default).
# Your key lives in the hidden file .env next to this file, so it never appears on screen.
import os, sys
from openai import OpenAI

ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if not os.path.exists(ENV_FILE):  # fresh download: create .env with a spot for your key
    with open(ENV_FILE, "w") as f:
        f.write("LLM_API_KEY=paste-your-key-here\n")
for line in open(ENV_FILE):
    name, sep, value = line.strip().partition("=")
    if sep and not name.startswith("#"):
        os.environ.setdefault(name.strip(), value.strip().strip("'\""))

API_KEY = os.getenv("LLM_API_KEY", "")
if not API_KEY or API_KEY == "paste-your-key-here":
    sys.exit(f"No key yet. Open {ENV_FILE} and paste your key after LLM_API_KEY=")

client = OpenAI(api_key=API_KEY, base_url=os.getenv("LLM_BASE_URL", "https://llm.cs.cityu.edu.hk/v1"))
MODEL = os.getenv("LLM_MODEL", "CS3383/DeepSeek-V4-Flash")
