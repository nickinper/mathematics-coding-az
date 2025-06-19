"""Core challenge framework for mathematical coding problems."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import time


class ChallengeLevel(Enum):
    """Challenge difficulty levels."""
    FOUNDATION = "foundation"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"


class MathematicalDomain(Enum):
    """Mathematical domains covered by challenges."""
    NUMBER_THEORY = "number_theory"
    LINEAR_ALGEBRA = "linear_algebra"
    CALCULUS = "calculus"
    DISCRETE_MATH = "discrete_math"
    PROBABILITY = "probability"
    NUMERICAL_ANALYSIS = "numerical_analysis"
    ABSTRACT_ALGEBRA = "abstract_algebra"
    TOPOLOGY = "topology"
    FUNCTIONAL_ANALYSIS = "functional_analysis"
    DIFFERENTIAL_GEOMETRY = "differential_geometry"
    CATEGORY_THEORY = "category_theory"
    MODEL_THEORY = "model_theory"
    INFORMATION_THEORY = "information_theory"
    GAME_THEORY = "game_theory"
    MATHEMATICAL_LOGIC = "mathematical_logic"


@dataclass
class MathematicalRequirement:
    """Represents a mathematical concept or proof requirement."""
    concept: str
    description: str
    proof_required: bool = False
    complexity_analysis: bool = False
    
    
@dataclass
class TestCase:
    """Individual test case for a challenge."""
    input_data: Any
    expected_output: Any
    timeout: float = 1.0
    description: str = ""
    
    
@dataclass
class ChallengeResult:
    """Result of a challenge submission."""
    passed: bool
    test_results: List[Tuple[TestCase, bool, float]]  # (test, passed, time)
    mathematical_score: float
    code_quality_score: float
    innovation_score: float
    total_score: float
    feedback: str
    errors: List[str]
    

class Challenge(ABC):
    """Base class for mathematical coding challenges."""
    
    def __init__(
        self,
        title: str,
        description: str,
        level: ChallengeLevel,
        domain: MathematicalDomain,
        mathematical_requirements: List[MathematicalRequirement],
        test_cases: List[TestCase],
        time_limit: float = 300.0,
    ):
        self.title = title
        self.description = description
        self.level = level
        self.domain = domain
        self.mathematical_requirements = mathematical_requirements
        self.test_cases = test_cases
        self.time_limit = time_limit
        
    @abstractmethod
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify the mathematical reasoning in the submission.
        
        Returns:
            Tuple of (score, feedback) where score is 0-1.0
        """
        pass
    
    @abstractmethod
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if the submission meets complexity requirements.
        
        Returns:
            Tuple of (meets_requirements, analysis)
        """
        pass
    
    def run_tests(self, student_function) -> List[Tuple[TestCase, bool, float]]:
        """Run all test cases against the student's implementation."""
        results = []
        
        for test_case in self.test_cases:
            try:
                start_time = time.time()
                result = student_function(test_case.input_data)
                execution_time = time.time() - start_time
                
                if execution_time > test_case.timeout:
                    results.append((test_case, False, execution_time))
                else:
                    passed = self._compare_outputs(result, test_case.expected_output)
                    results.append((test_case, passed, execution_time))
                    
            except Exception as e:
                results.append((test_case, False, float('inf')))
                
        return results
    
    def _compare_outputs(self, actual: Any, expected: Any) -> bool:
        """Compare actual output with expected output."""
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            return abs(actual - expected) < 1e-9
        return actual == expected
    
    def evaluate_submission(
        self, 
        submission_code: str, 
        student_function
    ) -> ChallengeResult:
        """Evaluate a complete submission."""
        # Run correctness tests
        test_results = self.run_tests(student_function)
        passed_tests = sum(1 for _, passed, _ in test_results if passed)
        correctness_score = passed_tests / len(test_results)
        
        # Verify mathematical reasoning
        math_score, math_feedback = self.verify_mathematical_reasoning(submission_code)
        
        # Analyze complexity
        complexity_ok, complexity_feedback = self.analyze_complexity(submission_code)
        
        # Calculate code quality score (placeholder)
        code_quality_score = self._evaluate_code_quality(submission_code)
        
        # Calculate innovation score (placeholder)
        innovation_score = self._evaluate_innovation(submission_code)
        
        # Calculate total score
        total_score = (
            correctness_score * 0.4 +
            math_score * 0.3 +
            code_quality_score * 0.2 +
            innovation_score * 0.1
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            test_results, math_feedback, complexity_feedback, correctness_score
        )
        
        return ChallengeResult(
            passed=correctness_score > 0.8 and math_score > 0.7,
            test_results=test_results,
            mathematical_score=math_score,
            code_quality_score=code_quality_score,
            innovation_score=innovation_score,
            total_score=total_score,
            feedback=feedback,
            errors=[]
        )
    
    def _evaluate_code_quality(self, code: str) -> float:
        """Evaluate code quality (placeholder implementation)."""
        # This would analyze code structure, readability, etc.
        return 0.8
    
    def _evaluate_innovation(self, code: str) -> float:
        """Evaluate innovation in the solution (placeholder implementation)."""
        # This would look for creative approaches, optimizations, etc.
        return 0.5
    
    def _generate_feedback(
        self, 
        test_results: List[Tuple[TestCase, bool, float]],
        math_feedback: str,
        complexity_feedback: str,
        correctness_score: float
    ) -> str:
        """Generate comprehensive feedback for the student."""
        feedback_parts = []
        
        # Test results feedback
        if correctness_score < 1.0:
            failed_tests = [test for test, passed, _ in test_results if not passed]
            feedback_parts.append(f"Failed {len(failed_tests)} test cases.")
        
        # Mathematical reasoning feedback
        feedback_parts.append(f"Mathematical reasoning: {math_feedback}")
        
        # Complexity feedback
        feedback_parts.append(f"Complexity analysis: {complexity_feedback}")
        
        return "\n".join(feedback_parts)