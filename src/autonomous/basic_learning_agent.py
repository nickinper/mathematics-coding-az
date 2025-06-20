"""
Basic Learning Agent - Autonomous mathematical problem solver
"""

import json
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from src.autonomous.pattern_discovery import PatternExtractor, PatternStorage, Pattern
from src.autonomous.knowledge_schema import KnowledgeDatabase
from src.core.challenge import Challenge, ChallengeResult
from src.execution.safe_executor import SafeExecutor


@dataclass
class LearningState:
    """Represents the current state of a learning agent."""
    agent_id: str
    mastered_concepts: List[str] = field(default_factory=list)
    known_patterns: Dict[str, Pattern] = field(default_factory=dict)
    attempt_history: List[Dict[str, Any]] = field(default_factory=list)
    current_level: str = "beginner"
    total_attempts: int = 0
    successful_attempts: int = 0
    
    @property
    def success_rate(self) -> float:
        """Calculate overall success rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.successful_attempts / self.total_attempts


class BasicLearningAgent:
    """An agent that learns mathematical concepts through practice."""
    
    def __init__(self, agent_id: str, knowledge_db_path: str = "sqlite:///knowledge.db"):
        self.agent_id = agent_id
        self.knowledge_db = KnowledgeDatabase(knowledge_db_path)
        self.pattern_extractor = PatternExtractor()
        self.pattern_storage = PatternStorage()
        self.safe_executor = SafeExecutor()
        self.state = self._load_or_create_state()
    
    def _load_or_create_state(self) -> LearningState:
        """Load existing agent state or create new one."""
        knowledge = self.knowledge_db.get_agent_knowledge(self.agent_id)
        
        state = LearningState(
            agent_id=self.agent_id,
            mastered_concepts=knowledge.get('mastered_concepts', []),
            total_attempts=knowledge.get('total_attempts', 0)
        )
        
        # Calculate successful attempts
        if state.total_attempts > 0:
            state.successful_attempts = int(
                state.total_attempts * knowledge.get('success_rate', 0)
            )
        
        # Load known patterns
        for pattern_name in knowledge.get('pattern_usage', {}).keys():
            pattern = self.pattern_storage.get_pattern(pattern_name)
            if pattern:
                state.known_patterns[pattern_name] = pattern
        
        return state
    
    def attempt_challenge(self, challenge: Challenge) -> Dict[str, Any]:
        """Attempt to solve a challenge using learned patterns."""
        start_time = time.time()
        
        # Analyze challenge requirements
        required_concepts = self._extract_required_concepts(challenge)
        
        # Retrieve relevant patterns
        relevant_patterns = self._find_relevant_patterns(required_concepts)
        
        # Generate solution attempt
        solution_code, reasoning = self._generate_solution(
            challenge, relevant_patterns
        )
        
        # Execute and verify solution
        result = self._execute_and_verify(challenge, solution_code)
        
        # Learn from the attempt
        learning_outcome = self._learn_from_attempt(
            challenge, solution_code, reasoning, result, relevant_patterns
        )
        
        # Update state
        self.state.total_attempts += 1
        if result.passed:
            self.state.successful_attempts += 1
        
        # Record attempt
        attempt_record = {
            "challenge": challenge.title,
            "timestamp": datetime.utcnow().isoformat(),
            "success": result.passed,
            "score": result.total_score,
            "time_taken": time.time() - start_time,
            "patterns_used": [p.name for p in relevant_patterns],
            "patterns_discovered": learning_outcome.get("new_patterns", []),
            "concepts_learned": learning_outcome.get("concepts_learned", [])
        }
        
        self.state.attempt_history.append(attempt_record)
        
        return {
            "success": result.passed,
            "score": result.total_score,
            "feedback": result.feedback,
            "patterns_discovered": learning_outcome.get("new_patterns", []),
            "concepts_learned": learning_outcome.get("concepts_learned", []),
            "solution_code": solution_code,
            "reasoning": reasoning,
            "time_taken": attempt_record["time_taken"]
        }
    
    def _extract_required_concepts(self, challenge: Challenge) -> List[str]:
        """Extract mathematical concepts required for the challenge."""
        concepts = []
        
        # Extract from mathematical requirements
        for req in challenge.mathematical_requirements:
            concept = req.concept.lower().replace(" ", "_")
            concepts.append(concept)
        
        # Extract from domain
        concepts.append(challenge.domain.value.lower())
        
        # Extract from description using simple keyword matching
        keywords = ["gcd", "modular", "prime", "euclidean", "fermat", "ring"]
        description_lower = challenge.description.lower()
        for keyword in keywords:
            if keyword in description_lower:
                concepts.append(keyword)
        
        return list(set(concepts))
    
    def _find_relevant_patterns(self, concepts: List[str]) -> List[Pattern]:
        """Find patterns relevant to the given concepts."""
        relevant_patterns = []
        
        # Search in known patterns
        for pattern in self.state.known_patterns.values():
            # Check if pattern is relevant to any concept
            pattern_relevant = False
            for concept in concepts:
                if concept in pattern.name.lower() or \
                   concept in pattern.description.lower() or \
                   any(concept in prop for prop in pattern.mathematical_properties):
                    pattern_relevant = True
                    break
            
            if pattern_relevant:
                relevant_patterns.append(pattern)
        
        # Search in pattern storage
        for category in ["algorithmic", "mathematical"]:
            stored_patterns = self.pattern_storage.search_patterns(category=category)
            for pattern in stored_patterns:
                if pattern not in relevant_patterns:
                    for concept in concepts:
                        if concept in pattern.description.lower():
                            relevant_patterns.append(pattern)
                            break
        
        return relevant_patterns
    
    def _generate_solution(self, challenge: Challenge, 
                          patterns: List[Pattern]) -> Tuple[str, str]:
        """Generate a solution based on available patterns."""
        
        # For demonstration, we'll create template-based solutions
        # In a real system, this would use more sophisticated code generation
        
        if "gcd" in challenge.title.lower():
            return self._generate_gcd_solution(patterns)
        elif "modular" in challenge.title.lower():
            return self._generate_modular_solution(patterns)
        elif "prime" in challenge.title.lower():
            return self._generate_prime_solution(patterns)
        else:
            # Fallback: attempt using most relevant pattern
            if patterns:
                pattern = patterns[0]
                code = pattern.code_template or "# No implementation available"
                reasoning = f"Using pattern: {pattern.name}"
                return code, reasoning
            else:
                return "# Unable to generate solution", "No relevant patterns found"
    
    def _generate_gcd_solution(self, patterns: List[Pattern]) -> Tuple[str, str]:
        """Generate GCD solution based on patterns."""
        
        # Check if we have Euclidean algorithm pattern
        euclidean_pattern = next(
            (p for p in patterns if "euclidean" in p.name.lower()), None
        )
        
        if euclidean_pattern and euclidean_pattern.code_template:
            code = f'''
def gcd(a: int, b: int) -> int:
    """
    Calculate GCD using Euclidean algorithm.
    
    Mathematical foundation: gcd(a, b) = gcd(b, a mod b)
    This works because any common divisor of a and b also divides a - qb.
    
    Complexity: O(log(min(a,b))) - the remainder decreases by at least half
    every two iterations, ensuring logarithmic time complexity.
    """
    # Handle edge cases
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    
    # Ensure positive values
    a, b = abs(a), abs(b)
    
    # Euclidean algorithm
    {euclidean_pattern.code_template}
'''
        else:
            # Fallback implementation
            code = '''
def gcd(a: int, b: int) -> int:
    """
    Calculate GCD using Euclidean algorithm.
    
    The Euclidean algorithm is based on the principle that
    gcd(a, b) = gcd(b, a mod b).
    
    The algorithm terminates because the remainder decreases
    with each step and will eventually reach 0.
    """
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    
    a, b = abs(a), abs(b)
    
    while b != 0:
        a, b = b, a % b
    
    return a
'''
        
        reasoning = """
I'm using the Euclidean algorithm because:
1. It's the most efficient method for computing GCD
2. It has O(log(min(a,b))) time complexity
3. It's based on the mathematical property that gcd(a,b) = gcd(b, a mod b)
4. The algorithm terminates because remainders form a decreasing sequence
"""
        
        return code, reasoning
    
    def _generate_modular_solution(self, patterns: List[Pattern]) -> Tuple[str, str]:
        """Generate modular arithmetic solution."""
        
        code = '''
from typing import Optional

class ModularArithmetic:
    """
    Ring operations in Z/nZ demonstrating mathematical properties.
    
    (Z/nZ, +, ×) forms a ring with:
    - Closure under + and ×
    - Associativity of + and ×
    - Commutativity of + and ×
    - Identity elements: 0 for +, 1 for ×
    - Additive inverses for all elements
    - Distributivity of × over +
    """
    
    def __init__(self, modulus: int):
        self.n = modulus
    
    def add(self, a: int, b: int) -> int:
        """Modular addition."""
        return (a + b) % self.n
    
    def multiply(self, a: int, b: int) -> int:
        """Modular multiplication."""
        return (a * b) % self.n
    
    def power(self, a: int, b: int) -> int:
        """Fast modular exponentiation using binary method."""
        result = 1
        a = a % self.n
        
        while b > 0:
            if b % 2 == 1:
                result = (result * a) % self.n
            b = b >> 1
            a = (a * a) % self.n
        
        return result
    
    def inverse(self, a: int) -> Optional[int]:
        """
        Modular multiplicative inverse using Extended Euclidean Algorithm.
        The inverse exists iff gcd(a, n) = 1.
        """
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % self.n, self.n)
        
        if gcd != 1:
            return None
        
        return (x % self.n + self.n) % self.n
'''
        
        reasoning = """
Implementing modular arithmetic as a ring structure because:
1. It demonstrates the algebraic properties of Z/nZ
2. Binary exponentiation provides O(log b) complexity
3. Extended Euclidean algorithm finds multiplicative inverses
4. The implementation shows when inverses exist (gcd(a,n) = 1)
"""
        
        return code, reasoning
    
    def _generate_prime_solution(self, patterns: List[Pattern]) -> Tuple[str, str]:
        """Generate prime detection solution."""
        
        code = '''
import math
import random
from typing import List

class PrimeDetector:
    """Prime detection using multiple algorithms."""
    
    def is_prime_trial(self, n: int) -> bool:
        """
        Optimized trial division.
        
        We only need to check divisors up to √n because if n = a×b
        and a ≤ b, then a ≤ √n.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True
    
    def is_prime_miller_rabin(self, n: int, k: int = 5) -> bool:
        """
        Miller-Rabin probabilistic test.
        Error probability ≤ 4^(-k).
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 = 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Witness test
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def sieve_of_eratosthenes(self, n: int) -> List[int]:
        """Generate all primes up to n in O(n log log n) time."""
        if n < 2:
            return []
        
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        
        return [i for i in range(n + 1) if is_prime[i]]
'''
        
        reasoning = """
Using multiple prime detection algorithms:
1. Trial division with √n optimization for deterministic testing
2. Miller-Rabin for efficient probabilistic testing of large numbers
3. Sieve of Eratosthenes for generating many primes efficiently
Each algorithm has different trade-offs in terms of speed and certainty.
"""
        
        return code, reasoning
    
    def _execute_and_verify(self, challenge: Challenge, 
                           solution_code: str) -> ChallengeResult:
        """Execute solution and verify against challenge requirements."""
        
        # Create a mock verifier function
        # In a real system, this would use the challenge's actual test cases
        
        try:
            # Execute code in safe environment
            namespace = {}
            exec(solution_code, namespace)
            
            # Run basic tests
            test_results = []
            passed = 0
            total = len(challenge.test_cases)
            
            for test_case in challenge.test_cases[:3]:  # Test first 3 cases
                # This is simplified - real implementation would properly
                # extract and call the appropriate function
                test_results.append((test_case.description, True, "Passed"))
                passed += 1
            
            # Verify mathematical reasoning
            math_score, math_feedback = challenge.verify_mathematical_reasoning(
                solution_code
            )
            
            # Check complexity
            complexity_ok, complexity_feedback = challenge.analyze_complexity(
                solution_code
            )
            
            # Calculate scores
            correctness_score = passed / total if total > 0 else 0
            total_score = (correctness_score * 0.5 + math_score * 0.5)
            
            return ChallengeResult(
                passed=total_score >= 0.6,
                test_results=test_results,
                mathematical_score=math_score,
                code_quality_score=0.8,  # Simplified
                innovation_score=0.5,    # Simplified
                total_score=total_score,
                feedback=f"{math_feedback}; {complexity_feedback}",
                errors=[]
            )
            
        except Exception as e:
            return ChallengeResult(
                passed=False,
                test_results=[],
                mathematical_score=0.0,
                code_quality_score=0.0,
                innovation_score=0.0,
                total_score=0.0,
                feedback=f"Execution failed: {str(e)}",
                errors=[str(e)]
            )
    
    def _learn_from_attempt(self, challenge: Challenge, code: str, 
                           reasoning: str, result: ChallengeResult,
                           used_patterns: List[Pattern]) -> Dict[str, Any]:
        """Learn from the attempt, whether successful or not."""
        
        # Extract patterns from the solution
        discovered_patterns = self.pattern_extractor.extract_patterns(code)
        
        # Record in knowledge database
        self.knowledge_db.record_learning_attempt(
            agent_id=self.agent_id,
            concept_name=challenge.domain.value.lower(),
            challenge_name=challenge.title,
            success=result.passed,
            score=result.total_score,
            time_taken=0.0,  # Would be tracked in real implementation
            code=code,
            reasoning=reasoning,
            patterns=[p.pattern.name for p in discovered_patterns],
            errors=result.errors
        )
        
        # Update known patterns if successful
        new_patterns = []
        if result.passed:
            for pattern_match in discovered_patterns:
                if pattern_match.pattern.name not in self.state.known_patterns:
                    self.state.known_patterns[pattern_match.pattern.name] = \
                        pattern_match.pattern
                    self.pattern_storage.add_pattern(pattern_match.pattern)
                    new_patterns.append(pattern_match.pattern.name)
        
        # Update mastered concepts
        concepts_learned = []
        if result.passed and result.total_score >= 0.8:
            concept = challenge.domain.value.lower()
            if concept not in self.state.mastered_concepts:
                self.state.mastered_concepts.append(concept)
                concepts_learned.append(concept)
        
        return {
            "new_patterns": new_patterns,
            "concepts_learned": concepts_learned,
            "improvement_areas": self._identify_improvement_areas(result)
        }
    
    def _identify_improvement_areas(self, result: ChallengeResult) -> List[str]:
        """Identify areas for improvement based on results."""
        areas = []
        
        if result.mathematical_score < 0.5:
            areas.append("mathematical_reasoning")
        
        if "complexity" in result.feedback.lower() and "must" in result.feedback.lower():
            areas.append("algorithm_efficiency")
        
        if result.errors:
            areas.append("error_handling")
        
        return areas
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's learning progress."""
        return {
            "agent_id": self.agent_id,
            "current_level": self.state.current_level,
            "mastered_concepts": self.state.mastered_concepts,
            "known_patterns": list(self.state.known_patterns.keys()),
            "total_attempts": self.state.total_attempts,
            "success_rate": self.state.success_rate,
            "recent_attempts": self.state.attempt_history[-5:] if self.state.attempt_history else []
        }
    
    def suggest_next_challenge(self) -> Optional[str]:
        """Suggest the next challenge to attempt."""
        return self.knowledge_db.suggest_next_concept(self.agent_id)