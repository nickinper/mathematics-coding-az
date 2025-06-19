"""Tests for mathematical coding challenges."""

import pytest
from src.challenges.level1.number_theory import RSAChallenge, ModularExponentiationChallenge
from src.core.challenge import ChallengeLevel, MathematicalDomain


class TestRSAChallenge:
    """Test suite for RSA Challenge."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.challenge = RSAChallenge()
    
    def test_challenge_properties(self):
        """Test basic challenge properties."""
        assert self.challenge.title == "RSA Encryption from Scratch"
        assert self.challenge.level == ChallengeLevel.FOUNDATION
        assert self.challenge.domain == MathematicalDomain.NUMBER_THEORY
        assert len(self.challenge.mathematical_requirements) == 4
        assert len(self.challenge.test_cases) == 3
    
    def test_mathematical_reasoning_verification(self):
        """Test mathematical reasoning verification."""
        # Test submission with good mathematical reasoning
        good_submission = '''
        """
        RSA Implementation with Mathematical Proof
        
        Fermat's Little Theorem states that if p is prime and a is not divisible by p,
        then a^(p-1) ≡ 1 (mod p). This is the foundation of RSA decryption.
        
        For RSA, we have (m^e)^d ≡ m (mod n) by Euler's theorem since ed ≡ 1 (mod φ(n)).
        
        The modular exponentiation uses binary exponentiation for O(log n) complexity.
        We use the Miller-Rabin primality test for generating primes.
        The Euler's totient function φ(n) = (p-1)(q-1) for n = p*q.
        """
        
        def mod_exp(base, exp, mod):
            # Binary exponentiation - O(log exp)
            result = 1
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                base = (base * base) % mod
                exp //= 2
            return result
        '''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(good_submission)
        assert score > 0.8  # Should score highly
        assert "Fermat's Little Theorem" in feedback
        
        # Test submission with poor mathematical reasoning
        poor_submission = '''
        def encrypt(message):
            return message + "encrypted"
        '''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(poor_submission)
        assert score < 0.3  # Should score poorly
        assert "Missing" in feedback
    
    def test_complexity_analysis(self):
        """Test complexity analysis."""
        # Good implementation with binary exponentiation
        efficient_code = '''
        def mod_exp(base, exp, mod):
            result = 1
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                base = (base * base) % mod
                exp //= 2
            return result
        '''
        
        meets_req, analysis = self.challenge.analyze_complexity(efficient_code)
        assert meets_req == True
        assert "O(log n)" in analysis or "binary" in analysis.lower()
        
        # Inefficient implementation
        inefficient_code = '''
        def mod_exp(base, exp, mod):
            result = 1
            for i in range(exp):
                result = (result * base) % mod
            return result
        '''
        
        meets_req, analysis = self.challenge.analyze_complexity(inefficient_code)
        assert meets_req == False
        assert "O(log n)" in analysis


class TestModularExponentiationChallenge:
    """Test suite for Modular Exponentiation Challenge."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.challenge = ModularExponentiationChallenge()
    
    def test_challenge_properties(self):
        """Test basic challenge properties."""
        assert "Modular Exponentiation" in self.challenge.title
        assert self.challenge.level == ChallengeLevel.FOUNDATION
        assert self.challenge.domain == MathematicalDomain.NUMBER_THEORY
        assert len(self.challenge.test_cases) == 3
    
    def test_mathematical_reasoning_verification(self):
        """Test mathematical reasoning verification for modular exponentiation."""
        good_submission = '''
        """
        Binary Exponentiation Algorithm
        
        The square-and-multiply method works by representing the exponent
        in binary and using the property that:
        a^(2k) = (a^2)^k and a^(2k+1) = a * (a^2)^k
        
        This gives us O(log exp) complexity instead of O(exp).
        """
        '''
        
        score, feedback = self.challenge.verify_mathematical_reasoning(good_submission)
        assert score > 0.6
        assert "Square-and-multiply" in feedback or "Binary" in feedback
    
    def test_binary_exponentiation_detection(self):
        """Test detection of binary exponentiation algorithm."""
        binary_exp_code = '''
        def mod_exp(base, exp, modulus):
            result = 1
            base = base % modulus
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % modulus
                exp = exp >> 1
                base = (base * base) % modulus
            return result
        '''
        
        assert self.challenge._has_binary_exponentiation(binary_exp_code) == True
        
        naive_code = '''
        def mod_exp(base, exp, modulus):
            result = 1
            for i in range(exp):
                result = (result * base) % modulus
            return result
        '''
        
        assert self.challenge._has_binary_exponentiation(naive_code) == False


@pytest.fixture
def sample_test_function():
    """Sample function for testing challenge evaluation."""
    def mod_exp(base, exp, modulus):
        """Efficient modular exponentiation."""
        result = 1
        base = base % modulus
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % modulus
            exp = exp >> 1
            base = (base * base) % modulus
        return result
    
    return mod_exp


class TestChallengeEvaluation:
    """Test challenge evaluation system."""
    
    def test_modular_exp_evaluation(self, sample_test_function):
        """Test evaluation of modular exponentiation function."""
        challenge = ModularExponentiationChallenge()
        
        # Test function against challenge test cases
        for test_case in challenge.test_cases:
            if isinstance(test_case.input_data, tuple):
                base, exp, mod = test_case.input_data
                result = sample_test_function(base, exp, mod)
                expected = test_case.expected_output
                
                # For large numbers, use Python's built-in pow for comparison
                if exp > 1000:
                    expected = pow(base, exp, mod)
                
                assert result == expected, f"Failed for input {test_case.input_data}"
    
    def test_challenge_result_creation(self):
        """Test creation of challenge results."""
        challenge = RSAChallenge()
        
        # Mock submission code
        submission_code = '''
        def rsa_implementation():
            # Fermat's Little Theorem ensures decryption works
            # Using Miller-Rabin for primality testing
            # Binary exponentiation for O(log n) complexity
            pass
        '''
        
        # Mock student function (would normally be extracted from submission)
        def mock_student_function(input_data):
            return input_data.get("message", "")
        
        # Evaluate submission
        result = challenge.evaluate_submission(submission_code, mock_student_function)
        
        assert hasattr(result, 'passed')
        assert hasattr(result, 'mathematical_score')
        assert hasattr(result, 'total_score')
        assert hasattr(result, 'feedback')
        assert isinstance(result.feedback, str)


def test_challenge_integration():
    """Integration test for the complete challenge system."""
    challenge = ModularExponentiationChallenge()
    
    # Sample working implementation
    working_code = '''
    def mod_exp(base, exp, modulus):
        """
        Fast modular exponentiation using binary method.
        Time complexity: O(log exp)
        
        Mathematical basis: Binary representation of exponent
        allows us to compute result efficiently using
        square-and-multiply algorithm.
        """
        result = 1
        base = base % modulus
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % modulus
            exp = exp >> 1
            base = (base * base) % modulus
        return result
    '''
    
    # Test mathematical reasoning
    math_score, math_feedback = challenge.verify_mathematical_reasoning(working_code)
    assert math_score > 0.5
    
    # Test complexity analysis
    complexity_ok, complexity_feedback = challenge.analyze_complexity(working_code)
    assert complexity_ok == True