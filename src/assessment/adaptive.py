"""Adaptive difficulty and curriculum progression system."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import math
import time

from src.core.challenge import MathematicalDomain, ChallengeLevel
from src.core.curriculum import CurriculumUnit, LearningObjective, LearningPath


class AdaptiveStrategy(Enum):
    """Strategies for adaptive difficulty adjustment."""
    GRADUAL = "gradual"  # Slowly increase/decrease difficulty
    RESPONSIVE = "responsive"  # Quickly respond to performance
    EXPLORATORY = "exploratory"  # Occasionally push beyond comfort zone
    REINFORCEMENT = "reinforcement"  # Focus on reinforcing weak areas


@dataclass
class StudentProfile:
    """Student profile for adaptive learning."""
    id: str
    learning_velocity: Dict[MathematicalDomain, float] = field(default_factory=dict)
    proficiency_levels: Dict[str, float] = field(default_factory=dict)  # objective_id -> level
    attempt_history: List[Dict[str, Any]] = field(default_factory=list)
    completed_units: List[str] = field(default_factory=list)
    current_path: Optional[str] = None
    preferred_strategy: AdaptiveStrategy = AdaptiveStrategy.GRADUAL
    
    def update_proficiency(self, objective_id: str, score: float) -> None:
        """Update proficiency level for a learning objective."""
        # Simple weighted average with previous score
        if objective_id in self.proficiency_levels:
            prev_level = self.proficiency_levels[objective_id]
            # More weight to new score if it's higher (faster progress)
            weight = 0.6 if score > prev_level else 0.3
            self.proficiency_levels[objective_id] = (
                prev_level * (1 - weight) + score * weight
            )
        else:
            self.proficiency_levels[objective_id] = score
    
    def get_domain_proficiency(self, domain: MathematicalDomain) -> float:
        """Get overall proficiency in a domain."""
        # This would typically use data from curriculum manager
        # to identify which objectives belong to this domain
        domain_objectives = [
            obj_id for obj_id in self.proficiency_levels.keys()
            if obj_id.startswith(domain.value[:2].upper())
        ]
        
        if not domain_objectives:
            return 0.0
            
        return sum(self.proficiency_levels[obj_id] 
                  for obj_id in domain_objectives) / len(domain_objectives)
    
    def record_attempt(self, challenge_id: str, score: float, time_spent: float) -> None:
        """Record an attempt at a challenge."""
        self.attempt_history.append({
            "challenge_id": challenge_id,
            "score": score,
            "time_spent": time_spent,
            "timestamp": time.time()
        })
    
    def complete_unit(self, unit_id: str) -> None:
        """Mark a curriculum unit as completed."""
        if unit_id not in self.completed_units:
            self.completed_units.append(unit_id)


class AdaptiveDifficulty:
    """Manages adaptive difficulty for challenges."""
    
    def __init__(self):
        self.difficulty_levels = {
            ChallengeLevel.FOUNDATION: (0.3, 0.5),  # (min_proficiency, target_proficiency)
            ChallengeLevel.INTERMEDIATE: (0.5, 0.7),
            ChallengeLevel.ADVANCED: (0.7, 0.9)
        }
    
    def recommend_difficulty(
        self,
        student: StudentProfile,
        domain: MathematicalDomain,
        current_level: Optional[ChallengeLevel] = None
    ) -> ChallengeLevel:
        """Recommend an appropriate difficulty level."""
        proficiency = student.get_domain_proficiency(domain)
        
        # Determine appropriate level based on proficiency
        if proficiency < self.difficulty_levels[ChallengeLevel.FOUNDATION][1]:
            recommended = ChallengeLevel.FOUNDATION
        elif proficiency < self.difficulty_levels[ChallengeLevel.INTERMEDIATE][1]:
            recommended = ChallengeLevel.INTERMEDIATE
        else:
            recommended = ChallengeLevel.ADVANCED
            
        # Apply adaptive strategy
        if student.preferred_strategy == AdaptiveStrategy.EXPLORATORY:
            # Occasionally push to higher level
            if (current_level == ChallengeLevel.FOUNDATION and 
                proficiency >= self.difficulty_levels[ChallengeLevel.FOUNDATION][0] * 1.2):
                return ChallengeLevel.INTERMEDIATE
            elif (current_level == ChallengeLevel.INTERMEDIATE and
                  proficiency >= self.difficulty_levels[ChallengeLevel.INTERMEDIATE][0] * 1.2):
                return ChallengeLevel.ADVANCED
                
        elif student.preferred_strategy == AdaptiveStrategy.REINFORCEMENT:
            # Stay at current level longer for reinforcement
            if current_level and proficiency < self.difficulty_levels[current_level][1] * 1.1:
                return current_level
                
        return recommended
    
    def adjust_challenge_parameters(
        self,
        base_parameters: Dict[str, Any],
        student: StudentProfile,
        domain: MathematicalDomain
    ) -> Dict[str, Any]:
        """Adjust challenge parameters based on student profile."""
        proficiency = student.get_domain_proficiency(domain)
        params = base_parameters.copy()
        
        # Adjust time limit based on proficiency
        if "time_limit" in params:
            time_factor = 1.0 + max(0, 0.5 - proficiency)  # More time for lower proficiency
            params["time_limit"] = params["time_limit"] * time_factor
        
        # Adjust test case difficulty
        if "test_cases" in params:
            # In a real implementation, this would select appropriate test cases
            # from a difficulty-stratified pool
            pass
            
        # Adjust hint availability
        params["hints_available"] = proficiency < 0.7
        
        return params
    
    def calculate_achievement_level(self, scores: List[float], expected_difficulty: float) -> float:
        """Calculate achievement level considering challenge difficulty."""
        if not scores:
            return 0.0
            
        avg_score = sum(scores) / len(scores)
        
        # Adjust for difficulty (higher achievement for same score on harder challenges)
        achievement = avg_score * (1.0 + expected_difficulty * 0.5)
        
        return min(1.0, achievement)


class CurriculumAdapter:
    """Adapts curriculum progression based on student performance."""
    
    def recommend_next_unit(
        self,
        student: StudentProfile,
        available_units: List[CurriculumUnit]
    ) -> Optional[CurriculumUnit]:
        """Recommend the next curriculum unit for a student."""
        if not available_units:
            return None
            
        # Filter to units not yet completed
        candidate_units = [unit for unit in available_units
                          if unit.id not in student.completed_units]
        
        if not candidate_units:
            return None
            
        # Check prerequisites
        qualified_units = []
        for unit in candidate_units:
            prerequisites = unit.prerequisite_units or []
            if all(prereq in student.completed_units for prereq in prerequisites):
                qualified_units.append(unit)
                
        if not qualified_units:
            return None
            
        # Find best match based on student's proficiency
        best_unit = None
        best_match_score = -float('inf')
        
        for unit in qualified_units:
            # Calculate average proficiency for unit's objectives
            objectives_proficiency = []
            for objective in unit.learning_objectives:
                if objective.id in student.proficiency_levels:
                    objectives_proficiency.append(student.proficiency_levels[objective.id])
                else:
                    objectives_proficiency.append(0.0)
                    
            avg_proficiency = sum(objectives_proficiency) / len(objectives_proficiency)
            
            # Calculate match score (prefer units with proficiency just below target)
            target_proficiency = 0.7  # Target proficiency level
            match_score = -abs(avg_proficiency - (target_proficiency - 0.2))
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_unit = unit
                
        return best_unit
    
    def generate_personalized_path(
        self,
        student: StudentProfile,
        base_path: LearningPath,
        available_units: List[CurriculumUnit]
    ) -> LearningPath:
        """Generate a personalized learning path for a student."""
        # Start with base path
        personalized_path = LearningPath(
            id=f"{base_path.id}_personalized_{student.id}",
            name=f"Personalized {base_path.name}",
            description=f"Customized version of {base_path.name} for your learning profile",
            target_audience="Individual student",
            units=[]
        )
        
        # Add core units from base path that match prerequisites
        for unit in base_path.units:
            prerequisites = unit.prerequisite_units or []
            if all(prereq in student.completed_units for prereq in prerequisites):
                personalized_path.units.append(unit)
        
        # Identify weak areas
        weak_domains = []
        for domain in MathematicalDomain:
            proficiency = student.get_domain_proficiency(domain)
            if proficiency < 0.5:
                weak_domains.append(domain)
        
        # Add units for weak areas
        for domain in weak_domains:
            domain_units = [unit for unit in available_units 
                           if unit.domain == domain and unit.id not in student.completed_units]
            
            # Sort by level
            domain_units.sort(key=lambda u: u.level.value)
            
            # Add up to 2 units for each weak domain
            for unit in domain_units[:2]:
                if unit not in personalized_path.units:
                    personalized_path.units.append(unit)
        
        return personalized_path
    
    def evaluate_path_completion(self, student: StudentProfile, path: LearningPath) -> float:
        """Evaluate the completion percentage of a learning path."""
        if not path.units:
            return 0.0
            
        completed_units = [unit for unit in path.units 
                          if unit.id in student.completed_units]
        
        return len(completed_units) / len(path.units)
    
    def recommend_learning_strategy(self, student: StudentProfile) -> AdaptiveStrategy:
        """Recommend an adaptive learning strategy based on student profile."""
        if not student.attempt_history:
            return AdaptiveStrategy.GRADUAL
            
        # Calculate learning velocity
        recent_attempts = student.attempt_history[-10:]
        scores = [attempt["score"] for attempt in recent_attempts]
        
        # Check for consistent high performance
        if all(score > 0.8 for score in scores):
            return AdaptiveStrategy.EXPLORATORY
            
        # Check for struggling performance
        if all(score < 0.6 for score in scores):
            return AdaptiveStrategy.REINFORCEMENT
            
        # Check for inconsistent performance
        score_variance = sum((score - sum(scores)/len(scores))**2 for score in scores) / len(scores)
        if score_variance > 0.04:  # High variance
            return AdaptiveStrategy.GRADUAL
            
        # Default to responsive for moderate, consistent performance
        return AdaptiveStrategy.RESPONSIVE