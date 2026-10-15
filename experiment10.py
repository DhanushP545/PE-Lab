import os
import json
import yaml
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
# PART A: DATASET AND BASIC JSON GENERATION
# =========================================================

dataset = {
    "student_name": "Rahul",
    "department": "Computer Science",
    "courses": [
        {"course_name": "Python", "credits": 4, "status": "Completed"},
        {"course_name": "Database Systems", "credits": 3, "status": "In Progress"},
        {"course_name": "Machine Learning", "credits": 4, "status": "Pending"}
    ]
}

basic_prompt = f"""
Convert the following student information into valid JSON.

Student information:
{json.dumps(dataset, indent=2)}

Return only a JSON object with these keys:
student_name, department, courses.

Each course must contain:
course_name, credits, status.

Do not include Markdown fences or explanations.
"""

json_response = ask_model(basic_prompt)

print("\n" + "=" * 70)
print("BASIC JSON GENERATION")
print("=" * 70)
print(json_response)


# =========================================================
# PART B: JSON SYNTAX VALIDATION
# =========================================================

def parse_json(response):
    response = response.strip()

    if response.startswith("```"):
        lines = response.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response = "\n".join(lines).strip()

    return json.loads(response)


def validate_json_structure(data):
    if not isinstance(data, dict):
        return False

    if not all(key in data for key in
               ["student_name", "department", "courses"]):
        return False

    if not isinstance(data["student_name"], str):
        return False

    if not isinstance(data["department"], str):
        return False

    if not isinstance(data["courses"], list):
        return False

    for course in data["courses"]:
        if not isinstance(course, dict):
            return False

        if not all(key in course for key in
                   ["course_name", "credits", "status"]):
            return False

        if not isinstance(course["course_name"], str):
            return False

        if not isinstance(course["credits"], int) or isinstance(
            course["credits"], bool
        ):
            return False

        if not isinstance(course["status"], str):
            return False

    return True


try:
    json_data = parse_json(json_response)
    json_syntax_valid = True
except (json.JSONDecodeError, ValueError):
    json_data = None
    json_syntax_valid = False

print("\n" + "=" * 70)
print("JSON SYNTAX VALIDATION")
print("=" * 70)
print("JSON Syntax:", "PASS" if json_syntax_valid else "FAIL")


# =========================================================
# PART C: JSON STRUCTURE VALIDATION
# =========================================================

json_structure_valid = (
    validate_json_structure(json_data)
    if json_syntax_valid else False
)

print("\n" + "=" * 70)
print("JSON STRUCTURE VALIDATION")
print("=" * 70)
print("JSON Structure:",
      "PASS" if json_structure_valid else "FAIL")


# =========================================================
# PART D: REFINE PROMPT IF VALIDATION FAILS
# =========================================================

refined_response = None

if not json_syntax_valid or not json_structure_valid:

    print("\nJSON validation failed. Refining the prompt...")

    refined_prompt = f"""
Convert the following information into valid JSON.

Information:
{json.dumps(dataset, indent=2)}

STRICT REQUIREMENTS:
1. Return exactly one JSON object.
2. Use double quotes for all keys and string values.
3. Use the keys student_name, department, and courses.
4. Each course must contain course_name, credits, and status.
5. credits must be an integer.
6. courses must be a JSON array.
7. Do not include comments, trailing commas, Markdown fences,
   or explanations.
8. Ensure that the output can be parsed using Python json.loads().

Return only the JSON object.
"""

    refined_response = ask_model(refined_prompt)

    print("\n" + "=" * 70)
    print("REFINED JSON RESPONSE")
    print("=" * 70)
    print(refined_response)

    try:
        json_data = parse_json(refined_response)
        json_syntax_valid = True
    except (json.JSONDecodeError, ValueError):
        json_data = None
        json_syntax_valid = False

    json_structure_valid = (
        validate_json_structure(json_data)
        if json_syntax_valid else False
    )

    print("\nRefined JSON Syntax:",
          "PASS" if json_syntax_valid else "FAIL")

    print("Refined JSON Structure:",
          "PASS" if json_structure_valid else "FAIL")


# =========================================================
# PART E: GENERATE YAML
# =========================================================

yaml_data = None
yaml_response = None
yaml_syntax_valid = False
yaml_structure_valid = False
formats_match = False

if json_syntax_valid and json_structure_valid:

    yaml_response = yaml.safe_dump(
        json_data,
        sort_keys=False,
        allow_unicode=True
    )

    print("\n" + "=" * 70)
    print("GENERATED YAML")
    print("=" * 70)
    print(yaml_response)

    # =====================================================
    # PART F: YAML SYNTAX VALIDATION
    # =====================================================

    try:
        yaml_data = yaml.safe_load(yaml_response)
        yaml_syntax_valid = True
    except yaml.YAMLError:
        yaml_syntax_valid = False

    print("\n" + "=" * 70)
    print("YAML SYNTAX VALIDATION")
    print("=" * 70)
    print("YAML Syntax:",
          "PASS" if yaml_syntax_valid else "FAIL")

    # =====================================================
    # PART G: YAML STRUCTURE VALIDATION
    # =====================================================

    yaml_structure_valid = (
        validate_json_structure(yaml_data)
        if yaml_syntax_valid else False
    )

    print("\n" + "=" * 70)
    print("YAML STRUCTURE VALIDATION")
    print("=" * 70)
    print("YAML Structure:",
          "PASS" if yaml_structure_valid else "FAIL")

    # =====================================================
    # PART H: COMPARE JSON AND YAML
    # =====================================================

    formats_match = (
        json_data == yaml_data
        if yaml_syntax_valid else False
    )

    print("\n" + "=" * 70)
    print("JSON VS YAML COMPARISON")
    print("=" * 70)
    print("JSON and YAML represent the same data:",
          "PASS" if formats_match else "FAIL")

else:
    print("\nJSON is invalid. YAML generation skipped.")


# =========================================================
# PART I: RECORD RESULTS
# =========================================================

results = {
    "JSON Syntax": "PASS" if json_syntax_valid else "FAIL",
    "JSON Structure": "PASS" if json_structure_valid else "FAIL",
    "YAML Syntax": "PASS" if yaml_syntax_valid else "FAIL",
    "YAML Structure": "PASS" if yaml_structure_valid else "FAIL",
    "JSON-YAML Match": "PASS" if formats_match else "FAIL"
}

print("\n" + "=" * 70)
print("EXPERIMENT RESULTS")
print("=" * 70)

for criterion, result in results.items():
    print(f"{criterion:25}: {result}")


# =========================================================
# PART J: SAVE OUTPUTS
# =========================================================

if json_syntax_valid and json_structure_valid:
    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

    print("\nSaved: output.json")

if yaml_syntax_valid and yaml_structure_valid:
    with open("output.yaml", "w", encoding="utf-8") as file:
        file.write(yaml_response)

    print("Saved: output.yaml")


# =========================================================
# PART K: CONCLUSION
# =========================================================

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

if (
    json_syntax_valid
    and json_structure_valid
    and yaml_syntax_valid
    and yaml_structure_valid
    and formats_match
):
    print(
        "Structured data was generated and validated successfully. "
        "JSON and YAML represent equivalent data."
    )
else:
    print(
        "One or more validation checks failed. "
        "Review the results and refine the prompt if necessary."
    )