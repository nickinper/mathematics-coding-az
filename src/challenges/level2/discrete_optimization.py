"""Discrete optimization challenges focusing on the Traveling Salesman Problem."""

import re
import math
import random
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class TSPChallenge(Challenge):
    """Traveling Salesman Problem requiring deep discrete math understanding."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Graph Theory",
                description="Model the TSP as a complete weighted graph",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="NP-Completeness",
                description="Explain why TSP is NP-Complete and its implications",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Approximation Algorithms",
                description="Implement an approximation algorithm with provable bounds",
                proof_required=True,
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Local Search Techniques",
                description="Implement local search improvements like 2-opt or 3-opt",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="The Traveling Salesman Problem",
            description="""
Implement a sophisticated solution to the Traveling Salesman Problem (TSP).

Your implementation must include:
1. A mathematical model of the TSP as a complete weighted graph
2. A minimum spanning tree-based approximation algorithm
3. A local search improvement technique (2-opt or 3-opt)
4. A dynamic programming approach for small instances

Mathematical Proof Requirements:
- Prove that TSP is NP-Complete (or reference the standard proof)
- Prove the approximation ratio of your MST-based algorithm
- Analyze the time complexity of your approach
- Provide mathematical justification for your local search method

Example Usage:
```python
# Create a TSP instance
cities = [(0, 0), (1, 3), (5, 2), (7, 1), (9, 6), (3, 7)]
tsp_solver = TSPSolver(cities)

# Generate initial approximate solution
initial_tour = tsp_solver.approximate()

# Improve solution using local search
improved_tour = tsp_solver.local_search(initial_tour)

# For small instances, find the optimal solution
optimal_tour = tsp_solver.solve_exact(max_cities=10)
```
            """,
            level=ChallengeLevel.INTERMEDIATE,
            domain=MathematicalDomain.DISCRETE_MATH,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1200.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for TSP implementations."""
        test_cases = []
        
        # Small instance (exact solution possible)
        small_cities = [(0, 0), (1, 3), (5, 2), (7, 1)]
        small_optimal_length = self._compute_optimal_tsp(small_cities)
        
        test_cases.append(TestCase(
            input_data={
                "cities": small_cities,
                "method": "exact"
            },
            expected_output={
                "length": small_optimal_length,
                "tour_valid": True
            },
            description="Small TSP instance (exact solution)"
        ))
        
        # Medium instance (approximation quality test)
        medium_cities = self._generate_cities(15)
        
        test_cases.append(TestCase(
            input_data={
                "cities": medium_cities,
                "method": "approximate"
            },
            expected_output={
                "approximation_ratio": lambda x: x <= 2.0,  # Should be within 2x optimal
                "tour_valid": True
            },
            description="Medium TSP instance (approximation)"
        ))
        
        # Large instance (performance test)
        large_cities = self._generate_cities(50)
        
        test_cases.append(TestCase(
            input_data={
                "cities": large_cities,
                "method": "local_search",
                "initial_method": "nearest_neighbor"
            },
            expected_output={
                "improvement": lambda x: x > 0.0,  # Should improve upon initial solution
                "runtime": lambda x: x < 5.0,  # Should run in under 5 seconds
                "tour_valid": True
            },
            description="Large TSP instance (local search)",
            timeout=10.0
        ))
        
        # Euclidean TSP specific test
        test_cases.append(TestCase(
            input_data={
                "cities": self._generate_cities(20),
                "method": "christofides"
            },
            expected_output={
                "approximation_ratio": lambda x: x <= 1.5,  # Christofides should be within 1.5x optimal
                "tour_valid": True
            },
            description="Euclidean TSP (Christofides algorithm)"
        ))
        
        return test_cases
    
    def _generate_cities(self, n: int, max_coord: int = 100) -> List[Tuple[float, float]]:
        """Generate n random cities with coordinates."""
        random.seed(42)  # For reproducible test cases
        return [(random.uniform(0, max_coord), random.uniform(0, max_coord)) for _ in range(n)]
    
    def _compute_optimal_tsp(self, cities: List[Tuple[float, float]]) -> float:
        """Compute optimal TSP tour length for small instances using brute force."""
        if len(cities) > 10:
            raise ValueError("Too many cities for exact solution")
            
        # Simple implementation for test cases only
        def distance(city1, city2):
            return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
            
        n = len(cities)
        min_length = float('inf')
        
        import itertools
        for tour in itertools.permutations(range(n)):
            length = 0
            for i in range(n):
                length += distance(cities[tour[i]], cities[tour[(i + 1) % n]])
            min_length = min(min_length, length)
            
        return min_length
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in TSP solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for graph theory model
        if self._contains_graph_theory_model(submission):
            score += 0.25
            feedback_parts.append("✓ Graph theory model for TSP found")
        else:
            feedback_parts.append("✗ Missing graph theory model for TSP")
        
        # Check for NP-completeness discussion
        if self._contains_np_completeness(submission):
            score += 0.25
            feedback_parts.append("✓ NP-completeness of TSP explained")
        else:
            feedback_parts.append("✗ Missing explanation of TSP's NP-completeness")
        
        # Check for approximation algorithm analysis
        if self._contains_approximation_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Approximation algorithm analysis found")
        else:
            feedback_parts.append("✗ Missing analysis of approximation algorithm")
        
        # Check for local search justification
        if self._contains_local_search_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Local search technique mathematically justified")
        else:
            feedback_parts.append("✗ Missing mathematical justification for local search")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_approximation(submission) and 
            self._has_efficient_local_search(submission)):
            return True, "Efficient algorithms for approximation and local search detected"
        elif self._has_efficient_approximation(submission):
            return False, "Approximation algorithm is efficient, but local search needs improvement"
        elif self._has_efficient_local_search(submission):
            return False, "Local search is efficient, but approximation algorithm needs improvement"
        else:
            return False, "Both approximation and local search algorithms need efficiency improvements"
    
    def _contains_graph_theory_model(self, text: str) -> bool:
        """Check if submission contains a graph theory model of TSP."""
        patterns = [
            r'complete\s+graph',
            r'weighted\s+graph',
            r'edge.*weight|weight.*edge',
            r'hamiltonian\s+cycle',
            r'adjacency\s+matrix'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_np_completeness(self, text: str) -> bool:
        """Check if submission explains TSP's NP-completeness."""
        patterns = [
            r'np.*complete|np.*hard',
            r'np-complete.*reduction',
            r'exponential.*time',
            r'complexity.*class',
            r'intractable'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_approximation_analysis(self, text: str) -> bool:
        """Check if submission analyzes approximation algorithm."""
        patterns = [
            r'approximation.*ratio|ratio.*approximation',
            r'minimum.*spanning.*tree|mst',
            r'christofides',
            r'triangle.*inequality',
            r'2-approximation|2.*approximation'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_local_search_explanation(self, text: str) -> bool:
        """Check if submission explains local search methods."""
        patterns = [
            r'2-opt|3-opt|k-opt',
            r'local.*search',
            r'hill.*climbing',
            r'edge.*swap',
            r'local.*minimum'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_approximation(self, code: str) -> bool:
        """Check for efficient approximation algorithm."""
        # Look for MST or Christofides algorithm patterns
        patterns = [
            r'minimum.*spanning.*tree|mst',
            r'kruskal|prim',
            r'christofides',
            r'matching.*algorithm',
            r'O\(n\^2\)'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_efficient_local_search(self, code: str) -> bool:
        """Check for efficient local search implementation."""
        patterns = [
            r'2-opt|two-opt',
            r'3-opt|three-opt',
            r'for.*swap',
            r'improve.*solution',
            r'delta.*improvement'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)