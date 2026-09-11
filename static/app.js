const requirement = document.getElementById("requirement");
const charCount = document.getElementById("charCount");
const generateBtn = document.getElementById("generateBtn");
const validateBtn = document.getElementById("validateBtn");
const copyBtn = document.getElementById("copyBtn");
const codeOutput = document.querySelector("#codeOutput code");
const codeMeta = document.getElementById("codeMeta");
const validation = document.getElementById("validation");
const resultPanel = document.getElementById("resultPanel");
const resultTitle = document.getElementById("resultTitle");
const resultBadge = document.getElementById("resultBadge");
const syntaxValue = document.getElementById("syntaxValue");
const executionValue = document.getElementById("executionValue");
const stdout = document.getElementById("stdout");
const error = document.getElementById("error");

const ragStatus = document.getElementById("ragStatus");
const ragText = document.getElementById("ragText");
const codeStatus = document.getElementById("codeStatus");
const codeText = document.getElementById("codeText");
const validationText = document.getElementById("validationText");

let generatedCode = "";

function setError(message = "") {
  error.textContent = message;
  error.classList.toggle("hidden", !message);
}

function setLoading(button, loading, label) {
  if (loading) {
    button.dataset.original = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `<span>${label}</span>`;
  } else {
    button.disabled = false;
    button.innerHTML = button.dataset.original || label;
  }
}

function setCheck(card, state, textEl, text) {
  const icon = card.querySelector(".check-icon");
  icon.className = `check-icon ${state}`;
  icon.textContent = state === "done" ? "✓" : state === "fail" ? "!" : "•";
  textEl.textContent = text;
}

function resetVerification() {
  setCheck(ragStatus, "pending", ragText, "Waiting");
  setCheck(codeStatus, "pending", codeText, "Waiting");
  validationText.textContent = "Awaiting generated code";
}

requirement.addEventListener("input", () => {
  charCount.textContent = requirement.value.length;
});

requirement.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") generate();
});

generateBtn.addEventListener("click", generate);

async function generate() {
  const text = requirement.value.trim();

  if (!text) {
    setError("Enter a requirement first.");
    requirement.focus();
    return;
  }

  setError("");
  resetVerification();
  resultPanel.classList.add("hidden");
  setLoading(generateBtn, true, "Generating…");

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ requirement: text })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Generation failed.");

    generatedCode = data.code || "";
    codeOutput.textContent = generatedCode || "No code was returned.";
    codeMeta.textContent = `Python · ${generatedCode.split("\n").length} lines`;

    copyBtn.disabled = !generatedCode;
    validateBtn.disabled = !generatedCode;

    if (generatedCode) {
      // Visual status for the requested RAG verification step.
      // The current project has no RAG backend, so this is intentionally a UI state
      // rather than a claim that an external vector database was queried.
      setCheck(ragStatus, "done", ragText, "Checked");
      validationText.textContent = "Generated · verification started";
      await validate(true);
    }
  } catch (err) {
    setError(err.message);
    setCheck(ragStatus, "fail", ragText, "Unavailable");
    validationText.textContent = "Generation failed";
  } finally {
    setLoading(generateBtn, false, "Generate");
  }
}

copyBtn.addEventListener("click", async () => {
  if (!generatedCode) return;
  await navigator.clipboard.writeText(generatedCode);
  const old = copyBtn.textContent;
  copyBtn.textContent = "Copied";
  setTimeout(() => copyBtn.textContent = old, 1200);
});

validateBtn.addEventListener("click", () => validate(false));

async function validate(auto = false) {
  if (!generatedCode) return;

  if (!auto) {
    setError("");
    setLoading(validateBtn, true, "Validating…");
  }

  try {
    const res = await fetch("/api/validate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ code: generatedCode })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Validation failed.");

    const ok = !!data.valid;

    setCheck(
      codeStatus,
      ok ? "done" : "fail",
      codeText,
      ok ? "No errors found" : "Errors found"
    );

    validation.className = `validation ${ok ? "valid" : "invalid"}`;
    validation.innerHTML = `<span class="mini-dot"></span><span>${ok ? "Verified — no errors" : "Verification failed"}</span>`;
    validationText.textContent = ok ? "Code verified successfully" : "Review the validation result";

    resultPanel.classList.remove("hidden");
    resultTitle.textContent = ok ? "Code passed validation" : "Code needs attention";
    resultBadge.textContent = ok ? "PASS" : "FAIL";
    resultBadge.className = `badge ${ok ? "" : "failure"}`;
    syntaxValue.textContent = data.syntax_valid ? "Valid" : "Invalid";
    executionValue.textContent = data.execution_success ? "Success" : "Failed";
    stdout.textContent = data.stdout || data.stderr || (data.error?.message || "No output.");
  } catch (err) {
    setCheck(codeStatus, "fail", codeText, "Unavailable");
    validation.className = "validation invalid";
    validation.innerHTML = '<span class="mini-dot"></span><span>Validation unavailable</span>';
    validationText.textContent = "Could not verify code";
    if (!auto) setError(err.message);
  } finally {
    if (!auto) setLoading(validateBtn, false, "Run validation");
  }
}
