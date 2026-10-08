import os
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# SETUP
# =========================================================

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

# =========================================================
# PART A: BASIC PROMPT
# =========================================================

basic_prompt = """
Explain the benefits of cloud computing for students.
"""

basic_response = ask_model(basic_prompt)

print("\n" + "=" * 70)
print("BASIC PROMPT RESPONSE")
print("=" * 70)

print(basic_response)


# =========================================================
# PART B: STRUCTURED PROMPT
# =========================================================

structured_prompt = """
Explain the benefits of cloud computing for college students.

Follow this exact output format:

# Benefits of Cloud Computing

## Introduction
Write a short introduction of 2-3 sentences.

## Key Benefits
Provide exactly 5 benefits as bullet points.

## Comparison
Create a Markdown table with exactly these columns:

| Benefit | Explanation | Student Use |

Include 5 rows in the table.

## Conclusion
Write a short conclusion of 2-3 sentences.

Do not add any sections other than the ones specified above.
"""

structured_response = ask_model(structured_prompt)

print("\n" + "=" * 70)
print("STRUCTURED PROMPT RESPONSE")
print("=" * 70)

print(structured_response)


# =========================================================
# PART C: FORMAT CHECK
# =========================================================

def check_format(response):

    checks = {
        "title": "# Benefits of Cloud Computing" in response,
        "introduction": "## Introduction" in response,
        "key_benefits": "## Key Benefits" in response,
        "five_bullets": response.count("\n- ") >= 5,
        "comparison": "## Comparison" in response,
        "markdown_table": "|" in response,
        "table_header": (
            "| Benefit | Explanation | Student Use |"
            in response
        ),
        "five_table_rows": response.count("|") >= 18,
        "conclusion": "## Conclusion" in response
    }

    return checks


format_results = check_format(structured_response)

print("\n" + "=" * 70)
print("INITIAL FORMAT CHECK")
print("=" * 70)

for criterion, result in format_results.items():
    status = "PASS" if result else "FAIL"
    print(f"{criterion:20} : {status}")


# =========================================================
# PART D: CHECK WHETHER FORMAT IS ACCEPTABLE
# =========================================================

format_good = all(format_results.values())


if format_good:

    final_response = structured_response

    print("\n" + "=" * 70)
    print("FORMAT ACCEPTED")
    print("=" * 70)

    print("The structured response satisfies all required format criteria.")


else:

    print("\n" + "=" * 70)
    print("FORMAT NOT ACCEPTED")
    print("=" * 70)

    print("Some format requirements were not satisfied.")
    print("Refining the prompt...")


    # =====================================================
    # PART E: REFINED STRUCTURED PROMPT
    # =====================================================

    refined_prompt = """
Explain the benefits of cloud computing for college students.

You MUST follow the format below exactly.

# Benefits of Cloud Computing

## Introduction
Write exactly 2-3 sentences.

## Key Benefits
Write exactly 5 bullet points.
Every benefit must begin with "- ".

## Comparison
Create a Markdown table.

The table MUST have this exact header:

| Benefit | Explanation | Student Use |
|---|---|---|

The table MUST contain exactly 5 data rows.

## Conclusion
Write exactly 2-3 sentences.

Rules:
1. Use the headings exactly as provided.
2. Do not change the heading names.
3. Use exactly 5 bullet points.
4. Use exactly 5 rows in the Markdown table.
5. Do not add any extra sections.
6. Do not use HTML tables.
7. Return only the requested formatted answer.
"""

    refined_response = ask_model(refined_prompt)

    print("\n" + "=" * 70)
    print("REFINED PROMPT RESPONSE")
    print("=" * 70)

    print(refined_response)

    final_response = refined_response


    # =====================================================
    # PART F: FINAL FORMAT CHECK
    # =====================================================

    refined_format_results = check_format(refined_response)

    print("\n" + "=" * 70)
    print("FINAL FORMAT CHECK")
    print("=" * 70)

    for criterion, result in refined_format_results.items():
        status = "PASS" if result else "FAIL"
        print(f"{criterion:20} : {status}")

    if all(refined_format_results.values()):

        print("\nFinal status: FORMAT ACCEPTED")

    else:

        print("\nFinal status: FORMAT STILL NEEDS IMPROVEMENT")


# =========================================================
# PART G: FINAL RESULT
# =========================================================

print("\n" + "=" * 70)
print("FINAL RECORDED RESPONSE")
print("=" * 70)

print(final_response)


# =========================================================
# PART H: EXPERIMENT SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("EXPERIMENT SUMMARY")
print("=" * 70)

print("""
Basic Prompt:
Generated a general response without strict formatting instructions.

Structured Prompt:
Requested headings, bullet points, and a Markdown table.

Format Verification:
The generated response was checked against the required format.

Refinement:
If the response failed any format requirement, a more explicit
structured prompt was used to generate the response again.

Final Result:
The final response was recorded after format verification.
""")