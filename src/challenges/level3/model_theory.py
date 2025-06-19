"""Advanced model theory challenges."""

import re
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class FirstOrderLogicChallenge(Challenge):
    """First-order logic challenge requiring advanced mathematical understanding."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="First-Order Logic",
                description="Understand and work with first-order logic syntax and semantics",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Model Theory",
                description="Construct models and countermodels for logical statements",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Proof Theory",
                description="Develop formal proofs for logical statements",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Decidability",
                description="Analyze decidability of fragments of first-order logic",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Automated Theorem Prover for First-Order Logic",
            description="""
# Automated Theorem Prover for First-Order Logic

## Problem Statement

You are tasked with implementing a simplified automated theorem prover for a fragment of first-order logic. Your system should be able to determine whether a given logical statement is valid, satisfiable, or unsatisfiable, and provide appropriate proofs or countermodels.

## Mathematical Foundation

First-order logic (FOL) extends propositional logic by adding quantifiers (∀, ∃) and predicates. A key distinction in FOL is between:

- **Validity**: A formula is valid if it is true in all possible interpretations
- **Satisfiability**: A formula is satisfiable if there exists at least one interpretation where it is true
- **Unsatisfiability**: A formula is unsatisfiable if it is false in all possible interpretations

## Task

Your task is to implement a resolution-based theorem prover that can:

1. Convert first-order logic formulas into clausal normal form (CNF)
2. Apply unification and resolution to prove or disprove statements
3. Generate countermodels for invalid statements
4. Determine the satisfiability of a set of clauses

## Input Format

Your system should accept formulas in a simplified first-order logic syntax:

- Logical connectives: & (and), | (or), ~ (not), -> (implies), <-> (if and only if)
- Quantifiers: A (for all), E (exists)
- Variables: x, y, z, etc.
- Constants: a, b, c, etc.
- Predicates: P(x), Q(x,y), etc.
- Functions: f(x), g(x,y), etc.

## Examples

1. `A x (P(x) -> Q(x))` - For all x, if P(x) then Q(x)
2. `E x (P(x) & ~Q(x))` - There exists an x such that P(x) and not Q(x)
3. `A x (P(x)) -> A x (Q(x))` - If for all x, P(x), then for all x, Q(x)

## Mathematical Proof Requirements

1. Prove the correctness of your CNF conversion algorithm
2. Prove the soundness and completeness of your resolution procedure
3. Analyze the decidability and complexity of your approach
4. Explain the limitations of your system with respect to the undecidability of full first-order logic

## Example

```
Input: [A x (P(x) -> Q(x)), P(a), ~Q(a)]
Output: UNSATISFIABLE
Proof: Resolution derivation of the empty clause
```

```
Input: [A x (P(x) -> Q(x)), P(a)]
Output: SATISFIABLE
Model: Domain = {a}, P = {a}, Q = {a}
```

Your solution should include a clear explanation of the algorithms used, the mathematical theory behind them, and proofs of correctness.
            """,
            level=ChallengeLevel.ADVANCED,
            domain=MathematicalDomain.MODEL_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1200.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for first-order logic challenge."""
        test_cases = []
        
        # Test case 1: Basic unsatisfiable set
        test_cases.append(TestCase(
            input_data={
                "formulas": [
                    "A x (P(x) -> Q(x))",
                    "P(a)",
                    "~Q(a)"
                ]
            },
            expected_output={
                "result": "UNSATISFIABLE",
                "proof_type": "resolution"
            },
            description="Basic unsatisfiable set with modus ponens"
        ))
        
        # Test case 2: Basic satisfiable set
        test_cases.append(TestCase(
            input_data={
                "formulas": [
                    "A x (P(x) -> Q(x))",
                    "P(a)"
                ]
            },
            expected_output={
                "result": "SATISFIABLE",
                "model": {
                    "domain": ["a"],
                    "predicates": {
                        "P": ["a"],
                        "Q": ["a"]
                    }
                }
            },
            description="Basic satisfiable set"
        ))
        
        # Test case 3: Universal instantiation
        test_cases.append(TestCase(
            input_data={
                "formulas": [
                    "A x (P(x))",
                    "~P(b)"
                ]
            },
            expected_output={
                "result": "UNSATISFIABLE",
                "proof_type": "resolution"
            },
            description="Universal instantiation contradiction"
        ))
        
        # Test case 4: Existential instantiation
        test_cases.append(TestCase(
            input_data={
                "formulas": [
                    "E x (P(x) & Q(x))",
                    "A x (~P(x))"
                ]
            },
            expected_output={
                "result": "UNSATISFIABLE",
                "proof_type": "resolution"
            },
            description="Existential and universal quantifier contradiction"
        ))
        
        # Test case 5: More complex example with functions
        test_cases.append(TestCase(
            input_data={
                "formulas": [
                    "A x (P(x) -> P(f(x)))",
                    "P(a)",
                    "~P(f(f(a)))"
                ]
            },
            expected_output={
                "result": "UNSATISFIABLE",
                "proof_type": "resolution"
            },
            description="Function symbols with transitivity"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in first-order logic solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for explanation of CNF conversion
        if self._contains_cnf_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Clear explanation of CNF conversion")
        else:
            feedback_parts.append("✗ Insufficient explanation of CNF conversion")
        
        # Check for resolution explanation
        if self._contains_resolution_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Thorough explanation of resolution procedure")
        else:
            feedback_parts.append("✗ Missing or incomplete resolution explanation")
        
        # Check for unification explanation
        if self._contains_unification_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Detailed unification algorithm explanation")
        else:
            feedback_parts.append("✗ Insufficient unification explanation")
        
        # Check for soundness and completeness discussion
        if self._contains_soundness_completeness(submission):
            score += 0.25
            feedback_parts.append("✓ Rigorous discussion of soundness and completeness")
        else:
            feedback_parts.append("✗ Missing or inadequate soundness and completeness analysis")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for decidability and complexity analysis
        has_decidability = self._contains_decidability_discussion(submission)
        has_complexity = self._contains_complexity_analysis(submission)
        
        if has_decidability and has_complexity:
            return True, "Comprehensive analysis of decidability and complexity"
        elif has_decidability:
            return False, "Good discussion of decidability but lacking complexity analysis"
        elif has_complexity:
            return False, "Good complexity analysis but lacking decidability discussion"
        else:
            return False, "Missing both decidability and complexity analysis"
    
    def _contains_cnf_explanation(self, text: str) -> bool:
        """Check if submission explains CNF conversion."""
        patterns = [
            r'clausal.*normal.*form',
            r'cnf.*conversion',
            r'prenex.*normal.*form',
            r'skolemization',
            r'eliminating.*quantifiers'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_resolution_explanation(self, text: str) -> bool:
        """Check if submission explains resolution procedure."""
        patterns = [
            r'resolution.*principle',
            r'resolution.*rule',
            r'resolvent',
            r'empty.*clause',
            r'derive.*contradiction'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_unification_explanation(self, text: str) -> bool:
        """Check if submission explains unification."""
        patterns = [
            r'unification.*algorithm',
            r'most.*general.*unifier',
            r'mgu',
            r'substitution',
            r'term.*matching'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_soundness_completeness(self, text: str) -> bool:
        """Check if submission discusses soundness and completeness."""
        patterns = [
            r'soundness',
            r'completeness',
            r'if.*formula.*valid.*proof',
            r'if.*proof.*exists.*formula.*valid',
            r'herbrand.*theorem'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_decidability_discussion(self, text: str) -> bool:
        """Check if submission discusses decidability."""
        patterns = [
            r'decidability',
            r'undecidable',
            r'church.*turing',
            r'entscheidungsproblem',
            r'decidable.*fragment'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_complexity_analysis(self, text: str) -> bool:
        """Check if submission analyzes complexity."""
        patterns = [
            r'time.*complexity',
            r'space.*complexity',
            r'exponential',
            r'intractable',
            r'np-complete'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)


class ModelComparisonChallenge(Challenge):
    """Model comparison challenge requiring advanced mathematical understanding."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Mathematical Structures",
                description="Understand and define mathematical structures as models",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Isomorphism",
                description="Determine isomorphism between mathematical structures",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Elementary Equivalence",
                description="Analyze elementary equivalence of models",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Definability",
                description="Determine which properties are definable in a given language",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Model Comparison and Classification",
            description="""
# Model Comparison and Classification Challenge

## Problem Statement

You are tasked with developing a system that can analyze and compare mathematical structures (models) to determine their properties, relationships, and classifications according to model theory.

## Mathematical Foundation

In model theory, a *structure* or *model* consists of:
- A non-empty domain (universe)
- Interpretations of constant symbols, function symbols, and relation symbols

Two key relationships between models are:
- **Isomorphism**: Two models are isomorphic if there exists a bijective function between their domains that preserves all relations and functions
- **Elementary Equivalence**: Two models are elementarily equivalent if they satisfy exactly the same first-order sentences

## Task

Your task is to implement a system that can:

1. Define and represent mathematical structures (like graphs, groups, or ordered sets)
2. Determine whether two given structures are isomorphic
3. Check if two structures are elementarily equivalent but not isomorphic
4. Find examples of properties that are definable or undefinable in first-order logic

## Input Format

Your system should accept descriptions of mathematical structures in a structured format:
- Domain elements
- Interpretations of constant symbols
- Interpretations of function symbols
- Interpretations of relation symbols

## Mathematical Proof Requirements

1. Prove the correctness of your isomorphism checking algorithm
2. Prove the correctness of your elementary equivalence checking algorithm
3. Provide rigorous proofs of definability or undefinability of properties
4. Analyze the complexity of your algorithms

## Examples

Example 1: Two isomorphic graphs
```
Structure A:
Domain: {1, 2, 3, 4}
Relations: Edge = {(1,2), (2,3), (3,4), (4,1)}

Structure B:
Domain: {a, b, c, d}
Relations: Edge = {(a,b), (b,c), (c,d), (d,a)}

Output: ISOMORPHIC
Isomorphism: 1→a, 2→b, 3→c, 4→d
```

Example 2: Elementarily equivalent but non-isomorphic models
```
Structure A:
Domain: ℤ (integers)
Relations: < (standard ordering)

Structure B:
Domain: ℤ + ℚ (integers followed by rationals)
Relations: < (standard ordering with all integers before all rationals)

Output: ELEMENTARILY EQUIVALENT, NOT ISOMORPHIC
Explanation: Both satisfy the theory of dense linear orders without endpoints
```

Your solution should include a clear explanation of the algorithms used, the mathematical theory behind them, and proofs of correctness.
            """,
            level=ChallengeLevel.ADVANCED,
            domain=MathematicalDomain.MODEL_THEORY,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1200.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for model comparison challenge."""
        test_cases = []
        
        # Test case 1: Isomorphic finite graphs
        test_cases.append(TestCase(
            input_data={
                "structure_a": {
                    "domain": [1, 2, 3, 4],
                    "relations": {
                        "edge": [(1, 2), (2, 3), (3, 4), (4, 1)]
                    }
                },
                "structure_b": {
                    "domain": ["a", "b", "c", "d"],
                    "relations": {
                        "edge": [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")]
                    }
                },
                "query": "check_isomorphism"
            },
            expected_output={
                "result": "ISOMORPHIC",
                "mapping": {"1": "a", "2": "b", "3": "c", "4": "d"}
            },
            description="Isomorphic cycle graphs"
        ))
        
        # Test case 2: Non-isomorphic graphs
        test_cases.append(TestCase(
            input_data={
                "structure_a": {
                    "domain": [1, 2, 3, 4],
                    "relations": {
                        "edge": [(1, 2), (2, 3), (3, 4), (4, 1)]
                    }
                },
                "structure_b": {
                    "domain": ["a", "b", "c", "d"],
                    "relations": {
                        "edge": [("a", "b"), ("b", "c"), ("c", "d"), ("d", "b")]
                    }
                },
                "query": "check_isomorphism"
            },
            expected_output={
                "result": "NOT_ISOMORPHIC",
                "reason": "Different graph structure"
            },
            description="Non-isomorphic graphs"
        ))
        
        # Test case 3: Elementarily equivalent but non-isomorphic structures
        test_cases.append(TestCase(
            input_data={
                "structure_a": {
                    "description": "Standard model of natural numbers with order",
                    "domain_type": "natural_numbers",
                    "relations": {
                        "order": "standard"
                    }
                },
                "structure_b": {
                    "description": "Non-standard model of natural numbers with order",
                    "domain_type": "natural_numbers_with_infinite_element",
                    "relations": {
                        "order": "standard_with_infinite"
                    }
                },
                "query": "check_elementary_equivalence"
            },
            expected_output={
                "result": "ELEMENTARILY_EQUIVALENT_NOT_ISOMORPHIC",
                "explanation": "Both satisfy first-order Peano arithmetic but differ in cardinality"
            },
            description="Models of arithmetic"
        ))
        
        # Test case 4: Definability in structures
        test_cases.append(TestCase(
            input_data={
                "structure": {
                    "description": "Dense linear order without endpoints",
                    "domain_type": "rational_numbers",
                    "relations": {
                        "order": "standard"
                    }
                },
                "property": "being_a_natural_number",
                "query": "check_definability"
            },
            expected_output={
                "result": "NOT_DEFINABLE",
                "explanation": "Natural numbers are not definable in a dense linear order using first-order logic"
            },
            description="Definability in dense linear orders"
        ))
        
        # Test case 5: Group isomorphism
        test_cases.append(TestCase(
            input_data={
                "structure_a": {
                    "domain": [0, 1, 2, 3],
                    "operations": {
                        "addition": [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
                    }
                },
                "structure_b": {
                    "domain": ["e", "a", "b", "c"],
                    "operations": {
                        "multiplication": [["e", "a", "b", "c"], ["a", "b", "c", "e"], ["b", "c", "e", "a"], ["c", "e", "a", "b"]]
                    }
                },
                "query": "check_isomorphism"
            },
            expected_output={
                "result": "ISOMORPHIC",
                "mapping": {"0": "e", "1": "a", "2": "b", "3": "c"}
            },
            description="Isomorphic cyclic groups"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in model comparison solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for model theory fundamentals
        if self._contains_model_theory_fundamentals(submission):
            score += 0.25
            feedback_parts.append("✓ Solid understanding of model theory fundamentals")
        else:
            feedback_parts.append("✗ Lacking explanation of model theory fundamentals")
        
        # Check for isomorphism explanation
        if self._contains_isomorphism_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Clear explanation of isomorphism and algorithm")
        else:
            feedback_parts.append("✗ Insufficient explanation of isomorphism")
        
        # Check for elementary equivalence explanation
        if self._contains_elementary_equivalence_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Thorough explanation of elementary equivalence")
        else:
            feedback_parts.append("✗ Missing or incomplete elementary equivalence explanation")
        
        # Check for definability analysis
        if self._contains_definability_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Rigorous analysis of definability in first-order logic")
        else:
            feedback_parts.append("✗ Lacking analysis of definability")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for complexity analysis of isomorphism and equivalence checking
        has_isomorphism_complexity = self._contains_isomorphism_complexity(submission)
        has_equivalence_complexity = self._contains_equivalence_complexity(submission)
        
        if has_isomorphism_complexity and has_equivalence_complexity:
            return True, "Comprehensive complexity analysis of both isomorphism and elementary equivalence"
        elif has_isomorphism_complexity:
            return False, "Good complexity analysis of isomorphism but lacking for elementary equivalence"
        elif has_equivalence_complexity:
            return False, "Good complexity analysis of elementary equivalence but lacking for isomorphism"
        else:
            return False, "Missing complexity analysis for both algorithms"
    
    def _contains_model_theory_fundamentals(self, text: str) -> bool:
        """Check if submission explains model theory fundamentals."""
        patterns = [
            r'model.*theory',
            r'mathematical.*structure',
            r'domain.*universe',
            r'interpretation',
            r'first.?order.*logic'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_isomorphism_explanation(self, text: str) -> bool:
        """Check if submission explains isomorphism."""
        patterns = [
            r'isomorphism',
            r'bijective.*function',
            r'structure.*preserving',
            r'graph.*isomorphism',
            r'isomorphic.*structures'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_elementary_equivalence_explanation(self, text: str) -> bool:
        """Check if submission explains elementary equivalence."""
        patterns = [
            r'elementary.*equivalence',
            r'same.*first.?order.*sentences',
            r'ehrenfeucht.?fraisse',
            r'back.*forth',
            r'lowenheim.?skolem'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_definability_analysis(self, text: str) -> bool:
        """Check if submission explains definability."""
        patterns = [
            r'definability',
            r'definable.*property',
            r'first.?order.*definable',
            r'undefinable',
            r'expressive.*power'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_isomorphism_complexity(self, text: str) -> bool:
        """Check if submission analyzes isomorphism complexity."""
        patterns = [
            r'graph.*isomorphism.*np',
            r'isomorphism.*complexity',
            r'exponential.*worst.*case',
            r'polynomial.*time.*special',
            r'GI.*complexity.*class'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_equivalence_complexity(self, text: str) -> bool:
        """Check if submission analyzes elementary equivalence complexity."""
        patterns = [
            r'elementary.*equivalence.*undecidable',
            r'equivalence.*complexity',
            r'ehrenfeucht.*game.*complexity',
            r'model.*checking.*complexity',
            r'satisfiability.*complexity'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)