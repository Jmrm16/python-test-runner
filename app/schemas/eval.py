from typing import Optional
from pydantic import BaseModel, Field


class EvalRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Candidate Python solution code")
    tests: str = Field(..., min_length=1, description="Pytest test cases validating the code")
    timeout_seconds: Optional[float] = Field(5.0, ge=0.5, le=15.0, description="Max runtime limit")


class EvalResponse(BaseModel):
    passed: bool
    exit_code: int
    duration_ms: float
    stdout: str
    stderr: str
    timed_out: bool
