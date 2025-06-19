"""Dual-layer verification framework for correctness and mathematical reasoning."""

import ast
import inspect
import re
from typing import Any, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

import sympy as sp
import numpy as np


class MathematicalVerifier(ABC):
    """Base class for mathematical reasoning verification."""
    
    @abstractmethod
    def verify_proof(self, proof_text: str) -> Tuple[bool, float, str]:
        """Verify a mathematical proof.
        
        Returns:
            Tuple of (valid, confidence_score, feedback)
        """
        pass
    
    @abstractmethod
    def check_derivation(self, derivation: str) -> Tuple[bool, str]:
        """Check mathematical derivation steps.
        
        Returns:
            Tuple of (valid, feedback)
        """
        pass


class ComplexityAnalyzer:
    """Analyzes algorithmic complexity of code."""
    
    def analyze_time_complexity(self, code: str) -> Tuple[str, float]:
        """Analyze time complexity of given code.
        
        Returns:
            Tuple of (complexity_class, confidence)
        """
        try:
            tree = ast.parse(code)
            analyzer = ComplexityVisitor()
            analyzer.visit(tree)
            return analyzer.get_complexity()
        except Exception as e:
            return "unknown", 0.0
    
    def analyze_space_complexity(self, code: str) -> Tuple[str, float]:
        """Analyze space complexity of given code."""
        # Simplified space complexity analysis
        if "recursion" in code.lower() or "recursive" in code.lower():
            return "O(n)", 0.7
        if any(data_struct in code for data_struct in ["list", "dict", "set"]):
            return "O(n)", 0.8
        return "O(1)", 0.9


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor for complexity analysis."""
    
    def __init__(self):
        self.loops = 0
        self.nested_loops = 0
        self.recursive_calls = 0
        self.loop_depth = 0
        
    def visit_For(self, node):
        self.loops += 1
        self.loop_depth += 1
        if self.loop_depth > 1:
            self.nested_loops += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        
    def visit_While(self, node):
        self.loops += 1
        self.loop_depth += 1
        if self.loop_depth > 1:
            self.nested_loops += 1
        self.generic_visit(node)
        self.loop_depth -= 1
        
    def visit_Call(self, node):
        # Simple heuristic for recursion detection
        if isinstance(node.func, ast.Name):
            # This would need more sophisticated analysis in practice
            pass
        self.generic_visit(node)
        
    def get_complexity(self) -> Tuple[str, float]:
        """Determine complexity based on analysis."""
        if self.nested_loops >= 2:
            return "O(n³)", 0.8
        elif self.nested_loops >= 1:
            return "O(n²)", 0.9
        elif self.loops >= 1:
            return "O(n)", 0.9
        elif self.recursive_calls > 0:
            return "O(2ⁿ)", 0.7  # Conservative estimate
        else:
            return "O(1)", 0.9


class SymbolicVerifier(MathematicalVerifier):
    """Verifies mathematical reasoning using symbolic computation."""
    
    def verify_proof(self, proof_text: str) -> Tuple[bool, float, str]:
        """Verify mathematical proof using pattern matching and symbolic logic."""
        # Extract mathematical statements
        equations = self._extract_equations(proof_text)
        
        if not equations:
            return False, 0.0, "No mathematical statements found"
        
        # Verify each equation
        valid_count = 0
        total_count = len(equations)
        
        for eq in equations:
            try:
                if self._verify_equation(eq):
                    valid_count += 1
            except Exception:
                pass
                
        confidence = valid_count / total_count if total_count > 0 else 0.0
        
        if confidence > 0.8:
            return True, confidence, "Mathematical reasoning appears sound"
        elif confidence > 0.5:
            return False, confidence, "Some mathematical steps need verification"
        else:
            return False, confidence, "Mathematical reasoning has significant gaps"
    
    def check_derivation(self, derivation: str) -> Tuple[bool, str]:
        """Check step-by-step mathematical derivation."""
        steps = self._extract_derivation_steps(derivation)
        
        for i, step in enumerate(steps[:-1]):
            next_step = steps[i + 1]
            if not self._verify_step_transition(step, next_step):
                return False, f"Invalid transition at step {i + 1}"
        
        return True, "Derivation steps are valid"
    
    def _extract_equations(self, text: str) -> List[str]:
        """Extract mathematical equations from text."""
        # Pattern to match equations (simplified)
        equation_pattern = r'[^=]*=[^=]*'
        return re.findall(equation_pattern, text)
    
    def _verify_equation(self, equation: str) -> bool:
        """Verify a single equation using SymPy."""
        try:
            # Parse and verify the equation
            left, right = equation.split('=')
            left_expr = sp.sympify(left.strip())
            right_expr = sp.sympify(right.strip())
            
            # Check if they're symbolically equal
            return sp.simplify(left_expr - right_expr) == 0
        except Exception:
            return False
    
    def _extract_derivation_steps(self, derivation: str) -> List[str]:
        """Extract individual steps from derivation."""
        # Split by common step indicators
        steps = re.split(r'\n|;|→|⟹', derivation)
        return [step.strip() for step in steps if step.strip()]
    
    def _verify_step_transition(self, step1: str, step2: str) -> bool:
        """Verify that step2 follows logically from step1."""
        try:
            expr1 = sp.sympify(step1)
            expr2 = sp.sympify(step2)
            
            # Check if the transformation is valid (simplified check)
            diff = sp.simplify(expr1 - expr2)
            return diff == 0 or self._is_valid_transformation(expr1, expr2)
        except Exception:
            return False
    
    def _is_valid_transformation(self, expr1, expr2) -> bool:
        """Check if transformation from expr1 to expr2 is valid."""
        # This would contain more sophisticated transformation rules
        # For now, just check if they're algebraically equivalent
        return sp.simplify(expr1 - expr2) == 0


class VerificationFramework:
    """Main verification framework combining correctness and mathematical reasoning."""
    
    def __init__(self):
        self.mathematical_verifier = SymbolicVerifier()
        self.complexity_analyzer = ComplexityAnalyzer()
    
    def verify_submission(
        self, 
        code: str, 
        mathematical_reasoning: str,
        expected_complexity: Optional[str] = None
    ) -> Dict[str, Any]:
        """Comprehensive verification of code and mathematical reasoning."""
        results = {}
        
        # Verify mathematical reasoning
        math_valid, math_confidence, math_feedback = self.mathematical_verifier.verify_proof(
            mathematical_reasoning
        )
        
        results['mathematical_verification'] = {
            'valid': math_valid,
            'confidence': math_confidence,
            'feedback': math_feedback
        }
        
        # Analyze complexity
        time_complexity, time_confidence = self.complexity_analyzer.analyze_time_complexity(code)
        space_complexity, space_confidence = self.complexity_analyzer.analyze_space_complexity(code)
        
        results['complexity_analysis'] = {
            'time_complexity': time_complexity,
            'time_confidence': time_confidence,
            'space_complexity': space_complexity,
            'space_confidence': space_confidence,
            'meets_requirements': (
                expected_complexity is None or 
                self._complexity_matches(time_complexity, expected_complexity)
            )
        }
        
        # Overall assessment
        results['overall_score'] = self._calculate_overall_score(results)
        
        return results
    
    def _complexity_matches(self, actual: str, expected: str) -> bool:
        """Check if actual complexity matches expected."""
        # Simplified complexity matching
        complexity_order = {
            'O(1)': 1,
            'O(log n)': 2,
            'O(n)': 3,
            'O(n log n)': 4,
            'O(n²)': 5,
            'O(n³)': 6,
            'O(2ⁿ)': 7
        }
        
        return complexity_order.get(actual, 100) <= complexity_order.get(expected, 0)
    
    def _calculate_overall_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall verification score."""
        math_score = results['mathematical_verification']['confidence']
        complexity_penalty = 0.0 if results['complexity_analysis']['meets_requirements'] else 0.3
        
        return max(0.0, math_score - complexity_penalty)