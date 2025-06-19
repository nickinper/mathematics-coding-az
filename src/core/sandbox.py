"""Safe execution environment for running student code with security restrictions."""

import ast
import sys
import time
import resource
import traceback
import contextlib
import io
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import threading
import signal
import importlib


class CodeAnalyzer(ast.NodeVisitor):
    """Analyzes code for security issues before execution."""
    
    def __init__(self):
        self.issues = []
        self.imports = []
        # Potentially dangerous builtins to restrict
        self.restricted_builtins = {
            'eval', 'exec', 'compile', 'globals', 'locals', 'getattr',
            'setattr', 'delattr', '__import__', 'open', 'input',
            'memoryview', 'breakpoint', 'help'
        }
        # Potentially dangerous modules to restrict
        self.restricted_modules = {
            'os', 'sys', 'subprocess', 'shutil', 'pathlib', 'pickle',
            'marshal', 'shelve', 'socket', 'asyncio', 'multiprocessing',
            'threading', 'ctypes', 'signal'
        }
    
    def visit_Call(self, node):
        """Check for calls to restricted functions."""
        if isinstance(node.func, ast.Name):
            if node.func.id in self.restricted_builtins:
                self.issues.append(f"Restricted builtin '{node.func.id}' used")
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Check for restricted module imports."""
        for name in node.names:
            self.imports.append(name.name)
            if name.name in self.restricted_modules:
                self.issues.append(f"Restricted module '{name.name}' imported")
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Check for restricted module imports using 'from'."""
        if node.module in self.restricted_modules:
            self.issues.append(f"Restricted module '{node.module}' imported")
        self.imports.append(node.module)
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Check for accessing dangerous attributes."""
        attr_chain = self._get_attribute_chain(node)
        if attr_chain and attr_chain[0] in self.restricted_modules:
            self.issues.append(f"Accessing attributes from restricted module '{attr_chain[0]}'")
        if '__' in node.attr:
            # Check for dunder methods that might be dangerous
            if node.attr in {'__subclasses__', '__globals__', '__builtins__', '__getattribute__', '__setattr__'}:
                self.issues.append(f"Potentially dangerous attribute '{node.attr}' accessed")
        self.generic_visit(node)
    
    def _get_attribute_chain(self, node):
        """Recursively get the attribute chain, e.g., 'os.path.join' -> ['os', 'path', 'join']."""
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                return [node.value.id, node.attr]
            elif isinstance(node.value, ast.Attribute):
                chain = self._get_attribute_chain(node.value)
                if chain:
                    return chain + [node.attr]
        return None


class ResourceLimiter:
    """Limits CPU, memory, and other resources for sandboxed code execution."""
    
    def __init__(
        self,
        cpu_time_limit: float = 5.0,  # seconds
        memory_limit: int = 100 * 1024 * 1024,  # 100 MB
        stack_limit: int = 8 * 1024 * 1024  # 8 MB
    ):
        self.cpu_time_limit = cpu_time_limit
        self.memory_limit = memory_limit
        self.stack_limit = stack_limit
    
    def __enter__(self):
        """Set resource limits when entering the context."""
        # Set CPU time limit
        resource.setrlimit(resource.RLIMIT_CPU, (self.cpu_time_limit, self.cpu_time_limit))
        
        # Set memory limit
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
        
        # Set stack limit
        resource.setrlimit(resource.RLIMIT_STACK, (self.stack_limit, self.stack_limit))
        
        # Return self for potential future use
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Reset resource limits when exiting the context."""
        # No need to explicitly reset as process will either continue normally
        # or be terminated if it hit a resource limit
        pass


class TimeoutError(Exception):
    """Custom exception for code execution timeout."""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeouts."""
    raise TimeoutError("Code execution timed out")


class Sandbox:
    """Safe execution environment for student code."""
    
    def __init__(
        self,
        allowed_modules: Optional[List[str]] = None,
        cpu_limit: float = 5.0,
        memory_limit: int = 100 * 1024 * 1024,
        timeout: float = 10.0
    ):
        """Initialize the sandbox with security and resource limits."""
        self.allowed_modules = allowed_modules or [
            'math', 'random', 'datetime', 'collections', 'itertools',
            'functools', 'heapq', 'bisect', 'array', 'copy', 're', 'json',
            'hashlib', 'base64', 'decimal', 'fractions', 'statistics',
            'numpy', 'scipy', 'sympy', 'pandas'
        ]
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit
        self.timeout = timeout
    
    def analyze_code(self, code: str) -> Tuple[bool, List[str]]:
        """Analyze code for security issues before execution."""
        try:
            tree = ast.parse(code)
            analyzer = CodeAnalyzer()
            analyzer.visit(tree)
            
            return len(analyzer.issues) == 0, analyzer.issues
        except SyntaxError as e:
            return False, [f"Syntax error: {str(e)}"]
    
    def prepare_safe_globals(self) -> Dict[str, Any]:
        """Prepare a safe globals dictionary for execution."""
        safe_builtins = {
            k: v for k, v in __builtins__.items()
            if k not in CodeAnalyzer().restricted_builtins
        }
        
        # Create fresh globals with restricted builtins
        globals_dict = {
            '__builtins__': safe_builtins,
            'print': print,  # Allow print for debugging
            'len': len,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'all': all,
            'any': any,
            'round': round,
            'sorted': sorted,
            'reversed': reversed,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'frozenset': frozenset,
            'bool': bool,
            'int': int,
            'float': float,
            'str': str,
            'complex': complex,
        }
        
        # Import allowed modules
        for module_name in self.allowed_modules:
            try:
                if '.' in module_name:
                    # Handle submodules like numpy.linalg
                    parts = module_name.split('.')
                    base_module = importlib.import_module(parts[0])
                    current = base_module
                    
                    # Add the base module
                    if parts[0] not in globals_dict:
                        globals_dict[parts[0]] = base_module
                    
                    # Navigate to the submodule
                    for part in parts[1:]:
                        current = getattr(current, part)
                    
                    # Add the full path too
                    globals_dict[module_name] = current
                else:
                    # Simple module import
                    module = importlib.import_module(module_name)
                    globals_dict[module_name] = module
            except (ImportError, AttributeError):
                # Skip modules that can't be imported
                pass
        
        return globals_dict
    
    def execute_code(
        self,
        code: str,
        function_name: Optional[str] = None,
        args: List[Any] = None
    ) -> Tuple[bool, Any, str, float]:
        """
        Execute code in a sandboxed environment.
        
        Args:
            code: Python code to execute
            function_name: Optional name of function to call after execution
            args: Arguments to pass to the function
            
        Returns:
            Tuple of (success, result, output, execution_time)
        """
        # First analyze the code for security issues
        is_safe, issues = self.analyze_code(code)
        if not is_safe:
            return False, None, f"Security issues found: {', '.join(issues)}", 0.0
        
        # Prepare for capturing stdout
        stdout_buffer = io.StringIO()
        
        # Prepare result container that can be accessed from the worker thread
        result_container = {'success': False, 'result': None, 'output': '', 'time': 0.0}
        
        # Define the worker function
        def worker():
            start_time = time.time()
            
            try:
                # Redirect stdout
                with contextlib.redirect_stdout(stdout_buffer):
                    # Apply resource limits
                    with ResourceLimiter(
                        cpu_time_limit=self.cpu_limit,
                        memory_limit=self.memory_limit
                    ):
                        # Prepare a safe globals dictionary
                        globals_dict = self.prepare_safe_globals()
                        
                        # Execute the code
                        exec(code, globals_dict)
                        
                        # If a function name is provided, call the function
                        if function_name is not None:
                            if function_name in globals_dict:
                                func = globals_dict[function_name]
                                if callable(func):
                                    result_container['result'] = func(*(args or []))
                                else:
                                    raise TypeError(f"{function_name} is not callable")
                            else:
                                raise NameError(f"{function_name} not found in the code")
                        else:
                            # Just return the globals as the result
                            result_container['result'] = {
                                k: v for k, v in globals_dict.items()
                                if k != '__builtins__' and not k.startswith('_')
                            }
                
                result_container['success'] = True
                
            except Exception as e:
                result_container['output'] = f"Error: {str(e)}\n{traceback.format_exc()}"
                result_container['success'] = False
            finally:
                result_container['time'] = time.time() - start_time
                result_container['output'] = stdout_buffer.getvalue()
        
        # Create and start the worker thread
        thread = threading.Thread(target=worker)
        thread.daemon = True
        
        # Set a timer for timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(self.timeout) + 1)  # +1 for safety
        
        try:
            thread.start()
            thread.join(self.timeout)
            
            if thread.is_alive():
                # Thread is still running after timeout
                return False, None, "Execution timed out", self.timeout
            
            return (
                result_container['success'],
                result_container['result'],
                result_container['output'],
                result_container['time']
            )
            
        except TimeoutError:
            return False, None, "Execution timed out", self.timeout
        
        finally:
            # Reset the alarm
            signal.alarm(0)
    
    def test_submission(
        self,
        code: str,
        test_cases: List[Dict[str, Any]],
        function_name: str
    ) -> Dict[str, Any]:
        """
        Test a code submission against provided test cases.
        
        Args:
            code: Student code submission
            test_cases: List of test cases with input and expected output
            function_name: Name of function to test
            
        Returns:
            Dictionary with test results
        """
        # First analyze the code for security issues
        is_safe, issues = self.analyze_code(code)
        if not is_safe:
            return {
                'passed': False,
                'tests_passed': 0,
                'total_tests': len(test_cases),
                'error': f"Security issues found: {', '.join(issues)}",
                'execution_time': 0.0,
                'test_results': []
            }
        
        # Prepare the globals dictionary only once
        globals_dict = self.prepare_safe_globals()
        
        # Execute the code to define functions
        try:
            exec(code, globals_dict)
        except Exception as e:
            return {
                'passed': False,
                'tests_passed': 0,
                'total_tests': len(test_cases),
                'error': f"Error in code: {str(e)}\n{traceback.format_exc()}",
                'execution_time': 0.0,
                'test_results': []
            }
        
        # Check if the function exists
        if function_name not in globals_dict:
            return {
                'passed': False,
                'tests_passed': 0,
                'total_tests': len(test_cases),
                'error': f"Function '{function_name}' not found in the code",
                'execution_time': 0.0,
                'test_results': []
            }
        
        func = globals_dict[function_name]
        if not callable(func):
            return {
                'passed': False,
                'tests_passed': 0,
                'total_tests': len(test_cases),
                'error': f"'{function_name}' is not callable",
                'execution_time': 0.0,
                'test_results': []
            }
        
        # Run tests
        test_results = []
        total_time = 0.0
        tests_passed = 0
        
        for i, test_case in enumerate(test_cases):
            input_data = test_case.get('input', [])
            expected_output = test_case.get('expected_output')
            
            start_time = time.time()
            try:
                # Apply resource limits
                with ResourceLimiter(
                    cpu_time_limit=self.cpu_limit,
                    memory_limit=self.memory_limit
                ):
                    # Redirect stdout
                    stdout_buffer = io.StringIO()
                    with contextlib.redirect_stdout(stdout_buffer):
                        # Set timeout
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(int(self.timeout) + 1)
                        
                        # Call the function
                        if isinstance(input_data, list):
                            result = func(*input_data)
                        elif isinstance(input_data, dict):
                            result = func(**input_data)
                        else:
                            result = func(input_data)
                        
                        # Reset the alarm
                        signal.alarm(0)
                    
                    execution_time = time.time() - start_time
                    total_time += execution_time
                    
                    # Check if the result matches the expected output
                    if callable(expected_output):
                        # If expected_output is a function, it's a custom checker
                        passed = expected_output(result)
                    else:
                        # Otherwise do a direct comparison
                        passed = result == expected_output
                    
                    if passed:
                        tests_passed += 1
                    
                    test_results.append({
                        'test_case': i + 1,
                        'input': input_data,
                        'expected': str(expected_output) if not callable(expected_output) else "Custom checker",
                        'actual': result,
                        'passed': passed,
                        'execution_time': execution_time,
                        'output': stdout_buffer.getvalue()
                    })
                    
            except Exception as e:
                execution_time = time.time() - start_time
                total_time += execution_time
                
                test_results.append({
                    'test_case': i + 1,
                    'input': input_data,
                    'expected': str(expected_output) if not callable(expected_output) else "Custom checker",
                    'actual': None,
                    'passed': False,
                    'execution_time': execution_time,
                    'error': f"{type(e).__name__}: {str(e)}",
                    'traceback': traceback.format_exc()
                })
        
        return {
            'passed': tests_passed == len(test_cases),
            'tests_passed': tests_passed,
            'total_tests': len(test_cases),
            'execution_time': total_time,
            'test_results': test_results
        }


def run_code_in_sandbox(
    code: str,
    function_name: Optional[str] = None,
    args: List[Any] = None,
    timeout: float = 10.0,
    memory_limit: int = 100 * 1024 * 1024,
    allowed_modules: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function to run code in a sandbox and return structured results.
    
    Args:
        code: Python code to execute
        function_name: Optional name of function to call after execution
        args: Arguments to pass to the function
        timeout: Maximum execution time in seconds
        memory_limit: Maximum memory usage in bytes
        allowed_modules: List of module names allowed to be imported
        
    Returns:
        Dictionary with execution results
    """
    sandbox = Sandbox(
        allowed_modules=allowed_modules,
        cpu_limit=timeout,
        memory_limit=memory_limit,
        timeout=timeout
    )
    
    success, result, output, execution_time = sandbox.execute_code(
        code, function_name, args
    )
    
    return {
        'success': success,
        'result': result,
        'output': output,
        'execution_time': execution_time
    }


def test_submission_with_cases(
    code: str,
    test_cases: List[Dict[str, Any]],
    function_name: str,
    timeout: float = 10.0,
    memory_limit: int = 100 * 1024 * 1024,
    allowed_modules: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function to test a submission against test cases.
    
    Args:
        code: Student code submission
        test_cases: List of test cases with input and expected output
        function_name: Name of function to test
        timeout: Maximum execution time in seconds
        memory_limit: Maximum memory usage in bytes
        allowed_modules: List of module names allowed to be imported
        
    Returns:
        Dictionary with test results
    """
    sandbox = Sandbox(
        allowed_modules=allowed_modules,
        cpu_limit=timeout,
        memory_limit=memory_limit,
        timeout=timeout
    )
    
    return sandbox.test_submission(code, test_cases, function_name)