"""Advanced abstract mathematics challenges focusing on category theory."""

import re
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class CategoryTheoryChallenge(Challenge):
    """Category theory challenge requiring advanced abstract mathematics."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Category Definition",
                description="Define a mathematical category with objects and morphisms",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Functors",
                description="Implement functors between categories",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Natural Transformations",
                description="Define and implement natural transformations between functors",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Monads",
                description="Implement a monad with bind and return operations",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Functional Programming with Category Theory",
            description="""
Implement a functional programming library based on category theory principles.

Your implementation must include:
1. A representation of categories with objects and morphisms
2. Functors between categories (e.g., Maybe, List)
3. Natural transformations between functors
4. A monad implementation with bind (>>=) and return operations

Mathematical Proof Requirements:
- Prove that your categories satisfy the category laws (identity and associativity)
- Prove that your functors preserve structure between categories
- Prove that your natural transformations satisfy the naturality condition
- Prove that your monads satisfy the monad laws (left identity, right identity, associativity)

Example Usage:
```python
# Define a simple category
category = Category(
    objects=["A", "B", "C"],
    morphisms={
        ("A", "B"): [lambda x: x + 1],
        ("B", "C"): [lambda x: x * 2],
        ("A", "C"): [lambda x: (x + 1) * 2],
    }
)

# Create a functor (e.g., Maybe functor)
maybe_functor = MaybeFunctor()

# Apply the functor to values
result1 = maybe_functor.map(lambda x: x + 1, Just(5))  # Just(6)
result2 = maybe_functor.map(lambda x: x + 1, Nothing())  # Nothing

# Use monadic operations
result3 = Just(5).bind(lambda x: Just(x + 1))  # Just(6)
result4 = Nothing().bind(lambda x: Just(x + 1))  # Nothing
```
            """,
            level=ChallengeLevel.ADVANCED,
            domain=MathematicalDomain.CATEGORY_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1200.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for category theory implementations."""
        test_cases = []
        
        # Test case for category laws
        test_cases.append(TestCase(
            input_data={
                "operation": "category_laws",
                "objects": ["A", "B", "C"],
                "morphisms": {
                    "f": ("A", "B"),
                    "g": ("B", "C"),
                    "h": ("A", "C")
                }
            },
            expected_output={
                "identity_law": True,
                "associativity_law": True
            },
            description="Category laws verification"
        ))
        
        # Test case for functor properties
        test_cases.append(TestCase(
            input_data={
                "operation": "functor_laws",
                "functor_type": "maybe",
                "value": 5,
                "f": lambda x: x + 1,
                "g": lambda x: x * 2
            },
            expected_output={
                "preserves_identity": True,
                "preserves_composition": True
            },
            description="Functor laws for Maybe functor"
        ))
        
        # Test case for natural transformation
        test_cases.append(TestCase(
            input_data={
                "operation": "natural_transformation",
                "source_functor": "maybe",
                "target_functor": "list",
                "value": 5
            },
            expected_output={
                "naturality_condition": True,
                "transforms_correctly": True
            },
            description="Natural transformation between functors"
        ))
        
        # Test case for monad laws
        test_cases.append(TestCase(
            input_data={
                "operation": "monad_laws",
                "monad_type": "maybe",
                "value": 5,
                "f": lambda x: {"just": x + 1},
                "g": lambda x: {"just": x * 2}
            },
            expected_output={
                "left_identity": True,
                "right_identity": True,
                "associativity": True
            },
            description="Monad laws for Maybe monad"
        ))
        
        # Test case for practical application
        test_cases.append(TestCase(
            input_data={
                "operation": "practical_application",
                "input_data": [1, 2, None, 4, 5],
                "transform": lambda x: x * 2 if x is not None else None
            },
            expected_output={
                "result_correct": True,
                "handles_edge_cases": True
            },
            description="Practical application of categorical abstractions"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in category theory solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for category theory fundamentals
        if self._contains_category_theory_fundamentals(submission):
            score += 0.25
            feedback_parts.append("✓ Category theory fundamentals properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of category theory fundamentals")
        
        # Check for functor laws
        if self._contains_functor_laws(submission):
            score += 0.25
            feedback_parts.append("✓ Functor laws properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of functor laws")
        
        # Check for natural transformation
        if self._contains_natural_transformation(submission):
            score += 0.25
            feedback_parts.append("✓ Natural transformations properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of natural transformations")
        
        # Check for monad laws
        if self._contains_monad_laws(submission):
            score += 0.25
            feedback_parts.append("✓ Monad laws properly explained")
        else:
            feedback_parts.append("✗ Missing explanation of monad laws")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_functors(submission) and 
            self._has_efficient_monads(submission)):
            return True, "Efficient implementation of functors and monads detected"
        elif self._has_efficient_functors(submission):
            return False, "Functors are implemented efficiently, but monad implementation needs improvement"
        elif self._has_efficient_monads(submission):
            return False, "Monads are implemented efficiently, but functor implementation needs improvement"
        else:
            return False, "Both functor and monad implementations need efficiency improvements"
    
    def _contains_category_theory_fundamentals(self, text: str) -> bool:
        """Check if submission explains category theory fundamentals."""
        patterns = [
            r'category.*objects.*morphisms',
            r'identity.*morphism',
            r'associativity.*composition',
            r'commutative.*diagram',
            r'domain.*codomain'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_functor_laws(self, text: str) -> bool:
        """Check if submission explains functor laws."""
        patterns = [
            r'functor.*preserve.*structure',
            r'functor.*preserve.*identity',
            r'functor.*preserve.*composition',
            r'F\(g \circ f\).*=.*F\(g\) \circ F\(f\)',
            r'F\(id_A\).*=.*id_F\(A\)'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_natural_transformation(self, text: str) -> bool:
        """Check if submission explains natural transformations."""
        patterns = [
            r'natural.*transformation',
            r'naturality.*condition',
            r'natural.*square',
            r'η_B \circ F\(f\).*=.*G\(f\) \circ η_A',
            r'map.*between.*functors'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_monad_laws(self, text: str) -> bool:
        """Check if submission explains monad laws."""
        patterns = [
            r'monad.*laws',
            r'left.*identity.*monad',
            r'right.*identity.*monad',
            r'associativity.*monad',
            r'return.*bind'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_functors(self, code: str) -> bool:
        """Check for efficient functor implementation."""
        patterns = [
            r'class.*Functor',
            r'def.*map',
            r'def.*fmap',
            r'preserves.*structure',
            r'Maybe.*functor'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_efficient_monads(self, code: str) -> bool:
        """Check for efficient monad implementation."""
        patterns = [
            r'class.*Monad',
            r'def.*bind',
            r'def.*return',
            r'>>=',
            r'flatMap'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)