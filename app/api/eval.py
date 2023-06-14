from fastapi import APIRouter, HTTPException, status
from app.schemas.eval import EvalRequest, EvalResponse
from app.sandbox.runner import CodeSandboxRunner
from app.config import settings

router = APIRouter(prefix="/eval", tags=["Code Evaluation"])

@router.post("/", response_model=EvalResponse, status_code=status.HTTP_200_OK)
def evaluate_submission(payload: EvalRequest):
    timeout = payload.timeout_seconds or settings.DEFAULT_TIMEOUT_SECONDS
    runner = CodeSandboxRunner(timeout_seconds=timeout)
    return runner.evaluate(payload.code, payload.tests)
