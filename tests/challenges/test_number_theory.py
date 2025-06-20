"""
Test suite for Number Theory challenges
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.challenges.implementations.number_theory import (
    GCDBasicsChallenge,
    ModularArithmeticChallenge,
    PrimeDetectionChallenge
)


class TestGCDBasicsChallenge:
    """Test GCD Basics Challenge verification."""
    
    def setup_method(self):
        self.challenge = GCDBasicsChallenge()
    
    def test_good_solution_verification(self):
        """Test verification of a well-documented solution."""
        good_solution = '''
def gcd(a: int, b: int) -> int:
    """
    Calculate GCD using the Euclidean algorithm.
    
    The Euclidean algorithm is based on the principle:
    gcd(a, b) = gcd(b, a mod b)
    
    This works because any divisor of a and b also divides a - qb.
    
    Complexity: O(log(min(a,b)))
    Proof: Each iteration reduces the smaller number by at least half,
    so the algorithm terminates in logarithmic steps.
    
    The algorithm will terminate because b decreases with each iteration
    and will eventually reach 0.
    """
    # Handle edge cases
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    
    # Make sure we work with positive numbers
    a, b = abs(a), abs(b)
    
    # Apply Euclidean algorithm
    while b != 0:
        a, b = b, a % b
    
    return a
'''
        
        # Test mathematical reasoning
        score, feedback = self.challenge.verify_mathematical_reasoning(good_solution)
        assert score >= 0.6, f"Good solution should score well, got {score}"
        assert "✓" in feedback, "Should have positive feedback"
        
        # Test complexity analysis
        is_efficient, complexity_feedback = self.challenge.analyze_complexity(good_solution)
        assert is_efficient, "Should detect Euclidean algorithm"
        
        # Test pattern extraction
        patterns = self.challenge.extract_patterns(good_solution)
        assert "iterative_euclidean" in patterns["algorithmic"]
        assert "modular_reduction" in patterns["mathematical"]
        assert "early_termination" in patterns["optimization"]
    
    def test_brute_force_rejection(self):
        """Test that brute force solutions are rejected."""
        brute_force = '''
def gcd(a: int, b: int) -> int:
    """Find GCD by checking all divisors."""
    result = 1
    for i in range(1, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            result = i
    return result
'''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(brute_force)
        assert score < 0.3, "Brute force should score poorly"
        
        is_efficient, feedback = self.challenge.analyze_complexity(brute_force)
        assert not is_efficient, "Should reject brute force approach"
        assert "Euclidean algorithm" in feedback
    
    def test_library_usage_rejection(self):
        """Test that using math.gcd is rejected."""
        library_solution = '''
import math

def gcd(a: int, b: int) -> int:
    """Just use the library."""
    return math.gcd(a, b)
'''
        
        is_valid, feedback = self.challenge.analyze_complexity(library_solution)
        assert not is_valid, "Should reject library usage"
    
    def test_recursive_solution(self):
        """Test recognition of recursive implementation."""
        recursive_solution = '''
def gcd(a: int, b: int) -> int:
    """
    Recursive Euclidean algorithm.
    
    Mathematical principle: gcd(a, b) = gcd(b, a % b)
    Base case: gcd(a, 0) = a
    
    This is tail recursive and has O(log(min(a,b))) complexity.
    """
    if b == 0:
        return abs(a)
    return gcd(b, a % b)
'''
        
        patterns = self.challenge.extract_patterns(recursive_solution)
        assert "recursive_euclidean" in patterns["algorithmic"]
        assert "tail_recursion" in patterns["algorithmic"]
        
        score, _ = self.challenge.verify_mathematical_reasoning(recursive_solution)
        assert score >= 0.4


class TestModularArithmeticChallenge:
    """Test Modular Arithmetic Challenge verification."""
    
    def setup_method(self):
        self.challenge = ModularArithmeticChallenge()
    
    def test_complete_implementation(self):
        """Test verification of complete modular arithmetic system."""
        complete_solution = '''
class ModularArithmetic:
    """
    Modular arithmetic operations demonstrating ring properties.
    
    (Z/nZ, +, ×) forms a ring because:
    - Closure: (a + b) mod n and (a × b) mod n are in Z/nZ
    - Associativity: Both + and × are associative
    - Commutativity: Both + and × are commutative
    - Identity: 0 for addition, 1 for multiplication
    - Additive inverse: For every a, there exists -a ≡ n-a (mod n)
    - Distributivity: a × (b + c) ≡ (a × b) + (a × c) (mod n)
    """
    
    def __init__(self, modulus: int):
        self.n = modulus
        self._inverse_cache = {}
    
    def add(self, a: int, b: int) -> int:
        """Modular addition."""
        return (a + b) % self.n
    
    def multiply(self, a: int, b: int) -> int:
        """Modular multiplication."""
        return (a * b) % self.n
    
    def power(self, a: int, b: int) -> int:
        """
        Fast modular exponentiation using binary method.
        Time complexity: O(log b)
        """
        result = 1
        a = a % self.n
        while b > 0:
            if b % 2 == 1:
                result = (result * a) % self.n
            b = b >> 1
            a = (a * a) % self.n
        return result
    
    def inverse(self, a: int) -> Optional[int]:
        """
        Find modular multiplicative inverse using Extended Euclidean Algorithm.
        
        The inverse exists if and only if gcd(a, n) = 1.
        We find x, y such that ax + ny = gcd(a, n).
        If gcd = 1, then ax ≡ 1 (mod n), so x is the inverse.
        
        For prime modulus, we can also use Fermat's Little Theorem:
        a^(p-1) ≡ 1 (mod p), so a^(p-2) ≡ a^(-1) (mod p)
        """
        if a in self._inverse_cache:
            return self._inverse_cache[a]
        
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % self.n, self.n)
        
        if gcd != 1:
            return None  # No inverse exists
        
        inverse = (x % self.n + self.n) % self.n
        self._inverse_cache[a] = inverse
        return inverse
'''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(complete_solution)
        assert score >= 0.8, f"Complete solution should score well, got {score}"
        assert "Ring properties explained" in feedback
        assert "Extended Euclidean Algorithm implemented" in feedback
        
        patterns = self.challenge.extract_patterns(complete_solution)
        assert "extended_euclidean" in patterns["algorithmic"]
        assert "binary_exponentiation" in patterns["algorithmic"]
        assert "ring_operations" in patterns["mathematical"]
        assert "inverse_caching" in patterns["optimization"]
    
    def test_fermat_optimization(self):
        """Test detection of Fermat's theorem optimization."""
        fermat_solution = '''
def inverse(self, a: int) -> Optional[int]:
    """
    For prime modulus, use Fermat's Little Theorem:
    Since a^(p-1) ≡ 1 (mod p) for prime p and gcd(a,p) = 1,
    we have a^(p-2) ≡ a^(-1) (mod p).
    
    This is more efficient than Extended Euclidean for large primes.
    """
    if self.is_prime(self.n):
        return self.power(a, self.n - 2)
    else:
        # Fall back to Extended Euclidean
        return self.inverse_extended_gcd(a)
'''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(fermat_solution)
        assert "Fermat's Little Theorem mentioned" in feedback
        
        patterns = self.challenge.extract_patterns(fermat_solution)
        assert "fermat_optimization" in patterns["optimization"]


class TestPrimeDetectionChallenge:
    """Test Prime Detection Challenge verification."""
    
    def setup_method(self):
        self.challenge = PrimeDetectionChallenge()
    
    def test_comprehensive_solution(self):
        """Test verification of solution with multiple algorithms."""
        comprehensive_solution = '''
import math
import random

class PrimeDetector:
    """Multiple prime detection algorithms with analysis."""
    
    def is_prime_trial(self, n: int) -> bool:
        """
        Optimized trial division up to √n.
        
        Why √n is sufficient:
        If n = a × b and a ≤ b, then a ≤ √n.
        So if n has a factor, it must have one ≤ √n.
        
        Complexity: O(√n)
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # Check odd divisors up to √n
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def is_prime_miller_rabin(self, n: int, k: int = 5) -> bool:
        """
        Miller-Rabin probabilistic primality test.
        
        Based on Fermat's Little Theorem and its converse.
        Write n-1 = 2^r × d where d is odd.
        
        Error probability: At most 4^(-k) for k rounds.
        With k=5, error rate < 0.1%.
        
        Complexity: O(k log³ n)
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 = 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness loop
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False  # Composite
        
        return True  # Probably prime
    
    def sieve_of_eratosthenes(self, n: int) -> List[int]:
        """
        Generate all primes up to n.
        
        Algorithm: Mark all multiples of each prime as composite.
        Correctness: Every composite number has a prime factor,
        so it will be marked when we process that prime.
        
        Complexity: O(n log log n)
        """
        if n < 2:
            return []
        
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if is_prime[i]:
                # Mark multiples starting from i²
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        
        return [i for i in range(n + 1) if is_prime[i]]
    
    def count_primes(self, n: int) -> int:
        """
        Count primes ≤ n.
        
        By the Prime Number Theorem: π(n) ≈ n/ln(n)
        This gives us an approximation of prime density.
        """
        return len(self.sieve_of_eratosthenes(n))
'''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(comprehensive_solution)
        assert score >= 0.8, f"Comprehensive solution should score well, got {score}"
        assert "√n optimization explained" in feedback
        assert "Miller-Rabin algorithm explained" in feedback
        assert "Error probability analysis present" in feedback
        
        is_efficient, _ = self.challenge.analyze_complexity(comprehensive_solution)
        assert is_efficient, "Should recognize efficient implementations"
        
        patterns = self.challenge.extract_patterns(comprehensive_solution)
        assert "trial_division" in patterns["algorithmic"]
        assert "miller_rabin" in patterns["algorithmic"]
        assert "sieve_of_eratosthenes" in patterns["algorithmic"]
        assert "sqrt_bound" in patterns["optimization"]
    
    def test_inefficient_sieve(self):
        """Test detection of inefficient sieve implementation."""
        bad_sieve = '''
def sieve_of_eratosthenes(self, n: int) -> List[int]:
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for p in primes:
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes
'''
        
        is_efficient, feedback = self.challenge.analyze_complexity(bad_sieve)
        assert not is_efficient, "Should detect inefficient sieve"
        assert "O(n log log n)" in feedback


if __name__ == "__main__":
    pytest.main([__file__, "-v"])