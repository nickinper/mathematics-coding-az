"""Assessment rubrics for mathematical coding challenges."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any

from src.core.challenge import MathematicalDomain, ChallengeLevel


class RubricCriteria(Enum):
    """Criteria used in assessment rubrics."""
    MATHEMATICAL_CORRECTNESS = "mathematical_correctness"
    MATHEMATICAL_RIGOR = "mathematical_rigor"
    PROOF_QUALITY = "proof_quality"
    ALGORITHMIC_IMPLEMENTATION = "algorithmic_implementation"
    CODE_QUALITY = "code_quality"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    CREATIVITY = "creativity"
    EXPLANATION_CLARITY = "explanation_clarity"


@dataclass
class CriterionDescriptor:
    """Describes expectations for a single criterion at different levels."""
    criterion: RubricCriteria
    description: str
    weight: float
    excellent_descriptor: str
    good_descriptor: str
    satisfactory_descriptor: str
    needs_improvement_descriptor: str
    excellent_score_range: Tuple[float, float] = (0.85, 1.0)
    good_score_range: Tuple[float, float] = (0.7, 0.85)
    satisfactory_score_range: Tuple[float, float] = (0.5, 0.7)
    needs_improvement_score_range: Tuple[float, float] = (0.0, 0.5)

    def get_descriptor_for_score(self, score: float) -> str:
        """Get the appropriate descriptor text for a given score."""
        if self.excellent_score_range[0] <= score <= self.excellent_score_range[1]:
            return self.excellent_descriptor
        elif self.good_score_range[0] <= score < self.good_score_range[1]:
            return self.good_descriptor
        elif self.satisfactory_score_range[0] <= score < self.satisfactory_score_range[1]:
            return self.satisfactory_descriptor
        else:
            return self.needs_improvement_descriptor


@dataclass
class AssessmentRubric:
    """Comprehensive assessment rubric for a mathematical coding challenge."""
    name: str
    description: str
    domain: MathematicalDomain
    level: ChallengeLevel
    criteria: List[CriterionDescriptor] = field(default_factory=list)
    total_points: int = 100
    
    def add_criterion(self, criterion: CriterionDescriptor) -> None:
        """Add a criterion to the rubric."""
        self.criteria.append(criterion)
    
    def evaluate(self, scores: Dict[RubricCriteria, float]) -> Dict[str, Any]:
        """Evaluate a submission against this rubric."""
        total_score = 0.0
        weighted_total = 0.0
        criterion_results = []
        
        for criterion_desc in self.criteria:
            if criterion_desc.criterion not in scores:
                continue
                
            score = scores[criterion_desc.criterion]
            weighted_score = score * criterion_desc.weight
            weighted_total += criterion_desc.weight
            total_score += weighted_score
            
            criterion_results.append({
                "criterion": criterion_desc.criterion.value,
                "score": score,
                "weighted_score": weighted_score,
                "descriptor": criterion_desc.get_descriptor_for_score(score)
            })
        
        # Normalize if weights don't sum to 1
        if weighted_total > 0:
            final_score = total_score / weighted_total
        else:
            final_score = 0.0
            
        # Convert to point scale if needed
        points = final_score * self.total_points
        
        return {
            "total_score": final_score,
            "total_points": points,
            "criterion_results": criterion_results,
            "letter_grade": self._score_to_letter(final_score)
        }
    
    def _score_to_letter(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 0.9:
            return "A"
        elif score >= 0.8:
            return "B"
        elif score >= 0.7:
            return "C"
        elif score >= 0.6:
            return "D"
        else:
            return "F"


class RubricFactory:
    """Factory for creating assessment rubrics."""
    
    @classmethod
    def create_number_theory_rubric(cls, level: ChallengeLevel) -> AssessmentRubric:
        """Create a rubric for number theory challenges."""
        rubric = AssessmentRubric(
            name=f"{level.value.title()} Number Theory Assessment",
            description=f"Assessment rubric for {level.value} number theory challenges",
            domain=MathematicalDomain.NUMBER_THEORY,
            level=level
        )
        
        # Add criteria based on level
        if level == ChallengeLevel.FOUNDATION:
            cls._add_foundation_criteria(rubric)
        elif level == ChallengeLevel.INTERMEDIATE:
            cls._add_intermediate_criteria(rubric)
        elif level == ChallengeLevel.ADVANCED:
            cls._add_advanced_criteria(rubric)
            
        return rubric
    
    @classmethod
    def create_linear_algebra_rubric(cls, level: ChallengeLevel) -> AssessmentRubric:
        """Create a rubric for linear algebra challenges."""
        rubric = AssessmentRubric(
            name=f"{level.value.title()} Linear Algebra Assessment",
            description=f"Assessment rubric for {level.value} linear algebra challenges",
            domain=MathematicalDomain.LINEAR_ALGEBRA,
            level=level
        )
        
        # Add criteria based on level
        if level == ChallengeLevel.FOUNDATION:
            cls._add_foundation_criteria(rubric)
        elif level == ChallengeLevel.INTERMEDIATE:
            cls._add_intermediate_criteria(rubric)
        elif level == ChallengeLevel.ADVANCED:
            cls._add_advanced_criteria(rubric)
            
        return rubric
    
    @classmethod
    def _add_foundation_criteria(cls, rubric: AssessmentRubric) -> None:
        """Add foundation level criteria to rubric."""
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.MATHEMATICAL_CORRECTNESS,
            description="Correctness of mathematical approach and results",
            weight=0.4,
            excellent_descriptor="Perfect mathematical implementation with comprehensive understanding",
            good_descriptor="Mostly correct mathematical implementation with good understanding",
            satisfactory_descriptor="Basic mathematical implementation with some understanding",
            needs_improvement_descriptor="Incorrect mathematical implementation with limited understanding"
        ))
        
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.ALGORITHMIC_IMPLEMENTATION,
            description="Implementation of algorithm and code correctness",
            weight=0.3,
            excellent_descriptor="Flawless implementation with excellent design",
            good_descriptor="Correct implementation with good design",
            satisfactory_descriptor="Working implementation with acceptable design",
            needs_improvement_descriptor="Flawed implementation with poor design"
        ))
        
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.CODE_QUALITY,
            description="Code structure, readability, and documentation",
            weight=0.2,
            excellent_descriptor="Exceptionally well-structured, documented, and readable code",
            good_descriptor="Well-structured, documented, and readable code",
            satisfactory_descriptor="Adequately structured code with basic documentation",
            needs_improvement_descriptor="Poorly structured code with minimal documentation"
        ))
        
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.EXPLANATION_CLARITY,
            description="Clarity of mathematical explanation",
            weight=0.1,
            excellent_descriptor="Crystal clear explanation with excellent mathematical communication",
            good_descriptor="Clear explanation with good mathematical communication",
            satisfactory_descriptor="Basic explanation with adequate mathematical communication",
            needs_improvement_descriptor="Unclear explanation with poor mathematical communication"
        ))
    
    @classmethod
    def _add_intermediate_criteria(cls, rubric: AssessmentRubric) -> None:
        """Add intermediate level criteria to rubric."""
        # Include foundation criteria with adjusted weights
        cls._add_foundation_criteria(rubric)
        
        # Add more sophisticated criteria
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.MATHEMATICAL_RIGOR,
            description="Rigor in mathematical reasoning and proofs",
            weight=0.3,
            excellent_descriptor="Highly rigorous mathematical reasoning with formal proofs",
            good_descriptor="Rigorous mathematical reasoning with mostly correct proofs",
            satisfactory_descriptor="Basic mathematical reasoning with attempted proofs",
            needs_improvement_descriptor="Limited mathematical reasoning without proper proofs"
        ))
        
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.PERFORMANCE_OPTIMIZATION,
            description="Optimization of algorithm and performance considerations",
            weight=0.2,
            excellent_descriptor="Highly optimized solution with excellent performance analysis",
            good_descriptor="Well-optimized solution with good performance analysis",
            satisfactory_descriptor="Basic optimization with some performance analysis",
            needs_improvement_descriptor="Unoptimized solution with minimal performance analysis"
        ))
    
    @classmethod
    def _add_advanced_criteria(cls, rubric: AssessmentRubric) -> None:
        """Add advanced level criteria to rubric."""
        # Include intermediate criteria
        cls._add_intermediate_criteria(rubric)
        
        # Add most sophisticated criteria
        rubric.add_criterion(CriterionDescriptor(
            criterion=RubricCriteria.CREATIVITY,
            description="Creativity and innovation in approach",
            weight=0.2,
            excellent_descriptor="Highly creative and innovative approach",
            good_descriptor="Creative approach with novel elements",
            satisfactory_descriptor="Somewhat creative approach with some original elements",
            needs_improvement_descriptor="Standard approach without creativity"
        ))
        
        # Adjust weights for advanced level
        for criterion in rubric.criteria:
            if criterion.criterion == RubricCriteria.MATHEMATICAL_RIGOR:
                criterion.weight = 0.35
            elif criterion.criterion == RubricCriteria.PROOF_QUALITY:
                criterion.weight = 0.25


def get_rubric_for_challenge(domain: MathematicalDomain, level: ChallengeLevel) -> AssessmentRubric:
    """Get the appropriate rubric for a challenge based on domain and level."""
    factory = RubricFactory()
    
    if domain == MathematicalDomain.NUMBER_THEORY:
        return factory.create_number_theory_rubric(level)
    elif domain == MathematicalDomain.LINEAR_ALGEBRA:
        return factory.create_linear_algebra_rubric(level)
    else:
        # Default to number theory for now
        return factory.create_number_theory_rubric(level)