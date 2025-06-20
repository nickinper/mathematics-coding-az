"""
GCD Basics Challenge - Foundation of Number Theory
Focuses on the Euclidean algorithm and its mathematical properties.
"""

import re
import ast
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain,
    MathematicalRequirement, TestCase
)


class GCDBasicsChallenge(Challenge):
    """Greatest Common Divisor challenge emphasizing the Euclidean algorithm."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Euclidean Algorithm",
                description="Implement GCD using the Euclidean algorithm: gcd(a,b) = gcd(b, a mod b)",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Complexity Analysis",
                description="Prove that the algorithm runs in O(log(min(a,b))) time",
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Mathematical Properties",
                description="Demonstrate understanding of GCD properties: gcd(a,b) = gcd(b,a), gcd(a,0) = a",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Bezout's Identity Preparation",
                description="Explain how the algorithm can be extended to find x,y where ax + by = gcd(a,b)",
                proof_required=False
            )
        ]
        
        test_cases = [
            # Basic cases
            TestCase(
                input_data={"a": 48, "b": 18},
                expected_output=6,
                description="Basic positive integers"
            ),
            TestCase(
                input_data={"a": 17, "b": 13},
                expected_output=1,
                description="Coprime numbers"
            ),
            # Edge cases
            TestCase(
                input_data={"a": 0, "b": 5},
                expected_output=5,
                description="Zero handling"
            ),
            TestCase(
                input_data={"a": 5, "b": 0},
                expected_output=5,
                description="Zero as second argument"
            ),
            TestCase(
                input_data={"a": 0, "b": 0},
                expected_output=0,
                description="Both zeros"
            ),
            # Large numbers
            TestCase(
                input_data={"a": 1071, "b": 462},
                expected_output=21,
                description="Larger numbers requiring multiple steps"
            ),
            TestCase(
                input_data={"a": 123456789, "b": 987654321},
                expected_output=9,
                description="Very large numbers"
            ),
            # Fibonacci numbers (worst case for Euclidean algorithm)
            TestCase(
                input_data={"a": 987, "b": 610},
                expected_output=1,
                description="Consecutive Fibonacci numbers (worst case)"
            )
        ]
        
        super().__init__(
            title="GCD Basics - Euclidean Algorithm",
            description="""
Implement the Greatest Common Divisor (GCD) function using the Euclidean algorithm.

Requirements:
1. Must use the Euclidean algorithm (not brute force)
2. Must handle all edge cases correctly
3. Must achieve O(log(min(a,b))) time complexity
4. Must explain the mathematical foundation

Mathematical Foundation:
The Euclidean algorithm is based on the principle that:
gcd(a, b) = gcd(b, a mod b)

This works because any common divisor of a and b also divides a - qb (where q = a // b).

Function signature: gcd(a: int, b: int) -> int

Example:
```python
def gcd(a: int, b: int) -> int:
    # Your implementation here
    pass
```

Your solution should demonstrate understanding of:
- Why the algorithm terminates
- Why it produces the correct result
- How many steps it takes (complexity analysis)
- Connection to Bezout's identity (optional but valuable)
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.NUMBER_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=60.0
        )
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical understanding in the GCD implementation."""
        score = 0.0
        feedback_parts = []
        
        # Check for Euclidean algorithm explanation
        if self._contains_euclidean_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Euclidean algorithm explanation found")
        else:
            feedback_parts.append("✗ Missing explanation of Euclidean algorithm principle")
        
        # Check for complexity analysis
        if self._contains_complexity_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Complexity analysis present")
        else:
            feedback_parts.append("✗ Missing O(log(min(a,b))) complexity analysis")
        
        # Check for mathematical properties understanding
        if self._contains_gcd_properties(submission):
            score += 0.25
            feedback_parts.append("✓ GCD properties explained")
        else:
            feedback_parts.append("✗ Missing explanation of GCD mathematical properties")
        
        # Check for algorithm termination proof
        if self._contains_termination_proof(submission):
            score += 0.15
            feedback_parts.append("✓ Algorithm termination explained")
        else:
            feedback_parts.append("✗ Missing proof of algorithm termination")
        
        # Bonus: Bezout's identity connection
        if self._mentions_bezout_identity(submission):
            score += 0.1
            feedback_parts.append("✓ Bonus: Connected to Bezout's identity")
        
        return min(score, 1.0), "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Verify the implementation uses Euclidean algorithm (not brute force)."""
        # Parse the code to check for Euclidean algorithm pattern
        if self._uses_euclidean_algorithm(submission):
            return True, "Euclidean algorithm implementation detected"
        else:
            return False, "Must use Euclidean algorithm (not brute force or library functions)"
    
    def extract_patterns(self, submission: str) -> Dict[str, List[str]]:
        """Extract mathematical and algorithmic patterns from the solution."""
        patterns = {
            "algorithmic": [],
            "mathematical": [],
            "optimization": [],
            "theoretical": []
        }
        
        # Algorithmic patterns
        if "while" in submission and "!= 0" in submission:
            patterns["algorithmic"].append("iterative_euclidean")
        if self._has_recursive_pattern(submission):
            patterns["algorithmic"].append("recursive_euclidean")
        if self._has_tail_recursion(submission):
            patterns["algorithmic"].append("tail_recursion")
        
        # Mathematical patterns
        if "%" in submission or "mod" in submission.lower():
            patterns["mathematical"].append("modular_reduction")
        if self._swaps_arguments(submission):
            patterns["mathematical"].append("argument_ordering")
        
        # Optimization patterns
        if self._handles_zero_early(submission):
            patterns["optimization"].append("early_termination")
        if self._optimizes_for_equal_args(submission):
            patterns["optimization"].append("equal_args_optimization")
        
        # Theoretical connections
        if "bezout" in submission.lower():
            patterns["theoretical"].append("bezout_identity")
        if "coprime" in submission.lower() or "relatively prime" in submission.lower():
            patterns["theoretical"].append("coprimality")
        
        return patterns
    
    def _contains_euclidean_explanation(self, code: str) -> bool:
        """Check if code explains the Euclidean algorithm."""
        patterns = [
            r"euclidean.*algorithm",
            r"gcd\(a,\s*b\)\s*=\s*gcd\(b,\s*a\s*mod\s*b\)",
            r"gcd\(a,\s*b\)\s*=\s*gcd\(b,\s*a\s*%\s*b\)",
            r"principle.*gcd.*remainder"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _contains_complexity_analysis(self, code: str) -> bool:
        """Check for complexity analysis."""
        patterns = [
            r"o\(log.*min\(a,\s*b\)\)",
            r"logarithmic.*complexity",
            r"fibonacci.*worst.*case",
            r"steps.*proportional.*log"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _contains_gcd_properties(self, code: str) -> bool:
        """Check for GCD properties explanation."""
        patterns = [
            r"gcd\(a,\s*b\)\s*=\s*gcd\(b,\s*a\)",
            r"gcd\(a,\s*0\)\s*=\s*a",
            r"commutative.*property",
            r"gcd.*properties"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _contains_termination_proof(self, code: str) -> bool:
        """Check for algorithm termination explanation."""
        patterns = [
            r"terminat",
            r"remainder.*decreas",
            r"eventually.*reach.*zero",
            r"finite.*steps"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _mentions_bezout_identity(self, code: str) -> bool:
        """Check if Bezout's identity is mentioned."""
        patterns = [
            r"bezout",
            r"bézout",
            r"extended.*euclidean",
            r"ax\s*\+\s*by\s*=\s*gcd"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _uses_euclidean_algorithm(self, code: str) -> bool:
        """Check if the implementation uses Euclidean algorithm."""
        # Look for characteristic patterns
        has_modulo = "%" in code or "mod" in code.lower()
        has_loop = "while" in code or ("def" in code and "return" in code and "gcd" in code)
        
        # Check for brute force patterns (negative indicators)
        brute_force_patterns = [
            r"for.*range.*min",
            r"i\s*in\s*range.*1",
            r"factor.*list",
            r"divisors"
        ]
        has_brute_force = any(re.search(pattern, code.lower()) for pattern in brute_force_patterns)
        
        # Check for library usage (negative indicator)
        uses_library = "math.gcd" in code or "import math" in code
        
        return has_modulo and has_loop and not has_brute_force and not uses_library
    
    def _has_recursive_pattern(self, code: str) -> bool:
        """Check if solution uses recursion."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "gcd":
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Name) and child.func.id == "gcd":
                                return True
        except:
            pass
        return False
    
    def _has_tail_recursion(self, code: str) -> bool:
        """Check for tail recursion pattern."""
        if not self._has_recursive_pattern(code):
            return False
        
        # Simple heuristic: check if recursive call is in return statement
        return bool(re.search(r"return\s+gcd\s*\(", code))
    
    def _swaps_arguments(self, code: str) -> bool:
        """Check if implementation handles argument ordering."""
        patterns = [
            r"if\s+a\s*<\s*b",
            r"if\s+b\s*>\s*a",
            r"swap.*a.*b",
            r"a,\s*b\s*=\s*b,\s*a"
        ]
        return any(re.search(pattern, code) for pattern in patterns)
    
    def _handles_zero_early(self, code: str) -> bool:
        """Check for early termination on zero."""
        patterns = [
            r"if\s+b\s*==\s*0",
            r"if\s+not\s+b",
            r"while\s+b\s*!=\s*0",
            r"while\s+b:"
        ]
        return any(re.search(pattern, code) for pattern in patterns)
    
    def _optimizes_for_equal_args(self, code: str) -> bool:
        """Check if solution optimizes for equal arguments."""
        patterns = [
            r"if\s+a\s*==\s*b",
            r"a\s*==\s*b.*return\s+a"
        ]
        return any(re.search(pattern, code) for pattern in patterns)