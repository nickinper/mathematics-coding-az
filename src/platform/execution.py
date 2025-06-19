"""Execution service for running student code in the platform."""

import asyncio
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple, Union
import importlib

from src.core.sandbox import Sandbox, run_code_in_sandbox, test_submission_with_cases
from src.core.challenge import TestCase, ChallengeResult


class ExecutionService:
    """Service for executing student code submissions safely."""
    
    def __init__(
        self,
        timeout: float = 10.0,
        memory_limit: int = 100 * 1024 * 1024,
        allowed_modules: Optional[List[str]] = None
    ):
        """Initialize the execution service."""
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.allowed_modules = allowed_modules or [
            'math', 'random', 'datetime', 'collections', 'itertools',
            'functools', 'heapq', 'bisect', 'array', 'copy', 're', 'json',
            'hashlib', 'base64', 'decimal', 'fractions', 'statistics',
            'numpy', 'scipy', 'sympy', 'pandas'
        ]
    
    async def execute_submission(
        self,
        code: str,
        test_cases: List[TestCase],
        function_name: Optional[str] = None
    ) -> ChallengeResult:
        """
        Execute a code submission against test cases.
        
        Args:
            code: Student code submission
            test_cases: List of test cases to run
            function_name: Name of function to test
            
        Returns:
            ChallengeResult with detailed execution information
        """
        # Convert TestCase objects to the format expected by the sandbox
        sandbox_test_cases = []
        
        for test_case in test_cases:
            sandbox_test_cases.append({
                'input': test_case.input_data,
                'expected_output': test_case.expected_output,
                'description': test_case.description,
                'timeout': test_case.timeout
            })
        
        # Use an executor to run the code in a separate process for extra safety
        try:
            # Create a sandbox instance
            sandbox = Sandbox(
                allowed_modules=self.allowed_modules,
                cpu_limit=self.timeout,
                memory_limit=self.memory_limit,
                timeout=self.timeout
            )
            
            # Run security checks first
            is_safe, issues = sandbox.analyze_code(code)
            if not is_safe:
                return ChallengeResult(
                    passed=False,
                    test_results=[],
                    mathematical_score=0.0,
                    code_quality_score=0.0,
                    innovation_score=0.0,
                    total_score=0.0,
                    feedback=f"Security issues found: {', '.join(issues)}",
                    errors=[f"Security violation: {issue}" for issue in issues]
                )
            
            # Run submission synchronously since it's using a separate process
            if function_name:
                result = test_submission_with_cases(
                    code=code,
                    test_cases=sandbox_test_cases,
                    function_name=function_name,
                    timeout=self.timeout,
                    memory_limit=self.memory_limit,
                    allowed_modules=self.allowed_modules
                )
            else:
                # Execute the code without specific function call
                exec_result = run_code_in_sandbox(
                    code=code,
                    timeout=self.timeout,
                    memory_limit=self.memory_limit,
                    allowed_modules=self.allowed_modules
                )
                
                if not exec_result['success']:
                    return ChallengeResult(
                        passed=False,
                        test_results=[],
                        mathematical_score=0.0,
                        code_quality_score=0.0,
                        innovation_score=0.0,
                        total_score=0.0,
                        feedback=f"Execution error: {exec_result['output']}",
                        errors=[exec_result['output']]
                    )
                
                # Try to find functions in the global namespace and test them
                # This is a heuristic approach since we don't know the function name
                globals_dict = exec_result['result']
                functions = {
                    name: func for name, func in globals_dict.items()
                    if callable(func) and not name.startswith('_')
                }
                
                if not functions:
                    return ChallengeResult(
                        passed=False,
                        test_results=[],
                        mathematical_score=0.0,
                        code_quality_score=0.0,
                        innovation_score=0.0,
                        total_score=0.0,
                        feedback="No callable functions found in the submission",
                        errors=["No callable functions found"]
                    )
                
                # Try to find a function that works with the test cases
                for func_name in functions:
                    result = test_submission_with_cases(
                        code=code,
                        test_cases=sandbox_test_cases,
                        function_name=func_name,
                        timeout=self.timeout,
                        memory_limit=self.memory_limit,
                        allowed_modules=self.allowed_modules
                    )
                    
                    if result['tests_passed'] > 0:
                        break
                else:
                    # No function passed any tests
                    return ChallengeResult(
                        passed=False,
                        test_results=[],
                        mathematical_score=0.0,
                        code_quality_score=0.0,
                        innovation_score=0.0,
                        total_score=0.0,
                        feedback="No function in the submission passed any tests",
                        errors=["No function passed tests"]
                    )
            
            # Convert results to ChallengeResult format
            test_results = []
            for i, test_result in enumerate(result.get('test_results', [])):
                test_case = test_cases[i] if i < len(test_cases) else None
                execution_time = test_result.get('execution_time', 0.0)
                
                test_results.append(
                    (test_case, test_result.get('passed', False), execution_time)
                )
            
            # Calculate scores based on test results
            passed_tests = sum(1 for _, passed, _ in test_results if passed)
            total_tests = len(test_results)
            
            # Simple scoring for demonstration purposes
            # In a real system, you would use more sophisticated scoring
            if total_tests > 0:
                correctness_score = passed_tests / total_tests
            else:
                correctness_score = 0.0
            
            # These scores would come from other evaluators in a real system
            mathematical_score = correctness_score * 0.8  # Placeholder
            code_quality_score = 0.7  # Placeholder
            innovation_score = 0.5  # Placeholder
            
            # Calculate total score with weights
            total_score = (
                correctness_score * 0.4 +
                mathematical_score * 0.3 +
                code_quality_score * 0.2 +
                innovation_score * 0.1
            )
            
            # Generate feedback
            if result.get('passed', False):
                feedback = f"All tests passed! Execution time: {result.get('execution_time', 0.0):.2f}s"
            else:
                feedback = (
                    f"Passed {passed_tests}/{total_tests} tests. "
                    f"Execution time: {result.get('execution_time', 0.0):.2f}s"
                )
                
                # Add error details
                errors = []
                for test_result in result.get('test_results', []):
                    if not test_result.get('passed', False) and 'error' in test_result:
                        errors.append(f"Test {test_result.get('test_case', 0)}: {test_result['error']}")
            
            return ChallengeResult(
                passed=result.get('passed', False),
                test_results=test_results,
                mathematical_score=mathematical_score,
                code_quality_score=code_quality_score,
                innovation_score=innovation_score,
                total_score=total_score,
                feedback=feedback,
                errors=result.get('errors', [])
            )
            
        except Exception as e:
            # Handle any unexpected errors
            error_message = f"Error executing submission: {str(e)}\n{traceback.format_exc()}"
            return ChallengeResult(
                passed=False,
                test_results=[],
                mathematical_score=0.0,
                code_quality_score=0.0,
                innovation_score=0.0,
                total_score=0.0,
                feedback=error_message,
                errors=[error_message]
            )


# Singleton instance
execution_service = ExecutionService()


def get_execution_service() -> ExecutionService:
    """Get the singleton execution service instance."""
    return execution_service