import os
import sys
import tempfile
import subprocess
import time
from typing import Dict, Any

class ExecutionTimeoutError(Exception):
    """Raised when the sandboxed process exceeds the maximum allowed time."""

class CodeSandboxRunner:
    """Executes Python code in an isolated subprocess sandbox."""
    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout_seconds = timeout_seconds

    def evaluate(self, candidate_code: str, test_suite: str) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="sandbox_run_") as tmpdir:
            solution_file = os.path.join(tmpdir, "solution.py")
            test_file = os.path.join(tmpdir, "test_solution.py")

            with open(solution_file, "w", encoding="utf-8") as f:
                f.write(candidate_code)

            with open(test_file, "w", encoding="utf-8") as f:
                f.write("from solution import *\n\n" + test_suite)

            cmd = [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short", "-p", "no:cacheprovider"]
            try:
                proc = subprocess.run(cmd, cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=self.timeout_seconds)
                return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "timed_out": False}
            except subprocess.TimeoutExpired as exc:
                return {"passed": False, "exit_code": -1, "stdout": exc.stdout if exc.stdout else "", "stderr": f"Execution exceeded maximum timeout of {self.timeout_seconds}s.", "timed_out": True}
