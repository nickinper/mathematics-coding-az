"""API routes for code execution."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from .database import get_db
from .models import User, Challenge, Submission
from .authentication import get_current_active_user
from src.execution.safe_executor import SafeExecutor, CodeValidator, ExecutionStatus


# Initialize executor globally
executor = SafeExecutor(
    docker_image="mathcoding-executor:latest",
    timeout=5.0,
    memory_limit="256m",
    cpu_limit=0.5
)
code_validator = CodeValidator(executor)


# Pydantic models for API
class CodeExecutionRequest(BaseModel):
    code: str
    test_cases: List[Dict[str, Any]]
    language: str = "python"
    timeout: Optional[float] = None
    memory_limit: Optional[str] = None


class SubmissionExecuteRequest(BaseModel):
    submission_id: int


# Initialize router
execution_router = APIRouter()


@execution_router.post("/execute")
async def execute_code(
    request: CodeExecutionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Execute code in sandboxed environment."""
    try:
        result = await executor.execute_code(
            request.code,
            request.test_cases,
            request.language,
            request.timeout,
            request.memory_limit
        )
        
        return {
            "status": result.status.value,
            "output": result.output,
            "error": result.error,
            "execution_time": result.execution_time,
            "memory_used": result.memory_used,
            "test_results": result.test_results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Execution error: {str(e)}"
        )


@execution_router.post("/validate")
async def validate_code(
    request: CodeExecutionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Validate code for security and execute it."""
    # First, validate the code
    is_valid, error_message = code_validator.validate_code(request.code)
    if not is_valid:
        return {
            "status": "error",
            "message": error_message,
            "is_valid": False
        }
    
    # Execute the code
    result = await executor.execute_code(
        request.code,
        request.test_cases,
        request.language,
        request.timeout,
        request.memory_limit
    )
    
    return {
        "status": result.status.value,
        "output": result.output,
        "error": result.error,
        "execution_time": result.execution_time,
        "memory_used": result.memory_used,
        "test_results": result.test_results,
        "is_valid": True
    }


@execution_router.post("/submissions/{submission_id}/execute")
async def execute_submission(
    submission_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Execute and validate a submission."""
    # Get submission
    submission = db.query(Submission).filter(
        Submission.id == submission_id,
        Submission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Get challenge
    challenge = db.query(Challenge).filter(Challenge.id == submission.challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Execute code
    result = await code_validator.validate_submission(
        submission_id,
        submission.code,
        {
            'test_cases': challenge.test_cases,
            'time_limit': challenge.time_limit,
            'memory_limit': "256m"  # Default
        }
    )
    
    # Update submission with results
    submission.passed = result['status'] == 'success' and result['functional_score'] > 0.8
    submission.functional_score = result['functional_score']
    submission.execution_time = result['execution_time']
    submission.test_results = result['test_results']
    
    # Add execution results to feedback
    if not submission.feedback:
        submission.feedback = {}
    submission.feedback['execution_results'] = {
        'status': result['status'],
        'message': result.get('message', ''),
        'test_results': result['test_results']
    }
    
    db.commit()
    db.refresh(submission)
    
    return {
        "submission_id": submission_id,
        "status": result['status'],
        "passed": submission.passed,
        "functional_score": submission.functional_score,
        "execution_time": submission.execution_time,
        "test_results": submission.test_results,
        "message": result.get('message', '')
    }


@execution_router.get("/metrics")
async def get_execution_metrics(
    current_user: User = Depends(get_current_active_user)
):
    """Get metrics about code execution."""
    # In a production system, this would return real metrics
    return {
        "total_executions": 2048,
        "successful_executions": 1850,
        "failed_executions": 198,
        "average_execution_time": 0.85,
        "average_memory_usage": 45.3,
        "executions_by_hour": [
            {"hour": "00:00", "count": 42},
            {"hour": "01:00", "count": 36},
            {"hour": "02:00", "count": 28},
            # Additional hours...
        ]
    }