"""
Generate mathematical problems for progressive AI learning
"""
import random
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import sympy as sp


@dataclass
class MathProblem:
    id: str
    concept: str
    difficulty: int
    problem_statement: str
    function_signature: str
    test_cases: List[Dict]
    constraints: Dict
    expected_complexity: str
    hints: List[str]
    mathematical_insight: str
    optimal_approach: str


class MathProblemGenerator:
    def __init__(self):
        self.problem_id_counter = 0
        
    def generate_problem(self, concept: str, difficulty: int = 1) -> MathProblem:
        """Generate a problem based on concept and difficulty"""
        generators = {
            "arithmetic": self._generate_arithmetic_problem,
            "number_theory": self._generate_number_theory_problem,
            "linear_algebra": self._generate_linear_algebra_problem,
            "calculus": self._generate_calculus_problem,
            "optimization": self._generate_optimization_problem,
            "graph_theory": self._generate_graph_theory_problem,
        }
        
        generator = generators.get(concept, self._generate_arithmetic_problem)
        return generator(difficulty)
    
    def _generate_arithmetic_problem(self, difficulty: int) -> MathProblem:
        """Generate arithmetic problems with increasing complexity"""
        self.problem_id_counter += 1
        
        if difficulty == 1:  # Basic modular arithmetic
            mod = random.choice([7, 13, 17, 23, 29])
            return MathProblem(
                id=f"arith_{self.problem_id_counter}",
                concept="arithmetic",
                difficulty=difficulty,
                problem_statement=f"""
                Implement efficient modular exponentiation.
                Given integers base, exponent, and modulus, compute (base^exponent) % modulus.
                
                Mathematical insight: Use the property that (a*b) % m = ((a%m) * (b%m)) % m
                """,
                function_signature="def mod_exp(base: int, exp: int, mod: int) -> int:",
                test_cases=[
                    {"input": {"base": 2, "exp": 10, "mod": 1000}, "expected": 24},
                    {"input": {"base": 3, "exp": 100, "mod": 7}, "expected": 4},
                    {"input": {"base": 5, "exp": 1000000, "mod": 13}, "expected": 8},
                ],
                constraints={"base": "0 <= base <= 10^9", "exp": "0 <= exp <= 10^18", "mod": "1 <= mod <= 10^9"},
                expected_complexity="O(log exp)",
                hints=[
                    "Binary exponentiation reduces complexity from O(exp) to O(log exp)",
                    "Express exponent in binary form",
                    "Handle overflow by taking modulo at each step"
                ],
                mathematical_insight="Fermat's Little Theorem can optimize when mod is prime",
                optimal_approach="Binary exponentiation with modular reduction"
            )
        
        elif difficulty == 2:  # Extended GCD
            return MathProblem(
                id=f"arith_{self.problem_id_counter}",
                concept="arithmetic",
                difficulty=difficulty,
                problem_statement=f"""
                Implement the Extended Euclidean Algorithm.
                Given integers a and b, find integers x and y such that ax + by = gcd(a,b).
                
                Return (gcd, x, y).
                """,
                function_signature="def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:",
                test_cases=[
                    {"input": {"a": 30, "b": 18}, "expected": (6, -1, 2)},
                    {"input": {"a": 35, "b": 15}, "expected": (5, 1, -2)},
                    {"input": {"a": 1071, "b": 462}, "expected": (21, -6, 14)},
                ],
                constraints={"a": "0 <= a <= 10^9", "b": "0 <= b <= 10^9"},
                expected_complexity="O(log min(a,b))",
                hints=[
                    "Work backwards from the Euclidean algorithm",
                    "Use the relation: gcd(a,b) = gcd(b, a%b)",
                    "Track coefficients through the recursion"
                ],
                mathematical_insight="Bézout's identity guarantees the existence of x and y",
                optimal_approach="Recursive extended Euclidean algorithm"
            )
        
        else:  # difficulty >= 3: Chinese Remainder Theorem
            return MathProblem(
                id=f"arith_{self.problem_id_counter}",
                concept="arithmetic",
                difficulty=difficulty,
                problem_statement=f"""
                Solve a system of modular equations using the Chinese Remainder Theorem.
                Given lists of remainders and moduli, find the smallest positive x such that:
                x ≡ remainders[i] (mod moduli[i]) for all i.
                
                All moduli are pairwise coprime.
                """,
                function_signature="def chinese_remainder(remainders: List[int], moduli: List[int]) -> int:",
                test_cases=[
                    {"input": {"remainders": [2, 3, 2], "moduli": [3, 5, 7]}, "expected": 23},
                    {"input": {"remainders": [1, 4, 6], "moduli": [5, 7, 11]}, "expected": 116},
                    {"input": {"remainders": [3, 4, 5], "moduli": [7, 11, 13]}, "expected": 213},
                ],
                constraints={"n": "2 <= n <= 100", "moduli[i]": "2 <= moduli[i] <= 1000"},
                expected_complexity="O(n * log M) where M = product of moduli",
                hints=[
                    "Use the formula: x = Σ(ai * Mi * yi) mod M",
                    "Mi = M / moduli[i], yi is modular inverse of Mi mod moduli[i]",
                    "Extended GCD helps find modular inverses"
                ],
                mathematical_insight="CRT provides unique solution modulo product of moduli",
                optimal_approach="Direct CRT construction with modular inverses"
            )
    
    def _generate_number_theory_problem(self, difficulty: int) -> MathProblem:
        """Generate number theory problems"""
        self.problem_id_counter += 1
        
        if difficulty == 1:  # Prime checking
            return MathProblem(
                id=f"numth_{self.problem_id_counter}",
                concept="number_theory",
                difficulty=difficulty,
                problem_statement=f"""
                Implement the Miller-Rabin primality test.
                Given an integer n, determine if it's prime using probabilistic testing.
                Use k rounds of testing for accuracy.
                """,
                function_signature="def is_prime_miller_rabin(n: int, k: int = 5) -> bool:",
                test_cases=[
                    {"input": {"n": 97, "k": 5}, "expected": True},
                    {"input": {"n": 561, "k": 5}, "expected": False},  # Carmichael number
                    {"input": {"n": 2147483647, "k": 5}, "expected": True},  # Mersenne prime
                ],
                constraints={"n": "2 <= n <= 10^18", "k": "1 <= k <= 20"},
                expected_complexity="O(k * log³ n)",
                hints=[
                    "Express n-1 as 2^r * d where d is odd",
                    "Test with random witnesses a in [2, n-2]",
                    "Check if a^d ≡ 1 (mod n) or a^(2^i * d) ≡ -1 (mod n)"
                ],
                mathematical_insight="Based on Fermat's Little Theorem with strong witnesses",
                optimal_approach="Miller-Rabin with carefully chosen witness bases"
            )
        
        elif difficulty == 2:  # Euler's totient
            return MathProblem(
                id=f"numth_{self.problem_id_counter}",
                concept="number_theory",
                difficulty=difficulty,
                problem_statement=f"""
                Compute Euler's totient function φ(n) efficiently.
                φ(n) counts integers <= n that are coprime to n.
                
                Use prime factorization: φ(n) = n * Π(1 - 1/p) for all prime factors p.
                """,
                function_signature="def euler_totient(n: int) -> int:",
                test_cases=[
                    {"input": {"n": 12}, "expected": 4},  # φ(12) = 4 (1,5,7,11)
                    {"input": {"n": 100}, "expected": 40},
                    {"input": {"n": 999999}, "expected": 466560},
                ],
                constraints={"n": "1 <= n <= 10^9"},
                expected_complexity="O(√n)",
                hints=[
                    "Find prime factors efficiently",
                    "Use the multiplicative property of φ",
                    "φ(p^k) = p^(k-1) * (p-1) for prime p"
                ],
                mathematical_insight="Totient is multiplicative: φ(mn) = φ(m)φ(n) if gcd(m,n)=1",
                optimal_approach="Prime factorization with running product"
            )
        
        else:  # difficulty >= 3: Discrete logarithm
            return MathProblem(
                id=f"numth_{self.problem_id_counter}",
                concept="number_theory",
                difficulty=difficulty,
                problem_statement=f"""
                Solve the discrete logarithm problem using Baby-step Giant-step algorithm.
                Given g^x ≡ h (mod p), find x.
                
                p is prime, g is a generator of multiplicative group mod p.
                """,
                function_signature="def discrete_log(g: int, h: int, p: int) -> int:",
                test_cases=[
                    {"input": {"g": 5, "h": 3, "p": 23}, "expected": 16},
                    {"input": {"g": 3, "h": 13, "p": 17}, "expected": 4},
                    {"input": {"g": 2, "h": 6, "p": 11}, "expected": 4},
                ],
                constraints={"p": "p is prime, p <= 10^6"},
                expected_complexity="O(√p * log p)",
                hints=[
                    "Set m = ceil(√p)",
                    "Compute baby steps: g^j for j in [0, m)",
                    "Compute giant steps: h * g^(-mi) for i in [0, m)"
                ],
                mathematical_insight="Time-memory tradeoff: O(√p) time and space",
                optimal_approach="Baby-step Giant-step with hash table"
            )
    
    def _generate_linear_algebra_problem(self, difficulty: int) -> MathProblem:
        """Generate linear algebra problems"""
        self.problem_id_counter += 1
        
        if difficulty == 1:  # Matrix operations
            return MathProblem(
                id=f"linalg_{self.problem_id_counter}",
                concept="linear_algebra",
                difficulty=difficulty,
                problem_statement=f"""
                Implement optimized matrix multiplication for sparse matrices.
                Given two sparse matrices A and B, compute C = A × B efficiently.
                
                Use Compressed Sparse Row (CSR) format for optimal performance.
                """,
                function_signature="def sparse_matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:",
                test_cases=[
                    {
                        "input": {
                            "A": [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
                            "B": [[4, 0, 0], [0, 5, 0], [0, 0, 6]]
                        },
                        "expected": [[4, 0, 0], [0, 10, 0], [0, 0, 18]]
                    }
                ],
                constraints={"n": "1 <= n <= 1000", "sparsity": "< 10% non-zero elements"},
                expected_complexity="O(nnz(A) * avg_cols_per_row(B))",
                hints=[
                    "Store only non-zero elements",
                    "Use row pointers for efficient traversal",
                    "Skip computations for zero elements"
                ],
                mathematical_insight="Sparse matrix algorithms reduce complexity based on sparsity pattern",
                optimal_approach="CSR format with smart iteration over non-zeros"
            )
        
        elif difficulty == 2:  # Eigenvalues
            return MathProblem(
                id=f"linalg_{self.problem_id_counter}",
                concept="linear_algebra",
                difficulty=difficulty,
                problem_statement=f"""
                Implement the QR algorithm for eigenvalue computation.
                Given a symmetric matrix A, find all eigenvalues.
                
                Use Householder reflections for QR decomposition.
                """,
                function_signature="def eigenvalues_qr(A: List[List[float]], epsilon: float = 1e-10) -> List[float]:",
                test_cases=[
                    {
                        "input": {"A": [[4, 1], [1, 3]], "epsilon": 1e-10},
                        "expected": [5.0, 2.0]  # Sorted eigenvalues
                    }
                ],
                constraints={"n": "2 <= n <= 100", "symmetric": True},
                expected_complexity="O(n³) per iteration",
                hints=[
                    "First reduce to Hessenberg form",
                    "Apply QR iterations until convergence",
                    "Use shifts for faster convergence"
                ],
                mathematical_insight="QR algorithm preserves eigenvalues while converging to diagonal form",
                optimal_approach="QR with Wilkinson shift and deflation"
            )
        
        else:  # difficulty >= 3: Advanced decompositions
            return MathProblem(
                id=f"linalg_{self.problem_id_counter}",
                concept="linear_algebra",
                difficulty=difficulty,
                problem_statement=f"""
                Implement Singular Value Decomposition (SVD) using the Golub-Kahan algorithm.
                Given matrix A, find U, Σ, V such that A = U × Σ × V^T.
                
                Handle numerical stability for ill-conditioned matrices.
                """,
                function_signature="def svd(A: List[List[float]]) -> Tuple[List[List[float]], List[float], List[List[float]]]:",
                test_cases=[
                    {
                        "input": {"A": [[1, 2], [3, 4], [5, 6]]},
                        "expected": "Check: ||A - U×Σ×V^T|| < 1e-10"
                    }
                ],
                constraints={"m": "1 <= m <= 500", "n": "1 <= n <= 500"},
                expected_complexity="O(mn²) for m >= n",
                hints=[
                    "First reduce to bidiagonal form",
                    "Apply Golub-Kahan SVD iteration",
                    "Handle small singular values carefully"
                ],
                mathematical_insight="SVD reveals the fundamental structure of linear transformations",
                optimal_approach="Two-phase: Bidiagonalization then iterative diagonalization"
            )
    
    def _generate_calculus_problem(self, difficulty: int) -> MathProblem:
        """Generate calculus and numerical methods problems"""
        self.problem_id_counter += 1
        
        if difficulty <= 2:
            return MathProblem(
                id=f"calc_{self.problem_id_counter}",
                concept="calculus",
                difficulty=difficulty,
                problem_statement=f"""
                Implement adaptive Simpson's rule for numerical integration.
                Given function f and interval [a,b], compute ∫f(x)dx with error < epsilon.
                
                Use recursive subdivision for adaptive precision.
                """,
                function_signature="def adaptive_simpson(f: callable, a: float, b: float, epsilon: float) -> float:",
                test_cases=[
                    {
                        "input": {"f": "lambda x: x**2", "a": 0, "b": 1, "epsilon": 1e-10},
                        "expected": 0.333333333333
                    }
                ],
                constraints={"epsilon": "1e-15 <= epsilon <= 1e-3"},
                expected_complexity="O(log(1/epsilon))",
                hints=[
                    "Compare Simpson's rule on whole interval vs sum of halves",
                    "Recursively subdivide if error too large",
                    "Use Richardson extrapolation for error estimate"
                ],
                mathematical_insight="Adaptive methods concentrate computation where needed",
                optimal_approach="Recursive Simpson with error estimation"
            )
        
        else:
            return MathProblem(
                id=f"calc_{self.problem_id_counter}",
                concept="calculus",
                difficulty=difficulty,
                problem_statement=f"""
                Solve stiff ordinary differential equations using implicit Runge-Kutta methods.
                Implement the Radau IIA method for y' = f(t,y) with y(t0) = y0.
                
                Handle the nonlinear system arising from implicit formulation.
                """,
                function_signature="def radau_iia(f: callable, t_span: Tuple[float, float], y0: List[float], n_steps: int) -> Tuple[List[float], List[List[float]]]:",
                test_cases=[
                    {
                        "input": {
                            "f": "lambda t, y: [-1000*y[0] + 3000 - 2000*exp(-t)]",
                            "t_span": (0, 1),
                            "y0": [0],
                            "n_steps": 10
                        },
                        "expected": "Check stability and accuracy"
                    }
                ],
                constraints={"stiffness_ratio": "> 1000"},
                expected_complexity="O(n_steps * n³) where n = dimension",
                hints=[
                    "Use Newton's method for implicit equations",
                    "Implement proper step size control",
                    "Consider L-stable methods for stiff problems"
                ],
                mathematical_insight="Implicit methods provide stability for stiff systems",
                optimal_approach="Radau IIA with adaptive Newton iteration"
            )
    
    def _generate_optimization_problem(self, difficulty: int) -> MathProblem:
        """Generate optimization problems"""
        self.problem_id_counter += 1
        
        return MathProblem(
            id=f"opt_{self.problem_id_counter}",
            concept="optimization",
            difficulty=difficulty,
            problem_statement=f"""
            Implement the interior point method for linear programming.
            Minimize c^T x subject to Ax = b, x >= 0.
            
            Use the primal-dual path following approach with Mehrotra's predictor-corrector.
            """,
            function_signature="def interior_point_lp(c: List[float], A: List[List[float]], b: List[float], epsilon: float = 1e-8) -> List[float]:",
            test_cases=[
                {
                    "input": {
                        "c": [1, 2],
                        "A": [[1, 1], [2, 1]],
                        "b": [3, 4],
                        "epsilon": 1e-8
                    },
                    "expected": "Optimal solution with objective value"
                }
            ],
            constraints={"m": "constraints", "n": "variables", "condition": "A has full row rank"},
            expected_complexity="O(n³) per iteration",
            hints=[
                "Form the KKT system",
                "Use Cholesky factorization for normal equations",
                "Implement adaptive step size with centering parameter"
            ],
            mathematical_insight="Follow central path to optimal solution",
            optimal_approach="Mehrotra's predictor-corrector with sparse linear algebra"
        )
    
    def _generate_graph_theory_problem(self, difficulty: int) -> MathProblem:
        """Generate graph theory problems"""
        self.problem_id_counter += 1
        
        return MathProblem(
            id=f"graph_{self.problem_id_counter}",
            concept="graph_theory",
            difficulty=difficulty,
            problem_statement=f"""
            Implement the push-relabel algorithm for maximum flow.
            Given a flow network with capacities, find the maximum flow from source to sink.
            
            Use the highest-label rule and gap relabeling for efficiency.
            """,
            function_signature="def max_flow_push_relabel(graph: Dict[int, List[Tuple[int, int]]], source: int, sink: int) -> int:",
            test_cases=[
                {
                    "input": {
                        "graph": {0: [(1, 10), (2, 10)], 1: [(2, 2), (3, 4), (4, 8)], 2: [(4, 9)], 3: [(5, 10)], 4: [(3, 6), (5, 10)]},
                        "source": 0,
                        "sink": 5
                    },
                    "expected": 19
                }
            ],
            constraints={"V": "vertices <= 10^4", "E": "edges <= 10^5"},
            expected_complexity="O(V²E) worst case, O(V²√E) with heuristics",
            hints=[
                "Maintain height function and excess flow",
                "Push flow when possible, relabel when stuck",
                "Use gap relabeling to speed convergence"
            ],
            mathematical_insight="Max-flow min-cut theorem guarantees correctness",
            optimal_approach="Push-relabel with FIFO selection and gap relabeling"
        )
    
    def generate_problem_set(self, concept: str, count: int = 5, 
                           difficulty_range: Tuple[int, int] = (1, 3)) -> List[MathProblem]:
        """Generate a set of problems for a concept"""
        problems = []
        for _ in range(count):
            difficulty = random.randint(*difficulty_range)
            problems.append(self.generate_problem(concept, difficulty))
        return problems
    
    def generate_diagnostic_test(self, concepts: List[str]) -> List[MathProblem]:
        """Generate a diagnostic test covering multiple concepts"""
        problems = []
        for concept in concepts:
            # One easy and one medium problem per concept
            problems.append(self.generate_problem(concept, difficulty=1))
            problems.append(self.generate_problem(concept, difficulty=2))
        return problems