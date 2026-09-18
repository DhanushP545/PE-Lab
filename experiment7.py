import os
import random
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenRouter client
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

prompt1 = "Explain about Block-Chain technology"
prompt2 = "Explain about Block-Chain tehcnology in less than 500 words, as if I am a first year computer science student. "

def generate_multiple(prompt, number=3):
    outputs = []
    for i in range(number):
        result = ask_model(prompt)
        outputs.append(result)
    return outputs

outputs1 = generate_multiple(prompt1,3)
outputs2 = generate_multiple(prompt2,3)
print("\n===== PROMPT 1 OUTPUTS =====")
for i, output in enumerate(outputs1, start=1):
    print(f"\n--- Output {i} ---")
    print(output)

print("\n===== PROMPT 2 OUTPUTS =====")
for i, output in enumerate(outputs2, start=1):
    print(f"\n--- Output {i} ---")
    print(output)

"""
------------------END OF MANUAL CODE-----------------------
"""