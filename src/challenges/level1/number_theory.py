"""Number Theory challenges focusing on RSA encryption implementation."""

import re
import random
from typing import Any, Tuple
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class RSAChallenge(Challenge):
    """RSA encryption implementation requiring deep number theory understanding."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Fermat's Little Theorem",
                description="Prove why a^(p-1) ≡ 1 (mod p) ensures RSA decryption works",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Modular Exponentiation",
                description="Implement fast modular exponentiation with O(log n) complexity",
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Prime Number Generation",
                description="Use Miller-Rabin primality test for key generation",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Euler's Totient Function",
                description="Calculate φ(n) for RSA key generation",
                proof_required=True
            )
        ]
        
        test_cases = [
            TestCase(
                input_data={"message": "HELLO", "bits": 512},
                expected_output="HELLO",
                description="Basic encryption/decryption"
            ),
            TestCase(
                input_data={"message": "MATHEMATICS", "bits": 1024},
                expected_output="MATHEMATICS", 
                description="Larger key size"
            ),
            TestCase(
                input_data={"message": "A" * 100, "bits": 2048},
                expected_output="A" * 100,
                description="Long message with large key"
            )
        ]
        
        super().__init__(
            title="RSA Encryption from Scratch",
            description="""
Implement RSA encryption/decryption from mathematical first principles.

Your implementation must include:
1. Prime generation using Miller-Rabin primality test
2. Fast modular exponentiation (must be O(log n))
3. Key generation with proper φ(n) calculation
4. Encryption and decryption functions

Mathematical Proof Requirements:
- Prove why Fermat's Little Theorem ensures decryption works
- Derive the mathematical basis for your modular exponentiation algorithm
- Prove the correctness of your Miller-Rabin implementation
- Analyze the security assumptions of your RSA implementation

Example Usage:
```python
rsa = RSA()
public_key, private_key = rsa.generate_keys(bits=1024)
ciphertext = rsa.encrypt("HELLO", public_key)
plaintext = rsa.decrypt(ciphertext, private_key)
assert plaintext == "HELLO"
```
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.NUMBER_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=600.0
        )
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in RSA implementation."""
        score = 0.0
        feedback_parts = []
        
        # Check for Fermat's Little Theorem proof
        if self._contains_fermats_proof(submission):
            score += 0.3
            feedback_parts.append("✓ Fermat's Little Theorem explanation found")
        else:
            feedback_parts.append("✗ Missing proof of why RSA decryption works (Fermat's Little Theorem)")
        
        # Check for modular exponentiation understanding
        if self._contains_modexp_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Modular exponentiation complexity analysis present")
        else:
            feedback_parts.append("✗ Missing analysis of modular exponentiation algorithm")
        
        # Check for Miller-Rabin understanding
        if self._contains_miller_rabin_proof(submission):
            score += 0.25
            feedback_parts.append("✓ Miller-Rabin primality test reasoning found")
        else:
            feedback_parts.append("✗ Missing mathematical justification for primality testing")
        
        # Check for Euler's totient understanding
        if self._contains_totient_calculation(submission):
            score += 0.2
            feedback_parts.append("✓ Euler's totient function properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of φ(n) calculation")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets O(log n) modular exponentiation requirement."""
        # Check for efficient modular exponentiation
        if self._has_fast_modexp(submission):
            return True, "Fast modular exponentiation (O(log n)) detected"
        else:
            return False, "Modular exponentiation must be O(log n) - use binary exponentiation"
    
    def _contains_fermats_proof(self, code: str) -> bool:
        """Check if code contains explanation of Fermat's Little Theorem."""
        patterns = [
            r"fermat.*little.*theorem",
            r"a\^?\(p-1\).*≡.*1.*mod.*p",
            r"decryption.*works.*because",
            r"mathematical.*basis.*rsa"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _contains_modexp_analysis(self, code: str) -> bool:
        """Check for modular exponentiation complexity analysis."""
        patterns = [
            r"o\(log.*n\)",
            r"binary.*exponentiation",
            r"square.*and.*multiply",
            r"complexity.*log"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _contains_miller_rabin_proof(self, code: str) -> bool:
        """Check for Miller-Rabin understanding."""
        patterns = [
            r"miller.*rabin",
            r"primality.*test",
            r"witness.*composite",
            r"probabilistic.*prime"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _contains_totient_calculation(self, code: str) -> bool:
        """Check for Euler's totient function explanation."""
        patterns = [
            r"euler.*totient",
            r"φ\(n\)",
            r"phi\(n\)",
            r"\(p-1\)\*\(q-1\)"
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_fast_modexp(self, code: str) -> bool:
        """Check if code implements fast modular exponentiation."""
        # Look for signs of binary exponentiation
        patterns = [
            r"while.*exp.*>.*0",
            r"exp.*%.*2.*==.*0",
            r"exp.*//=.*2",
            r"result.*\*=.*base",
            r"base.*\*=.*base"
        ]
        return len([p for p in patterns if re.search(p, code)]) >= 3


class ModularExponentiationChallenge(Challenge):
    """Focused challenge on implementing fast modular exponentiation."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Binary Exponentiation",
                description="Derive and implement the square-and-multiply algorithm",
                proof_required=True,
                complexity_analysis=True
            )
        ]
        
        test_cases = [
            TestCase(
                input_data=(2, 10, 1000),
                expected_output=pow(2, 10, 1000),
                description="Small numbers"
            ),
            TestCase(
                input_data=(12345, 67890, 98765),
                expected_output=pow(12345, 67890, 98765),
                description="Medium numbers"
            ),
            TestCase(
                input_data=(2**1000, 2**1000, 2**1024),
                expected_output=pow(2**1000, 2**1000, 2**1024),
                timeout=0.1,
                description="Large numbers - must be efficient"
            )
        ]
        
        super().__init__(
            title="Fast Modular Exponentiation",
            description="""
Implement modular exponentiation: compute (base^exp) mod modulus efficiently.

Your algorithm MUST run in O(log exp) time complexity.

Mathematical Requirements:
- Derive the binary exponentiation algorithm from first principles
- Prove why the square-and-multiply method works
- Analyze time complexity rigorously
- Explain why naive exponentiation fails for large numbers

Function signature: mod_exp(base, exp, modulus) -> int
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.NUMBER_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=120.0
        )
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify understanding of binary exponentiation."""
        score = 0.0
        feedback = []
        
        if "square" in submission.lower() and "multiply" in submission.lower():
            score += 0.4
            feedback.append("✓ Square-and-multiply method identified")
        
        if re.search(r"o\(log.*exp?\)", submission.lower()):
            score += 0.3
            feedback.append("✓ Correct complexity analysis")
        
        if "binary" in submission.lower() and "representation" in submission.lower():
            score += 0.3
            feedback.append("✓ Binary representation understanding")
        
        return score, "; ".join(feedback)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Check for O(log n) implementation."""
        if self._has_binary_exponentiation(submission):
            return True, "Binary exponentiation algorithm detected"
        return False, "Must implement binary exponentiation for O(log n) complexity"
    
    def _has_binary_exponentiation(self, code: str) -> bool:
        """Detect binary exponentiation pattern."""
        # Look for the characteristic loop structure
        has_while = "while" in code and "exp" in code
        has_bit_ops = ("%" in code and "2" in code) or ("&" in code and "1" in code)
        has_squaring = "*=" in code or "**" in code
        
        return has_while and has_bit_ops and has_squaring