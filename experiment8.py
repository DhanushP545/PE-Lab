import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "openrouter/free"

def ask_model(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content.strip()

prompt_1 = "Find out latest telugu films released in the past 2 weeks, and rank them according to public reviews."
prompt_2 = "Find out biryani places in vijayawada, and rank them according to reviews on various platforms."

results = []
for i in range(3):
    response_1 = ask_model(prompt_1)
    response_2 = ask_model(prompt_2)

    results.append({
        "run" : i+1,
        "prompt" : prompt_1,
        "response" : response_1
    })

    results.append({
        "run" : i+1,
        "prompt" : prompt_2,
        "response" : response_2
    })

df = pd.DataFrame(results)
print(df)
