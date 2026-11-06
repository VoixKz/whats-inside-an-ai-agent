# Build a tiny AI agent, step by step

| File | What it adds | Try asking |
|---|---|---|
| `step0_chat.py` | Just the LLM: text in, text out | What files are in my folder? |
| `step1_tool.py` | One tool + a menu. The LLM can **ask** to run code, but never sees the result | What is 2 to the power of 200? Use Python. |
| `step2_loop.py` | The loop: results go back to the LLM until it gives a final answer. **Now it is an agent.** | Which numbers below 50 are prime? Check with Python. |
| `mini_agent.py` | Step 3, a bigger harness: 3 tools, a system prompt, a step limit, errors sent back to the LLM | Write is_prime in primes.py and test it |
| `offline_demo.py` | Backup demo with a pre-recorded LLM. No internet, no key | (nothing, just run it) |
| `llm.py` | The one place that connects to the LLM. Reads your key from `.env` | |
| `check_llm.py` | Checks your key, lists the models, tests a tool call | |

## 1. Install

```bash
pip install openai
```

No Python on this computer? On the GitHub page click **Code → Codespaces → Create codespace**. You get VS Code in the browser with `openai` already installed. Then follow the steps below in its terminal (open `.env` there with `code .env`).

## 2. Put your key in `.env` (once, and never on screen)

`.env` is a hidden file in this folder. Downloaded from GitHub and there is no `.env` yet? Run `python check_llm.py` once: it creates `.env` for you. Then open it:

```bash
open -e .env        # Mac (TextEdit)
notepad .env        # Windows
```

Replace `paste-your-key-here` with your key and save. The code reads the key from there, so it never appears in the code, the slides or the terminal.

By default it uses CityU's server, `https://llm.cs.cityu.edu.hk/v1`. For another OpenAI-compatible provider, change `LLM_BASE_URL` and `LLM_MODEL` in `.env`, for example DeepSeek: `https://api.deepseek.com` and `deepseek-flash`.

**Never share `.env`.** Before you send this folder to anyone, delete your key from it.

## 3. Check the connection

```bash
python check_llm.py
```

It lists the models on the server. If it says your `LLM_MODEL` is not in the list, copy a name from the list into `.env`. It should end with `OK tool calling works` and `Ready for the demo.`

## 4. Run the steps in order

```bash
python step0_chat.py
python step1_tool.py
python step2_loop.py
python mini_agent.py
python offline_demo.py    # works with no key and no internet
```

Before any code runs, the agent asks `[y/n]`. Read the code first and only type `y` if it is safe.

## Make it yours

- Add a `list_files` tool (hint: `os.listdir`)
- Add an "always allow" answer to the `[y/n]` question
- Print how many steps the agent used
- Ask it to build a small game in `game.html`
