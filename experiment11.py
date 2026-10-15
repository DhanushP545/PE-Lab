import os
import re
import pandas as pd
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
# PART A: SELECT LOGIC PUZZLE
# =========================================================

puzzle = """
A three-digit secret code has distinct digits.

Clue 1: 682 - One digit is correct and in the right position.
Clue 2: 614 - One digit is correct but in the wrong position.
Clue 3: 206 - Two digits are correct but both are in the wrong positions.
Clue 4: 738 - No digit is correct.
Clue 5: 780 - One digit is correct but in the wrong position.

Find the three-digit secret code.
"""

expected_answer = "042"


# =========================================================
# PART B: DIRECT PROMPT
# =========================================================

direct_prompt = f"""
Solve the following logic puzzle.

{puzzle}

Return the three-digit code and a brief explanation.
Preserve leading zeros if any.
"""

direct_response = ask_model(direct_prompt)

print("\n" + "=" * 70)
print("DIRECT PROMPT RESPONSE")
print("=" * 70)

print(direct_response)


# =========================================================
# PART C: STEPWISE PROMPT
# =========================================================

stepwise_prompt = f"""
Solve the following logic puzzle using a structured approach.

{puzzle}

Follow these steps:

1. Analyze the clue 738 to eliminate impossible digits.
2. Analyze the clue 780 to identify a possible digit and
   determine its position.
3. Use clues 682 and 206 to determine the positions of
   the remaining digits.
4. Use clue 614 to verify the remaining digit and its position.
5. Combine the constraints and give the final three-digit code.

Provide a brief justification for each step.
Return the final code separately.
"""

stepwise_response = ask_model(stepwise_prompt)

print("\n" + "=" * 70)
print("STEPWISE PROMPT RESPONSE")
print("=" * 70)

print(stepwise_response)


# =========================================================
# PART D: DECOMPOSE INTO FOUR SUBPROBLEMS
# =========================================================

subproblems = [
    {
        "name": "Subproblem 1 - Eliminate Digits",
        "prompt": """
Analyze clue 738: no digit is correct.

Which digits must be eliminated from the secret code?
Return the eliminated digits and a brief explanation.
"""
    },
    {
        "name": "Subproblem 2 - Identify the First Constraint",
        "prompt": """
Using the puzzle clues, analyze 780:
one digit is correct but in the wrong position.

Combine this with the fact that 7, 3, and 8 are absent.
Identify the digit that must be present and state which
position it cannot occupy.
Give a brief explanation.
"""
    },
    {
        "name": "Subproblem 3 - Determine Digit Positions",
        "prompt": """
Use these clues:
682: one digit is correct and in the right position.
206: two digits are correct but both are in the wrong positions.

Using the eliminated digits 7, 3, and 8, determine the
positions and identities of the digits that can be established.
Give a brief explanation.
"""
    },
    {
        "name": "Subproblem 4 - Verify the Remaining Digit",
        "prompt": """
Use clue 614: one digit is correct but in the wrong position.

Combine it with the other puzzle clues to determine the
remaining digit and its valid position.

State the resulting three-digit code if it can be determined.
Give a brief explanation.
"""
    }
]

subproblem_results = []

for subproblem in subproblems:

    prompt = f"""
You are solving one part of a logic puzzle.

FULL PUZZLE:
{puzzle}

{ subproblem["prompt"] }

Do not assume that an unverified guess is correct.
Provide only the result of this subproblem and a brief explanation.
"""

    response = ask_model(prompt)

    subproblem_results.append({
        "subproblem": subproblem["name"],
        "response": response
    })

    print("\n" + "=" * 70)
    print(subproblem["name"])
    print("=" * 70)

    print(response)


# =========================================================
# PART E: COMBINE PARTIAL ANSWERS
# =========================================================

partial_answers = "\n\n".join(
    f"{item['subproblem']}:\n{item['response']}"
    for item in subproblem_results
)

combine_prompt = f"""
Solve the original logic puzzle by combining the following
partial results.

ORIGINAL PUZZLE:
{puzzle}

PARTIAL RESULTS:
{partial_answers}

Instructions:
1. Check whether the partial results agree with each other.
2. Apply all five original clues to the proposed code.
3. Correct any inconsistency.
4. Return the final three-digit code.
5. Include a brief verification of all five clues.

Preserve leading zeros.
"""

decomposed_response = ask_model(combine_prompt)

print("\n" + "=" * 70)
print("COMBINED SOLUTION")
print("=" * 70)

print(decomposed_response)


# =========================================================
# PART F: EXTRACT AND VERIFY FINAL ANSWERS
# =========================================================

def extract_code(response):
    if not isinstance(response, str):
        return None

    patterns = [
        r"(?i)(?:final\s+)?(?:secret\s+)?code\s*[:=]\s*`?(\d{3})`?",
        r"(?i)(?:final\s+answer|answer)\s*[:=]\s*`?(\d{3})`?",
        r"(?<!\d)(\d{3})(?!\d)"
    ]

    for pattern in patterns:
        match = re.search(pattern, response)

        if match:
            return match.group(1)

    return None


def verify_code(code):
    if code is None or len(code) != 3:
        return False

    if len(set(code)) != 3:
        return False

    def correct_positions(a, b):
        return sum(x == y for x, y in zip(a, b))

    def common_digits(a, b):
        return len(set(a) & set(b))

    return (
        correct_positions(code, "682") == 1
        and common_digits(code, "682") == 1
        and correct_positions(code, "614") == 0
        and common_digits(code, "614") == 1
        and correct_positions(code, "206") == 0
        and common_digits(code, "206") == 2
        and common_digits(code, "738") == 0
        and correct_positions(code, "780") == 0
        and common_digits(code, "780") == 1
    )


direct_code = extract_code(direct_response)
stepwise_code = extract_code(stepwise_response)
decomposed_code = extract_code(decomposed_response)

direct_correct = verify_code(direct_code)
stepwise_correct = verify_code(stepwise_code)
decomposed_correct = verify_code(decomposed_code)

print("\n" + "=" * 70)
print("INDEPENDENT VERIFICATION")
print("=" * 70)

print("Expected Code  :", expected_answer)
print("Direct Code    :", direct_code)
print("Stepwise Code  :", stepwise_code)
print("Decomposed Code:", decomposed_code)

print("\nDirect Answer Valid    :", direct_correct)
print("Stepwise Answer Valid  :", stepwise_correct)
print("Decomposed Answer Valid:", decomposed_correct)


# =========================================================
# PART G: CALCULATE ACCURACY
# =========================================================

methods = [
    ("Direct Prompt", direct_correct),
    ("Stepwise Prompt", stepwise_correct),
    ("Task Decomposition", decomposed_correct)
]

accuracy_results = pd.DataFrame(
    [
        {
            "Method": name,
            "Correct": int(correct),
            "Total": 1,
            "Accuracy (%)": 100.0 if correct else 0.0
        }
        for name, correct in methods
    ]
)

print("\n" + "=" * 70)
print("ACCURACY COMPARISON")
print("=" * 70)

print(accuracy_results.to_string(index=False))


# =========================================================
# PART H: LABORATORY OBSERVATION TABLE
# =========================================================

observation_table = pd.DataFrame([
    {
        "Method": "Direct Answer",
        "Final Answer": direct_code or "Not extracted",
        "Correct": "Yes" if direct_correct else "No",
        "Explanation": "Solved using a single prompt."
    },
    {
        "Method": "Stepwise Answer",
        "Final Answer": stepwise_code or "Not extracted",
        "Correct": "Yes" if stepwise_correct else "No",
        "Explanation": "Solved using sequential instructions."
    },
    {
        "Method": "Task Decomposition",
        "Final Answer": decomposed_code or "Not extracted",
        "Correct": "Yes" if decomposed_correct else "No",
        "Explanation": "Solved using four subproblems and combined results."
    }
])

print("\n" + "=" * 70)
print("LABORATORY OBSERVATION TABLE")
print("=" * 70)

print(observation_table.to_string(index=False))


# =========================================================
# PART I: FINAL CONCLUSION
# =========================================================

print("\n" + "=" * 70)
print("EXPERIMENT CONCLUSION")
print("=" * 70)

if decomposed_correct and not direct_correct:
    print(
        "Task decomposition solved the puzzle correctly, "
        "while the direct approach did not."
    )
elif direct_correct and decomposed_correct:
    print(
        "Both direct prompting and task decomposition solved "
        "the puzzle correctly. Compare their explanations "
        "and intermediate results."
    )
elif direct_correct:
    print(
        "The direct approach solved the puzzle correctly, "
        "but the decomposed approach requires review."
    )
else:
    print(
        "One or more approaches failed verification. "
        "Inspect the generated responses and refine the prompts."
    )