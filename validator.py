import ast
import os
import subprocess
import sys
import tempfile


def check_syntax(code):
    try:
        ast.parse(code)
        return {"syntax_valid": True, "error": None}
    except SyntaxError as exc:
        return {
            "syntax_valid": False,
            "error": {
                "type": "SyntaxError",
                "message": exc.msg,
                "line": exc.lineno,
                "column": exc.offset
            }
        }


def run_code(code, timeout=3):
    syntax = check_syntax(code)

    if not syntax["syntax_valid"]:
        return {
            "valid": False,
            "syntax_valid": False,
            "execution_success": False,
            "stdout": "",
            "stderr": "",
            "error": syntax["error"]
        }

    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as file:
            file.write(code)
            temp_file = file.name

        result = subprocess.run(
            [sys.executable, "-I", temp_file],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            return {
                "valid": True,
                "syntax_valid": True,
                "execution_success": True,
                "stdout": result.stdout[:5000],
                "stderr": result.stderr[:5000],
                "error": None
            }

        return {
            "valid": False,
            "syntax_valid": True,
            "execution_success": False,
            "stdout": result.stdout[:5000],
            "stderr": result.stderr[:5000],
            "error": {
                "type": "RuntimeError",
                "message": result.stderr[:2000]
            }
        }

    except subprocess.TimeoutExpired:
        return {
            "valid": False,
            "syntax_valid": True,
            "execution_success": False,
            "stdout": "",
            "stderr": "",
            "error": {
                "type": "TimeoutError",
                "message": "Code exceeded the 3-second execution limit."
            }
        }
    except Exception as exc:
        return {
            "valid": False,
            "syntax_valid": True,
            "execution_success": False,
            "stdout": "",
            "stderr": "",
            "error": {"type": type(exc).__name__, "message": str(exc)}
        }
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def validate_code(code):
    return run_code(code)
