"""Linear Algebra challenges focusing on matrix transformations."""

import re
import numpy as np
from typing import Any, Tuple, List
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class MatrixTransformChallenge(Challenge):
    """Matrix transformation challenge requiring linear algebra understanding."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Matrix Operations",
                description="Implement basic matrix operations (multiplication, addition)",
                proof_required=False
            ),
            MathematicalRequirement(
                concept="Linear Transformations",
                description="Understand and implement linear transformations",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Change of Basis",
                description="Implement change of basis transformations",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Matrix Decomposition",
                description="Implement eigenvalue decomposition",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Matrix Transformations",
            description="""
Implement a comprehensive matrix transformation library in pure Python.

Your implementation must include:
1. Matrix class with basic operations (add, subtract, multiply)
2. Linear transformation functions (rotation, scaling, shearing)
3. Change of basis transformations
4. Eigenvalue decomposition for 2x2 matrices

Mathematical Proof Requirements:
- Prove that the composition of linear transformations is also a linear transformation
- Prove that a change of basis is a linear transformation
- Analyze the complexity of your eigenvalue decomposition algorithm

Example Usage:
```python
# Create matrices
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

# Basic operations
C = A + B
D = A * B  # Matrix multiplication

# Transformations
rotated = rotate(A, angle=45)  # Rotate by 45 degrees
scaled = scale(A, sx=2, sy=3)  # Scale by factors of 2 and 3

# Change of basis
new_basis = Matrix([[1, 1], [0, 1]])
transformed = change_basis(A, new_basis)

# Eigenvalues
eigenvalues, eigenvectors = decompose(A)
```
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.LINEAR_ALGEBRA,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=600.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for matrix transformations."""
        test_cases = []
        
        # Basic operations test
        test_cases.append(TestCase(
            input_data={
                "operation": "add",
                "A": [[1, 2], [3, 4]],
                "B": [[5, 6], [7, 8]]
            },
            expected_output=[[6, 8], [10, 12]],
            description="Matrix addition"
        ))
        
        test_cases.append(TestCase(
            input_data={
                "operation": "multiply",
                "A": [[1, 2], [3, 4]],
                "B": [[5, 6], [7, 8]]
            },
            expected_output=[[19, 22], [43, 50]],
            description="Matrix multiplication"
        ))
        
        # Rotation test
        test_cases.append(TestCase(
            input_data={
                "operation": "rotate",
                "matrix": [[1, 0], [0, 1]],
                "angle": 90
            },
            expected_output=[[0, -1], [1, 0]],
            description="90-degree rotation",
            timeout=2.0
        ))
        
        # Scaling test
        test_cases.append(TestCase(
            input_data={
                "operation": "scale",
                "matrix": [[1, 2], [3, 4]],
                "sx": 2,
                "sy": 3
            },
            expected_output=[[2, 4], [9, 12]],
            description="Non-uniform scaling"
        ))
        
        # Eigenvalue test
        test_cases.append(TestCase(
            input_data={
                "operation": "decompose",
                "matrix": [[2, 1], [1, 2]]
            },
            expected_output={
                "eigenvalues": [3, 1],
                "eigenvectors": [[1, 1], [1, -1]]
            },
            description="Eigenvalue decomposition"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in matrix transformations."""
        score = 0.0
        feedback_parts = []
        
        # Check for linear transformation proof
        if self._contains_linear_transform_proof(submission):
            score += 0.3
            feedback_parts.append("✓ Linear transformation composition proof found")
        else:
            feedback_parts.append("✗ Missing proof for linear transformation composition")
        
        # Check for change of basis understanding
        if self._contains_basis_change_proof(submission):
            score += 0.3
            feedback_parts.append("✓ Change of basis explanation present")
        else:
            feedback_parts.append("✗ Missing change of basis mathematical justification")
        
        # Check for eigenvalue understanding
        if self._contains_eigenvalue_explanation(submission):
            score += 0.2
            feedback_parts.append("✓ Eigenvalue decomposition reasoning found")
        else:
            feedback_parts.append("✗ Missing eigenvalue decomposition explanation")
        
        # Check for matrix properties
        if self._contains_matrix_properties(submission):
            score += 0.2
            feedback_parts.append("✓ Matrix properties correctly explained")
        else:
            feedback_parts.append("✗ Missing explanation of key matrix properties")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient eigenvalue calculation
        if self._has_efficient_eigenvalue(submission):
            return True, "Efficient eigenvalue calculation detected"
        else:
            return False, "Eigenvalue calculation should be O(n³) or better"
    
    def _contains_linear_transform_proof(self, text: str) -> bool:
        """Check if submission contains proof for linear transformations."""
        patterns = [
            r'composition.*linear.*transformation',
            r'T\(S\(.*\)\)',
            r'linearity.*preserved',
            r'T\(ax\+by\).*=.*aT\(x\)\+bT\(y\)'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_basis_change_proof(self, text: str) -> bool:
        """Check if submission contains proof for change of basis."""
        patterns = [
            r'change.*basis.*linear',
            r'basis.*transformation',
            r'coordinate.*transformation',
            r'P\^-1.*A.*P'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_eigenvalue_explanation(self, text: str) -> bool:
        """Check if submission explains eigenvalue decomposition."""
        patterns = [
            r'eigenvalue.*eigenvector',
            r'A.*v.*=.*lambda.*v',
            r'characteristic.*equation',
            r'diagonalization'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_matrix_properties(self, text: str) -> bool:
        """Check if submission explains matrix properties."""
        patterns = [
            r'invertible|non-singular',
            r'determinant',
            r'orthogonal',
            r'symmetric',
            r'positive.*definite'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_eigenvalue(self, code: str) -> bool:
        """Check for efficient eigenvalue calculation."""
        # Signs of efficient implementation
        efficient_patterns = [
            r'characteristic.*polynomial',
            r'quadratic.*formula',
            r'eigenvalues.*2x2',
            r'power.*iteration'
        ]
        return any(re.search(pattern, code.lower()) for pattern in efficient_patterns)