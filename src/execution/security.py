"""
Security module for code execution.

This module provides additional security features:
- Code validation and sanitization
- Import/builtin restrictions
- Resource monitoring
"""

import re
import ast
import yaml
import os
import logging
from typing import List, Dict, Tuple, Optional, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeSanitizer:
    """Sanitizes and checks code for security issues."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize code sanitizer with security configuration.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config = self._load_config(config_path)
        self.blocked_imports = set(self.config["security"]["blocked_imports"])
        self.dangerous_builtins = set(self.config["security"]["dangerous_builtins"])
        self.blocked_functions = set(self.config["security"]["blocked_functions"])
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML file."""
        default_config = {
            "security": {
                "blocked_imports": [
                    "os", "sys", "subprocess", "socket", "requests", 
                    "urllib", "shutil", "threading", "multiprocessing"
                ],
                "dangerous_builtins": [
                    "eval", "exec", "compile", "__import__", "open"
                ],
                "blocked_functions": [
                    "breakpoint", "help", "dir", "vars"
                ]
            }
        }
        
        if not config_path or not os.path.exists(config_path):
            logger.warning("Config path not provided or does not exist. Using default config.")
            return default_config
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("execution", default_config)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return default_config
    
    def validate_code(self, code: str) -> Tuple[bool, str]:
        """
        Validate code for security issues.
        
        Args:
            code: The code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for disallowed imports using AST parsing
        try:
            tree = ast.parse(code)
            
            # Collect imports
            imports = self._collect_imports(tree)
            disallowed_imports = imports.intersection(self.blocked_imports)
            
            if disallowed_imports:
                return False, f"Security violation: Disallowed imports: {', '.join(disallowed_imports)}"
            
            # Check for dangerous builtins
            builtins_used = self._collect_builtins(tree)
            disallowed_builtins = builtins_used.intersection(self.dangerous_builtins)
            
            if disallowed_builtins:
                return False, f"Security violation: Disallowed builtins: {', '.join(disallowed_builtins)}"
            
            # Check for disallowed functions
            functions_used = self._collect_functions(tree)
            disallowed_functions = functions_used.intersection(self.blocked_functions)
            
            if disallowed_functions:
                return False, f"Security violation: Disallowed functions: {', '.join(disallowed_functions)}"
            
            return True, ""
            
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Error validating code: {str(e)}"
    
    def _collect_imports(self, tree: ast.AST) -> Set[str]:
        """
        Collect all imported modules from AST.
        
        Args:
            tree: AST tree of the code
            
        Returns:
            Set of imported module names
        """
        imports = set()
        
        for node in ast.walk(tree):
            # Regular imports: import os, sys
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name.split('.')[0])
            
            # From imports: from os import path
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])
        
        return imports
    
    def _collect_builtins(self, tree: ast.AST) -> Set[str]:
        """
        Collect all builtin functions used in the code.
        
        Args:
            tree: AST tree of the code
            
        Returns:
            Set of builtin function names used
        """
        builtins_used = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in self.dangerous_builtins:
                    builtins_used.add(node.func.id)
        
        return builtins_used
    
    def _collect_functions(self, tree: ast.AST) -> Set[str]:
        """
        Collect all function calls in the code.
        
        Args:
            tree: AST tree of the code
            
        Returns:
            Set of function names called
        """
        functions = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                functions.add(node.func.id)
        
        return functions
    
    def sanitize_code(self, code: str) -> str:
        """
        Sanitize code by removing dangerous constructs.
        
        Args:
            code: The code to sanitize
            
        Returns:
            Sanitized code
        """
        # This is a simple example of sanitization
        # In a real implementation, we would use more sophisticated techniques
        
        # Remove __import__ calls
        code = re.sub(r'__import__\s*\(', '# __import__(', code)
        
        # Remove eval/exec calls
        code = re.sub(r'eval\s*\(', '# eval(', code)
        code = re.sub(r'exec\s*\(', '# exec(', code)
        
        return code


class ResourceMonitor:
    """Monitors resource usage during code execution."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize resource monitor with limits configuration.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config = self._load_config(config_path)
        self.max_output_size = self.config["limits"]["max_output_size"]
        self.max_containers = self.config["limits"]["max_containers"]
        self.cleanup_interval = self.config["limits"]["cleanup_interval"]
        self.rate_limit = self.config["limits"]["rate_limit"]
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML file."""
        default_config = {
            "limits": {
                "max_output_size": 1048576,  # 1MB
                "max_containers": 10,
                "cleanup_interval": 300,  # 5 minutes
                "rate_limit": 10  # requests per minute
            }
        }
        
        if not config_path or not os.path.exists(config_path):
            logger.warning("Config path not provided or does not exist. Using default config.")
            return default_config
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("execution", default_config)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return default_config
    
    def check_output_size(self, output: str) -> bool:
        """
        Check if output size exceeds the limit.
        
        Args:
            output: The output to check
            
        Returns:
            True if output size is within limit, False otherwise
        """
        return len(output.encode('utf-8')) <= self.max_output_size
    
    def truncate_output(self, output: str) -> str:
        """
        Truncate output to max size.
        
        Args:
            output: The output to truncate
            
        Returns:
            Truncated output
        """
        if len(output.encode('utf-8')) <= self.max_output_size:
            return output
        
        # Truncate to slightly less than the limit to add a message
        truncated = output.encode('utf-8')[:self.max_output_size - 100].decode('utf-8', errors='ignore')
        return truncated + "\n... [output truncated due to size limit]"