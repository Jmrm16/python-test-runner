from fastapi import APIRouter, HTTPException, status
from app.schemas.eval import EvalRequest, EvalResponse
from app.sandbox.runner import CodeSandboxRunner
from app.config import settings

router = APIRouter(prefix="/eval", tags=["Code Evaluation"])


@router.post("/", response_model=EvalResponse, status_code=status.HTTP_200_OK)
def evaluate_submission(payload: EvalRequest):
    """
    Submits candidate code and pytest assertions to an isolated execution sandbox.
    Returns test execution results, execution duration, and failure diagnostics.
    """
    if len(payload.code.encode("utf-8")) > settings.MAX_CODE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Code payload exceeds max size limit of {settings.MAX_CODE_SIZE_BYTES} bytes."
        )

    timeout = payload.timeout_seconds or settings.DEFAULT_TIMEOUT_SECONDS
    runner = CodeSandboxRunner(timeout_seconds=timeout)
    result = runner.evaluate(payload.code, payload.tests)
    return result
