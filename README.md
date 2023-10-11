# Python Test Runner API

An isolated code execution and test evaluation microservice built with **Python 3.11** and **FastAPI**.

Designed for automated grading, LLM code benchmark evaluations (e.g. SWE-bench tasks), and dynamic assertion verification within ephemeral process sandboxes.

---

## 🌟 Key Features

- **Ephemeral Sandboxed Execution:** Each candidate submission is evaluated inside a dedicated temporary workspace and executed via isolated subprocesses.
- **Strict Timeout Enforcement:** Protects against infinite loops, blocking I/O, and CPU starvation through configurable subprocess deadlines (`timeout_seconds`).
- **Structured Pytest Reporting:** Captures standard output, standard error, execution duration in milliseconds, and exit status codes.
- **Payload Size Guards:** Rejects malicious or oversized payloads before execution via Pydantic schema validation.

---

## 🛠️ Architecture

```text
python-test-runner/
├── app/
│   ├── api/             # REST endpoints (POST /api/v1/eval/)
│   ├── sandbox/         # Subprocess runner, timeout monitors, and isolation
│   ├── schemas/         # Pydantic v2 DTOs (EvalRequest, EvalResponse)
│   ├── config.py        # Settings and limit configurations
│   └── main.py          # FastAPI application factory
├── tests/               # Pytest suite validating execution, failures, and timeouts
├── Dockerfile           # Minimal Python 3.11 slim image
└── requirements.txt
```

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/Jmrm16/python-test-runner.git
cd python-test-runner
pip install -r requirements.txt
```

### 2. Run the Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive documentation is available at `http://localhost:8000/docs`.

### 3. Example API Request

```bash
curl -X POST "http://localhost:8000/api/v1/eval/" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1: return n\n    return fibonacci(n-1) + fibonacci(n-2)\n",
    "tests": "def test_fib():\n    assert fibonacci(5) == 5\n    assert fibonacci(6) == 8\n",
    "timeout_seconds": 3.0
  }'
```

*Response:*
```json
{
  "passed": true,
  "exit_code": 0,
  "duration_ms": 142.3,
  "stdout": "test_solution.py::test_fib PASSED [100%]\n",
  "stderr": "",
  "timed_out": false
}
```

---

## 🧪 Testing

```bash
pytest -v
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

