"""Intermediate challenges focused on optimization techniques."""

import re
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class DynamicProgrammingChallenge(Challenge):
    """Dynamic programming challenge requiring intermediate mathematics."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Recurrence Relations",
                description="Formulate and solve mathematical recurrence relations",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Optimization Theory",
                description="Apply mathematical optimization techniques",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Time Complexity Analysis",
                description="Analyze the time complexity of recursive vs. dynamic solutions",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Optimal Matrix Chain Multiplication",
            description="""
# Optimal Matrix Chain Multiplication Challenge

## Problem Statement

Given a sequence of matrices, find the most efficient way to multiply these matrices together. The problem is not actually to perform the multiplications, but merely to decide in which order to perform the multiplications.

We have many options to multiply a chain of matrices because matrix multiplication is associative. In other words, no matter how we parenthesize the product, the result will be the same. However, the order in which we perform the multiplications affects the total number of simple arithmetic operations needed to compute the product, or the efficiency.

## Mathematical Foundation

For example, suppose we have four matrices A, B, C, and D of dimensions 10×30, 30×5, 5×60, and 60×10 respectively:

- Matrix A: 10×30
- Matrix B: 30×5
- Matrix C: 5×60
- Matrix D: 60×10

We can multiply them in several ways:
1. ((A×B)×C)×D
2. (A×(B×C))×D
3. A×((B×C)×D)
4. A×(B×(C×D))

Each approach requires different numbers of operations:
- If we multiply two matrices of dimensions p×q and q×r, the number of scalar multiplications needed is p×q×r.

## Task

Your task is to implement a dynamic programming solution to the matrix chain multiplication problem that minimizes the number of scalar multiplications needed to compute the chain product.

### Input
- An array `p` where `p[i-1]` × `p[i]` are the dimensions of matrix `i`
- For example, if matrix 1 is of dimension 10×30, matrix 2 is of dimension 30×5, and matrix 3 is of dimension 5×60, then `p = [10, 30, 5, 60]`

### Output
- The minimum number of scalar multiplications needed
- The optimal parenthesization of the matrix chain

## Mathematical Proof Requirements

1. Derive the recurrence relation for this problem
2. Prove the correctness of your dynamic programming approach
3. Analyze the time and space complexity of your solution
4. Prove that your solution always finds the optimal parenthesization

## Example

```
Input: p = [40, 20, 30, 10, 30]
Output: Minimum number of operations: 26000
Optimal parenthesization: ((A×B)×(C×D))
```

Your solution should include a clear explanation of your dynamic programming approach, the mathematical reasoning behind it, and a proof of its optimality.
            """,
            level=ChallengeLevel.INTERMEDIATE,
            domain=MathematicalDomain.OPTIMIZATION_TECHNIQUES,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=600.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for matrix chain multiplication."""
        test_cases = []
        
        # Test case 1: Small example
        test_cases.append(TestCase(
            input_data={
                "p": [40, 20, 30, 10, 30]
            },
            expected_output={
                "min_operations": 26000,
                "parenthesization": "((A1×A2)×(A3×A4))"
            },
            description="Small matrix chain"
        ))
        
        # Test case 2: Medium example
        test_cases.append(TestCase(
            input_data={
                "p": [10, 30, 5, 60, 10, 20]
            },
            expected_output={
                "min_operations": 11000,
                "parenthesization": "((A1×(A2×A3))×(A4×A5))"
            },
            description="Medium matrix chain"
        ))
        
        # Test case 3: Large example
        test_cases.append(TestCase(
            input_data={
                "p": [30, 35, 15, 5, 10, 20, 25]
            },
            expected_output={
                "min_operations": 15125,
                "parenthesization": "((A1×(A2×A3))×((A4×A5)×A6))"
            },
            description="Large matrix chain"
        ))
        
        # Test case 4: Special case - 2 matrices
        test_cases.append(TestCase(
            input_data={
                "p": [10, 20, 30]
            },
            expected_output={
                "min_operations": 6000,
                "parenthesization": "(A1×A2)"
            },
            description="Two matrices only"
        ))
        
        # Test case 5: Special case - 1 matrix
        test_cases.append(TestCase(
            input_data={
                "p": [10, 20]
            },
            expected_output={
                "min_operations": 0,
                "parenthesization": "A1"
            },
            description="Single matrix (no multiplications needed)"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in matrix chain multiplication solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for recurrence relation
        if self._contains_recurrence_relation(submission):
            score += 0.3
            feedback_parts.append("✓ Correct recurrence relation formulation")
        else:
            feedback_parts.append("✗ Missing or incorrect recurrence relation")
        
        # Check for optimization proof
        if self._contains_optimization_proof(submission):
            score += 0.3
            feedback_parts.append("✓ Clear proof of optimality")
        else:
            feedback_parts.append("✗ Missing proof that solution is optimal")
        
        # Check for complexity analysis
        if self._contains_complexity_analysis(submission):
            score += 0.3
            feedback_parts.append("✓ Thorough complexity analysis")
        else:
            feedback_parts.append("✗ Insufficient complexity analysis")
        
        # Check for subproblem structure explanation
        if self._contains_subproblem_explanation(submission):
            score += 0.1
            feedback_parts.append("✓ Clear explanation of subproblem structure")
        else:
            feedback_parts.append("✗ Missing explanation of subproblem structure")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check if solution has O(n^3) time complexity and O(n^2) space complexity
        has_time_analysis = re.search(r'[oO]\(n\^3\)|[oO]\(n³\)|cubic|O\(n\*\*3\)', submission.lower()) is not None
        has_space_analysis = re.search(r'[oO]\(n\^2\)|[oO]\(n²\)|quadratic|O\(n\*\*2\)', submission.lower()) is not None
        
        if has_time_analysis and has_space_analysis:
            return True, "Correct complexity analysis with O(n^3) time and O(n^2) space"
        elif has_time_analysis:
            return False, "Time complexity correct (O(n^3)), but space complexity analysis is missing or incorrect"
        elif has_space_analysis:
            return False, "Space complexity correct (O(n^2)), but time complexity analysis is missing or incorrect"
        else:
            return False, "Missing or incorrect complexity analysis"
    
    def _contains_recurrence_relation(self, text: str) -> bool:
        """Check if submission contains proper recurrence relation."""
        patterns = [
            r'm\[i,j\].*=.*min',
            r'm\[i\]\[j\].*=.*min',
            r'dp\[i,j\].*=.*min',
            r'dp\[i\]\[j\].*=.*min',
            r'recurrence.*relation',
            r'optimal.*substructure'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_optimization_proof(self, text: str) -> bool:
        """Check if submission contains proof of optimality."""
        patterns = [
            r'proof.*optimal',
            r'prove.*optimal',
            r'optimal.*solution',
            r'minimizes.*operations',
            r'greedy.*approach.*not.*work'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_complexity_analysis(self, text: str) -> bool:
        """Check if submission contains complexity analysis."""
        patterns = [
            r'time.*complexity.*[oO]\(n\^3\)',
            r'time.*complexity.*[oO]\(n³\)',
            r'time.*complexity.*cubic',
            r'space.*complexity.*[oO]\(n\^2\)',
            r'space.*complexity.*[oO]\(n²\)',
            r'space.*complexity.*quadratic'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_subproblem_explanation(self, text: str) -> bool:
        """Check if submission explains subproblem structure."""
        patterns = [
            r'subproblem',
            r'sub-problem',
            r'overlapping.*problems',
            r'optimal.*substructure',
            r'memoization'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)


class LinearProgrammingChallenge(Challenge):
    """Linear programming challenge requiring intermediate mathematics."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Linear Programming",
                description="Formulate and solve linear programming problems",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Constraint Optimization",
                description="Work with constraints and objective functions",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Simplex Method",
                description="Understand the mathematical foundation of the simplex algorithm",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Resource Allocation Optimizer",
            description="""
# Resource Allocation Optimizer Challenge

## Problem Statement

You are tasked with developing a resource allocation optimizer for a manufacturing company. The company produces different products using limited resources, and you need to determine the optimal production quantities to maximize profit.

## Mathematical Foundation

This is a classic linear programming problem that can be formulated as:

Maximize: c₁x₁ + c₂x₂ + ... + cₙxₙ (profit function)

Subject to:
- a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ ≤ b₁
- a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ ≤ b₂
- ...
- aₘ₁x₁ + aₘ₂x₂ + ... + aₘₙxₙ ≤ bₘ
- x₁, x₂, ..., xₙ ≥ 0

Where:
- xᵢ represents the quantity of product i to produce
- cᵢ represents the profit per unit of product i
- aᵢⱼ represents the amount of resource i used to produce one unit of product j
- bᵢ represents the available amount of resource i

## Task

Your task is to implement a solver for this linear programming problem using the Simplex method. You should be able to:

1. Parse the input data (objective function coefficients, constraint coefficients, and resource limits)
2. Formulate the problem in standard form (with slack variables)
3. Apply the Simplex algorithm to find the optimal solution
4. Return the optimal values of the decision variables and the maximum profit

## Mathematical Proof Requirements

1. Explain the mathematical theory behind the Simplex method
2. Prove the correctness of your implementation
3. Analyze the time complexity of your solution
4. Discuss potential issues like degeneracy and how your solution handles them

## Example

```
Input:
Objective function: 3x₁ + 5x₂ (maximize)
Constraints:
  2x₁ + x₂ ≤ 8
  x₁ + 2x₂ ≤ 10
  x₁ ≥ 0, x₂ ≥ 0

Output:
Optimal solution: x₁ = 3, x₂ = 2
Maximum profit: 19
```

Your solution should include a clear explanation of the Simplex method, the mathematical reasoning behind it, and a proof of its optimality for this problem.
            """,
            level=ChallengeLevel.INTERMEDIATE,
            domain=MathematicalDomain.OPTIMIZATION_TECHNIQUES,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=900.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for linear programming challenge."""
        test_cases = []
        
        # Test case 1: Basic example
        test_cases.append(TestCase(
            input_data={
                "objective": [3, 5],
                "constraints": [
                    {"coefficients": [2, 1], "limit": 8},
                    {"coefficients": [1, 2], "limit": 10}
                ]
            },
            expected_output={
                "optimal_values": [3, 2],
                "maximum_profit": 19
            },
            description="Basic two-variable problem"
        ))
        
        # Test case 2: Three variables
        test_cases.append(TestCase(
            input_data={
                "objective": [2, 3, 1],
                "constraints": [
                    {"coefficients": [1, 1, 1], "limit": 10},
                    {"coefficients": [2, 1, 0], "limit": 8},
                    {"coefficients": [0, 1, 2], "limit": 7}
                ]
            },
            expected_output={
                "optimal_values": [2, 6, 2],
                "maximum_profit": 26
            },
            description="Three-variable problem"
        ))
        
        # Test case 3: Larger problem
        test_cases.append(TestCase(
            input_data={
                "objective": [5, 4, 3, 2],
                "constraints": [
                    {"coefficients": [1, 2, 1, 1], "limit": 40},
                    {"coefficients": [2, 1, 1, 0], "limit": 30},
                    {"coefficients": [1, 1, 0, 1], "limit": 20}
                ]
            },
            expected_output={
                "optimal_values": [10, 15, 0, 0],
                "maximum_profit": 110
            },
            description="Four-variable problem"
        ))
        
        # Test case 4: Unique optimal solution
        test_cases.append(TestCase(
            input_data={
                "objective": [3, 2],
                "constraints": [
                    {"coefficients": [2, 1], "limit": 10},
                    {"coefficients": [1, 1], "limit": 6},
                    {"coefficients": [1, 0], "limit": 4}
                ]
            },
            expected_output={
                "optimal_values": [4, 2],
                "maximum_profit": 16
            },
            description="Problem with unique optimal solution"
        ))
        
        # Test case 5: Multiple optimal solutions (should find one of them)
        test_cases.append(TestCase(
            input_data={
                "objective": [1, 1],
                "constraints": [
                    {"coefficients": [1, 1], "limit": 10},
                    {"coefficients": [1, 0], "limit": 5}
                ]
            },
            expected_output={
                "optimal_values": [5, 5],
                "maximum_profit": 10
            },
            description="Problem with multiple optimal solutions"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in linear programming solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for simplex method explanation
        if self._contains_simplex_explanation(submission):
            score += 0.3
            feedback_parts.append("✓ Clear explanation of the Simplex method")
        else:
            feedback_parts.append("✗ Insufficient explanation of the Simplex method")
        
        # Check for standard form conversion
        if self._contains_standard_form(submission):
            score += 0.2
            feedback_parts.append("✓ Correct formulation of the problem in standard form")
        else:
            feedback_parts.append("✗ Missing or incorrect standard form formulation")
        
        # Check for pivoting explanation
        if self._contains_pivoting_explanation(submission):
            score += 0.2
            feedback_parts.append("✓ Clear explanation of the pivoting process")
        else:
            feedback_parts.append("✗ Missing explanation of pivoting operations")
        
        # Check for optimality conditions
        if self._contains_optimality_conditions(submission):
            score += 0.2
            feedback_parts.append("✓ Correct explanation of optimality conditions")
        else:
            feedback_parts.append("✗ Missing or incorrect optimality conditions")
        
        # Check for edge cases discussion
        if self._contains_edge_cases(submission):
            score += 0.1
            feedback_parts.append("✓ Thorough discussion of edge cases")
        else:
            feedback_parts.append("✗ Missing discussion of potential edge cases")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for analysis of Simplex algorithm complexity
        if self._contains_complexity_analysis(submission):
            return True, "Correct analysis of Simplex algorithm complexity"
        else:
            return False, "Missing or incorrect analysis of Simplex algorithm complexity"
    
    def _contains_simplex_explanation(self, text: str) -> bool:
        """Check if submission explains the Simplex method."""
        patterns = [
            r'simplex.*method',
            r'simplex.*algorithm',
            r'tableau',
            r'basic.*feasible.*solution',
            r'pivot.*row.*column'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_standard_form(self, text: str) -> bool:
        """Check if submission explains standard form conversion."""
        patterns = [
            r'standard.*form',
            r'slack.*variable',
            r'inequality.*constraint',
            r'augmented.*matrix'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_pivoting_explanation(self, text: str) -> bool:
        """Check if submission explains pivoting process."""
        patterns = [
            r'pivot.*operation',
            r'pivoting.*process',
            r'row.*operation',
            r'gaussian.*elimination',
            r'entering.*leaving.*variable'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_optimality_conditions(self, text: str) -> bool:
        """Check if submission explains optimality conditions."""
        patterns = [
            r'optimality.*condition',
            r'optimal.*solution',
            r'reduced.*cost',
            r'shadow.*price',
            r'no.*negative.*coefficient'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_edge_cases(self, text: str) -> bool:
        """Check if submission discusses edge cases."""
        patterns = [
            r'degeneracy',
            r'cycling',
            r'multiple.*solution',
            r'unbounded',
            r'infeasible'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_complexity_analysis(self, text: str) -> bool:
        """Check if submission contains complexity analysis of Simplex."""
        patterns = [
            r'exponential.*worst.*case',
            r'polynomial.*average',
            r'klee.*minty',
            r'time.*complexity',
            r'space.*complexity'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)