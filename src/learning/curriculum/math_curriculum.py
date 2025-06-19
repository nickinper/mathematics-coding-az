"""
Mathematical Curriculum Manager for Progressive AI Learning
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class Difficulty(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class ComplexityClass(Enum):
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEARITHMIC = "O(n log n)"
    QUADRATIC = "O(n²)"
    CUBIC = "O(n³)"
    EXPONENTIAL = "O(2^n)"


@dataclass
class MathConcept:
    name: str
    category: str
    difficulty: Difficulty
    prerequisites: List[str]
    computational_complexity: ComplexityClass
    key_algorithms: List[str]
    theoretical_depth: int  # 1-10 scale
    

@dataclass
class ProblemTemplate:
    concept: str
    problem_type: str
    input_constraints: Dict
    expected_complexity: ComplexityClass
    mathematical_properties: List[str]
    test_case_generator: str  # Function name for generating test cases


class MathematicalCurriculum:
    def __init__(self):
        self.concepts = self._initialize_concepts()
        self.learning_path = self._build_learning_path()
        
    def _initialize_concepts(self) -> Dict[str, MathConcept]:
        """Initialize the mathematical concept hierarchy"""
        return {
            # Foundation Level
            "arithmetic": MathConcept(
                name="Arithmetic Operations",
                category="foundations",
                difficulty=Difficulty.BEGINNER,
                prerequisites=[],
                computational_complexity=ComplexityClass.CONSTANT,
                key_algorithms=["modular_exponentiation", "fast_multiplication"],
                theoretical_depth=3
            ),
            "number_theory": MathConcept(
                name="Number Theory",
                category="foundations",
                difficulty=Difficulty.BEGINNER,
                prerequisites=["arithmetic"],
                computational_complexity=ComplexityClass.LOGARITHMIC,
                key_algorithms=["euclidean_algorithm", "sieve_of_eratosthenes"],
                theoretical_depth=5
            ),
            # Intermediate Level
            "linear_algebra": MathConcept(
                name="Linear Algebra",
                category="core_mathematics",
                difficulty=Difficulty.INTERMEDIATE,
                prerequisites=["arithmetic"],
                computational_complexity=ComplexityClass.CUBIC,
                key_algorithms=["gaussian_elimination", "svd", "eigendecomposition"],
                theoretical_depth=7
            ),
            "calculus": MathConcept(
                name="Calculus & Numerical Methods",
                category="core_mathematics",
                difficulty=Difficulty.INTERMEDIATE,
                prerequisites=["arithmetic", "linear_algebra"],
                computational_complexity=ComplexityClass.QUADRATIC,
                key_algorithms=["newton_raphson", "runge_kutta", "monte_carlo"],
                theoretical_depth=8
            ),
            # Advanced Level
            "optimization": MathConcept(
                name="Optimization Theory",
                category="advanced_mathematics",
                difficulty=Difficulty.ADVANCED,
                prerequisites=["linear_algebra", "calculus"],
                computational_complexity=ComplexityClass.EXPONENTIAL,
                key_algorithms=["gradient_descent", "simplex", "interior_point"],
                theoretical_depth=9
            ),
            "graph_theory": MathConcept(
                name="Graph Theory & Combinatorics",
                category="advanced_mathematics",
                difficulty=Difficulty.ADVANCED,
                prerequisites=["number_theory", "linear_algebra"],
                computational_complexity=ComplexityClass.EXPONENTIAL,
                key_algorithms=["dijkstra", "floyd_warshall", "max_flow"],
                theoretical_depth=8
            ),
            # Expert Level - Software Engineering Mathematics
            "computational_complexity": MathConcept(
                name="Computational Complexity Theory",
                category="theoretical_cs",
                difficulty=Difficulty.EXPERT,
                prerequisites=["optimization", "graph_theory"],
                computational_complexity=ComplexityClass.EXPONENTIAL,
                key_algorithms=["np_complete_reductions", "approximation_algorithms"],
                theoretical_depth=10
            ),
            "quantum_computing": MathConcept(
                name="Quantum Computing Mathematics",
                category="cutting_edge",
                difficulty=Difficulty.EXPERT,
                prerequisites=["linear_algebra", "computational_complexity"],
                computational_complexity=ComplexityClass.EXPONENTIAL,
                key_algorithms=["shor", "grover", "quantum_fourier_transform"],
                theoretical_depth=10
            )
        }
    
    def _build_learning_path(self) -> List[List[str]]:
        """Build progressive learning path based on prerequisites"""
        levels = []
        remaining = set(self.concepts.keys())
        
        while remaining:
            current_level = []
            for concept_name in list(remaining):
                concept = self.concepts[concept_name]
                # Check if all prerequisites are already in previous levels
                if all(prereq in [c for level in levels for c in level] 
                      for prereq in concept.prerequisites):
                    current_level.append(concept_name)
            
            if not current_level:  # Handle concepts with no prerequisites
                current_level = [c for c in remaining 
                               if not self.concepts[c].prerequisites]
            
            levels.append(current_level)
            remaining -= set(current_level)
            
        return levels
    
    def get_concept_problems(self, concept_name: str) -> List[ProblemTemplate]:
        """Generate problem templates for a concept"""
        concept = self.concepts.get(concept_name)
        if not concept:
            return []
        
        # Generate problems based on concept properties
        problems = []
        
        if concept_name == "arithmetic":
            problems.extend([
                ProblemTemplate(
                    concept="arithmetic",
                    problem_type="modular_arithmetic",
                    input_constraints={"n": "1 <= n <= 10^18", "mod": "1 <= mod <= 10^9"},
                    expected_complexity=ComplexityClass.LOGARITHMIC,
                    mathematical_properties=["fermat_little_theorem", "chinese_remainder"],
                    test_case_generator="generate_modular_arithmetic_tests"
                ),
                ProblemTemplate(
                    concept="arithmetic",
                    problem_type="prime_factorization",
                    input_constraints={"n": "1 <= n <= 10^12"},
                    expected_complexity=ComplexityClass.LINEAR,
                    mathematical_properties=["fundamental_theorem_arithmetic"],
                    test_case_generator="generate_prime_factor_tests"
                )
            ])
        elif concept_name == "linear_algebra":
            problems.extend([
                ProblemTemplate(
                    concept="linear_algebra",
                    problem_type="matrix_multiplication_optimized",
                    input_constraints={"n": "1 <= n <= 1000", "sparse": "density < 0.1"},
                    expected_complexity=ComplexityClass.QUADRATIC,
                    mathematical_properties=["strassen_algorithm", "sparse_optimization"],
                    test_case_generator="generate_matrix_mult_tests"
                ),
                ProblemTemplate(
                    concept="linear_algebra",
                    problem_type="eigenvalue_computation",
                    input_constraints={"n": "1 <= n <= 500"},
                    expected_complexity=ComplexityClass.CUBIC,
                    mathematical_properties=["power_iteration", "qr_decomposition"],
                    test_case_generator="generate_eigenvalue_tests"
                )
            ])
        
        return problems
    
    def assess_understanding(self, concept_name: str, 
                           solution_metrics: Dict) -> Tuple[float, List[str]]:
        """Assess understanding of a concept based on solution metrics"""
        concept = self.concepts.get(concept_name)
        if not concept:
            return 0.0, ["Unknown concept"]
        
        score = 0.0
        feedback = []
        
        # Check correctness
        if solution_metrics.get("all_tests_passed", False):
            score += 0.4
        else:
            feedback.append("Some test cases failed - review edge cases")
        
        # Check complexity
        actual_complexity = solution_metrics.get("time_complexity", "O(n²)")
        if actual_complexity == concept.computational_complexity.value:
            score += 0.3
            feedback.append("Optimal complexity achieved!")
        else:
            feedback.append(f"Can optimize from {actual_complexity} to {concept.computational_complexity.value}")
        
        # Check mathematical rigor
        if solution_metrics.get("uses_key_algorithms", False):
            score += 0.2
            feedback.append("Good use of fundamental algorithms")
        
        # Check code clarity
        if solution_metrics.get("code_clarity_score", 0) > 0.8:
            score += 0.1
            feedback.append("Clear, mathematically sound implementation")
        
        return score, feedback
    
    def get_next_concepts(self, mastered_concepts: List[str]) -> List[str]:
        """Suggest next concepts to learn based on mastered concepts"""
        next_concepts = []
        
        for concept_name, concept in self.concepts.items():
            if concept_name not in mastered_concepts:
                # Check if all prerequisites are mastered
                if all(prereq in mastered_concepts for prereq in concept.prerequisites):
                    next_concepts.append(concept_name)
        
        # Sort by difficulty
        next_concepts.sort(key=lambda c: self.concepts[c].difficulty.value)
        
        return next_concepts
    
    def generate_learning_report(self, student_progress: Dict) -> Dict:
        """Generate comprehensive learning progress report"""
        mastered = student_progress.get("mastered_concepts", [])
        attempted = student_progress.get("attempted_concepts", {})
        
        report = {
            "current_level": self._determine_level(mastered),
            "mastery_percentage": len(mastered) / len(self.concepts) * 100,
            "recommended_next": self.get_next_concepts(mastered)[:3],
            "strengths": self._identify_strengths(mastered, attempted),
            "areas_for_improvement": self._identify_weaknesses(attempted),
            "learning_path_progress": self._calculate_path_progress(mastered)
        }
        
        return report
    
    def _determine_level(self, mastered: List[str]) -> str:
        """Determine current mathematical proficiency level"""
        if len(mastered) < 2:
            return "Beginner"
        elif all(c in mastered for c in ["arithmetic", "number_theory"]):
            if any(c in mastered for c in ["linear_algebra", "calculus"]):
                return "Intermediate"
            return "Foundation Complete"
        elif any(c in mastered for c in ["optimization", "graph_theory"]):
            return "Advanced"
        elif any(c in mastered for c in ["computational_complexity", "quantum_computing"]):
            return "Expert"
        return "Intermediate"
    
    def _identify_strengths(self, mastered: List[str], attempted: Dict) -> List[str]:
        """Identify mathematical strengths"""
        strengths = []
        categories = {}
        
        for concept_name in mastered:
            category = self.concepts[concept_name].category
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            if count >= 2:
                strengths.append(f"Strong foundation in {category}")
        
        return strengths
    
    def _identify_weaknesses(self, attempted: Dict) -> List[str]:
        """Identify areas needing improvement"""
        weaknesses = []
        
        for concept, metrics in attempted.items():
            if metrics.get("average_score", 0) < 0.7:
                weaknesses.append(f"Review {concept} - focus on {metrics.get('common_errors', ['implementation'])[0]}")
        
        return weaknesses
    
    def _calculate_path_progress(self, mastered: List[str]) -> Dict:
        """Calculate progress through learning path"""
        progress = {}
        
        for level_idx, level_concepts in enumerate(self.learning_path):
            level_name = f"Level {level_idx + 1}"
            mastered_in_level = [c for c in level_concepts if c in mastered]
            progress[level_name] = {
                "completed": len(mastered_in_level),
                "total": len(level_concepts),
                "percentage": len(mastered_in_level) / len(level_concepts) * 100 if level_concepts else 0
            }
        
        return progress