"""Tests for the execution API."""

import pytest
import os
import sys
import json
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.execution.safe_executor import ExecutionStatus, ExecutionResult
from src.platform.server import app


client = TestClient(app)


@pytest.fixture
def mock_current_user():
    """Fixture for mocking the current user dependency."""
    with patch("src.platform.authentication.get_current_active_user", autospec=True) as mock:
        mock.return_value = MagicMock(id=1, username="test_user")
        yield mock


@pytest.fixture
def mock_executor():
    """Fixture for mocking the SafeExecutor."""
    with patch("src.platform.execution_api.executor", autospec=True) as mock:
        yield mock


def test_execute_code_endpoint_success(mock_current_user, mock_executor):
    """Test the execute code endpoint with successful execution."""
    # Mock the execute_code method
    mock_result = ExecutionResult(
        status=ExecutionStatus.SUCCESS,
        output="",
        error="",
        execution_time=0.5,
        memory_used=10.5,
        test_results={"total": 2, "passed": 2, "failed": 0, "details": []}
    )
    mock_executor.execute_code = AsyncMock(return_value=mock_result)
    
    # Define test data
    test_data = {
        "code": "def add(a, b): return a + b",
        "test_cases": [
            {"input": {"a": 2, "b": 3}, "expected_output": 5, "function": "add"},
            {"input": {"a": -1, "b": 1}, "expected_output": 0, "function": "add"}
        ],
        "language": "python"
    }
    
    # Make the request
    response = client.post(
        "/api/execution/execute",
        json=test_data,
        headers={"Authorization": "Bearer test_token"}
    )
    
    # Check the response
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["test_results"] == {"total": 2, "passed": 2, "failed": 0, "details": []}


def test_execute_code_endpoint_error(mock_current_user, mock_executor):
    """Test the execute code endpoint with execution error."""
    # Mock the execute_code method
    mock_result = ExecutionResult(
        status=ExecutionStatus.ERROR,
        output="",
        error="NameError: name 'undefined_var' is not defined",
        execution_time=0.2,
        memory_used=5.2,
        test_results={"total": 1, "passed": 0, "failed": 1, "details": []}
    )
    mock_executor.execute_code = AsyncMock(return_value=mock_result)
    
    # Define test data
    test_data = {
        "code": "def broken_function(): return undefined_var",
        "test_cases": [
            {"input": {}, "expected_output": None, "function": "broken_function"}
        ],
        "language": "python"
    }
    
    # Make the request
    response = client.post(
        "/api/execution/execute",
        json=test_data,
        headers={"Authorization": "Bearer test_token"}
    )
    
    # Check the response
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert "NameError" in response.json()["error"]


def test_validate_code_endpoint_valid(mock_current_user, mock_executor):
    """Test the validate code endpoint with valid code."""
    # Mock the validate_code method
    code_validator = MagicMock()
    code_validator.validate_code.return_value = (True, "")
    mock_executor.execute_code = AsyncMock(return_value=ExecutionResult(
        status=ExecutionStatus.SUCCESS,
        output="",
        error="",
        execution_time=0.3,
        memory_used=8.7,
        test_results={"total": 1, "passed": 1, "failed": 0, "details": []}
    ))
    
    with patch("src.platform.execution_api.code_validator", code_validator):
        # Define test data
        test_data = {
            "code": "def add(a, b): return a + b",
            "test_cases": [
                {"input": {"a": 2, "b": 3}, "expected_output": 5, "function": "add"}
            ],
            "language": "python"
        }
        
        # Make the request
        response = client.post(
            "/api/execution/validate",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Check the response
        assert response.status_code == 200
        assert response.json()["is_valid"] is True
        assert response.json()["status"] == "success"


def test_validate_code_endpoint_invalid(mock_current_user):
    """Test the validate code endpoint with invalid code."""
    # Mock the validate_code method
    code_validator = MagicMock()
    code_validator.validate_code.return_value = (
        False, 
        "Security violation: Disallowed imports: os"
    )
    
    with patch("src.platform.execution_api.code_validator", code_validator):
        # Define test data
        test_data = {
            "code": "import os\ndef dangerous(): return os.system('rm -rf /')",
            "test_cases": [],
            "language": "python"
        }
        
        # Make the request
        response = client.post(
            "/api/execution/validate",
            json=test_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Check the response
        assert response.status_code == 200
        assert response.json()["is_valid"] is False
        assert "Security violation" in response.json()["message"]


def test_execute_submission_endpoint(mock_current_user):
    """Test the execute submission endpoint."""
    # Mock the database session
    db_session = MagicMock()
    
    # Mock the get_db dependency
    with patch("src.platform.execution_api.get_db", return_value=db_session):
        # Mock the submission and challenge
        submission = MagicMock(
            id=1,
            user_id=1,
            challenge_id=1,
            code="def add(a, b): return a + b",
            feedback={}
        )
        challenge = MagicMock(
            id=1,
            test_cases=[
                {"input": {"a": 2, "b": 3}, "expected_output": 5, "function": "add"}
            ],
            time_limit=5.0
        )
        
        # Mock the database query results
        db_session.query.return_value.filter.return_value.first.side_effect = [
            submission,  # First call for submission
            challenge    # Second call for challenge
        ]
        
        # Mock the validate_submission method
        code_validator = MagicMock()
        code_validator.validate_submission = AsyncMock(return_value={
            "status": "success",
            "functional_score": 1.0,
            "execution_time": 0.3,
            "test_results": {"total": 1, "passed": 1, "failed": 0}
        })
        
        with patch("src.platform.execution_api.code_validator", code_validator):
            # Make the request
            response = client.post(
                f"/api/execution/submissions/1/execute",
                headers={"Authorization": "Bearer test_token"}
            )
            
            # Check the response
            assert response.status_code == 200
            assert response.json()["status"] == "success"
            assert response.json()["functional_score"] == 1.0
            assert "execution_time" in response.json()
            
            # Verify submission was updated
            assert submission.passed is True
            assert submission.functional_score == 1.0
            assert "execution_results" in submission.feedback


def test_execution_metrics_endpoint(mock_current_user):
    """Test the execution metrics endpoint."""
    # Make the request
    response = client.get(
        "/api/execution/metrics",
        headers={"Authorization": "Bearer test_token"}
    )
    
    # Check the response
    assert response.status_code == 200
    assert "total_executions" in response.json()
    assert "successful_executions" in response.json()
    assert "average_execution_time" in response.json()


if __name__ == "__main__":
    pytest.main(["-v", __file__])