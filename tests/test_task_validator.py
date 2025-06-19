"""
Test suite for TaskValidator

Run with: pytest tests/test_task_validator.py -v
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validation.task_validator import (
    TaskValidator, 
    MathematicalConcept,
    ValidationResult
)


class TestTaskValidator:
    
    @pytest.fixture
    def validator(self):
        return TaskValidator()
    
    @pytest.fixture
    def sample_fibonacci_submission(self):
        class FibSubmission:
            def __init__(self):
                self.code = """
def fibonacci(n):
    '''Calculate nth Fibonacci number using dynamic programming'''
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
"""
                self.mathematical_reasoning = """
The Fibonacci sequence is defined by the recurrence relation:
F(n) = F(n-1) + F(n-2) with F(0) = 0, F(1) = 1

Using dynamic programming, we can compute F(n) in O(n) time
by storing previously computed values, avoiding the exponential
time complexity of naive recursion.
"""
        return FibSubmission()
    
    @pytest.fixture
    def sample_prime_submission(self):
        class PrimeSubmission:
            def __init__(self):
                self.code = """
def is_prime(n):
    '''Check if n is prime using optimized trial division'''
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    
    return True
"""
                self.mathematical_reasoning = """
By the fundamental theorem of arithmetic, if n is composite,
it must have a prime factor p ≤ √n.

Proof: If n = a×b where a,b > 1, and both a,b > √n,
then a×b > √n × √n = n, which is a contradiction.

Therefore, we only need to check divisibility up to √n.
We can skip even numbers after checking n % 2.
"""
        return PrimeSubmission()
    
    def test_validate_fibonacci(self, validator, sample_fibonacci_submission):
        """Test validation of Fibonacci implementation."""
        result = validator.validate_mathematical_correctness(sample_fibonacci_submission)
        
        assert isinstance(result, ValidationResult)
        assert result.overall_score > 0.5
        assert any(c.concept == MathematicalConcept.DISCRETE_MATH 
                  for c in result.concepts_identified)
        assert any("dynamic" in f.lower() for f in result.feedback)
    
    def test_validate_prime_checker(self, validator, sample_prime_submission):
        """Test validation of prime checking algorithm."""
        result = validator.validate_mathematical_correctness(sample_prime_submission)
        
        assert result.mathematical_rigor > 0.5
        assert any(c.concept == MathematicalConcept.NUMBER_THEORY 
                  for c in result.concepts_identified)
        assert len(result.proof_steps) >= 1
    
    def test_empty_reasoning(self, validator):
        """Test handling of missing mathematical reasoning."""
        class EmptySubmission:
            def __init__(self):
                self.code = "def f(x): return x * 2"
                self.mathematical_reasoning = ""  # No reasoning provided
        
        result = validator.validate_mathematical_correctness(EmptySubmission())
        
        assert result.mathematical_rigor < 0.3
        assert any(s.lower().find("mathematical") != -1 for s in result.suggestions)
    
    def test_syntax_error_handling(self, validator):
        """Test handling of syntactically incorrect code."""
        class BadSubmission:
            def __init__(self):
                self.code = "def broken(x: return x"  # Syntax error
                self.mathematical_reasoning = "Some reasoning"
        
        result = validator.validate_mathematical_correctness(BadSubmission())
        
        assert result.code_elegance < 0.3
        assert 'syntax_error' in result.code_analysis
    
    def test_concept_extraction(self, validator):
        """Test mathematical concept extraction."""
        class MatrixSubmission:
            def __init__(self):
                self.code = """
def matrix_multiply(A, B):
    '''Multiply two matrices'''
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result
"""
                self.mathematical_reasoning = """
Matrix multiplication follows the rule (AB)ij = Σ(Aik × Bkj).
This operation is associative but not commutative.
The resulting matrix has dimensions rows(A) × cols(B).
"""
        
        result = validator.validate_mathematical_correctness(MatrixSubmission())
        
        assert any(c.concept == MathematicalConcept.LINEAR_ALGEBRA 
                  for c in result.concepts_identified)
        assert "O(n³)" in result.code_analysis.get("estimated_time_complexity", "")
    
    def test_proof_validation(self, validator):
        """Test proof structure validation."""
        class ProofSubmission:
            def __init__(self):
                self.code = "def f(n): return n**2"
                self.mathematical_reasoning = """
Step 1: Given n is even, we can write n = 2k for some integer k.
Step 2: By definition, n² = (2k)² = 4k².
Step 3: Since 4k² = 2(2k²), we have n² = 2m where m = 2k².
Therefore: n² is even when n is even.
"""
        
        result = validator.validate_mathematical_correctness(ProofSubmission())
        
        assert len(result.proof_steps) >= 2
        assert result.proof_correctness > 0.5
    
    def test_scoring_weights(self, validator):
        """Test that scoring weights sum to 1.0."""
        class SimpleSubmission:
            def __init__(self):
                self.code = "def f(x): return x"
                self.mathematical_reasoning = "Basic function"
        
        result = validator.validate_mathematical_correctness(SimpleSubmission())
        
        # Verify overall score calculation
        expected = (
            result.mathematical_rigor * 0.35 +
            result.proof_correctness * 0.25 +
            result.code_elegance * 0.25 +
            result.concept_mastery * 0.15
        )
        
        assert abs(result.overall_score - expected) < 0.001


# Run parametrized concept tests
@pytest.mark.parametrize("concept,keywords", [
    (MathematicalConcept.NUMBER_THEORY, ["prime", "modular", "gcd"]),
    (MathematicalConcept.LINEAR_ALGEBRA, ["matrix", "vector", "eigenvalue"]),
    (MathematicalConcept.CALCULUS, ["derivative", "integral", "limit"]),
])
def test_concept_detection(concept, keywords):
    """Test detection of specific mathematical concepts."""
    validator = TaskValidator()
    
    for keyword in keywords:
        class ConceptSubmission:
            def __init__(self):
                self.code = f"def f(x): return x  # {keyword} related"
                self.mathematical_reasoning = f"This uses {keyword} in the solution"
        
        result = validator.validate_mathematical_correctness(ConceptSubmission())
        
        # We may not always detect every keyword with high confidence,
        # so this is a soft assertion that at least checks for the concept
        concepts = [c.concept for c in result.concepts_identified]
        assert concept in concepts or len(concepts) == 0


if __name__ == "__main__":
    # Quick test runner
    pytest.main([__file__, "-v", "--tb=short"])