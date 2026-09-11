import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

print("Client initialized successfully.")

prompt1 = "outerspace"
prompt2 = "Tell me briefly about outerspace. Limit your response to less than 350 words."
prompt3 = "Imagine you are a astrophysicist visitng a highschool, tell me about the all time best discoveries of outerspace. Follow a student-friendly structure *fact-a brief 1/2 line explanation* for each fact. Limit your response to 15 facts or lesser."


response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": prompt3
        }
    ]
)

print(f"\nRound3\nPrompt: {prompt3}")
print(response.choices[0].message.content)

