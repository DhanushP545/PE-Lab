import os
from dotenv import load_dotenv
import base64
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)
"""
prompt_ambiguous = 
Write a short paragraph about Python .


prompt_clear =
Write a short paragraph of the reptile python snake.


print("Client initialized successfully.")
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": prompt_clear
        }
    ]
)

print(f"\nPrompt: {prompt_clear}")
print(response.choices[0].message.content)
"""



"""-------------------------CASE 2--------------------------"""
"""
with open("paper.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

print("PDF loaded successfully.")
"""

prompt_corrected = """
You are an academic research assistant.

Analyze the provided research paper and produce a concise summary.

Your response must include:

1. Research Problem
   - What problem does the paper address?
   - Why is this problem important?

2. Methodology
   - Explain the main approach or methodology used by the authors.

3. Main Contributions
   - Identify the key contributions of the paper.
   - Explain why each contribution is significant.

4. Findings
   - Summarize the main results or findings reported in the paper.

Keep the response within 500 words.

Use clear headings and bullet points where appropriate.
Base your answer only on information contained in the provided paper.
Do not invent or assume information that is not stated in the paper.
"""
prompt_missing = "Summarize this paper and tell me its key contributions."
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_missing
                },
            ]
        }
    ]
)
"""
response_corrected = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_corrected
                },
                {
                    "type": "file",
                    "file": {
                        "filename": "paper.pdf",
                        "file_data": f"data:application/pdf;base64,{pdf_data}"
                    }
                }
            ]
        }
    ]
)
"""
print(f"\nPrompt : {prompt_missing}")
print(response.choices[0].message.content)