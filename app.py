from flask import Flask, render_template, request, jsonify
from generator import generate_code
from validator import validate_code

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/generate")
def api_generate():
    data = request.get_json(silent=True) or {}
    requirement = (data.get("requirement") or "").strip()
    if not requirement:
        return jsonify({"error": "Please enter a requirement."}), 400
    try:
        code = generate_code(requirement)
        return jsonify({"code": code})
    except Exception as exc:
        return jsonify({"error": "Generation failed.", "details": str(exc)}), 500

@app.post("/api/validate")
def api_validate():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")
    if not isinstance(code, str) or not code.strip():
        return jsonify({"error": "No Python code was supplied."}), 400
    try:
        return jsonify(validate_code(code))
    except Exception as exc:
        return jsonify({"error": "Validation failed.", "details": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
