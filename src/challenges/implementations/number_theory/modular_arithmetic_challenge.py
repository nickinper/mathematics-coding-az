"""
Modular Arithmetic Challenge - Ring Properties and Operations
"""

import re
import ast
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain,
    MathematicalRequirement, TestCase
)


class ModularArithmeticChallenge(Challenge):
    """Modular arithmetic operations demonstrating ring properties."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Ring Properties",
                description="Demonstrate that (Z/nZ, +, ×) forms a ring with closure, associativity, identity, and inverses",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Modular Inverse",
                description="Implement modular multiplicative inverse using Extended Euclidean Algorithm",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Chinese Remainder Theorem",
                description="Understand how to solve systems of congruences (bonus)",
                proof_required=False
            ),
            MathematicalRequirement(
                concept="Fermat's Little Theorem Application",
                description="Use Fermat's theorem for efficient modular exponentiation of inverses",
                proof_required=True
            )
        ]
        
        test_cases = [
            # Basic operations
            TestCase(
                input_data={"operation": "add", "a": 7, "b": 5, "n": 10},
                expected_output=2,
                description="Modular addition"
            ),
            TestCase(
                input_data={"operation": "multiply", "a": 7, "b": 5, "n": 10},
                expected_output=5,
                description="Modular multiplication"
            ),
            TestCase(
                input_data={"operation": "power", "a": 3, "b": 4, "n": 7},
                expected_output=4,
                description="Modular exponentiation"
            ),
            # Modular inverse
            TestCase(
                input_data={"operation": "inverse", "a": 3, "n": 11},
                expected_output=4,
                description="Modular inverse (3 * 4 ≡ 1 mod 11)"
            ),
            TestCase(
                input_data={"operation": "inverse", "a": 7, "n": 26},
                expected_output=15,
                description="Modular inverse with larger modulus"
            ),
            TestCase(
                input_data={"operation": "inverse", "a": 6, "n": 9},
                expected_output=None,
                description="No inverse exists (gcd(6,9) = 3 ≠ 1)"
            ),
            # Complex operations
            TestCase(
                input_data={"operation": "solve", "equation": "5x ≡ 3 (mod 11)"},
                expected_output=5,
                description="Solve linear congruence"
            )
        ]
        
        super().__init__(
            title="Modular Arithmetic - Ring Properties",
            description="""
Implement a comprehensive modular arithmetic system demonstrating ring properties.

Your implementation must include:
1. Basic operations: addition, multiplication, exponentiation (all mod n)
2. Modular multiplicative inverse using Extended Euclidean Algorithm
3. Proof that (Z/nZ, +, ×) forms a ring
4. Efficient algorithms using mathematical properties

Mathematical Requirements:
- Prove ring properties: closure, associativity, commutativity, identity, distributivity
- Implement Extended Euclidean Algorithm for finding inverses
- Show when inverses exist (gcd(a,n) = 1)
- Apply Fermat's Little Theorem for prime moduli

Function signature:
```python
class ModularArithmetic:
    def __init__(self, modulus: int):
        self.n = modulus
    
    def add(self, a: int, b: int) -> int:
        pass
    
    def multiply(self, a: int, b: int) -> int:
        pass
    
    def power(self, a: int, b: int) -> int:
        pass
    
    def inverse(self, a: int) -> Optional[int]:
        pass
```

Bonus: Implement Chinese Remainder Theorem solver
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.NUMBER_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=120.0
        )
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify understanding of ring theory and modular arithmetic."""
        score = 0.0
        feedback_parts = []
        
        # Check for ring properties explanation
        if self._contains_ring_properties(submission):
            score += 0.25
            feedback_parts.append("✓ Ring properties explained")
        else:
            feedback_parts.append("✗ Missing explanation of ring properties")
        
        # Check for Extended Euclidean Algorithm
        if self._contains_extended_euclidean(submission):
            score += 0.25
            feedback_parts.append("✓ Extended Euclidean Algorithm implemented")
        else:
            feedback_parts.append("✗ Missing Extended Euclidean Algorithm for inverses")
        
        # Check for inverse existence condition
        if self._explains_inverse_condition(submission):
            score += 0.2
            feedback_parts.append("✓ Inverse existence condition explained")
        else:
            feedback_parts.append("✗ Missing explanation of when inverses exist")
        
        # Check for Fermat's Little Theorem understanding
        if self._mentions_fermat_theorem(submission):
            score += 0.2
            feedback_parts.append("✓ Fermat's Little Theorem mentioned")
        else:
            feedback_parts.append("✗ Missing Fermat's Little Theorem application")
        
        # Bonus: Chinese Remainder Theorem
        if self._mentions_crt(submission):
            score += 0.1
            feedback_parts.append("✓ Bonus: Chinese Remainder Theorem discussed")
        
        return min(score, 1.0), "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Verify efficient implementation of modular operations."""
        if self._has_efficient_modpow(submission):
            return True, "Efficient modular exponentiation detected"
        else:
            return False, "Must use efficient modular exponentiation (O(log b))"
    
    def extract_patterns(self, submission: str) -> Dict[str, List[str]]:
        """Extract patterns related to modular arithmetic."""
        patterns = {
            "algorithmic": [],
            "mathematical": [],
            "optimization": [],
            "theoretical": []
        }
        
        # Algorithmic patterns
        if self._has_extended_gcd_pattern(submission):
            patterns["algorithmic"].append("extended_euclidean")
        if self._has_binary_exponentiation(submission):
            patterns["algorithmic"].append("binary_exponentiation")
        
        # Mathematical patterns
        if "%" in submission or "mod" in submission.lower():
            patterns["mathematical"].append("modular_reduction")
        if self._uses_ring_operations(submission):
            patterns["mathematical"].append("ring_operations")
        
        # Optimization patterns
        if self._caches_inverses(submission):
            patterns["optimization"].append("inverse_caching")
        if self._uses_fermat_for_primes(submission):
            patterns["optimization"].append("fermat_optimization")
        
        # Theoretical patterns
        if "ring" in submission.lower():
            patterns["theoretical"].append("ring_theory")
        if "chinese remainder" in submission.lower():
            patterns["theoretical"].append("crt")
        
        return patterns
    
    def _contains_ring_properties(self, code: str) -> bool:
        """Check for ring properties explanation."""
        ring_terms = [
            r"ring",
            r"closure",
            r"associativ",
            r"commutativ",
            r"identity.*element",
            r"distributiv"
        ]
        matches = sum(1 for term in ring_terms if re.search(term, code.lower()))
        return matches >= 3
    
    def _contains_extended_euclidean(self, code: str) -> bool:
        """Check for Extended Euclidean Algorithm."""
        patterns = [
            r"extended.*euclidean",
            r"bezout",
            r"ax\s*\+\s*by\s*=\s*gcd",
            r"def.*extended.*gcd"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _explains_inverse_condition(self, code: str) -> bool:
        """Check if code explains when modular inverses exist."""
        patterns = [
            r"gcd.*=.*1",
            r"coprime",
            r"relatively.*prime",
            r"inverse.*exists.*if"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _mentions_fermat_theorem(self, code: str) -> bool:
        """Check for Fermat's Little Theorem."""
        patterns = [
            r"fermat",
            r"a\^\(p-1\).*≡.*1",
            r"a\*\*\(p-1\).*%.*p.*==.*1",
            r"prime.*modulus"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _mentions_crt(self, code: str) -> bool:
        """Check for Chinese Remainder Theorem."""
        return bool(re.search(r"chinese.*remainder|crt", code.lower()))
    
    def _has_efficient_modpow(self, code: str) -> bool:
        """Check for efficient modular exponentiation."""
        # Look for binary exponentiation pattern
        patterns = [
            r"while.*exp|power|b.*>.*0",
            r"exp.*//.*2|exp.*>>.*1",
            r"result.*\*=.*base"
        ]
        matches = sum(1 for p in patterns if re.search(p, code))
        return matches >= 2
    
    def _has_extended_gcd_pattern(self, code: str) -> bool:
        """Check for extended GCD implementation."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if "extended" in node.name.lower() or "egcd" in node.name.lower():
                        # Check if it returns multiple values
                        for child in ast.walk(node):
                            if isinstance(child, ast.Return):
                                if isinstance(child.value, ast.Tuple):
                                    return True
        except:
            pass
        return False
    
    def _has_binary_exponentiation(self, code: str) -> bool:
        """Check for binary exponentiation pattern."""
        # Look for characteristic patterns of binary exponentiation
        patterns = [
            r"while.*b.*>.*0",
            r"b.*>>.*1|b.*//.*2",
            r"result.*\*.*a.*%"
        ]
        matches = sum(1 for p in patterns if re.search(p, code))
        return matches >= 2
    
    def _uses_ring_operations(self, code: str) -> bool:
        """Check if code implements ring operations."""
        ops = ["add", "multiply", "subtract"]
        return sum(1 for op in ops if op in code.lower()) >= 2
    
    def _caches_inverses(self, code: str) -> bool:
        """Check if implementation caches computed inverses."""
        cache_patterns = [
            r"cache|memo|stored",
            r"self\..*inverses.*=.*\{",
            r"@.*cache"
        ]
        return any(re.search(pattern, code.lower()) for pattern in cache_patterns)
    
    def _uses_fermat_for_primes(self, code: str) -> bool:
        """Check if Fermat's theorem is used for prime moduli."""
        fermat_patterns = [
            r"is.*prime.*fermat",
            r"pow.*p-2.*p",
            r"power.*n.*-.*2",
            r"a\*\*\(.*-2\).*%"
        ]
        return any(re.search(pattern, code.lower()) for pattern in fermat_patterns)