from app.sandbox.runner import CodeSandboxRunner


def test_sandbox_evaluates_valid_code_successfully():
    runner = CodeSandboxRunner(timeout_seconds=5.0)
    code = """
def add(a, b):
    return a + b
"""
    tests = """
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2
"""
    result = runner.evaluate(code, tests)
    assert result["passed"] is True
    assert result["exit_code"] == 0
    assert result["timed_out"] is False
    assert "PASSED" in result["stdout"]


def test_sandbox_detects_test_failures():
    runner = CodeSandboxRunner(timeout_seconds=5.0)
    code = """
def multiply(a, b):
    return a + b  # Bug: addition instead of multiplication
"""
    tests = """
def test_multiply():
    assert multiply(2, 4) == 8
"""
    result = runner.evaluate(code, tests)
    assert result["passed"] is False
    assert result["exit_code"] != 0
    assert "FAILED" in result["stdout"]


def test_sandbox_terminates_infinite_loops():
    runner = CodeSandboxRunner(timeout_seconds=1.5)
    code = """
import time

def infinite():
    while True:
        time.sleep(0.1)
"""
    tests = """
def test_infinite():
    infinite()
"""
    result = runner.evaluate(code, tests)
    assert result["passed"] is False
    assert result["timed_out"] is True
    assert "exceeded maximum timeout" in result["stderr"]
