import os


def generate_code(requirement: str) -> str:
    """
    Generate Python code from a natural-language requirement.
    Uses OpenAI when an API key is available.
    Otherwise, uses a simple offline generator.
    """

    requirement = requirement.strip()

    if not requirement:
        raise ValueError("Requirement cannot be empty.")

    if os.getenv("OPENAI_API_KEY"):
        return _openai_generate(requirement)


    return _offline_generate(requirement)


def _offline_generate(requirement: str) -> str:
    """
    Simple offline fallback generator.
    """

    r = requirement.lower()

    if "factorial" in r:
        return """def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    print(factorial(5))
"""

    if "fibonacci" in r:
        return """def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1
    result = []

    for _ in range(n):
        result.append(a)
        a, b = b, a + b

    return result


if __name__ == "__main__":
    print(fibonacci(10))
"""

    if "prime" in r:
        return """def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


if __name__ == "__main__":
    print(is_prime(17))
"""

    if "csv" in r:
        return """import csv


def read_csv_file(filename):
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


if __name__ == "__main__":
    print("CSV reader ready.")
"""

    if "flask" in r or "api" in r:
        return """from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({"message": "Hello, world!"})


if __name__ == "__main__":
    app.run(debug=True)
"""

    return f'''def solution():
    """Generated from this requirement:
    {requirement}
    """
    # TODO: implement the requested logic.
    pass


if __name__ == "__main__":
    solution()
'''


def _openai_generate(requirement: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

    prompt = f"""
Generate a complete executable Python solution for this software requirement:

{requirement}

Rules:
- Return ONLY Python code.
- Do not use Markdown code fences.
- Make the code executable.
- Include a small example/test in the main block when appropriate.
"""

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text.strip()