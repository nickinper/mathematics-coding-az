"""Advanced scoring system with learnability rewards and mathematical rigor assessment."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import ast
import re
import math

from src.core.challenge import ChallengeResult


class AssessmentCriteria(Enum):
    """Assessment criteria for mathematical coding challenges."""
    FUNCTIONAL_CORRECTNESS = "functional_correctness"
    MATHEMATICAL_RIGOR = "mathematical_rigor"
    CODE_QUALITY = "code_quality"
    INNOVATION = "innovation"
    PROOF_QUALITY = "proof_quality"
    COMPLEXITY_ANALYSIS = "complexity_analysis"


@dataclass
class LearnabilityReward:
    """Represents reward for productive learning behaviors."""
    exploration_bonus: float = 0.0
    mathematical_insight_bonus: float = 0.0
    failed_attempt_learning_bonus: float = 0.0
    alternative_approach_bonus: float = 0.0
    proof_attempt_bonus: float = 0.0
    
    @property
    def total_reward(self) -> float:
        """Calculate total learnability reward."""
        return (
            self.exploration_bonus +
            self.mathematical_insight_bonus +
            self.failed_attempt_learning_bonus +
            self.alternative_approach_bonus +
            self.proof_attempt_bonus
        )


@dataclass
class DetailedScore:
    """Comprehensive scoring breakdown."""
    criteria_scores: Dict[AssessmentCriteria, float]
    learnability_rewards: LearnabilityReward
    raw_score: float
    adjusted_score: float
    feedback: Dict[str, str]
    strengths: List[str]
    improvement_areas: List[str]


class MathematicalRigorAnalyzer:
    """Analyzes mathematical rigor in submissions."""
    
    def analyze_proof_quality(self, submission: str) -> Tuple[float, str]:
        """Analyze quality of mathematical proofs in submission."""
        score = 0.0
        feedback_parts = []
        
        # Check for proof structure
        if self._has_proof_structure(submission):
            score += 0.3
            feedback_parts.append("✓ Proper proof structure")
        else:
            feedback_parts.append("✗ Missing clear proof structure")
        
        # Check for mathematical notation
        if self._has_mathematical_notation(submission):
            score += 0.2
            feedback_parts.append("✓ Mathematical notation used")
        
        # Check for logical flow
        if self._has_logical_flow(submission):
            score += 0.3
            feedback_parts.append("✓ Logical flow in reasoning")
        else:
            feedback_parts.append("✗ Logical flow needs improvement")
        
        # Check for theorem citations
        if self._cites_theorems(submission):
            score += 0.2
            feedback_parts.append("✓ Relevant theorems cited")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_mathematical_insight(self, submission: str) -> Tuple[float, str]:
        """Analyze depth of mathematical insight."""
        score = 0.0
        feedback_parts = []
        
        # Check for mathematical concepts
        concepts = self._extract_mathematical_concepts(submission)
        if len(concepts) >= 3:
            score += 0.4
            feedback_parts.append(f"✓ Multiple mathematical concepts: {', '.join(concepts)}")
        
        # Check for derivations
        if self._has_derivations(submission):
            score += 0.3
            feedback_parts.append("✓ Mathematical derivations present")
        
        # Check for connections between concepts
        if self._has_concept_connections(submission):
            score += 0.3
            feedback_parts.append("✓ Connections between concepts shown")
        
        return score, "; ".join(feedback_parts)
    
    def _has_proof_structure(self, text: str) -> bool:
        """Check for proof structure indicators."""
        proof_indicators = [
            "proof:", "prove:", "to prove", "we need to show",
            "assume", "let", "suppose", "given", "therefore",
            "thus", "hence", "qed", "∎"
        ]
        return any(indicator in text.lower() for indicator in proof_indicators)
    
    def _has_mathematical_notation(self, text: str) -> bool:
        """Check for mathematical notation."""
        notation_patterns = [
            r'\\[a-zA-Z]+',  # LaTeX commands
            r'[∀∃∈∉⊂⊆∪∩∧∨¬→↔]',  # Mathematical symbols
            r'[α-ωΑ-Ω]',  # Greek letters
            r'\^[0-9]+',  # Exponents
            r'_{[^}]+}',  # Subscripts
        ]
        return any(re.search(pattern, text) for pattern in notation_patterns)
    
    def _has_logical_flow(self, text: str) -> bool:
        """Check for logical flow indicators."""
        flow_indicators = [
            "first", "second", "next", "then", "finally",
            "therefore", "thus", "hence", "consequently",
            "since", "because", "given that", "it follows"
        ]
        return sum(1 for indicator in flow_indicators if indicator in text.lower()) >= 3
    
    def _cites_theorems(self, text: str) -> bool:
        """Check for theorem citations."""
        theorem_patterns = [
            r'[Tt]heorem',
            r'[Ll]emma',
            r'[Cc]orollary',
            r'[Pp]roposition',
            r'[Ff]ermat.*[Ll]ittle.*[Tt]heorem',
            r'[Ee]uler.*[Tt]heorem',
            r'[Pp]ythagorean.*[Tt]heorem'
        ]
        return any(re.search(pattern, text) for pattern in theorem_patterns)
    
    def _extract_mathematical_concepts(self, text: str) -> List[str]:
        """Extract mathematical concepts mentioned."""
        concepts = []
        concept_patterns = {
            'modular arithmetic': r'modular.*arithmetic|mod.*arithmetic',
            'prime numbers': r'prime.*numbers?|primality',
            'matrix operations': r'matrix.*operations?|matrix.*multiplication',
            'derivatives': r'derivatives?|differentiation',
            'integrals': r'integrals?|integration',
            'probability': r'probability|probabilistic',
            'complexity': r'complexity.*analysis|time.*complexity',
            'algorithms': r'algorithms?|algorithmic'
        }
        
        for concept, pattern in concept_patterns.items():
            if re.search(pattern, text.lower()):
                concepts.append(concept)
        
        return concepts
    
    def _has_derivations(self, text: str) -> bool:
        """Check for mathematical derivations."""
        derivation_indicators = [
            "derive", "derivation", "step by step",
            "substitute", "simplify", "expand",
            "factor", "solve for", "rearrange"
        ]
        return any(indicator in text.lower() for indicator in derivation_indicators)
    
    def _has_concept_connections(self, text: str) -> bool:
        """Check for connections between mathematical concepts."""
        connection_indicators = [
            "relates to", "connected to", "combined with",
            "using", "applying", "based on", "follows from"
        ]
        return any(indicator in text.lower() for indicator in connection_indicators)


class CodeQualityAnalyzer:
    """Analyzes code quality aspects."""
    
    def analyze_code_structure(self, code: str) -> Tuple[float, str]:
        """Analyze code structure and organization."""
        score = 0.0
        feedback_parts = []
        
        try:
            tree = ast.parse(code)
            
            # Check for functions
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            if functions:
                score += 0.3
                feedback_parts.append("✓ Functions defined")
            
            # Check for docstrings
            if self._has_docstrings(tree):
                score += 0.2
                feedback_parts.append("✓ Documentation present")
            
            # Check for appropriate naming
            if self._has_good_naming(tree):
                score += 0.2
                feedback_parts.append("✓ Good variable naming")
            
            # Check for code organization
            if self._is_well_organized(tree):
                score += 0.3
                feedback_parts.append("✓ Well-organized code")
            
        except SyntaxError:
            feedback_parts.append("✗ Syntax errors present")
        
        return score, "; ".join(feedback_parts)
    
    def _has_docstrings(self, tree: ast.AST) -> bool:
        """Check for docstrings in functions."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if (node.body and 
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    return True
        return False
    
    def _has_good_naming(self, tree: ast.AST) -> bool:
        """Check for good variable naming conventions."""
        names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.append(node.id)
        
        # Check if names are descriptive (not single letters, except for common cases)
        descriptive_names = [name for name in names if len(name) > 1 or name in 'ijkn']
        return len(descriptive_names) / max(len(names), 1) > 0.7
    
    def _is_well_organized(self, tree: ast.AST) -> bool:
        """Check if code is well-organized."""
        # Simple heuristic: not too many nested levels
        max_depth = 0
        current_depth = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While, ast.If, ast.FunctionDef)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            # This is a simplified check - actual implementation would be more sophisticated
        
        return max_depth <= 4  # Reasonable nesting depth


class InnovationAnalyzer:
    """Analyzes innovation and creativity in solutions."""
    
    def analyze_innovation(self, code: str, submission_text: str) -> Tuple[float, str]:
        """Analyze innovative aspects of the solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for creative algorithmic approaches
        if self._has_creative_algorithm(code):
            score += 0.4
            feedback_parts.append("✓ Creative algorithmic approach")
        
        # Check for optimization insights
        if self._has_optimization_insights(submission_text):
            score += 0.3
            feedback_parts.append("✓ Optimization insights")
        
        # Check for mathematical extensions
        if self._has_mathematical_extensions(submission_text):
            score += 0.3
            feedback_parts.append("✓ Mathematical extensions")
        
        return score, "; ".join(feedback_parts)
    
    def _has_creative_algorithm(self, code: str) -> bool:
        """Check for creative algorithmic approaches."""
        # Look for less common approaches
        creative_patterns = [
            r'recursion.*memoization',
            r'divide.*conquer',
            r'dynamic.*programming',
            r'bit.*manipulation',
            r'mathematical.*optimization'
        ]
        return any(re.search(pattern, code.lower()) for pattern in creative_patterns)
    
    def _has_optimization_insights(self, text: str) -> bool:
        """Check for optimization insights."""
        optimization_keywords = [
            'optimization', 'efficient', 'faster', 'improved',
            'reduced complexity', 'memory efficient', 'cache friendly'
        ]
        return any(keyword in text.lower() for keyword in optimization_keywords)
    
    def _has_mathematical_extensions(self, text: str) -> bool:
        """Check for mathematical extensions beyond requirements."""
        extension_indicators = [
            'generalization', 'extended', 'additional property',
            'further analysis', 'alternative proof', 'related theorem'
        ]
        return any(indicator in text.lower() for indicator in extension_indicators)


class ScoringEngine:
    """Main scoring engine that combines all assessment criteria."""
    
    def __init__(self):
        self.rigor_analyzer = MathematicalRigorAnalyzer()
        self.quality_analyzer = CodeQualityAnalyzer()
        self.innovation_analyzer = InnovationAnalyzer()
        
        # Scoring weights
        self.weights = {
            AssessmentCriteria.FUNCTIONAL_CORRECTNESS: 0.4,
            AssessmentCriteria.MATHEMATICAL_RIGOR: 0.3,
            AssessmentCriteria.CODE_QUALITY: 0.2,
            AssessmentCriteria.INNOVATION: 0.1
        }
    
    def calculate_comprehensive_score(
        self,
        challenge_result: ChallengeResult,
        submission_code: str,
        submission_text: str,
        attempt_history: List[Dict[str, Any]] = None
    ) -> DetailedScore:
        """Calculate comprehensive score with detailed breakdown."""
        
        # Base scores from challenge result
        correctness_score = self._calculate_correctness_score(challenge_result)
        
        # Mathematical rigor analysis
        proof_score, proof_feedback = self.rigor_analyzer.analyze_proof_quality(submission_text)
        insight_score, insight_feedback = self.rigor_analyzer.analyze_mathematical_insight(submission_text)
        rigor_score = (proof_score + insight_score) / 2
        
        # Code quality analysis
        quality_score, quality_feedback = self.quality_analyzer.analyze_code_structure(submission_code)
        
        # Innovation analysis
        innovation_score, innovation_feedback = self.innovation_analyzer.analyze_innovation(
            submission_code, submission_text
        )
        
        # Compile criteria scores
        criteria_scores = {
            AssessmentCriteria.FUNCTIONAL_CORRECTNESS: correctness_score,
            AssessmentCriteria.MATHEMATICAL_RIGOR: rigor_score,
            AssessmentCriteria.CODE_QUALITY: quality_score,
            AssessmentCriteria.INNOVATION: innovation_score
        }
        
        # Calculate weighted raw score
        raw_score = sum(
            score * self.weights[criteria] 
            for criteria, score in criteria_scores.items()
        )
        
        # Calculate learnability rewards
        learnability_rewards = self._calculate_learnability_rewards(
            submission_code, submission_text, attempt_history or []
        )
        
        # Adjust score with learnability rewards
        adjusted_score = min(1.0, raw_score + learnability_rewards.total_reward)
        
        # Generate feedback
        feedback = {
            'correctness': self._generate_correctness_feedback(challenge_result),
            'mathematical_rigor': f"{proof_feedback}; {insight_feedback}",
            'code_quality': quality_feedback,
            'innovation': innovation_feedback
        }
        
        # Identify strengths and improvement areas
        strengths = self._identify_strengths(criteria_scores)
        improvement_areas = self._identify_improvement_areas(criteria_scores)
        
        return DetailedScore(
            criteria_scores=criteria_scores,
            learnability_rewards=learnability_rewards,
            raw_score=raw_score,
            adjusted_score=adjusted_score,
            feedback=feedback,
            strengths=strengths,
            improvement_areas=improvement_areas
        )
    
    def _calculate_correctness_score(self, result: ChallengeResult) -> float:
        """Calculate correctness score from challenge result."""
        if not result.test_results:
            return 0.0
        
        passed_tests = sum(1 for _, passed, _ in result.test_results if passed)
        total_tests = len(result.test_results)
        
        return passed_tests / total_tests
    
    def _calculate_learnability_rewards(
        self,
        code: str,
        text: str,
        attempt_history: List[Dict[str, Any]]
    ) -> LearnabilityReward:
        """Calculate learnability rewards for productive learning behaviors."""
        rewards = LearnabilityReward()
        
        # Exploration bonus
        if self._shows_exploration(code, text):
            rewards.exploration_bonus = 0.1
        
        # Mathematical insight bonus
        if self._shows_mathematical_insight(text):
            rewards.mathematical_insight_bonus = 0.15
        
        # Failed attempt learning bonus
        if len(attempt_history) > 1 and self._shows_learning_from_failure(text, attempt_history):
            rewards.failed_attempt_learning_bonus = 0.1
        
        # Alternative approach bonus
        if self._shows_alternative_approach(code, text):
            rewards.alternative_approach_bonus = 0.1
        
        # Proof attempt bonus
        if self._shows_proof_attempt(text):
            rewards.proof_attempt_bonus = 0.05
        
        return rewards
    
    def _shows_exploration(self, code: str, text: str) -> bool:
        """Check if submission shows mathematical exploration."""
        exploration_indicators = [
            'tried', 'attempted', 'explored', 'considered',
            'alternative', 'different approach', 'experiment'
        ]
        return any(indicator in text.lower() for indicator in exploration_indicators)
    
    def _shows_mathematical_insight(self, text: str) -> bool:
        """Check if submission demonstrates mathematical insight."""
        insight_indicators = [
            'insight', 'realization', 'understanding', 'connection',
            'mathematical property', 'key observation', 'important to note'
        ]
        return any(indicator in text.lower() for indicator in insight_indicators)
    
    def _shows_learning_from_failure(self, text: str, history: List[Dict[str, Any]]) -> bool:
        """Check if submission shows learning from previous failures."""
        learning_indicators = [
            'learned from', 'previous mistake', 'corrected', 'improved',
            'better understanding', 'now realize', 'fixed'
        ]
        return any(indicator in text.lower() for indicator in learning_indicators)
    
    def _shows_alternative_approach(self, code: str, text: str) -> bool:
        """Check if submission presents alternative approaches."""
        alternative_indicators = [
            'alternative', 'another way', 'different method',
            'could also', 'alternatively', 'other approach'
        ]
        return any(indicator in text.lower() for indicator in alternative_indicators)
    
    def _shows_proof_attempt(self, text: str) -> bool:
        """Check if submission contains proof attempts."""
        return self.rigor_analyzer._has_proof_structure(text)
    
    def _generate_correctness_feedback(self, result: ChallengeResult) -> str:
        """Generate feedback for correctness."""
        if result.passed:
            return "✓ All test cases passed"
        else:
            failed_count = sum(1 for _, passed, _ in result.test_results if not passed)
            return f"✗ {failed_count} test cases failed"
    
    def _identify_strengths(self, scores: Dict[AssessmentCriteria, float]) -> List[str]:
        """Identify strengths based on scores."""
        strengths = []
        for criteria, score in scores.items():
            if score >= 0.8:
                strengths.append(criteria.value.replace('_', ' ').title())
        return strengths
    
    def _identify_improvement_areas(self, scores: Dict[AssessmentCriteria, float]) -> List[str]:
        """Identify areas for improvement."""
        improvement_areas = []
        for criteria, score in scores.items():
            if score < 0.6:
                improvement_areas.append(criteria.value.replace('_', ' ').title())
        return improvement_areas