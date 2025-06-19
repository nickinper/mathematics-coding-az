"""
Safe Execution Engine for running student code in isolated environments.

This module provides secure code execution with:
- Docker-based sandboxing
- Resource limits (CPU, memory, execution time)
- Security validation
- Test case execution
"""

import asyncio
import docker
import json
import logging
import os
import re
import tempfile
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExecutionStatus(Enum):
    """Status of code execution."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    MEMORY_LIMIT = "memory_limit"
    SECURITY_VIOLATION = "security_violation"


class ExecutionResult:
    """Result of code execution."""
    
    def __init__(
        self,
        status: ExecutionStatus,
        output: str = "",
        error: str = "",
        execution_time: float = 0.0,
        memory_used: float = 0.0,
        test_results: Optional[Dict[str, Any]] = None
    ):
        self.status = status
        self.output = output
        self.error = error
        self.execution_time = execution_time
        self.memory_used = memory_used
        self.test_results = test_results or {}


class CodeValidator:
    """Validates code for security concerns and banned patterns."""
    
    def __init__(self, executor=None):
        self.executor = executor
        self.banned_imports = [
            "os", "sys", "subprocess", "socket", "requests", 
            "urllib", "shutil", "threading", "multiprocessing"
        ]
        self.banned_builtins = ["eval", "exec", "compile", "__import__", "open"]
        
    def validate_code(self, code: str) -> Tuple[bool, str]:
        """
        Validate code for security concerns.
        
        Args:
            code: The Python code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for banned imports
        import_pattern = r'^\s*import\s+(.*)|^\s*from\s+(.*?)\s+import'
        for line in code.splitlines():
            match = re.search(import_pattern, line)
            if match:
                imported_module = (match.group(1) or match.group(2)).strip()
                for banned in self.banned_imports:
                    if imported_module == banned or imported_module.startswith(f"{banned}."):
                        return False, f"Security violation: Import of '{banned}' is not allowed"
        
        # Check for banned builtins
        for banned_builtin in self.banned_builtins:
            if re.search(rf'\b{banned_builtin}\s*\(', code):
                return False, f"Security violation: Use of '{banned_builtin}' is not allowed"
        
        # Check for potential file operations
        if re.search(r'open\s*\(|__file__|file\s*\(', code):
            return False, "Security violation: File operations are not allowed"
        
        return True, ""
    
    async def validate_submission(
        self, 
        submission_id: int, 
        code: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate a submission for security and execute it.
        
        Args:
            submission_id: ID of the submission
            code: The submitted code
            parameters: Execution parameters including test_cases
            
        Returns:
            Dictionary with validation and execution results
        """
        # First, validate the code
        is_valid, error_message = self.validate_code(code)
        if not is_valid:
            return {
                "status": "error",
                "message": error_message,
                "functional_score": 0.0,
                "test_results": {},
                "execution_time": 0.0
            }
        
        # If we have an executor, run the tests
        if self.executor:
            result = await self.executor.execute_code(
                code, 
                parameters.get('test_cases', []),
                "python",
                parameters.get('time_limit', 5.0),
                parameters.get('memory_limit', "256m")
            )
            
            # Calculate functional score based on test results
            test_count = len(parameters.get('test_cases', []))
            passed_count = result.test_results.get('passed', 0)
            functional_score = passed_count / test_count if test_count > 0 else 0.0
            
            return {
                "status": result.status.value,
                "message": result.error if result.status != ExecutionStatus.SUCCESS else "",
                "functional_score": functional_score,
                "test_results": result.test_results,
                "execution_time": result.execution_time
            }
        
        return {
            "status": "error",
            "message": "Executor not available",
            "functional_score": 0.0,
            "test_results": {},
            "execution_time": 0.0
        }


class SafeExecutor:
    """Executes code in isolated Docker containers with resource limits."""
    
    def __init__(
        self,
        docker_image: str = "python:3.11-slim",
        timeout: float = 5.0,
        memory_limit: str = "256m",
        cpu_limit: float = 0.5
    ):
        self.docker_image = docker_image
        self.default_timeout = timeout
        self.default_memory_limit = memory_limit
        self.default_cpu_limit = cpu_limit
        
        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
            logger.info(f"Docker client initialized. Using image: {docker_image}")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {str(e)}")
            logger.warning("Continuing with mock Docker client for testing purposes.")
            self.docker_client = None
    
    async def execute_code(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        language: str = "python",
        timeout: Optional[float] = None,
        memory_limit: Optional[str] = None
    ) -> ExecutionResult:
        """
        Execute code in a sandboxed environment.
        
        Args:
            code: The code to execute
            test_cases: Test cases to run
            language: Programming language (currently only supports Python)
            timeout: Execution timeout in seconds
            memory_limit: Memory limit for execution
            
        Returns:
            ExecutionResult with execution status and details
        """
        if not self.docker_client:
            # Mock execution for testing when Docker is not available
            logger.warning("Using mock execution since Docker is not available")
            
            # Simple mock execution by evaluating the Python code directly
            # WARNING: This is only for testing and not secure for production!
            import importlib.util
            import sys
            from io import StringIO
            import traceback
            
            try:
                # Create a temporary module to execute the code
                spec = importlib.util.spec_from_loader("student_code", loader=None)
                module = importlib.util.module_from_spec(spec)
                sys.modules["student_code"] = module
                
                # Execute the code in the module
                exec(code, module.__dict__)
                
                # Process test cases
                test_results = {
                    "total": len(test_cases),
                    "passed": 0,
                    "failed": 0,
                    "details": []
                }
                
                for i, test_case in enumerate(test_cases):
                    test_detail = {"test_id": i}
                    
                    try:
                        # Get function from module
                        if "function" in test_case:
                            func_name = test_case["function"]
                            if not hasattr(module, func_name):
                                test_detail["status"] = "failed"
                                test_detail["message"] = f"Function '{func_name}' not found"
                                test_results["failed"] += 1
                                test_results["details"].append(test_detail)
                                continue
                            
                            func = getattr(module, func_name)
                            
                            # Prepare input
                            if isinstance(test_case.get("input"), dict):
                                args = []
                                kwargs = test_case["input"]
                            else:
                                args = test_case.get("input", [])
                                kwargs = {}
                            
                            # Call function
                            result = func(*args, **kwargs)
                            
                            # Check result
                            expected = test_case.get("expected_output")
                            if result == expected:
                                test_detail["status"] = "passed"
                                test_results["passed"] += 1
                            else:
                                test_detail["status"] = "failed"
                                test_detail["message"] = f"Expected {expected}, got {result}"
                                test_results["failed"] += 1
                            
                            test_detail["input"] = test_case.get("input")
                            test_detail["expected_output"] = expected
                            test_detail["actual_output"] = result
                            
                        else:
                            # Direct code execution (no function)
                            test_detail["status"] = "error"
                            test_detail["message"] = "Direct code execution not supported"
                            test_results["failed"] += 1
                            
                    except Exception as e:
                        test_detail["status"] = "error"
                        test_detail["message"] = f"Error: {str(e)}"
                        test_results["failed"] += 1
                    
                    test_results["details"].append(test_detail)
                
                return ExecutionResult(
                    status=ExecutionStatus.SUCCESS,
                    output="Mock execution completed",
                    execution_time=0.1,
                    memory_used=10.0,
                    test_results=test_results
                )
                
            except Exception as e:
                return ExecutionResult(
                    status=ExecutionStatus.ERROR,
                    error=f"Mock execution error: {str(e)}\n{traceback.format_exc()}"
                )
                
            # Remove temp module
            if "student_code" in sys.modules:
                del sys.modules["student_code"]
        
        # Use default values if not provided
        timeout = timeout or self.default_timeout
        memory_limit = memory_limit or self.default_memory_limit
        
        # Create temporary directory for code files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write code to file
            code_file_path = os.path.join(temp_dir, "code.py")
            with open(code_file_path, "w") as f:
                f.write(code)
            
            # Write test cases to file
            test_file_path = os.path.join(temp_dir, "tests.json")
            with open(test_file_path, "w") as f:
                json.dump(test_cases, f)
            
            # Write test runner
            runner_file_path = os.path.join(temp_dir, "runner.py")
            with open(runner_file_path, "w") as f:
                f.write(self._generate_test_runner())
            
            # Execute in container
            start_time = time.time()
            try:
                container = self.docker_client.containers.run(
                    self.docker_image,
                    command=["python", "/code/runner.py"],
                    volumes={
                        temp_dir: {
                            "bind": "/code",
                            "mode": "ro"  # Read-only mount
                        }
                    },
                    mem_limit=memory_limit,
                    nano_cpus=int(self.default_cpu_limit * 1e9),  # Convert to nano CPUs
                    network_mode="none",  # No network access
                    detach=True,
                    remove=True,
                    labels={"mathcoding-executor": "true"}
                )
                
                # Wait for container to finish or timeout
                try:
                    result = await asyncio.wait_for(
                        self._wait_for_container(container),
                        timeout=timeout
                    )
                    execution_time = time.time() - start_time
                    
                    # Parse test results
                    try:
                        result_data = json.loads(result)
                        return ExecutionResult(
                            status=ExecutionStatus.SUCCESS if result_data.get("error") == "" else ExecutionStatus.ERROR,
                            output=result_data.get("output", ""),
                            error=result_data.get("error", ""),
                            execution_time=execution_time,
                            memory_used=result_data.get("memory_used", 0.0),
                            test_results=result_data.get("test_results", {})
                        )
                    except json.JSONDecodeError:
                        return ExecutionResult(
                            status=ExecutionStatus.ERROR,
                            error=f"Failed to parse result: {result}",
                            execution_time=execution_time
                        )
                    
                except asyncio.TimeoutError:
                    # Kill the container if it's still running
                    try:
                        container.kill()
                    except:
                        pass
                    
                    return ExecutionResult(
                        status=ExecutionStatus.TIMEOUT,
                        error="Execution timed out",
                        execution_time=timeout
                    )
                
            except docker.errors.APIError as e:
                if "OOMKilled" in str(e):
                    return ExecutionResult(
                        status=ExecutionStatus.MEMORY_LIMIT,
                        error="Memory limit exceeded"
                    )
                return ExecutionResult(
                    status=ExecutionStatus.ERROR,
                    error=f"Docker API error: {str(e)}"
                )
            except Exception as e:
                logger.error(f"Error executing code: {str(e)}")
                return ExecutionResult(
                    status=ExecutionStatus.ERROR,
                    error=f"Execution error: {str(e)}"
                )
    
    async def _wait_for_container(self, container) -> str:
        """Wait for container to finish and return logs."""
        exit_code = container.wait()["StatusCode"]
        logs = container.logs().decode("utf-8", errors="replace")
        
        if exit_code != 0:
            logger.warning(f"Container exited with code {exit_code}: {logs}")
        
        return logs
    
    def _generate_test_runner(self) -> str:
        """Generate Python code for the test runner."""
        return """
import json
import sys
import traceback
import importlib.util
import resource

# Load test cases
with open('/code/tests.json', 'r') as f:
    test_cases = json.load(f)

# Load student code as module
try:
    spec = importlib.util.spec_from_file_location("student_code", "/code/code.py")
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)
except Exception as e:
    result = {
        "output": "",
        "error": f"Error loading code: {str(e)}\\n{traceback.format_exc()}",
        "memory_used": 0.0,
        "test_results": {
            "total": len(test_cases),
            "passed": 0,
            "failed": len(test_cases),
            "details": []
        }
    }
    print(json.dumps(result))
    sys.exit(1)

# Run test cases
test_results = {
    "total": len(test_cases),
    "passed": 0,
    "failed": 0,
    "details": []
}

output_buffer = ""
error_buffer = ""

for i, test_case in enumerate(test_cases):
    test_detail = {"test_id": i}
    
    try:
        # Get function from student module
        if "function" in test_case:
            func_name = test_case["function"]
            if not hasattr(student_module, func_name):
                test_detail["status"] = "error"
                test_detail["message"] = f"Function '{func_name}' not found"
                test_results["failed"] += 1
                test_results["details"].append(test_detail)
                continue
            
            func = getattr(student_module, func_name)
            
            # Prepare input
            if isinstance(test_case.get("input"), dict):
                args = []
                kwargs = test_case["input"]
            else:
                args = test_case.get("input", [])
                kwargs = {}
            
            # Call function
            result = func(*args, **kwargs)
            
            # Check result
            expected = test_case.get("expected_output")
            if result == expected:
                test_detail["status"] = "passed"
                test_results["passed"] += 1
            else:
                test_detail["status"] = "failed"
                test_detail["message"] = f"Expected {expected}, got {result}"
                test_results["failed"] += 1
                
        else:
            # Direct code execution (no function)
            # Not implemented yet
            test_detail["status"] = "error"
            test_detail["message"] = "Direct code execution not supported"
            test_results["failed"] += 1
            
    except Exception as e:
        test_detail["status"] = "error"
        test_detail["message"] = f"Error: {str(e)}\\n{traceback.format_exc()}"
        test_results["failed"] += 1
        error_buffer += f"Test {i} error: {str(e)}\\n"
    
    test_results["details"].append(test_detail)

# Get memory usage
memory_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB to MB

result = {
    "output": output_buffer,
    "error": error_buffer,
    "memory_used": memory_used,
    "test_results": test_results
}

print(json.dumps(result))
"""