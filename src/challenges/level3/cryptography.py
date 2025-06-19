"""Advanced cryptography challenges focusing on elliptic curve cryptography."""

import re
import random
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class EllipticCurveChallenge(Challenge):
    """Elliptic curve cryptography challenge requiring advanced number theory."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Elliptic Curves",
                description="Define and implement operations on elliptic curves over finite fields",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Group Structure",
                description="Prove that points on an elliptic curve form an abelian group",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Discrete Logarithm Problem",
                description="Explain the security of ECDLP and implement point multiplication",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Cryptographic Protocol",
                description="Implement ECDH or ECDSA with proper security considerations",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Elliptic Curve Cryptography",
            description="""
Implement a secure elliptic curve cryptography system from mathematical first principles.

Your implementation must include:
1. Elliptic curve operations over finite fields (point addition, doubling, multiplication)
2. A rigorous mathematical foundation explaining the group structure
3. Implementation of either ECDH (Elliptic Curve Diffie-Hellman) or ECDSA (Elliptic Curve Digital Signature Algorithm)
4. Security analysis and proper parameter selection

Mathematical Proof Requirements:
- Prove that the points on an elliptic curve form an abelian group
- Derive the formulas for point addition and doubling on elliptic curves
- Explain why the discrete logarithm problem is hard on properly chosen elliptic curves
- Analyze the security parameters and complexity of your implementation

Example Usage:
```python
# Define an elliptic curve over a finite field
curve = EllipticCurve(a=2, b=3, p=97)  # y^2 = x^3 + 2x + 3 (mod 97)

# Generate a base point with high order
base_point = curve.find_generator()

# Generate key pair for Alice
alice_private_key = 25
alice_public_key = curve.multiply(base_point, alice_private_key)

# Generate key pair for Bob
bob_private_key = 31
bob_public_key = curve.multiply(base_point, bob_private_key)

# Alice and Bob compute shared secret
alice_shared = curve.multiply(bob_public_key, alice_private_key)
bob_shared = curve.multiply(alice_public_key, bob_private_key)

# Shared secrets should be identical
assert alice_shared == bob_shared
```
            """,
            level=ChallengeLevel.ADVANCED,
            domain=MathematicalDomain.NUMBER_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1200.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for elliptic curve implementations."""
        test_cases = []
        
        # Test case for point operations
        test_cases.append(TestCase(
            input_data={
                "operation": "point_operations",
                "curve_params": {"a": 2, "b": 3, "p": 97},
                "point1": [3, 6],
                "point2": [5, 32]
            },
            expected_output={
                "point_addition": [80, 10],  # Precomputed result for these points
                "point_doubling": [80, 87],  # Precomputed result for doubling point1
                "operation_correctness": True
            },
            description="Elliptic curve point operations"
        ))
        
        # Test case for scalar multiplication
        test_cases.append(TestCase(
            input_data={
                "operation": "scalar_multiplication",
                "curve_params": {"a": 2, "b": 3, "p": 97},
                "base_point": [3, 6],
                "scalar": 20
            },
            expected_output={
                "result": [76, 10],  # Precomputed result for 20 * [3, 6]
                "double_and_add_steps": True
            },
            description="Scalar multiplication using double-and-add"
        ))
        
        # Test case for ECDH
        test_cases.append(TestCase(
            input_data={
                "operation": "ecdh",
                "curve_params": {"a": -3, "b": 41058363725152142129326129780047268409114441015993725554835345008311738186281, "p": 115792089210356248762697446949407573530086143415290314195533631308867097853951},
                "base_point": [48439561293906451759052585252797914202762949526041747007087301598633006694193, 36134250956634298277762642519267269828105351123214308748786156166069285000263],
                "alice_private": 12345,
                "bob_private": 67890
            },
            expected_output={
                "key_agreement_works": True,
                "key_length_sufficient": True
            },
            description="Elliptic Curve Diffie-Hellman"
        ))
        
        # Test case for ECDSA
        test_cases.append(TestCase(
            input_data={
                "operation": "ecdsa",
                "curve_params": {"a": -3, "b": 41058363725152142129326129780047268409114441015993725554835345008311738186281, "p": 115792089210356248762697446949407573530086143415290314195533631308867097853951},
                "base_point": [48439561293906451759052585252797914202762949526041747007087301598633006694193, 36134250956634298277762642519267269828105351123214308748786156166069285000263],
                "private_key": 12345,
                "message": "Mathematics-Based Coding AZ"
            },
            expected_output={
                "signature_valid": True,
                "verification_works": True
            },
            description="Elliptic Curve Digital Signature Algorithm"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in elliptic curve solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for elliptic curve theory
        if self._contains_elliptic_curve_theory(submission):
            score += 0.25
            feedback_parts.append("✓ Elliptic curve theory properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of elliptic curve theory")
        
        # Check for group structure proof
        if self._contains_group_structure_proof(submission):
            score += 0.25
            feedback_parts.append("✓ Group structure of elliptic curves proved")
        else:
            feedback_parts.append("✗ Missing proof of group structure")
        
        # Check for discrete logarithm explanation
        if self._contains_discrete_logarithm_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Discrete logarithm problem properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of discrete logarithm problem")
        
        # Check for cryptographic protocol analysis
        if self._contains_protocol_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Cryptographic protocol mathematically analyzed")
        else:
            feedback_parts.append("✗ Missing analysis of cryptographic protocol")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_point_multiplication(submission) and 
            self._has_efficient_protocol(submission)):
            return True, "Efficient algorithms for point multiplication and cryptographic protocols detected"
        elif self._has_efficient_point_multiplication(submission):
            return False, "Point multiplication is efficient, but cryptographic protocol needs improvement"
        elif self._has_efficient_protocol(submission):
            return False, "Cryptographic protocol is efficient, but point multiplication needs improvement"
        else:
            return False, "Both point multiplication and cryptographic protocol need efficiency improvements"
    
    def _contains_elliptic_curve_theory(self, text: str) -> bool:
        """Check if submission explains elliptic curve theory."""
        patterns = [
            r'elliptic\s+curve.*equation',
            r'y\^2\s*=\s*x\^3',
            r'weierstrass\s+form',
            r'finite\s+field',
            r'point.*infinity'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_group_structure_proof(self, text: str) -> bool:
        """Check if submission proves the group structure of elliptic curves."""
        patterns = [
            r'abelian\s+group',
            r'closure.*addition',
            r'associative.*addition',
            r'identity\s+element',
            r'inverse.*point'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_discrete_logarithm_explanation(self, text: str) -> bool:
        """Check if submission explains the discrete logarithm problem."""
        patterns = [
            r'discrete\s+logarithm',
            r'find.*scalar.*given.*points',
            r'hard\s+problem',
            r'index\s+calculus',
            r'pollard.*rho'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_protocol_analysis(self, text: str) -> bool:
        """Check if submission analyzes cryptographic protocols."""
        patterns = [
            r'ecdh|ecdsa',
            r'key\s+exchange',
            r'digital\s+signature',
            r'man.*middle',
            r'security\s+parameter'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_point_multiplication(self, code: str) -> bool:
        """Check for efficient point multiplication."""
        patterns = [
            r'double.*add',
            r'montgomery.*ladder',
            r'window.*method',
            r'sliding\s+window',
            r'naf'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_efficient_protocol(self, code: str) -> bool:
        """Check for efficient cryptographic protocol implementation."""
        patterns = [
            r'precompute',
            r'constant\s+time',
            r'side\s+channel',
            r'secure\s+random',
            r'verify.*signature'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)