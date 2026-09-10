from flask import Flask, request, jsonify, render_template_string
from generator import generate_code
from validator import validate_code

app = Flask(__name__)

# Embed your HTML directly into a string variable
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Codex | AI Code Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-main: #F8FAFC;
            --bg-card: #FFFFFF;
            --bg-header: #0F172A;
            --bg-editor: #F1F5F9;
            --bg-subtle: #F8FAFC;
            --accent-blue: #2563EB;
            --accent-dark-blue: #1D4ED8;
            --border-light: #E2E8F0;
            --border-strong: #CBD5E1;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --text-inverse: #FFFFFF;
            --success-bg: #ECFDF5;
            --success-border: #A7F3D0;
            --success-text: #047857;
            --error-bg: #FEF2F2;
            --error-border: #FECACA;
            --error-text: #B91C1C;
            --radius: 10px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }
        .navbar { background: var(--bg-header); border-bottom: 3px solid var(--accent-blue); padding: 14px 32px; display: flex; justify-content: space-between; align-items: center; }
        .brand { display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 1.2rem; color: var(--text-inverse); }
        .brand-icon { background: rgba(37, 99, 235, 0.2); color: #38BDF8; width: 38px; height: 38px; border-radius: 8px; display: flex; align-items: center; justify-content: center; }
        .container { max-width: 1280px; width: 100%; margin: 24px auto; padding: 0 24px; display: flex; flex-direction: column; gap: 20px; }
        .card { background: var(--bg-card); border: 1px solid var(--border-strong); border-top: 3px solid var(--accent-blue); border-radius: var(--radius); padding: 20px; }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid var(--border-light); }
        .card-title { font-size: 0.95rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }
        .chips-wrapper { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
        .chip { background: var(--bg-editor); color: var(--text-muted); border: 1px solid var(--border-strong); padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; cursor: pointer; }
        .chip:hover { background: var(--accent-blue); color: var(--text-inverse); }
        textarea { width: 100%; background: var(--bg-editor); border: 1px solid var(--border-strong); border-radius: 8px; color: var(--text-main); padding: 14px; font-size: 0.95rem; resize: vertical; outline: none; }
        .btn-blue { background: linear-gradient(135deg, var(--accent-blue), var(--accent-dark-blue)); color: white; border: none; padding: 10px 22px; border-radius: 6px; font-weight: 600; font-size: 0.9rem; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; }
        .btn-outline { background: #FFFFFF; color: var(--text-main); border: 1px solid var(--border-strong); padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }
        .workspace-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .code-box { background-color: var(--bg-editor); border: 1px solid var(--border-strong); border-radius: 8px; overflow: hidden; }
        .code-box-header { background: #E2E8F0; padding: 10px 16px; border-bottom: 1px solid var(--border-strong); font-size: 0.8rem; font-weight: 700; color: var(--accent-blue); display: flex; justify-content: space-between; }
        pre { padding: 16px; font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; line-height: 1.6; color: #0F172A; overflow-x: auto; max-height: 380px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 16px; }
        .metric-card { background: var(--bg-subtle); border: 1px solid var(--border-strong); border-radius: 8px; padding: 12px; display: flex; align-items: center; gap: 12px; }
        .metric-icon { font-size: 1.2rem; color: var(--accent-blue); }
        .console-box { border-radius: 8px; padding: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; min-height: 75px; max-height: 130px; overflow-y: auto; white-space: pre-wrap; margin-top: 6px; border: 1px solid var(--border-strong); }
        .console-stdout { background: var(--success-bg); border-color: var(--success-border); color: var(--success-text); }
        .console-stderr { background: var(--error-bg); border-color: var(--error-border); color: var(--error-text); }
        .console-idle { background: var(--bg-editor); color: var(--text-muted); }
        .text-success { color: var(--success-text) !important; }
        .text-error { color: var(--error-text) !important; }
        .spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.4); border-radius: 50%; border-top-color: #FFF; animation: spin 0.8s linear infinite; display: inline-block; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="brand">
            <div class="brand-icon"><i class="fa-solid fa-book-bookmark"></i></div>
            <span>Python Codex</span>
        </div>
    </nav>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <div class="card-title"><i class="fa-solid fa-scroll" style="color: var(--accent-blue);"></i> Requirement Specification</div>
            </div>
            <div class="chips-wrapper">
                <span class="chip" onclick="setPrompt('Write a function to calculate the factorial of a number.')">Factorial</span>
                <span class="chip" onclick="setPrompt('Generate a Fibonacci sequence function.')">Fibonacci</span>
                <span class="chip" onclick="setPrompt('Create a function to check if a number is prime.')">Prime Check</span>
                <span class="chip" onclick="setPrompt('Write a script to read a CSV file using dictionary reader.')">CSV Reader</span>
            </div>
            <textarea id="requirement" rows="3" placeholder="Describe the Python logic or algorithm..."></textarea>
            <div style="display: flex; justify-content: flex-end; margin-top: 14px;">
                <button class="btn-blue" id="btn-generate" onclick="generateCode()"><i class="fa-solid fa-wand-magic-sparkles"></i> Synthesize Code</button>
            </div>
        </div>
        <div class="workspace-grid">
            <div class="card">
                <div class="card-header">
                    <div class="card-title"><i class="fa-brands fa-python" style="color: var(--accent-blue);"></i> Generated Code Snippet</div>
                    <button class="btn-outline" onclick="copyCode()"><i class="fa-regular fa-copy"></i> Copy</button>
                </div>
                <div class="code-box">
                    <div class="code-box-header">
                        <span>main.py</span>
                        <span id="code-status">Idle</span>
                    </div>
                    <pre><code id="code-output"># Generated Python source code will appear here...</code></pre>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <div class="card-title"><i class="fa-solid fa-microchip" style="color: var(--accent-blue);"></i> Validation & Analytics</div>
                    <button class="btn-outline" onclick="validateCode()"><i class="fa-solid fa-play"></i> Re-Validate</button>
                </div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <i class="fa-solid fa-spell-check metric-icon" id="icon-syntax"></i>
                        <div><strong>Syntax Verification</strong><span id="text-syntax">Pending</span></div>
                    </div>
                    <div class="metric-card">
                        <i class="fa-solid fa-terminal metric-icon" id="icon-exec"></i>
                        <div><strong>Runtime Status</strong><span id="text-exec">Pending</span></div>
                    </div>
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Standard Output (Stdout):</span>
                    <div class="console-box console-idle" id="stdout-box">---</div>
                </div>
                <div>
                    <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Standard Error (Stderr):</span>
                    <div class="console-box console-idle" id="stderr-box">None</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function setPrompt(text) { document.getElementById('requirement').value = text; }
        async function generateCode() {
            const req = document.getElementById('requirement').value.trim();
            if (!req) return alert("Please enter a requirement.");
            const btn = document.getElementById('btn-generate');
            btn.disabled = true;
            btn.innerHTML = `<span class="spinner"></span> Synthesizing...`;
            try {
                const res = await fetch('/api/generate', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ requirement: req }) });
                const data = await res.json();
                if (res.ok && data.code) {
                    document.getElementById('code-output').textContent = data.code;
                    document.getElementById('code-status').textContent = "Generated";
                    await validateCode();
                }
            } catch (e) {}
            btn.disabled = false;
            btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Synthesize Code`;
        }
        async function validateCode() {
            const code = document.getElementById('code-output').textContent;
            if (!code || code.startsWith('#')) return;
            try {
                const res = await fetch('/api/validate', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ code }) });
                const data = await res.json();
                if (res.ok) {
                    document.getElementById('stdout-box').textContent = data.stdout || '(No output)';
                    document.getElementById('stderr-box').textContent = data.stderr || 'None';
                    document.getElementById('text-syntax').textContent = data.syntax_valid ? "Passed" : "Error";
                    document.getElementById('text-exec').textContent = data.execution_success ? "Success" : "Failed";
                }
            } catch (e) {}
        }
        function copyCode() {
            navigator.clipboard.writeText(document.getElementById('code-output').textContent).then(() => alert("Copied!"));
        }
    </script>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(HTML_TEMPLATE)

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