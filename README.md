# TCS AI Python Code Generator

A full-stack prototype for the TCS Technology Day problem statement:
natural-language requirement -> Python code -> syntax/runtime validation -> result.

## Run in VS Code

1. Open this extracted folder in VS Code.
2. Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install packages:

```powershell
pip install -r requirements.txt
```

4. Start:

```powershell
python app.py
```

5. Open http://127.0.0.1:5000

## GenAI mode

The app works immediately without an API key using its built-in offline generator.
For real LLM generation, set an API key in your environment:

```powershell
$env:OPENAI_API_KEY="your-key-here"
$env:OPENAI_MODEL="gpt-5.6-luna"
```

The app uses the OpenAI Responses API when the key is present.

## Tests

```powershell
pytest
```

## API

Generate:
`POST /api/generate`

```json
{"requirement":"Create a Python function that checks if a number is prime."}
```

Validate:
`POST /api/validate`

```json
{"code":"print('hello')"}
```

## Security note

The subprocess runner and timeout are suitable for a demo/prototype, not for executing hostile arbitrary code in production. A production service should use a properly isolated container/VM with network disabled, non-root execution, read-only filesystem, resource limits and OS-level security controls.
