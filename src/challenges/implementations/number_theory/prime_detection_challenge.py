"""
Prime Detection Challenge - Multiple Algorithms and Analysis
"""

import re
import ast
import math
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain,
    MathematicalRequirement, TestCase
)


class PrimeDetectionChallenge(Challenge):
    """Prime detection using multiple algorithms with complexity analysis."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Trial Division Optimization",
                description="Implement optimized trial division up to √n with proof of correctness",
                proof_required=True,
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Miller-Rabin Primality Test",
                description="Implement probabilistic primality testing with error analysis",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Sieve of Eratosthenes",
                description="Implement the sieve for finding all primes up to n",
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Prime Number Theorem",
                description="Understand the distribution of primes: π(n) ≈ n/ln(n)",
                proof_required=False
            )
        ]
        
        test_cases = [
            # Small primes
            TestCase(
                input_data={"n": 2, "method": "is_prime"},
                expected_output=True,
                description="Smallest prime"
            ),
            TestCase(
                input_data={"n": 17, "method": "is_prime"},
                expected_output=True,
                description="Small prime"
            ),
            # Composites
            TestCase(
                input_data={"n": 1, "method": "is_prime"},
                expected_output=False,
                description="1 is not prime"
            ),
            TestCase(
                input_data={"n": 91, "method": "is_prime"},
                expected_output=False,
                description="7 × 13 = 91"
            ),
            # Large primes
            TestCase(
                input_data={"n": 1000000007, "method": "is_prime"},
                expected_output=True,
                description="Large prime (10^9 + 7)"
            ),
            TestCase(
                input_data={"n": 2147483647, "method": "is_prime"},
                expected_output=True,
                description="Mersenne prime (2^31 - 1)"
            ),
            # Carmichael numbers (pseudoprimes)
            TestCase(
                input_data={"n": 561, "method": "is_prime"},
                expected_output=False,
                description="Carmichael number (3×11×17)"
            ),
            # Sieve test
            TestCase(
                input_data={"n": 30, "method": "sieve"},
                expected_output=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
                description="All primes up to 30"
            ),
            # Prime counting
            TestCase(
                input_data={"n": 100, "method": "count_primes"},
                expected_output=25,
                description="π(100) = 25"
            )
        ]
        
        super().__init__(
            title="Prime Detection - Multiple Algorithms",
            description="""
Implement multiple prime detection algorithms with mathematical analysis.

Requirements:
1. Optimized trial division with √n optimization
2. Miller-Rabin probabilistic primality test
3. Sieve of Eratosthenes for generating prime lists
4. Understanding of prime distribution

Your implementation should include:

```python
class PrimeDetector:
    def is_prime_trial(self, n: int) -> bool:
        '''Deterministic trial division'''
        pass
    
    def is_prime_miller_rabin(self, n: int, k: int = 5) -> bool:
        '''Probabilistic Miller-Rabin test with k rounds'''
        pass
    
    def sieve_of_eratosthenes(self, n: int) -> List[int]:
        '''Generate all primes up to n'''
        pass
    
    def count_primes(self, n: int) -> int:
        '''Count primes ≤ n using efficient method'''
        pass
```

Mathematical Analysis Required:
- Prove why checking up to √n is sufficient
- Analyze Miller-Rabin error probability: at most 4^(-k)
- Prove Sieve of Eratosthenes correctness
- Discuss prime density and distribution

Performance Requirements:
- Trial division: O(√n)
- Miller-Rabin: O(k log³ n)
- Sieve: O(n log log n)
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.NUMBER_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=180.0
        )
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical understanding of primality testing."""
        score = 0.0
        feedback_parts = []
        
        # Check for √n optimization explanation
        if self._explains_sqrt_optimization(submission):
            score += 0.25
            feedback_parts.append("✓ √n optimization explained")
        else:
            feedback_parts.append("✗ Missing explanation of why √n is sufficient")
        
        # Check for Miller-Rabin understanding
        if self._explains_miller_rabin(submission):
            score += 0.25
            feedback_parts.append("✓ Miller-Rabin algorithm explained")
        else:
            feedback_parts.append("✗ Missing Miller-Rabin mathematical foundation")
        
        # Check for error probability analysis
        if self._analyzes_error_probability(submission):
            score += 0.2
            feedback_parts.append("✓ Error probability analysis present")
        else:
            feedback_parts.append("✗ Missing Miller-Rabin error probability analysis")
        
        # Check for sieve correctness
        if self._explains_sieve_correctness(submission):
            score += 0.2
            feedback_parts.append("✓ Sieve correctness explained")
        else:
            feedback_parts.append("✗ Missing Sieve of Eratosthenes proof")
        
        # Bonus: Prime Number Theorem
        if self._mentions_prime_distribution(submission):
            score += 0.1
            feedback_parts.append("✓ Bonus: Prime distribution discussed")
        
        return min(score, 1.0), "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Verify efficient implementations."""
        issues = []
        
        if not self._has_sqrt_optimization(submission):
            issues.append("Trial division must use √n optimization")
        
        if not self._has_efficient_sieve(submission):
            issues.append("Sieve must be O(n log log n)")
        
        if issues:
            return False, "; ".join(issues)
        return True, "Efficient implementations detected"
    
    def extract_patterns(self, submission: str) -> Dict[str, List[str]]:
        """Extract patterns from prime detection algorithms."""
        patterns = {
            "algorithmic": [],
            "mathematical": [],
            "optimization": [],
            "theoretical": []
        }
        
        # Algorithmic patterns
        if self._has_trial_division(submission):
            patterns["algorithmic"].append("trial_division")
        if self._has_miller_rabin_pattern(submission):
            patterns["algorithmic"].append("miller_rabin")
        if self._has_sieve_pattern(submission):
            patterns["algorithmic"].append("sieve_of_eratosthenes")
        
        # Mathematical patterns
        if self._uses_modular_arithmetic(submission):
            patterns["mathematical"].append("modular_arithmetic")
        if self._uses_number_theory(submission):
            patterns["mathematical"].append("number_theory")
        
        # Optimization patterns
        if self._has_sqrt_optimization(submission):
            patterns["optimization"].append("sqrt_bound")
        if self._has_wheel_factorization(submission):
            patterns["optimization"].append("wheel_factorization")
        if self._has_early_exit(submission):
            patterns["optimization"].append("early_termination")
        
        # Theoretical patterns
        if self._mentions_fermat_test(submission):
            patterns["theoretical"].append("fermat_primality")
        if self._mentions_prime_distribution(submission):
            patterns["theoretical"].append("prime_number_theorem")
        
        return patterns
    
    def _explains_sqrt_optimization(self, code: str) -> bool:
        """Check for √n optimization explanation."""
        patterns = [
            r"sqrt|square.*root",
            r"if.*divisor.*>.*sqrt",
            r"factor.*pair",
            r"a\s*\*\s*b\s*=\s*n.*one.*<=.*sqrt"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _explains_miller_rabin(self, code: str) -> bool:
        """Check for Miller-Rabin explanation."""
        patterns = [
            r"miller.*rabin",
            r"witness",
            r"n-1\s*=\s*2\^r\s*\*\s*d",
            r"fermat.*test.*strong"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _analyzes_error_probability(self, code: str) -> bool:
        """Check for error probability analysis."""
        patterns = [
            r"error.*probability",
            r"4\^\(-k\)|1/4\^k",
            r"false.*positive.*rate",
            r"probabilistic.*guarantee"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _explains_sieve_correctness(self, code: str) -> bool:
        """Check for sieve correctness explanation."""
        patterns = [
            r"sieve.*eratosthenes",
            r"mark.*multiples",
            r"composite.*eliminated",
            r"unmarked.*prime"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _mentions_prime_distribution(self, code: str) -> bool:
        """Check for prime distribution discussion."""
        patterns = [
            r"prime.*number.*theorem",
            r"π\(n\)|pi\(n\)",
            r"n/ln\(n\)|n/log\(n\)",
            r"prime.*density"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_sqrt_optimization(self, code: str) -> bool:
        """Check if trial division uses √n optimization."""
        patterns = [
            r"sqrt\(|math\.sqrt",
            r"i\s*\*\s*i\s*<=\s*n",
            r"while.*<=.*int\(.*\*\*.*0\.5"
        ]
        return any(re.search(pattern, code) for pattern in patterns)
    
    def _has_efficient_sieve(self, code: str) -> bool:
        """Check for efficient sieve implementation."""
        # Look for characteristic sieve pattern
        has_array = "True" in code and "False" in code
        has_marking = re.search(r"for.*range.*\w+\s*\*\s*\w+|for.*range.*i\s*\*\s*i", code)
        has_sqrt_limit = "sqrt" in code or "**" in code
        return has_array and bool(has_marking) and has_sqrt_limit
    
    def _has_trial_division(self, code: str) -> bool:
        """Check for trial division pattern."""
        return bool(re.search(r"for.*range.*2.*sqrt|while.*<=.*sqrt", code))
    
    def _has_miller_rabin_pattern(self, code: str) -> bool:
        """Check for Miller-Rabin implementation."""
        patterns = [
            r"def.*miller.*rabin",
            r"witness|composite",
            r"pow.*n-1.*n"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_sieve_pattern(self, code: str) -> bool:
        """Check for sieve implementation."""
        return bool(re.search(r"sieve|eratosthenes", code.lower()))
    
    def _uses_modular_arithmetic(self, code: str) -> bool:
        """Check for modular arithmetic usage."""
        return "%" in code or "mod" in code.lower()
    
    def _uses_number_theory(self, code: str) -> bool:
        """Check for number theory concepts."""
        concepts = ["gcd", "coprime", "factor", "divisor"]
        return any(concept in code.lower() for concept in concepts)
    
    def _has_wheel_factorization(self, code: str) -> bool:
        """Check for wheel factorization optimization."""
        return bool(re.search(r"wheel|2.*3.*5|skip.*even", code.lower()))
    
    def _has_early_exit(self, code: str) -> bool:
        """Check for early termination patterns."""
        patterns = [
            r"if.*n.*<=.*1.*return",
            r"if.*n.*==.*2.*return.*True",
            r"if.*n.*%.*2.*==.*0.*return"
        ]
        return any(re.search(pattern, code) for pattern in patterns)
    
    def _mentions_fermat_test(self, code: str) -> bool:
        """Check for Fermat primality test mention."""
        return bool(re.search(r"fermat.*test|a\^\(n-1\).*mod.*n", code.lower()))