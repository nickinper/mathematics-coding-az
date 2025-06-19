"""Optimal failure workflow system for Mathematics-Based Coding AZ."""

import time
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import re

from .challenge import ChallengeResult


class FailureType(Enum):
    """Types of failures in mathematical coding challenges."""
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    MATHEMATICAL_ERROR = "mathematical_error"
    COMPLEXITY_ERROR = "complexity_error"
    PROOF_ERROR = "proof_error"


@dataclass
class FailureProfile:
    """Analysis of a submission failure."""
    failure_type: FailureType
    mathematical_concept: str
    specific_issue: str
    severity: float  # 0-1, where 1 is most severe
    learning_opportunity: str
    suggested_approach: str
    
    
@dataclass
class LearningPath:
    """Alternative learning pathway after failure."""
    approach_name: str
    description: str
    mathematical_focus: str
    estimated_difficulty: float
    prerequisites: List[str]


@dataclass
class FailureAttempt:
    """Individual failure attempt with context."""
    timestamp: float
    code: str
    failure_profile: FailureProfile
    attempt_number: int
    time_spent: float
    mathematical_concepts_used: List[str]
    
    
class HintGenerator:
    """Generates progressive hints based on failure analysis."""
    
    def generate_hints(
        self, 
        failure_profile: FailureProfile, 
        attempt_number: int
    ) -> List[str]:
        """Generate progressive hints based on failure type and attempt count."""
        if attempt_number == 1:
            return self._generate_high_level_hints(failure_profile)
        elif attempt_number == 2:
            return self._generate_specific_hints(failure_profile)
        elif attempt_number >= 3:
            return self._generate_concrete_hints(failure_profile)
        return []
    
    def _generate_high_level_hints(self, profile: FailureProfile) -> List[str]:
        """High-level mathematical insights."""
        hints = {
            FailureType.MATHEMATICAL_ERROR: [
                f"Consider the mathematical property that governs {profile.mathematical_concept}",
                "What theorem or principle applies to this problem?",
                "Think about the fundamental mathematical relationship here"
            ],
            FailureType.COMPLEXITY_ERROR: [
                "Your algorithm's time complexity can be improved",
                "Consider a more mathematically efficient approach",
                "Think about the mathematical structure that enables faster computation"
            ],
            FailureType.PROOF_ERROR: [
                "Your mathematical reasoning needs strengthening",
                "Consider what you're trying to prove more carefully",
                "Think about the logical structure of your argument"
            ]
        }
        return hints.get(profile.failure_type, ["Review the mathematical foundation"])
    
    def _generate_specific_hints(self, profile: FailureProfile) -> List[str]:
        """More specific mathematical guidance."""
        if profile.failure_type == FailureType.MATHEMATICAL_ERROR:
            return [
                f"The key insight involves {profile.mathematical_concept}. How does it apply here?",
                f"Try focusing on: {profile.learning_opportunity}",
                "Consider working through a simpler example first"
            ]
        elif profile.failure_type == FailureType.COMPLEXITY_ERROR:
            return [
                "Your current approach has higher complexity than needed",
                "Look for mathematical properties that enable optimization", 
                "Consider: can you reduce redundant calculations?"
            ]
        return [f"Focus on {profile.suggested_approach}"]
    
    def _generate_concrete_hints(self, profile: FailureProfile) -> List[str]:
        """Concrete stepping stones."""
        return [
            f"Try implementing this first: {profile.learning_opportunity}",
            "Here's a concrete step to focus on:",
            profile.suggested_approach,
            "Would you like to see a worked example of a similar problem?"
        ]


class AlternativePathGenerator:
    """Generates alternative solution approaches after repeated failures."""
    
    def suggest_approaches(
        self, 
        challenge_domain: str, 
        failed_attempts: List[FailureAttempt]
    ) -> List[LearningPath]:
        """Suggest alternative mathematical approaches."""
        if challenge_domain == "number_theory":
            return self._number_theory_paths(failed_attempts)
        elif challenge_domain == "linear_algebra":
            return self._linear_algebra_paths(failed_attempts)
        elif challenge_domain == "calculus":
            return self._calculus_paths(failed_attempts)
        return []
    
    def _number_theory_paths(self, attempts: List[FailureAttempt]) -> List[LearningPath]:
        """Alternative paths for number theory problems."""
        return [
            LearningPath(
                approach_name="Algebraic Approach",
                description="Focus on the algebraic properties and modular arithmetic",
                mathematical_focus="Modular arithmetic, group theory",
                estimated_difficulty=0.7,
                prerequisites=["Basic algebra", "Modular arithmetic"]
            ),
            LearningPath(
                approach_name="Algorithmic Approach", 
                description="Focus on the computational aspects and optimization",
                mathematical_focus="Algorithm design, complexity analysis",
                estimated_difficulty=0.8,
                prerequisites=["Algorithm analysis", "Time complexity"]
            ),
            LearningPath(
                approach_name="Proof-Based Approach",
                description="Start with mathematical proofs and derive the algorithm",
                mathematical_focus="Mathematical proofs, theorem application",
                estimated_difficulty=0.9,
                prerequisites=["Proof techniques", "Number theory theorems"]
            )
        ]
    
    def _linear_algebra_paths(self, attempts: List[FailureAttempt]) -> List[LearningPath]:
        """Alternative paths for linear algebra problems."""
        return [
            LearningPath(
                approach_name="Geometric Interpretation",
                description="Visualize the problem geometrically",
                mathematical_focus="Vector geometry, transformations",
                estimated_difficulty=0.6,
                prerequisites=["Vector operations", "Geometric intuition"]
            ),
            LearningPath(
                approach_name="Matrix Operations",
                description="Focus on matrix algebra and properties",
                mathematical_focus="Matrix algebra, eigenvalues",
                estimated_difficulty=0.8,
                prerequisites=["Matrix operations", "Linear transformations"]
            )
        ]
    
    def _calculus_paths(self, attempts: List[FailureAttempt]) -> List[LearningPath]:
        """Alternative paths for calculus problems."""
        return [
            LearningPath(
                approach_name="Analytical Approach",
                description="Use calculus techniques directly",
                mathematical_focus="Derivatives, optimization theory",
                estimated_difficulty=0.7,
                prerequisites=["Calculus", "Optimization"]
            ),
            LearningPath(
                approach_name="Numerical Approach",
                description="Approximate the solution numerically",
                mathematical_focus="Numerical methods, approximation theory",
                estimated_difficulty=0.6,
                prerequisites=["Numerical analysis", "Error analysis"]
            )
        ]


class StudentFailureProfile:
    """Tracks individual student's failure patterns and learning progress."""
    
    def __init__(self, student_id: str):
        self.student_id = student_id
        self.mathematical_gaps: Dict[str, List[FailureAttempt]] = defaultdict(list)
        self.successful_recoveries: List[Tuple[str, str]] = []  # (concept, recovery_method)
        self.learning_velocity: Dict[str, float] = {}  # concept -> learning_rate
        self.failure_history: List[FailureAttempt] = []
        
    def add_failure(self, attempt: FailureAttempt):
        """Record a new failure attempt."""
        self.failure_history.append(attempt)
        concept = attempt.failure_profile.mathematical_concept
        self.mathematical_gaps[concept].append(attempt)
        
    def add_success(self, concept: str, recovery_method: str):
        """Record successful recovery from failure."""
        self.successful_recoveries.append((concept, recovery_method))
        
        # Calculate learning velocity
        if concept in self.mathematical_gaps:
            attempts = len(self.mathematical_gaps[concept])
            total_time = sum(a.time_spent for a in self.mathematical_gaps[concept])
            self.learning_velocity[concept] = attempts / max(total_time, 1.0)
    
    def get_weakness_areas(self) -> List[Tuple[str, int]]:
        """Get mathematical concepts with most failures."""
        return sorted(
            [(concept, len(attempts)) for concept, attempts in self.mathematical_gaps.items()],
            key=lambda x: x[1],
            reverse=True
        )
    
    def get_learning_patterns(self) -> Dict[str, Any]:
        """Analyze learning patterns from failure history."""
        if not self.failure_history:
            return {}
            
        return {
            "average_attempts_to_success": self._calculate_avg_attempts(),
            "preferred_learning_style": self._identify_learning_style(),
            "mathematical_strengths": self._identify_strengths(),
            "recovery_strategies": self._analyze_recovery_strategies()
        }
    
    def _calculate_avg_attempts(self) -> float:
        """Calculate average attempts before success."""
        if not self.successful_recoveries:
            return 0.0
        
        total_attempts = 0
        for concept, _ in self.successful_recoveries:
            if concept in self.mathematical_gaps:
                total_attempts += len(self.mathematical_gaps[concept])
        
        return total_attempts / len(self.successful_recoveries)
    
    def _identify_learning_style(self) -> str:
        """Identify preferred learning approach."""
        # Analyze which hint types led to success
        return "visual"  # Placeholder
    
    def _identify_strengths(self) -> List[str]:
        """Identify mathematical areas of strength."""
        strengths = []
        for concept, velocity in self.learning_velocity.items():
            if velocity > 0.5:  # Fast learning
                strengths.append(concept)
        return strengths
    
    def _analyze_recovery_strategies(self) -> Dict[str, int]:
        """Analyze which recovery methods work best."""
        strategy_counts = defaultdict(int)
        for _, strategy in self.successful_recoveries:
            strategy_counts[strategy] += 1
        return dict(strategy_counts)


class FailureAnalyzer:
    """Main failure analysis system."""
    
    def __init__(self):
        self.hint_generator = HintGenerator()
        self.path_generator = AlternativePathGenerator()
        self.student_profiles: Dict[str, StudentFailureProfile] = {}
    
    def analyze_failure(
        self, 
        submission_code: str, 
        result: ChallengeResult,
        challenge_info: Dict[str, Any],
        student_id: str,
        attempt_number: int
    ) -> Dict[str, Any]:
        """Comprehensive failure analysis."""
        # Extract failure profile
        failure_profile = self._extract_failure_profile(
            submission_code, result, challenge_info
        )
        
        # Create failure attempt record
        attempt = FailureAttempt(
            timestamp=time.time(),
            code=submission_code,
            failure_profile=failure_profile,
            attempt_number=attempt_number,
            time_spent=0.0,  # Would be tracked elsewhere
            mathematical_concepts_used=self._extract_concepts_used(submission_code)
        )
        
        # Update student profile
        if student_id not in self.student_profiles:
            self.student_profiles[student_id] = StudentFailureProfile(student_id)
        
        self.student_profiles[student_id].add_failure(attempt)
        
        # Generate response
        return self._generate_failure_response(
            failure_profile, attempt_number, challenge_info, student_id
        )
    
    def _extract_failure_profile(
        self, 
        code: str, 
        result: ChallengeResult,
        challenge_info: Dict[str, Any]
    ) -> FailureProfile:
        """Extract detailed failure analysis."""
        # Determine primary failure type
        if not result.passed and result.mathematical_score < 0.5:
            failure_type = FailureType.MATHEMATICAL_ERROR
            concept = self._identify_missing_concept(code, challenge_info)
            issue = "Mathematical reasoning insufficient"
        elif result.mathematical_score > 0.7 and len(result.errors) > 0:
            failure_type = FailureType.LOGIC_ERROR
            concept = "Algorithm implementation"
            issue = "Implementation doesn't match mathematical understanding"
        else:
            failure_type = FailureType.COMPLEXITY_ERROR
            concept = "Algorithm efficiency"
            issue = "Correct but inefficient implementation"
        
        return FailureProfile(
            failure_type=failure_type,
            mathematical_concept=concept,
            specific_issue=issue,
            severity=1.0 - result.total_score,
            learning_opportunity=self._identify_learning_opportunity(failure_type, concept),
            suggested_approach=self._suggest_approach(failure_type, concept)
        )
    
    def _identify_missing_concept(self, code: str, challenge_info: Dict[str, Any]) -> str:
        """Identify which mathematical concept is missing or misunderstood."""
        domain = challenge_info.get('domain', 'unknown')
        
        if domain == 'number_theory':
            if 'fermat' not in code.lower():
                return "Fermat's Little Theorem"
            elif 'modular' not in code.lower():
                return "Modular arithmetic"
            elif 'prime' not in code.lower():
                return "Prime number theory"
        
        return "Unknown concept"
    
    def _extract_concepts_used(self, code: str) -> List[str]:
        """Extract mathematical concepts used in the code."""
        concepts = []
        
        # Look for mathematical terms in comments and docstrings
        math_terms = [
            'theorem', 'proof', 'lemma', 'modular', 'prime', 
            'matrix', 'determinant', 'eigenvalue', 'derivative',
            'integral', 'optimization', 'probability'
        ]
        
        for term in math_terms:
            if term in code.lower():
                concepts.append(term)
        
        return concepts
    
    def _identify_learning_opportunity(self, failure_type: FailureType, concept: str) -> str:
        """Identify the key learning opportunity."""
        opportunities = {
            FailureType.MATHEMATICAL_ERROR: f"Understanding {concept} more deeply",
            FailureType.COMPLEXITY_ERROR: f"Finding more efficient approach for {concept}",
            FailureType.PROOF_ERROR: f"Strengthening proof techniques for {concept}"
        }
        return opportunities.get(failure_type, f"Reviewing {concept}")
    
    def _suggest_approach(self, failure_type: FailureType, concept: str) -> str:
        """Suggest specific approach to overcome the failure."""
        suggestions = {
            FailureType.MATHEMATICAL_ERROR: f"Start with the mathematical foundation of {concept}",
            FailureType.COMPLEXITY_ERROR: f"Look for mathematical properties that enable optimization",
            FailureType.PROOF_ERROR: f"Break down the proof into smaller logical steps"
        }
        return suggestions.get(failure_type, f"Review {concept} fundamentals")
    
    def _generate_failure_response(
        self,
        failure_profile: FailureProfile,
        attempt_number: int,
        challenge_info: Dict[str, Any],
        student_id: str
    ) -> Dict[str, Any]:
        """Generate comprehensive failure response."""
        # Generate hints
        hints = self.hint_generator.generate_hints(failure_profile, attempt_number)
        
        # Generate alternative paths if multiple failures
        alternative_paths = []
        if attempt_number >= 3:
            student_profile = self.student_profiles[student_id]
            alternative_paths = self.path_generator.suggest_approaches(
                challenge_info.get('domain', ''),
                student_profile.failure_history[-3:]  # Last 3 attempts
            )
        
        return {
            'failure_analysis': {
                'type': failure_profile.failure_type.value,
                'concept': failure_profile.mathematical_concept,
                'issue': failure_profile.specific_issue,
                'severity': failure_profile.severity
            },
            'immediate_feedback': {
                'hints': hints,
                'learning_opportunity': failure_profile.learning_opportunity,
                'suggested_approach': failure_profile.suggested_approach
            },
            'alternative_paths': [
                {
                    'name': path.approach_name,
                    'description': path.description,
                    'focus': path.mathematical_focus,
                    'difficulty': path.estimated_difficulty,
                    'prerequisites': path.prerequisites
                }
                for path in alternative_paths
            ],
            'student_insights': self.student_profiles[student_id].get_learning_patterns()
        }