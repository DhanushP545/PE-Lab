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


# ---------------------------------------------------------
# CRICKET COMMENTARY TEST DATA
# ---------------------------------------------------------

test_data = [
    ("What a magnificent cover drive, that raced away to the boundary.", "Positive"),
    ("The batsman completely missed the ball and was bowled.", "Negative"),
    ("The next over will begin with the spinner bowling from the other end.", "Neutral"),
    ("Brilliant catch at slip to dismiss the dangerous batsman.", "Positive"),
    ("That was a terrible shot and the batsman has thrown his wicket away.", "Negative"),
    ("The scoreboard shows 145 runs for the loss of four wickets.", "Neutral"),
    ("An outstanding yorker under pressure, perfectly executed by the bowler.", "Positive"),
    ("The fielder dropped a simple catch and gave the batsman another chance.", "Negative"),
    ("The captain has decided to take the new ball.", "Neutral"),
    ("What an incredible innings from the opener, who has reached a brilliant century.", "Positive")
]


# ---------------------------------------------------------
# RANDOMLY SELECT 5 SAMPLES
# ---------------------------------------------------------

random.seed()   # Different samples each time

selected_data = random.sample(test_data, 5)

print("\nSelected 5 Random Cricket Commentaries:")
print("=" * 60)

for i, (sentence, expected) in enumerate(selected_data, start=1):
    print(f"T{i}: {sentence}")
    print(f"Expected: {expected}")
    print()


# ---------------------------------------------------------
# ZERO-SHOT CLASSIFICATION
# ---------------------------------------------------------

def zero_shot(sentence):

    # Intentionally less detailed zero-shot instruction.
    # No examples are provided.
    prompt = f"""
Classify the following cricket commentary into one of these
three categories:

Positive, Negative, or Neutral.

Judge the overall tone of the commentary. A statement about
a cricket event may sometimes be considered Neutral even if
the event is good or bad.

Commentary:
{sentence}

Return only one category name.
"""

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


# ---------------------------------------------------------
# FEW-SHOT CLASSIFICATION
# ---------------------------------------------------------

def few_shot(sentence):

    prompt = f"""
Classify the sentiment of the cricket commentary as exactly
one of these labels:

Positive
Negative
Neutral

Use the following examples as a guide.

Example 1:
Commentary: What a fantastic shot, straight through the covers!
Label: Positive

Example 2:
Commentary: The batsman played a terrible shot and lost his wicket.
Label: Negative

Example 3:
Commentary: The next over will be bowled by the spinner.
Label: Neutral

These examples show that praise or excitement is Positive,
poor performance or disappointment is Negative, and factual
information without clear emotion is Neutral.

Now classify the following commentary:

Commentary:
{sentence}

Return only the label.
"""

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


# ---------------------------------------------------------
# ZERO-SHOT RESULTS
# ---------------------------------------------------------

print("\n")
print("=" * 60)
print("ZERO-SHOT CLASSIFICATION")
print("=" * 60)

zero_results = []

for i, (sentence, expected) in enumerate(selected_data, start=1):

    prediction = zero_shot(sentence)

    zero_results.append(
        (sentence, expected, prediction)
    )

    print(f"\nT{i}")
    print("Commentary :", sentence)
    print("Expected   :", expected)
    print("Prediction :", prediction)


# ---------------------------------------------------------
# FEW-SHOT RESULTS
# ---------------------------------------------------------

print("\n")
print("=" * 60)
print("FEW-SHOT CLASSIFICATION")
print("=" * 60)

few_results = []

for i, (sentence, expected) in enumerate(selected_data, start=1):

    prediction = few_shot(sentence)

    few_results.append(
        (sentence, expected, prediction)
    )

    print(f"\nT{i}")
    print("Commentary :", sentence)
    print("Expected   :", expected)
    print("Prediction :", prediction)


# ---------------------------------------------------------
# CALCULATE ACCURACY
# ---------------------------------------------------------

zero_correct = sum(
    1
    for _, expected, prediction in zero_results
    if prediction.lower() == expected.lower()
)

few_correct = sum(
    1
    for _, expected, prediction in few_results
    if prediction.lower() == expected.lower()
)

zero_accuracy = (zero_correct / 5) * 100
few_accuracy = (few_correct / 5) * 100

improvement = few_accuracy - zero_accuracy


# ---------------------------------------------------------
# FINAL RESULTS
# ---------------------------------------------------------

print("\n")
print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(f"Zero-Shot Correct : {zero_correct}/5")
print(f"Zero-Shot Accuracy: {zero_accuracy:.2f}%")

print()

print(f"Few-Shot Correct  : {few_correct}/5")
print(f"Few-Shot Accuracy : {few_accuracy:.2f}%")

print()

print(f"Improvement       : {improvement:.2f}%")