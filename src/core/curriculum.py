"""Curriculum structure and progression system for Mathematics-Based Coding AZ."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from .challenge import MathematicalDomain, ChallengeLevel


class LearningObjectiveType(Enum):
    """Types of learning objectives."""
    CONCEPTUAL = "conceptual"  # Understanding a mathematical concept
    PROCEDURAL = "procedural"  # Implementing an algorithm or procedure
    PROOF = "proof"  # Proving a mathematical property
    ANALYSIS = "analysis"  # Analyzing complexity or characteristics
    APPLICATION = "application"  # Applying concepts to new problems


@dataclass
class LearningObjective:
    """Specific learning objective within a curriculum unit."""
    id: str
    name: str
    description: str
    objective_type: LearningObjectiveType
    mathematical_domain: MathematicalDomain
    proficiency_level: float = 0.0  # 0.0-1.0, will be updated as learner progresses
    prerequisites: List[str] = None  # IDs of prerequisite objectives


@dataclass
class CurriculumUnit:
    """A unit of study within the curriculum."""
    id: str
    title: str
    description: str
    domain: MathematicalDomain
    level: ChallengeLevel
    learning_objectives: List[LearningObjective]
    estimated_time_hours: float
    prerequisite_units: List[str] = None  # IDs of prerequisite units


@dataclass
class LearningPath:
    """A structured path through the curriculum."""
    id: str
    name: str
    description: str
    target_audience: str
    units: List[CurriculumUnit]
    optional_units: List[CurriculumUnit] = None


class CurriculumManager:
    """Manages the curriculum and learning progression."""

    def __init__(self):
        self.learning_objectives: Dict[str, LearningObjective] = {}
        self.curriculum_units: Dict[str, CurriculumUnit] = {}
        self.learning_paths: Dict[str, LearningPath] = {}
        self._initialize_curriculum()

    def get_objective(self, objective_id: str) -> Optional[LearningObjective]:
        """Get a learning objective by ID."""
        return self.learning_objectives.get(objective_id)

    def get_unit(self, unit_id: str) -> Optional[CurriculumUnit]:
        """Get a curriculum unit by ID."""
        return self.curriculum_units.get(unit_id)

    def get_path(self, path_id: str) -> Optional[LearningPath]:
        """Get a learning path by ID."""
        return self.learning_paths.get(path_id)

    def get_next_units(self, completed_unit_ids: List[str]) -> List[CurriculumUnit]:
        """Get next recommended units based on completed units."""
        completed_units = set(completed_unit_ids)
        candidate_units = []

        for unit_id, unit in self.curriculum_units.items():
            if unit_id not in completed_units:
                prerequisites = set(unit.prerequisite_units or [])
                if prerequisites.issubset(completed_units):
                    candidate_units.append(unit)

        return sorted(candidate_units, key=lambda u: u.level.value)

    def get_units_by_domain(self, domain: MathematicalDomain) -> List[CurriculumUnit]:
        """Get all curriculum units for a specific mathematical domain."""
        return [unit for unit in self.curriculum_units.values() 
                if unit.domain == domain]

    def get_units_by_level(self, level: ChallengeLevel) -> List[CurriculumUnit]:
        """Get all curriculum units for a specific difficulty level."""
        return [unit for unit in self.curriculum_units.values() 
                if unit.level == level]

    def get_objectives_by_domain(self, domain: MathematicalDomain) -> List[LearningObjective]:
        """Get all learning objectives for a specific mathematical domain."""
        return [obj for obj in self.learning_objectives.values() 
                if obj.mathematical_domain == domain]

    def get_prerequisite_tree(self, unit_id: str) -> Dict[str, List[str]]:
        """Get the prerequisite tree for a curriculum unit."""
        tree = {}
        
        def build_tree(current_id):
            if current_id in tree:
                return
            
            unit = self.curriculum_units.get(current_id)
            if not unit:
                return
            
            prerequisites = unit.prerequisite_units or []
            tree[current_id] = prerequisites
            
            for prereq_id in prerequisites:
                build_tree(prereq_id)
        
        build_tree(unit_id)
        return tree

    def update_proficiency(self, student_id: str, objective_id: str, score: float) -> None:
        """Update a student's proficiency on a learning objective."""
        # In a real system, this would update a database
        objective = self.learning_objectives.get(objective_id)
        if objective:
            # This is a simplified version - in production this would
            # update a student-specific record in a database
            objective.proficiency_level = score

    def get_learning_gaps(self, student_id: str, target_unit_id: str) -> List[LearningObjective]:
        """Identify learning gaps for a student targeting a specific unit."""
        # In a real system, this would compare student's proficiency levels
        # with required levels for the target unit
        # For now, return a placeholder list of objectives
        target_unit = self.curriculum_units.get(target_unit_id)
        if not target_unit:
            return []
            
        # Get prerequisites
        prereq_tree = self.get_prerequisite_tree(target_unit_id)
        prereq_units = set()
        
        for unit_id, prereqs in prereq_tree.items():
            prereq_units.update(prereqs)
        
        # Get all objectives from prerequisites
        gap_objectives = []
        for unit_id in prereq_units:
            unit = self.curriculum_units.get(unit_id)
            if unit:
                for objective in unit.learning_objectives:
                    if objective.proficiency_level < 0.7:  # Threshold for mastery
                        gap_objectives.append(objective)
        
        return gap_objectives

    def recommend_path(self, student_id: str, interests: List[MathematicalDomain]) -> LearningPath:
        """Recommend a learning path based on student interests."""
        # In a real system, this would use a more sophisticated algorithm
        # For now, pick the first path that includes the most interested domains
        
        best_path = None
        best_match_count = -1
        
        for path in self.learning_paths.values():
            domain_count = 0
            path_domains = set()
            
            for unit in path.units:
                path_domains.add(unit.domain)
            
            match_count = len([domain for domain in interests if domain in path_domains])
            
            if match_count > best_match_count:
                best_match_count = match_count
                best_path = path
        
        return best_path

    def _initialize_curriculum(self):
        """Initialize the curriculum with predefined content."""
        # Create learning objectives
        self._create_number_theory_objectives()
        self._create_linear_algebra_objectives()
        self._create_calculus_objectives()
        
        # Create curriculum units
        self._create_foundation_units()
        self._create_intermediate_units()
        self._create_advanced_units()
        
        # Create learning paths
        self._create_learning_paths()

    def _create_number_theory_objectives(self):
        """Create number theory learning objectives."""
        objectives = [
            LearningObjective(
                id="NT-001",
                name="Modular Arithmetic",
                description="Understand and apply the principles of modular arithmetic.",
                objective_type=LearningObjectiveType.CONCEPTUAL,
                mathematical_domain=MathematicalDomain.NUMBER_THEORY
            ),
            LearningObjective(
                id="NT-002",
                name="Fermat's Little Theorem",
                description="Understand and prove Fermat's Little Theorem.",
                objective_type=LearningObjectiveType.PROOF,
                mathematical_domain=MathematicalDomain.NUMBER_THEORY,
                prerequisites=["NT-001"]
            ),
            LearningObjective(
                id="NT-003",
                name="Fast Modular Exponentiation",
                description="Implement efficient algorithms for modular exponentiation.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.NUMBER_THEORY,
                prerequisites=["NT-001", "NT-002"]
            ),
            LearningObjective(
                id="NT-004",
                name="Prime Number Testing",
                description="Understand and implement primality testing algorithms.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.NUMBER_THEORY
            ),
            LearningObjective(
                id="NT-005",
                name="RSA Cryptosystem",
                description="Understand and implement the RSA encryption algorithm.",
                objective_type=LearningObjectiveType.APPLICATION,
                mathematical_domain=MathematicalDomain.NUMBER_THEORY,
                prerequisites=["NT-002", "NT-003", "NT-004"]
            )
        ]
        
        for obj in objectives:
            self.learning_objectives[obj.id] = obj

    def _create_linear_algebra_objectives(self):
        """Create linear algebra learning objectives."""
        objectives = [
            LearningObjective(
                id="LA-001",
                name="Matrix Operations",
                description="Understand and implement basic matrix operations.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.LINEAR_ALGEBRA
            ),
            LearningObjective(
                id="LA-002",
                name="Determinants",
                description="Calculate and understand the properties of determinants.",
                objective_type=LearningObjectiveType.CONCEPTUAL,
                mathematical_domain=MathematicalDomain.LINEAR_ALGEBRA,
                prerequisites=["LA-001"]
            ),
            LearningObjective(
                id="LA-003",
                name="Matrix Inverse",
                description="Compute matrix inverses and understand their properties.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.LINEAR_ALGEBRA,
                prerequisites=["LA-001", "LA-002"]
            ),
            LearningObjective(
                id="LA-004",
                name="Eigenvalues and Eigenvectors",
                description="Compute and understand eigenvalues and eigenvectors.",
                objective_type=LearningObjectiveType.CONCEPTUAL,
                mathematical_domain=MathematicalDomain.LINEAR_ALGEBRA,
                prerequisites=["LA-003"]
            ),
            LearningObjective(
                id="LA-005",
                name="Linear Transformations",
                description="Understand and apply linear transformations.",
                objective_type=LearningObjectiveType.APPLICATION,
                mathematical_domain=MathematicalDomain.LINEAR_ALGEBRA,
                prerequisites=["LA-001", "LA-004"]
            )
        ]
        
        for obj in objectives:
            self.learning_objectives[obj.id] = obj

    def _create_calculus_objectives(self):
        """Create calculus learning objectives."""
        objectives = [
            LearningObjective(
                id="CA-001",
                name="Limits and Continuity",
                description="Understand and compute limits and analyze continuity.",
                objective_type=LearningObjectiveType.CONCEPTUAL,
                mathematical_domain=MathematicalDomain.CALCULUS
            ),
            LearningObjective(
                id="CA-002",
                name="Differentiation",
                description="Compute derivatives and understand their properties.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.CALCULUS,
                prerequisites=["CA-001"]
            ),
            LearningObjective(
                id="CA-003",
                name="Integration",
                description="Compute integrals and understand their properties.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.CALCULUS,
                prerequisites=["CA-002"]
            ),
            LearningObjective(
                id="CA-004",
                name="Optimization",
                description="Solve optimization problems using calculus.",
                objective_type=LearningObjectiveType.APPLICATION,
                mathematical_domain=MathematicalDomain.CALCULUS,
                prerequisites=["CA-002", "CA-003"]
            ),
            LearningObjective(
                id="CA-005",
                name="Numerical Integration",
                description="Implement numerical integration algorithms.",
                objective_type=LearningObjectiveType.PROCEDURAL,
                mathematical_domain=MathematicalDomain.CALCULUS,
                prerequisites=["CA-003"]
            )
        ]
        
        for obj in objectives:
            self.learning_objectives[obj.id] = obj

    def _create_foundation_units(self):
        """Create foundation-level curriculum units."""
        units = [
            CurriculumUnit(
                id="UNIT-NT-FOUNDATION",
                title="Foundations of Number Theory",
                description="Introduction to number theory concepts and applications",
                domain=MathematicalDomain.NUMBER_THEORY,
                level=ChallengeLevel.FOUNDATION,
                learning_objectives=[
                    self.learning_objectives["NT-001"],
                    self.learning_objectives["NT-002"],
                    self.learning_objectives["NT-003"]
                ],
                estimated_time_hours=10.0
            ),
            CurriculumUnit(
                id="UNIT-LA-FOUNDATION",
                title="Foundations of Linear Algebra",
                description="Introduction to linear algebra concepts and applications",
                domain=MathematicalDomain.LINEAR_ALGEBRA,
                level=ChallengeLevel.FOUNDATION,
                learning_objectives=[
                    self.learning_objectives["LA-001"],
                    self.learning_objectives["LA-002"]
                ],
                estimated_time_hours=12.0
            ),
            CurriculumUnit(
                id="UNIT-CA-FOUNDATION",
                title="Foundations of Calculus",
                description="Introduction to calculus concepts and applications",
                domain=MathematicalDomain.CALCULUS,
                level=ChallengeLevel.FOUNDATION,
                learning_objectives=[
                    self.learning_objectives["CA-001"],
                    self.learning_objectives["CA-002"]
                ],
                estimated_time_hours=15.0
            )
        ]
        
        for unit in units:
            self.curriculum_units[unit.id] = unit

    def _create_intermediate_units(self):
        """Create intermediate-level curriculum units."""
        units = [
            CurriculumUnit(
                id="UNIT-NT-INTERMEDIATE",
                title="Intermediate Number Theory",
                description="Advanced number theory concepts and cryptographic applications",
                domain=MathematicalDomain.NUMBER_THEORY,
                level=ChallengeLevel.INTERMEDIATE,
                learning_objectives=[
                    self.learning_objectives["NT-004"],
                    self.learning_objectives["NT-005"]
                ],
                estimated_time_hours=15.0,
                prerequisite_units=["UNIT-NT-FOUNDATION"]
            ),
            CurriculumUnit(
                id="UNIT-LA-INTERMEDIATE",
                title="Intermediate Linear Algebra",
                description="Advanced linear algebra concepts and applications",
                domain=MathematicalDomain.LINEAR_ALGEBRA,
                level=ChallengeLevel.INTERMEDIATE,
                learning_objectives=[
                    self.learning_objectives["LA-003"],
                    self.learning_objectives["LA-004"]
                ],
                estimated_time_hours=18.0,
                prerequisite_units=["UNIT-LA-FOUNDATION"]
            ),
            CurriculumUnit(
                id="UNIT-CA-INTERMEDIATE",
                title="Intermediate Calculus",
                description="Advanced calculus concepts and applications",
                domain=MathematicalDomain.CALCULUS,
                level=ChallengeLevel.INTERMEDIATE,
                learning_objectives=[
                    self.learning_objectives["CA-003"],
                    self.learning_objectives["CA-004"]
                ],
                estimated_time_hours=20.0,
                prerequisite_units=["UNIT-CA-FOUNDATION"]
            )
        ]
        
        for unit in units:
            self.curriculum_units[unit.id] = unit

    def _create_advanced_units(self):
        """Create advanced-level curriculum units."""
        units = [
            CurriculumUnit(
                id="UNIT-NT-ADVANCED",
                title="Advanced Number Theory",
                description="Advanced cryptographic systems and number theory research",
                domain=MathematicalDomain.NUMBER_THEORY,
                level=ChallengeLevel.ADVANCED,
                learning_objectives=[
                    self.learning_objectives["NT-005"]  # More advanced application
                ],
                estimated_time_hours=25.0,
                prerequisite_units=["UNIT-NT-INTERMEDIATE"]
            ),
            CurriculumUnit(
                id="UNIT-LA-ADVANCED",
                title="Advanced Linear Algebra",
                description="Advanced linear algebra applications and computational methods",
                domain=MathematicalDomain.LINEAR_ALGEBRA,
                level=ChallengeLevel.ADVANCED,
                learning_objectives=[
                    self.learning_objectives["LA-005"]
                ],
                estimated_time_hours=22.0,
                prerequisite_units=["UNIT-LA-INTERMEDIATE"]
            ),
            CurriculumUnit(
                id="UNIT-CA-ADVANCED",
                title="Advanced Calculus",
                description="Advanced calculus applications and numerical methods",
                domain=MathematicalDomain.CALCULUS,
                level=ChallengeLevel.ADVANCED,
                learning_objectives=[
                    self.learning_objectives["CA-005"]
                ],
                estimated_time_hours=28.0,
                prerequisite_units=["UNIT-CA-INTERMEDIATE"]
            )
        ]
        
        for unit in units:
            self.curriculum_units[unit.id] = unit

    def _create_learning_paths(self):
        """Create learning paths through the curriculum."""
        paths = [
            LearningPath(
                id="PATH-CRYPTOGRAPHY",
                name="Cryptography Specialist",
                description="Focus on number theory and cryptographic applications",
                target_audience="Students interested in cybersecurity and cryptography",
                units=[
                    self.curriculum_units["UNIT-NT-FOUNDATION"],
                    self.curriculum_units["UNIT-NT-INTERMEDIATE"],
                    self.curriculum_units["UNIT-NT-ADVANCED"],
                    self.curriculum_units["UNIT-LA-FOUNDATION"]
                ],
                optional_units=[
                    self.curriculum_units["UNIT-LA-INTERMEDIATE"]
                ]
            ),
            LearningPath(
                id="PATH-DATA-SCIENCE",
                name="Data Science Mathematics",
                description="Focus on linear algebra and calculus for data science",
                target_audience="Students interested in data science and machine learning",
                units=[
                    self.curriculum_units["UNIT-LA-FOUNDATION"],
                    self.curriculum_units["UNIT-LA-INTERMEDIATE"],
                    self.curriculum_units["UNIT-CA-FOUNDATION"],
                    self.curriculum_units["UNIT-CA-INTERMEDIATE"]
                ],
                optional_units=[
                    self.curriculum_units["UNIT-LA-ADVANCED"],
                    self.curriculum_units["UNIT-CA-ADVANCED"]
                ]
            ),
            LearningPath(
                id="PATH-COMPREHENSIVE",
                name="Comprehensive Mathematical Foundations",
                description="Balanced approach covering all mathematical domains",
                target_audience="Students seeking a broad mathematical foundation",
                units=[
                    self.curriculum_units["UNIT-NT-FOUNDATION"],
                    self.curriculum_units["UNIT-LA-FOUNDATION"],
                    self.curriculum_units["UNIT-CA-FOUNDATION"],
                    self.curriculum_units["UNIT-NT-INTERMEDIATE"],
                    self.curriculum_units["UNIT-LA-INTERMEDIATE"],
                    self.curriculum_units["UNIT-CA-INTERMEDIATE"]
                ],
                optional_units=[
                    self.curriculum_units["UNIT-NT-ADVANCED"],
                    self.curriculum_units["UNIT-LA-ADVANCED"],
                    self.curriculum_units["UNIT-CA-ADVANCED"]
                ]
            )
        ]
        
        for path in paths:
            self.learning_paths[path.id] = path


# Singleton instance
curriculum_manager = CurriculumManager()


def get_curriculum_manager() -> CurriculumManager:
    """Get the singleton curriculum manager instance."""
    return curriculum_manager


def get_learning_objectives(domain: Optional[MathematicalDomain] = None) -> List[LearningObjective]:
    """Get learning objectives, optionally filtered by domain."""
    manager = get_curriculum_manager()
    
    if domain:
        return manager.get_objectives_by_domain(domain)
    return list(manager.learning_objectives.values())


def get_curriculum_units(level: Optional[ChallengeLevel] = None,
                        domain: Optional[MathematicalDomain] = None) -> List[CurriculumUnit]:
    """Get curriculum units, optionally filtered by level and/or domain."""
    manager = get_curriculum_manager()
    
    if level and domain:
        return [unit for unit in manager.curriculum_units.values()
                if unit.level == level and unit.domain == domain]
    elif level:
        return manager.get_units_by_level(level)
    elif domain:
        return manager.get_units_by_domain(domain)
    
    return list(manager.curriculum_units.values())


def get_learning_paths() -> List[LearningPath]:
    """Get all available learning paths."""
    manager = get_curriculum_manager()
    return list(manager.learning_paths.values())


def recommend_learning_path(student_id: str, interests: List[MathematicalDomain]) -> LearningPath:
    """Recommend a learning path based on student interests."""
    manager = get_curriculum_manager()
    return manager.recommend_path(student_id, interests)


def get_next_recommended_units(student_id: str, completed_unit_ids: List[str]) -> List[CurriculumUnit]:
    """Get next recommended units for a student based on completed units."""
    manager = get_curriculum_manager()
    return manager.get_next_units(completed_unit_ids)


def get_student_learning_gaps(student_id: str, target_unit_id: str) -> List[LearningObjective]:
    """Identify learning gaps for a student targeting a specific unit."""
    manager = get_curriculum_manager()
    return manager.get_learning_gaps(student_id, target_unit_id)