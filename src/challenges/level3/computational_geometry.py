"""Advanced computational geometry challenges focusing on Delaunay triangulation."""

import re
import random
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class DelaunayTriangulationChallenge(Challenge):
    """Delaunay triangulation challenge requiring advanced computational geometry."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Delaunay Triangulation",
                description="Define Delaunay triangulation and prove its properties",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Voronoi Diagrams",
                description="Explain the relationship between Delaunay triangulation and Voronoi diagrams",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Geometric Algorithms",
                description="Implement divide-and-conquer or incremental algorithm for Delaunay triangulation",
                proof_required=True,
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Robustness Analysis",
                description="Handle numerical precision issues and degenerate cases",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Delaunay Triangulation and Voronoi Diagrams",
            description="""
Implement a robust Delaunay triangulation algorithm with Voronoi diagram construction.

Your implementation must include:
1. A mathematically rigorous definition and implementation of Delaunay triangulation
2. Construction of the dual Voronoi diagram
3. Efficient algorithm (divide-and-conquer, incremental, or Fortune's algorithm)
4. Proper handling of edge cases and numerical robustness

Mathematical Proof Requirements:
- Prove the empty circle property of Delaunay triangulation
- Prove the relationship between Delaunay triangulation and Voronoi diagrams
- Analyze the time complexity of your algorithm
- Discuss how to handle numerical precision issues in geometric algorithms

Example Usage:
```python
# Create a set of points in 2D
points = [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]

# Construct Delaunay triangulation
delaunay = DelaunayTriangulation(points)
triangles = delaunay.triangulate()

# Check the empty circle property
for triangle in triangles:
    assert delaunay.check_empty_circle(triangle)

# Construct dual Voronoi diagram
voronoi = delaunay.construct_voronoi()
cells = voronoi.get_cells()

# Find the Voronoi cell containing a query point
query_point = (0.25, 0.25)
containing_cell = voronoi.locate_point(query_point)
```
            """,
            level=ChallengeLevel.ADVANCED,
            domain=MathematicalDomain.NUMERICAL_ANALYSIS,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1200.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for Delaunay triangulation implementations."""
        test_cases = []
        
        # Small point set for basic triangulation
        small_points = [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]
        
        test_cases.append(TestCase(
            input_data={
                "operation": "triangulate",
                "points": small_points
            },
            expected_output={
                "triangulation_valid": True,
                "empty_circle_property": True
            },
            description="Basic Delaunay triangulation"
        ))
        
        # Random points for more complex triangulation
        random.seed(42)  # For reproducible tests
        medium_points = [(random.random(), random.random()) for _ in range(20)]
        
        test_cases.append(TestCase(
            input_data={
                "operation": "triangulate",
                "points": medium_points
            },
            expected_output={
                "triangulation_valid": True,
                "edge_count_correct": True,
                "empty_circle_property": True
            },
            description="Medium-sized Delaunay triangulation"
        ))
        
        # Voronoi diagram construction
        test_cases.append(TestCase(
            input_data={
                "operation": "voronoi",
                "points": small_points
            },
            expected_output={
                "voronoi_valid": True,
                "cell_count_correct": True,
                "dual_property": True
            },
            description="Voronoi diagram construction"
        ))
        
        # Nearly collinear points (numerical robustness test)
        collinear_points = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 0.001), (1, 0.001), (2, 0.001), (3, 0.001)
        ]
        
        test_cases.append(TestCase(
            input_data={
                "operation": "triangulate_robust",
                "points": collinear_points
            },
            expected_output={
                "triangulation_valid": True,
                "handles_degeneracy": True
            },
            description="Robustness with nearly collinear points"
        ))
        
        # Performance test with larger point set
        large_points = [(random.random(), random.random()) for _ in range(100)]
        
        test_cases.append(TestCase(
            input_data={
                "operation": "performance",
                "points": large_points
            },
            expected_output={
                "time_complexity_valid": True,
                "triangulation_valid": True
            },
            description="Performance test with 100 points",
            timeout=10.0
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in Delaunay triangulation solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for Delaunay properties
        if self._contains_delaunay_properties(submission):
            score += 0.25
            feedback_parts.append("✓ Delaunay triangulation properties properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of Delaunay triangulation properties")
        
        # Check for Voronoi relationship
        if self._contains_voronoi_relationship(submission):
            score += 0.25
            feedback_parts.append("✓ Relationship with Voronoi diagrams explained")
        else:
            feedback_parts.append("✗ Missing explanation of Voronoi diagram relationship")
        
        # Check for algorithm analysis
        if self._contains_algorithm_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Algorithm properly analyzed")
        else:
            feedback_parts.append("✗ Missing analysis of triangulation algorithm")
        
        # Check for robustness discussion
        if self._contains_robustness_discussion(submission):
            score += 0.25
            feedback_parts.append("✓ Numerical robustness issues addressed")
        else:
            feedback_parts.append("✗ Missing discussion of numerical robustness")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_triangulation(submission) and 
            self._has_robust_implementation(submission)):
            return True, "Efficient and robust triangulation algorithm detected"
        elif self._has_efficient_triangulation(submission):
            return False, "Triangulation is efficient, but robustness needs improvement"
        elif self._has_robust_implementation(submission):
            return False, "Implementation is robust, but efficiency needs improvement"
        else:
            return False, "Both efficiency and robustness need improvement"
    
    def _contains_delaunay_properties(self, text: str) -> bool:
        """Check if submission explains Delaunay triangulation properties."""
        patterns = [
            r'empty\s+circle',
            r'circumcircle',
            r'maximize.*minimum.*angle',
            r'locally\s+equiangular',
            r'edge\s+flip'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_voronoi_relationship(self, text: str) -> bool:
        """Check if submission explains relationship with Voronoi diagrams."""
        patterns = [
            r'voronoi.*dual',
            r'delaunay.*dual',
            r'connect.*voronoi.*vertices',
            r'perpendicular.*bisector',
            r'circumcenter'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_algorithm_analysis(self, text: str) -> bool:
        """Check if submission analyzes the triangulation algorithm."""
        patterns = [
            r'divide.*conquer',
            r'incremental',
            r'fortune.*algorithm',
            r'time\s+complexity',
            r'O\(n\s*log\s*n\)'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_robustness_discussion(self, text: str) -> bool:
        """Check if submission discusses numerical robustness."""
        patterns = [
            r'numerical.*precision',
            r'floating.*point.*error',
            r'degenerate.*case',
            r'collinear.*point',
            r'exact.*arithmetic'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_triangulation(self, code: str) -> bool:
        """Check for efficient triangulation algorithm."""
        patterns = [
            r'divide.*conquer',
            r'bowyer.*watson',
            r'lawson.*flip',
            r'O\(n\s*log\s*n\)',
            r'cache.*circumcircle'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_robust_implementation(self, code: str) -> bool:
        """Check for robust geometric predicates."""
        patterns = [
            r'epsilon',
            r'handle.*degenerate',
            r'exact.*arithmetic',
            r'adaptive.*precision',
            r'shewchuk.*predicate'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)