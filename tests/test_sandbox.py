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
