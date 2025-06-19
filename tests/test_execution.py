"""Tests for the safe execution engine."""

import pytest
import asyncio
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.execution.safe_executor import SafeExecutor, ExecutionStatus, ExecutionResult
from src.execution.security import CodeSanitizer, ResourceMonitor


class MockContainer:
    """Mock Docker container for testing."""
    
    def __init__(self, exit_code=0, logs=""):
        self.exit_code = exit_code
        self.logs_data = logs.encode('utf-8')
    
    def wait(self):
        """Mock container wait method."""
        return {"StatusCode": self.exit_code}
    
    def logs(self):
        """Mock container logs method."""
        return self.logs_data
    
    def kill(self):
        """Mock container kill method."""
        pass


class MockDockerClient:
    """Mock Docker client for testing."""
    
    def __init__(self, container=None):
        self.container = container or MockContainer()
        self.containers = MagicMock()
        self.containers.run.return_value = self.container
        self.containers.list.return_value = []


@pytest.mark.asyncio
async def test_execute_code_success():
    """Test successful code execution."""
    # Create a mock Docker client with successful execution
    mock_container = MockContainer(
        exit_code=0,
        logs='{"output": "", "error": "", "memory_used": 10.5, "test_results": {"total": 2, "passed": 2, "failed": 0, "details": []}}'
    )
    mock_client = MockDockerClient(container=mock_container)
    
    # Create executor with mock client
    executor = SafeExecutor()
    executor.docker_client = mock_client
    
    # Execute simple code
    code = """
def add(a, b):
    return a + b
"""
    
    test_cases = [
        {'input': {'a': 2, 'b': 3}, 'expected_output': 5, 'function': 'add'},
        {'input': {'a': -1, 'b': 1}, 'expected_output': 0, 'function': 'add'},
    ]
    
    result = await executor.execute_code(code, test_cases)
    
    # Assert success
    assert result.status == ExecutionStatus.SUCCESS
    assert result.error == ""
    assert result.test_results == {"total": 2, "passed": 2, "failed": 0, "details": []}


@pytest.mark.asyncio
async def test_execute_code_error():
    """Test code execution with error."""
    # Create a mock Docker client with error execution
    mock_container = MockContainer(
        exit_code=1,
        logs='{"output": "", "error": "NameError: name \'undefined_var\' is not defined", "memory_used": 5.2, "test_results": {"total": 1, "passed": 0, "failed": 1, "details": []}}'
    )
    mock_client = MockDockerClient(container=mock_container)
    
    # Create executor with mock client
    executor = SafeExecutor()
    executor.docker_client = mock_client
    
    # Execute code with error
    code = """
def broken_function():
    return undefined_var
"""
    
    test_cases = [
        {'input': {}, 'expected_output': None, 'function': 'broken_function'},
    ]
    
    result = await executor.execute_code(code, test_cases)
    
    # Assert error
    assert result.status == ExecutionStatus.ERROR
    assert "NameError" in result.error
    assert result.test_results == {"total": 1, "passed": 0, "failed": 1, "details": []}


@pytest.mark.asyncio
async def test_execute_code_timeout():
    """Test code execution timeout."""
    # Create executor with mock client that will time out
    executor = SafeExecutor()
    
    # Mock the _wait_for_container method to simulate timeout
    async def mock_wait_for_container(container):
        await asyncio.sleep(0.5)  # Wait long enough to trigger timeout
        return '{"output": "", "error": "", "memory_used": 0, "test_results": {}}'
    
    executor._wait_for_container = mock_wait_for_container
    
    # Mock the Docker client to return a mock container
    mock_container = MockContainer()
    mock_client = MockDockerClient(container=mock_container)
    executor.docker_client = mock_client
    
    # Execute code with very short timeout
    code = """
import time
def slow_function():
    time.sleep(10)
    return 42
"""
    
    test_cases = [
        {'input': {}, 'expected_output': 42, 'function': 'slow_function'},
    ]
    
    result = await executor.execute_code(code, test_cases, timeout=0.1)
    
    # Assert timeout
    assert result.status == ExecutionStatus.TIMEOUT
    assert "timed out" in result.error.lower()


def test_code_sanitizer():
    """Test code sanitization."""
    sanitizer = CodeSanitizer()
    
    # Test disallowed imports
    code_with_import = """
import os
import sys

def dangerous_function():
    return os.system('ls')
"""
    is_valid, message = sanitizer.validate_code(code_with_import)
    assert not is_valid
    assert "Disallowed imports" in message
    
    # Test dangerous builtins
    code_with_eval = """
def dangerous_function(code):
    return eval(code)
"""
    is_valid, message = sanitizer.validate_code(code_with_eval)
    assert not is_valid
    assert "Disallowed builtins" in message
    
    # Test safe code
    safe_code = """
def add(a, b):
    return a + b
"""
    is_valid, message = sanitizer.validate_code(safe_code)
    assert is_valid
    assert message == ""


def test_resource_monitor():
    """Test resource monitoring."""
    monitor = ResourceMonitor()
    
    # Test output size checking
    small_output = "Hello, world!"
    assert monitor.check_output_size(small_output)
    
    # Generate a large output
    large_output = "x" * (monitor.max_output_size + 1000)
    assert not monitor.check_output_size(large_output)
    
    # Test output truncation
    truncated = monitor.truncate_output(large_output)
    assert len(truncated.encode('utf-8')) <= monitor.max_output_size
    assert "truncated" in truncated


if __name__ == "__main__":
    pytest.main(["-v", __file__])