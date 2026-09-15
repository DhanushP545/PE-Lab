import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "openai/gpt-chat-latest"


def ask_model(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content


# PART A: ROLE-BASED PROMPTING

neutral_prompt = """
Explain how to create a monthly budget.
"""

neutral_response = ask_model(neutral_prompt)

print("\n" + "=" * 60)
print("NEUTRAL RESPONSE")
print("=" * 60)
print(neutral_response)


role_prompt = """
You are a financial education advisor helping others.

Explain how a college student can create a monthly budget.

Use simple language.

Provide five practical steps.

Include one example monthly budget.

Focus on financial education rather than individualized investment advice.
"""

role_response = ask_model(role_prompt)

print("\n" + "=" * 60)
print("ROLE-BASED RESPONSE")
print("=" * 60)
print(role_response)


# PART B: NEGATIVE PROMPTING

unrestricted_prompt = """
Suggest ways for a student to choose a laptop for college.
"""

unrestricted_response = ask_model(unrestricted_prompt)

print("\n" + "=" * 60)
print("UNRESTRICTED RESPONSE")
print("=" * 60)
print(unrestricted_response)


negative_prompt = """
Suggest ways to choose a laptop for college.

Do not mention any brand names or specific product models.

Focus only on general factors such as:
budget, battery life, portability, performance,
storage, memory, and warranty.
"""

negative_response = ask_model(negative_prompt)

print("\n" + "=" * 60)
print("NEGATIVE PROMPT RESPONSE")
print("=" * 60)
print(negative_response)


brands = [
    "Apple", "Dell", "HP", "Lenovo", "ASUS", "Acer",
    "Microsoft", "Samsung", "MSI", "Razer", "Huawei", "LG"
]


def count_brand_references(text):
    return sum(
        1 for brand in brands
        if brand.lower() in text.lower()
    )


unrestricted_violations = count_brand_references(unrestricted_response)
negative_violations = count_brand_references(negative_response)

print("\n" + "=" * 60)
print("CONSTRAINT COMPLIANCE")
print("=" * 60)
print("Unrestricted violations :", unrestricted_violations)
print("Constrained violations  :", negative_violations)

if unrestricted_violations > 0:
    suppression_rate = (
        (unrestricted_violations - negative_violations)
        / unrestricted_violations
    ) * 100
else:
    suppression_rate = 0

print(f"Suppression Rate        : {suppression_rate:.2f}%")


# PART C: CONTRADICTORY PROMPT

contradictory_prompt = """
Recommend three specific laptop products for college students.

Do not mention any brand names or specific product models.
"""

contradictory_response = ask_model(contradictory_prompt)

print("\n" + "=" * 60)
print("CONTRADICTORY PROMPT RESPONSE")
print("=" * 60)
print(contradictory_response)


# PART D: REFINED PROMPT

refined_prompt = """
Recommend three categories of laptops suitable for college students.

Do not mention brands or specific product models.

For each category, describe:

1. Intended use
2. Performance level
3. Portability
4. Features to look for
"""

refined_response = ask_model(refined_prompt)

print("\n" + "=" * 60)
print("REFINED PROMPT RESPONSE")
print("=" * 60)
print(refined_response)


# PART E: COMBINED ROLE + STRUCTURED PROMPT

combined_prompt = """
You are a financial education advisor helping undergraduate students.

Explain the basics of saving and budgeting.

Organize your response into:

1. Saving
2. Budgeting
3. Emergency funds
4. Common mistakes
"""

combined_response = ask_model(combined_prompt)

print("\n" + "=" * 60)
print("COMBINED ROLE + STRUCTURED RESPONSE")
print("=" * 60)
print(combined_response)