import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

baseline_prompt = "Write a one-paragraph bio of Ada Lovelace."

response1 = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": baseline_prompt
        }
    ]
)

print("BASELINE RESPONSE")
print("-----------------")
print(response1.choices[0].message.content)

enhanced_prompt = """You are a history-of-computing educator.

Write a concise biography of Ada Lovelace for undergraduate
computer science students.

Include:
1. Her historical significance.
2. Her collaboration with Charles Babbage.
3. The Analytical Engine.
4. Her important notes on the Analytical Engine.
5. Why she is considered an important figure in the history
   of computer programming.

Write exactly one paragraph of approximately 120-150 words.
Use a clear, academic, student-friendly tone.
Focus on historically relevant information and avoid
unnecessary details."""

response2 = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": enhanced_prompt
        }
    ]
)

print("ENHANCED RESPONSE")
print("-----------------")
print(response2.choices[0].message.content)

