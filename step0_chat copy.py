# Step 0 - just the LLM: text in, text out.          pip install openai
import json, subprocess, sys
from llm import client, MODEL  # llm.py connects to the LLM; the key stays hidden in .env




question = input("You: ")
response = client.chat.completions.create(model=MODEL,
                                          messages=[{"role": "user", "content": question}])
print("AI:", response.choices[0].message.content)
