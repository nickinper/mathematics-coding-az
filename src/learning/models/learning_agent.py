"""
AI Learning Agent for Progressive Mathematical Education
"""
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np


@dataclass
class LearningState:
    """Track the agent's learning progress"""
    mastered_concepts: List[str] = field(default_factory=list)
    attempted_problems: Dict[str, List[Dict]] = field(default_factory=dict)
    concept_scores: Dict[str, float] = field(default_factory=dict)
    learning_velocity: Dict[str, float] = field(default_factory=dict)  # How fast agent learns each concept
    error_patterns: Dict[str, List[str]] = field(default_factory=dict)
    optimization_strategies: List[str] = field(default_factory=list)
    current_level: str = "Beginner"
    total_problems_solved: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "mastered_concepts": self.mastered_concepts,
            "concept_scores": self.concept_scores,
            "current_level": self.current_level,
            "total_problems_solved": self.total_problems_solved,
            "learning_velocity": self.learning_velocity
        }


class MathLearningAgent:
    """AI agent that learns mathematics progressively"""
    
    def __init__(self, agent_id: str, initial_knowledge: Optional[Dict] = None):
        self.agent_id = agent_id
        self.state = LearningState()
        self.curriculum = None  # Will be injected
        self.problem_generator = None  # Will be injected
        self.solution_strategies = self._initialize_strategies()
        self.learning_history = []
        
        if initial_knowledge:
            self._load_initial_knowledge(initial_knowledge)
    
    def _initialize_strategies(self) -> Dict[str, List[str]]:
        """Initialize problem-solving strategies"""
        return {
            "arithmetic": [
                "binary_exponentiation",
                "modular_reduction",
                "euclidean_algorithm"
            ],
            "number_theory": [
                "prime_factorization",
                "sieve_methods",
                "probabilistic_testing"
            ],
            "linear_algebra": [
                "gaussian_elimination",
                "lu_decomposition",
                "iterative_methods"
            ],
            "optimization": [
                "gradient_methods",
                "newton_methods",
                "interior_point"
            ]
        }
    
    def _load_initial_knowledge(self, knowledge: Dict):
        """Load pre-existing knowledge"""
        self.state.mastered_concepts = knowledge.get("mastered_concepts", [])
        self.state.concept_scores = knowledge.get("concept_scores", {})
    
    def attempt_problem(self, problem: 'MathProblem') -> Dict[str, Any]:
        """Attempt to solve a mathematical problem"""
        start_time = time.time()
        
        # Analyze problem
        analysis = self._analyze_problem(problem)
        
        # Generate solution approach
        approach = self._select_approach(problem, analysis)
        
        # Implement solution
        solution_code = self._generate_solution(problem, approach)
        
        # Self-test solution
        test_results = self._test_solution(solution_code, problem.test_cases)
        
        # Analyze complexity
        complexity_analysis = self._analyze_complexity(solution_code, problem)
        
        # Learn from attempt
        learning_outcome = self._learn_from_attempt(
            problem, 
            test_results, 
            complexity_analysis,
            time.time() - start_time
        )
        
        return {
            "problem_id": problem.id,
            "solution_code": solution_code,
            "test_results": test_results,
            "complexity_analysis": complexity_analysis,
            "learning_outcome": learning_outcome,
            "time_taken": time.time() - start_time
        }
    
    def _analyze_problem(self, problem: 'MathProblem') -> Dict:
        """Analyze problem characteristics"""
        return {
            "concept": problem.concept,
            "difficulty": problem.difficulty,
            "required_algorithms": self._identify_required_algorithms(problem),
            "mathematical_properties": problem.mathematical_insight,
            "similar_problems_solved": self._find_similar_problems(problem)
        }
    
    def _identify_required_algorithms(self, problem: 'MathProblem') -> List[str]:
        """Identify which algorithms might be needed"""
        algorithms = []
        
        # Pattern matching based on problem statement
        statement_lower = problem.problem_statement.lower()
        
        if "modular" in statement_lower or "mod" in statement_lower:
            algorithms.append("modular_arithmetic")
        if "prime" in statement_lower:
            algorithms.append("primality_testing")
        if "matrix" in statement_lower:
            algorithms.append("matrix_operations")
        if "eigenvalue" in statement_lower:
            algorithms.append("eigendecomposition")
        if "optimization" in statement_lower or "minimize" in statement_lower:
            algorithms.append("optimization_methods")
        
        return algorithms
    
    def _find_similar_problems(self, problem: 'MathProblem') -> List[str]:
        """Find similar problems the agent has solved"""
        similar = []
        concept_attempts = self.state.attempted_problems.get(problem.concept, [])
        
        for past_attempt in concept_attempts:
            if past_attempt.get("difficulty") == problem.difficulty:
                similar.append(past_attempt["problem_id"])
        
        return similar
    
    def _select_approach(self, problem: 'MathProblem', analysis: Dict) -> Dict:
        """Select solution approach based on analysis"""
        concept = problem.concept
        strategies = self.solution_strategies.get(concept, [])
        
        # Score each strategy based on past success
        strategy_scores = {}
        for strategy in strategies:
            score = self._calculate_strategy_score(strategy, problem, analysis)
            strategy_scores[strategy] = score
        
        # Select best strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        
        return {
            "primary_strategy": best_strategy,
            "backup_strategies": [s for s in strategies if s != best_strategy],
            "confidence": strategy_scores[best_strategy],
            "rationale": self._explain_strategy_choice(best_strategy, problem)
        }
    
    def _calculate_strategy_score(self, strategy: str, problem: 'MathProblem', analysis: Dict) -> float:
        """Calculate how suitable a strategy is for the problem"""
        score = 0.5  # Base score
        
        # Boost if strategy matches problem requirements
        if strategy in analysis["required_algorithms"]:
            score += 0.3
        
        # Consider past success with this strategy
        past_success = self._get_strategy_success_rate(strategy, problem.concept)
        score += past_success * 0.2
        
        return min(score, 1.0)
    
    def _get_strategy_success_rate(self, strategy: str, concept: str) -> float:
        """Get historical success rate with a strategy"""
        concept_attempts = self.state.attempted_problems.get(concept, [])
        if not concept_attempts:
            return 0.5  # No history, neutral score
        
        successes = sum(1 for attempt in concept_attempts 
                       if attempt.get("strategy") == strategy and attempt.get("success", False))
        total = sum(1 for attempt in concept_attempts if attempt.get("strategy") == strategy)
        
        return successes / total if total > 0 else 0.5
    
    def _explain_strategy_choice(self, strategy: str, problem: 'MathProblem') -> str:
        """Generate explanation for strategy selection"""
        explanations = {
            "binary_exponentiation": "Using binary exponentiation for O(log n) complexity",
            "modular_reduction": "Applying modular arithmetic properties to prevent overflow",
            "euclidean_algorithm": "Leveraging GCD properties for efficient computation",
            "prime_factorization": "Decomposing into prime factors for mathematical insight",
            "gaussian_elimination": "Systematic reduction to solve linear systems",
            "gradient_methods": "Following gradient for optimization convergence"
        }
        
        return explanations.get(strategy, f"Applying {strategy} based on problem structure")
    
    def _generate_solution(self, problem: 'MathProblem', approach: Dict) -> str:
        """Generate solution code based on selected approach"""
        # This is a simplified version - in reality, this would use
        # code generation models or templates
        
        strategy = approach["primary_strategy"]
        
        # Template-based generation for demonstration
        if problem.concept == "arithmetic" and strategy == "binary_exponentiation":
            return self._generate_binary_exp_solution(problem)
        elif problem.concept == "number_theory" and strategy == "prime_factorization":
            return self._generate_prime_factor_solution(problem)
        else:
            return self._generate_generic_solution(problem)
    
    def _generate_binary_exp_solution(self, problem: 'MathProblem') -> str:
        """Generate binary exponentiation solution"""
        return """def mod_exp(base: int, exp: int, mod: int) -> int:
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    
    return result"""
    
    def _generate_prime_factor_solution(self, problem: 'MathProblem') -> str:
        """Generate prime factorization solution"""
        return """def prime_factors(n: int) -> List[int]:
    factors = []
    
    # Handle 2 separately
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    
    # Check odd factors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n = n // i
        i += 2
    
    if n > 2:
        factors.append(n)
    
    return factors"""
    
    def _generate_generic_solution(self, problem: 'MathProblem') -> str:
        """Generate generic solution template"""
        return f"""{problem.function_signature}
    # TODO: Implement solution for {problem.concept}
    # Strategy: {problem.optimal_approach}
    pass"""
    
    def _test_solution(self, solution_code: str, test_cases: List[Dict]) -> Dict:
        """Test the solution against provided test cases"""
        # In reality, this would execute code in sandbox
        # For now, simulate test results
        
        passed_tests = 0
        total_tests = len(test_cases)
        test_details = []
        
        for i, test_case in enumerate(test_cases):
            # Simulate test execution
            passed = np.random.random() > 0.3  # 70% pass rate for simulation
            test_details.append({
                "test_id": i,
                "passed": passed,
                "input": test_case["input"],
                "expected": test_case.get("expected", "Unknown")
            })
            
            if passed:
                passed_tests += 1
        
        return {
            "passed": passed_tests,
            "total": total_tests,
            "success_rate": passed_tests / total_tests,
            "all_passed": passed_tests == total_tests,
            "details": test_details
        }
    
    def _analyze_complexity(self, solution_code: str, problem: 'MathProblem') -> Dict:
        """Analyze time and space complexity of solution"""
        # Simplified complexity analysis
        
        code_lower = solution_code.lower()
        
        # Detect loop patterns
        nested_loops = code_lower.count("for") + code_lower.count("while")
        
        # Estimate complexity
        if nested_loops == 0:
            time_complexity = "O(1)"
        elif nested_loops == 1:
            if "binary" in code_lower or ">> 1" in solution_code:
                time_complexity = "O(log n)"
            else:
                time_complexity = "O(n)"
        elif nested_loops == 2:
            time_complexity = "O(n²)"
        else:
            time_complexity = "O(n³)"
        
        # Check if optimal
        is_optimal = time_complexity == problem.expected_complexity
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": "O(1)" if "array" not in code_lower else "O(n)",
            "is_optimal": is_optimal,
            "expected": problem.expected_complexity,
            "optimization_suggestions": [] if is_optimal else ["Consider more efficient algorithm"]
        }
    
    def _learn_from_attempt(self, problem: 'MathProblem', test_results: Dict, 
                           complexity_analysis: Dict, time_taken: float) -> Dict:
        """Update learning state based on attempt"""
        success = test_results["all_passed"] and complexity_analysis["is_optimal"]
        
        # Update attempted problems
        if problem.concept not in self.state.attempted_problems:
            self.state.attempted_problems[problem.concept] = []
        
        attempt_record = {
            "problem_id": problem.id,
            "difficulty": problem.difficulty,
            "success": success,
            "test_success_rate": test_results["success_rate"],
            "complexity_optimal": complexity_analysis["is_optimal"],
            "time_taken": time_taken,
            "timestamp": datetime.now().isoformat()
        }
        
        self.state.attempted_problems[problem.concept].append(attempt_record)
        
        # Update concept score
        current_score = self.state.concept_scores.get(problem.concept, 0.0)
        score_delta = 0.1 * test_results["success_rate"]
        if complexity_analysis["is_optimal"]:
            score_delta += 0.05
        
        self.state.concept_scores[problem.concept] = min(current_score + score_delta, 1.0)
        
        # Update learning velocity
        self._update_learning_velocity(problem.concept, success, time_taken)
        
        # Check for mastery
        if self._check_concept_mastery(problem.concept):
            if problem.concept not in self.state.mastered_concepts:
                self.state.mastered_concepts.append(problem.concept)
        
        # Update total problems solved
        self.state.total_problems_solved += 1
        
        # Identify error patterns
        if not success:
            self._identify_error_patterns(problem, test_results, complexity_analysis)
        
        return {
            "success": success,
            "concept_progress": self.state.concept_scores[problem.concept],
            "mastery_achieved": problem.concept in self.state.mastered_concepts,
            "insights_gained": self._generate_insights(problem, success)
        }
    
    def _update_learning_velocity(self, concept: str, success: bool, time_taken: float):
        """Track how quickly the agent learns concepts"""
        if concept not in self.state.learning_velocity:
            self.state.learning_velocity[concept] = 0.5
        
        # Adjust velocity based on success and time
        velocity_delta = 0.1 if success else -0.05
        if time_taken < 60:  # Fast solution
            velocity_delta += 0.05
        
        self.state.learning_velocity[concept] = max(0.1, min(1.0, 
            self.state.learning_velocity[concept] + velocity_delta))
    
    def _check_concept_mastery(self, concept: str) -> bool:
        """Check if concept is mastered"""
        score = self.state.concept_scores.get(concept, 0)
        attempts = self.state.attempted_problems.get(concept, [])
        
        # Require high score and multiple successful attempts
        recent_attempts = attempts[-5:] if len(attempts) >= 5 else attempts
        success_rate = sum(1 for a in recent_attempts if a["success"]) / len(recent_attempts) if recent_attempts else 0
        
        return score >= 0.8 and success_rate >= 0.8 and len(attempts) >= 3
    
    def _identify_error_patterns(self, problem: 'MathProblem', test_results: Dict, complexity_analysis: Dict):
        """Identify patterns in errors"""
        if problem.concept not in self.state.error_patterns:
            self.state.error_patterns[problem.concept] = []
        
        errors = []
        
        if not test_results["all_passed"]:
            errors.append("test_failures")
        if not complexity_analysis["is_optimal"]:
            errors.append("suboptimal_complexity")
        
        self.state.error_patterns[problem.concept].extend(errors)
    
    def _generate_insights(self, problem: 'MathProblem', success: bool) -> List[str]:
        """Generate learning insights from attempt"""
        insights = []
        
        if success:
            insights.append(f"Successfully applied {problem.optimal_approach}")
            insights.append(f"Reinforced understanding of {problem.mathematical_insight}")
        else:
            insights.append(f"Need to review {problem.concept} fundamentals")
            insights.append(f"Study {problem.optimal_approach} approach")
        
        return insights
    
    def get_learning_report(self) -> Dict:
        """Generate comprehensive learning report"""
        return {
            "agent_id": self.agent_id,
            "current_state": self.state.to_dict(),
            "strengths": self._identify_strengths(),
            "weaknesses": self._identify_weaknesses(),
            "recommended_next_topics": self._recommend_next_topics(),
            "learning_trajectory": self._analyze_learning_trajectory()
        }
    
    def _identify_strengths(self) -> List[str]:
        """Identify agent's mathematical strengths"""
        strengths = []
        
        for concept, score in self.state.concept_scores.items():
            if score >= 0.7:
                strengths.append(f"Strong in {concept} (score: {score:.2f})")
        
        # Check for fast learning
        fast_concepts = [c for c, v in self.state.learning_velocity.items() if v >= 0.7]
        if fast_concepts:
            strengths.append(f"Fast learner in: {', '.join(fast_concepts)}")
        
        return strengths
    
    def _identify_weaknesses(self) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        # Low scoring concepts
        for concept, score in self.state.concept_scores.items():
            if score < 0.5:
                weaknesses.append(f"Struggling with {concept} (score: {score:.2f})")
        
        # Frequent error patterns
        for concept, errors in self.state.error_patterns.items():
            if len(errors) > 3:
                common_error = max(set(errors), key=errors.count)
                weaknesses.append(f"Recurring {common_error} in {concept}")
        
        return weaknesses
    
    def _recommend_next_topics(self) -> List[str]:
        """Recommend next topics to study"""
        if not self.curriculum:
            return ["Set curriculum to get recommendations"]
        
        return self.curriculum.get_next_concepts(self.state.mastered_concepts)[:3]
    
    def _analyze_learning_trajectory(self) -> Dict:
        """Analyze learning progress over time"""
        if not self.state.attempted_problems:
            return {"status": "Just starting"}
        
        total_attempts = sum(len(attempts) for attempts in self.state.attempted_problems.values())
        total_successes = sum(
            sum(1 for a in attempts if a["success"]) 
            for attempts in self.state.attempted_problems.values()
        )
        
        return {
            "total_attempts": total_attempts,
            "overall_success_rate": total_successes / total_attempts if total_attempts > 0 else 0,
            "concepts_mastered": len(self.state.mastered_concepts),
            "average_learning_velocity": np.mean(list(self.state.learning_velocity.values())) if self.state.learning_velocity else 0.5,
            "estimated_time_to_expert": self._estimate_time_to_expert()
        }
    
    def _estimate_time_to_expert(self) -> str:
        """Estimate time to reach expert level"""
        if not self.state.learning_velocity:
            return "Insufficient data"
        
        avg_velocity = np.mean(list(self.state.learning_velocity.values()))
        concepts_remaining = 8 - len(self.state.mastered_concepts)  # Assuming 8 total concepts
        
        # Rough estimate based on velocity
        problems_per_concept = 10
        minutes_per_problem = 5 / avg_velocity
        
        total_minutes = concepts_remaining * problems_per_concept * minutes_per_problem
        hours = total_minutes / 60
        
        if hours < 10:
            return f"~{hours:.1f} hours"
        else:
            return f"~{hours/24:.1f} days"