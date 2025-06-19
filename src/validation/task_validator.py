"""
Advanced TaskValidator for mathematical reasoning and code analysis.

This validator bridges code correctness with mathematical understanding,
providing comprehensive analysis of both implementation and reasoning.
"""

import ast
import re
import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import sympy as sp


class MathematicalConcept(Enum):
    """Mathematical concepts that can be identified in submissions."""
    NUMBER_THEORY = "number_theory"
    LINEAR_ALGEBRA = "linear_algebra"
    CALCULUS = "calculus"
    DISCRETE_MATH = "discrete_math"
    PROBABILITY = "probability"
    NUMERICAL_ANALYSIS = "numerical_analysis"
    ABSTRACT_ALGEBRA = "abstract_algebra"
    TOPOLOGY = "topology"
    COMPLEX_ANALYSIS = "complex_analysis"
    GRAPH_THEORY = "graph_theory"


@dataclass
class ProofStep:
    """Represents a single step in a mathematical proof."""
    statement: str
    justification: str
    line_number: int
    is_valid: bool = True
    confidence: float = 1.0


@dataclass
class ConceptUsage:
    """Tracks usage of a mathematical concept."""
    concept: MathematicalConcept
    confidence: float
    evidence: List[str]
    mastery_level: float  # 0-1 scale


@dataclass
class ValidationResult:
    """Comprehensive validation result."""
    mathematical_rigor: float  # 0-1
    proof_correctness: float  # 0-1 
    code_elegance: float  # 0-1
    concept_mastery: float  # 0-1
    
    concepts_identified: List[ConceptUsage]
    proof_steps: List[ProofStep]
    code_analysis: Dict[str, Any]
    feedback: List[str]
    suggestions: List[str]
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall validation score."""
        return (
            self.mathematical_rigor * 0.35 +
            self.proof_correctness * 0.25 +
            self.code_elegance * 0.25 +
            self.concept_mastery * 0.15
        )


class MathematicalConceptExtractor:
    """Extracts and identifies mathematical concepts from text and code."""
    
    def __init__(self):
        self.concept_patterns = {
            MathematicalConcept.NUMBER_THEORY: [
                r'prime\s+number', r'modular\s+arithmetic', r'gcd|lcm',
                r'fermat.*theorem', r'euler.*theorem', r'chinese.*remainder',
                r'divisibility', r'congruence', r'factorization'
            ],
            MathematicalConcept.LINEAR_ALGEBRA: [
                r'matrix|matrices', r'vector', r'eigenvalue|eigenvector',
                r'determinant', r'linear\s+transformation', r'basis',
                r'orthogonal', r'rank', r'null\s+space'
            ],
            MathematicalConcept.CALCULUS: [
                r'derivative|differentiation', r'integral|integration',
                r'limit', r'continuity', r'optimization', r'gradient',
                r'chain\s+rule', r'partial\s+derivative'
            ],
            MathematicalConcept.DISCRETE_MATH: [
                r'graph\s+theory', r'combinatorics', r'permutation',
                r'recursion|recurrence', r'dynamic\s*programming',
                r'complexity.*analysis', r'big.*o', r'algorithm',
                r'fibonacci', r'sequence', r'dp'
            ],
            MathematicalConcept.PROBABILITY: [
                r'probability', r'random', r'distribution', r'expectation',
                r'variance', r'bayes.*theorem', r'markov.*chain',
                r'monte.*carlo', r'statistics'
            ]
        }
        
        # Mathematical symbols and notation patterns
        self.math_symbols = [
            r'∑|\\sum', r'∏|\\prod', r'∫|\\int', r'∂|\\partial',
            r'∇|\\nabla', r'∈|\\in', r'∀|\\forall', r'∃|\\exists',
            r'≡|\\equiv', r'≤|\\leq', r'≥|\\geq', r'→|\\rightarrow'
        ]
    
    def extract_concepts(self, text: str, code: str) -> List[ConceptUsage]:
        """Extract mathematical concepts from submission text and code."""
        concepts = []
        full_text = (text + " " + code).lower()
        
        for concept, patterns in self.concept_patterns.items():
            evidence = []
            total_matches = 0
            
            for pattern in patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches)
                    total_matches += len(matches)
            
            if evidence:
                # Calculate confidence based on number and specificity of matches
                confidence = min(1.0, total_matches * 0.2 + len(evidence) * 0.1)
                mastery_level = self._assess_mastery_level(concept, full_text, evidence)
                
                concepts.append(ConceptUsage(
                    concept=concept,
                    confidence=confidence,
                    evidence=evidence[:5],  # Top 5 pieces of evidence
                    mastery_level=mastery_level
                ))
        
        return sorted(concepts, key=lambda x: x.confidence, reverse=True)
    
    def _assess_mastery_level(self, concept: MathematicalConcept, text: str, evidence: List[str]) -> float:
        """Assess mastery level of a mathematical concept."""
        # Advanced indicators for each concept
        advanced_indicators = {
            MathematicalConcept.NUMBER_THEORY: [
                'quadratic.*residue', 'carmichael.*number', 'primitive.*root',
                'diophantine.*equation', 'continued.*fraction'
            ],
            MathematicalConcept.LINEAR_ALGEBRA: [
                'singular.*value.*decomposition', 'jordan.*normal.*form',
                'spectral.*theorem', 'gram.*schmidt', 'cholesky.*decomposition'
            ],
            MathematicalConcept.CALCULUS: [
                'taylor.*series', 'fourier.*transform', 'lagrange.*multiplier',
                'implicit.*function.*theorem', 'fundamental.*theorem'
            ]
        }
        
        base_score = min(0.7, len(evidence) * 0.1)
        
        if concept in advanced_indicators:
            advanced_matches = sum(1 for pattern in advanced_indicators[concept]
                                 if re.search(pattern, text, re.IGNORECASE))
            advanced_bonus = min(0.3, advanced_matches * 0.15)
            return base_score + advanced_bonus
        
        return base_score


class ProofAnalyzer:
    """Analyzes mathematical proofs for structure and validity."""
    
    def __init__(self):
        self.proof_indicators = [
            r'proof:', r'to\s+prove', r'we\s+need\s+to\s+show',
            r'assume', r'suppose', r'let', r'given', r'since',
            r'therefore', r'thus', r'hence', r'it\s+follows',
            r'by\s+definition', r'by\s+theorem', r'by\s+lemma',
            r'qed', r'∎', r'this\s+completes\s+the\s+proof'
        ]
        
        self.logical_connectives = [
            r'if\s+and\s+only\s+if', r'necessary\s+and\s+sufficient',
            r'implies?', r'equivalent', r'contradiction', r'contrapositive'
        ]
    
    def analyze_proof(self, text: str) -> Tuple[List[ProofStep], float]:
        """Analyze proof structure and return steps with correctness score."""
        # Split text into logical units (sentences/paragraphs)
        sentences = self._split_into_logical_units(text)
        
        proof_steps = []
        for i, sentence in enumerate(sentences):
            if self._is_proof_step(sentence):
                step = self._create_proof_step(sentence, i)
                proof_steps.append(step)
        
        # Calculate overall proof correctness
        if not proof_steps:
            # Give some credit for having a mathematical explanation even without formal proof steps
            if len(text.strip()) > 100:
                return [], 0.4
            return [], 0.0
        
        valid_steps = sum(1 for step in proof_steps if step.is_valid)
        correctness = valid_steps / len(proof_steps)
        
        # Bonus for good proof structure
        structure_bonus = self._assess_proof_structure(proof_steps, text)
        # Give higher base score for having at least one proof step
        base_bonus = min(0.3, 0.1 * len(proof_steps))
        
        correctness = min(1.0, correctness + structure_bonus + base_bonus)
        
        return proof_steps, correctness
    
    def _split_into_logical_units(self, text: str) -> List[str]:
        """Split text into logical units for proof analysis."""
        # Split by sentences and filter out very short ones
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _is_proof_step(self, sentence: str) -> bool:
        """Determine if a sentence represents a proof step."""
        return any(re.search(indicator, sentence, re.IGNORECASE) 
                  for indicator in self.proof_indicators)
    
    def _create_proof_step(self, sentence: str, line_number: int) -> ProofStep:
        """Create a ProofStep object from a sentence."""
        # Extract statement and justification
        parts = re.split(r'\b(?:since|because|by|as)\b', sentence, 1, re.IGNORECASE)
        
        if len(parts) == 2:
            statement = parts[0].strip()
            justification = parts[1].strip()
        else:
            statement = sentence.strip()
            justification = "No explicit justification provided"
        
        # Simple validity check
        is_valid = self._validate_proof_step(statement, justification)
        confidence = self._calculate_step_confidence(statement, justification)
        
        return ProofStep(
            statement=statement,
            justification=justification,
            line_number=line_number,
            is_valid=is_valid,
            confidence=confidence
        )
    
    def _validate_proof_step(self, statement: str, justification: str) -> bool:
        """Validate a single proof step."""
        # Check for mathematical rigor indicators
        rigor_indicators = [
            'theorem', 'lemma', 'definition', 'axiom', 'hypothesis',
            'induction', 'contradiction', 'construction'
        ]
        
        has_justification = len(justification) > 5 and justification != "No explicit justification provided"
        has_rigor = any(indicator in justification.lower() for indicator in rigor_indicators)
        
        return has_justification and (has_rigor or len(justification) > 20)
    
    def _calculate_step_confidence(self, statement: str, justification: str) -> float:
        """Calculate confidence in proof step validity."""
        confidence = 0.5  # Base confidence
        
        # Boost for explicit justification
        if "No explicit justification" not in justification:
            confidence += 0.2
        
        # Boost for mathematical terms
        math_terms = ['theorem', 'lemma', 'definition', 'proof', 'given']
        confidence += min(0.2, sum(0.05 for term in math_terms 
                                  if term in justification.lower()))
        
        # Boost for logical structure
        if any(conn in statement.lower() for conn in ['if', 'then', 'therefore']):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _assess_proof_structure(self, steps: List[ProofStep], full_text: str) -> float:
        """Assess overall proof structure quality."""
        bonus = 0.0
        
        # Bonus for clear beginning
        if any(indicator in full_text.lower()[:100] 
               for indicator in ['proof:', 'to prove', 'we will show']):
            bonus += 0.1
        
        # Bonus for clear conclusion
        if any(indicator in full_text.lower()[-100:] 
               for indicator in ['qed', 'thus', 'therefore', 'completes']):
            bonus += 0.1
        
        # Bonus for logical flow
        if len(steps) > 2:
            logical_words = ['therefore', 'thus', 'hence', 'so', 'then']
            transitions = sum(1 for step in steps[1:] 
                            if any(word in step.statement.lower() for word in logical_words))
            bonus += min(0.1, transitions * 0.03)
        
        return bonus


class CodeAnalyzer:
    """Analyzes code structure, complexity, and mathematical content."""
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Comprehensive code analysis."""
        try:
            tree = ast.parse(code)
            analyzer = CodeVisitor()
            analyzer.visit(tree)
            
            return {
                'functions_defined': analyzer.function_count,
                'classes_defined': analyzer.class_count,
                'complexity_score': self._calculate_complexity_score(analyzer),
                'mathematical_operations': analyzer.math_operations,
                'documentation_quality': self._assess_documentation(tree),
                'algorithmic_patterns': self._identify_patterns(analyzer),
                'estimated_time_complexity': self._estimate_complexity(analyzer),
                'code_structure_score': self._assess_structure(analyzer)
            }
        except SyntaxError:
            return {
                'syntax_error': True,
                'functions_defined': 0,
                'complexity_score': 0.0,
                'code_structure_score': 0.0
            }
    
    def _calculate_complexity_score(self, visitor) -> float:
        """Calculate code complexity score."""
        # Cyclomatic complexity estimate
        complexity = (visitor.if_statements + visitor.loops + 
                     visitor.try_blocks + visitor.function_count)
        
        # Normalize to 0-1 scale (target: 5-15 for good complexity)
        normalized = 1.0 - abs(complexity - 10) / 20
        return max(0.0, min(1.0, normalized))
    
    def _assess_documentation(self, tree: ast.AST) -> float:
        """Assess quality of code documentation."""
        docstring_count = 0
        comment_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    docstring_count += 1
        
        # Simple documentation score
        return min(1.0, docstring_count * 0.3)
    
    def _identify_patterns(self, visitor) -> List[str]:
        """Identify common algorithmic patterns."""
        patterns = []
        
        if visitor.loops > 0 and visitor.recursive_calls > 0:
            patterns.append("hybrid_iteration_recursion")
        elif visitor.recursive_calls > 0:
            patterns.append("recursive")
        elif visitor.nested_loops > 0:
            patterns.append("nested_iteration")
        elif visitor.loops > 0:
            patterns.append("iterative")
        
        if visitor.math_operations > 5:
            patterns.append("math_intensive")
        
        return patterns
    
    def _estimate_complexity(self, visitor) -> str:
        """Estimate time complexity based on code structure."""
        if visitor.nested_loops >= 2:
            return "O(n³) or higher"
        elif visitor.nested_loops >= 1:
            return "O(n²)"
        elif visitor.loops > 0:
            return "O(n)"
        elif visitor.recursive_calls > 0:
            return "O(2ⁿ) or O(n) depending on implementation"
        else:
            return "O(1)"
    
    def _assess_structure(self, visitor) -> float:
        """Assess overall code structure quality."""
        score = 0.5  # Base score
        
        # Bonus for functions
        if visitor.function_count > 0:
            score += 0.2
        
        # Bonus for appropriate complexity
        if 1 <= visitor.function_count <= 5:
            score += 0.1
        
        # Penalty for excessive nesting
        if visitor.max_nesting > 4:
            score -= 0.2
        
        return max(0.0, min(1.0, score))


class CodeVisitor(ast.NodeVisitor):
    """AST visitor for code analysis."""
    
    def __init__(self):
        self.function_count = 0
        self.class_count = 0
        self.loops = 0
        self.nested_loops = 0
        self.if_statements = 0
        self.try_blocks = 0
        self.recursive_calls = 0
        self.math_operations = 0
        self.max_nesting = 0
        self.current_nesting = 0
        self.current_function = None
    
    def visit_FunctionDef(self, node):
        self.function_count += 1
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_ClassDef(self, node):
        self.class_count += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.loops += 1
        if self.current_nesting > 0:
            self.nested_loops += 1
        self._visit_with_nesting(node)
    
    def visit_While(self, node):
        self.loops += 1
        if self.current_nesting > 0:
            self.nested_loops += 1
        self._visit_with_nesting(node)
    
    def visit_If(self, node):
        self.if_statements += 1
        self._visit_with_nesting(node)
    
    def visit_Try(self, node):
        self.try_blocks += 1
        self.generic_visit(node)
    
    def visit_Call(self, node):
        # Check for recursive calls
        if (isinstance(node.func, ast.Name) and 
            self.current_function and 
            node.func.id == self.current_function):
            self.recursive_calls += 1
        
        # Check for mathematical operations
        if isinstance(node.func, ast.Name):
            math_funcs = ['pow', 'sqrt', 'log', 'exp', 'sin', 'cos', 'tan']
            if node.func.id in math_funcs:
                self.math_operations += 1
        
        self.generic_visit(node)
    
    def visit_BinOp(self, node):
        # Count mathematical binary operations
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, 
                               ast.Mod, ast.Pow, ast.FloorDiv)):
            self.math_operations += 1
        self.generic_visit(node)
    
    def _visit_with_nesting(self, node):
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1


class TaskValidator:
    """Main TaskValidator class that orchestrates all validation components."""
    
    def __init__(self):
        self.concept_extractor = MathematicalConceptExtractor()
        self.proof_analyzer = ProofAnalyzer()
        self.code_analyzer = CodeAnalyzer()
    
    def validate_mathematical_correctness(self, submission) -> ValidationResult:
        """
        Comprehensive validation of mathematical reasoning and code quality.
        
        Args:
            submission: Object with .code and .mathematical_reasoning attributes
            
        Returns:
            ValidationResult with detailed analysis
        """
        code = getattr(submission, 'code', '')
        reasoning = getattr(submission, 'mathematical_reasoning', '')
        
        # Extract mathematical concepts
        concepts = self.concept_extractor.extract_concepts(reasoning, code)
        
        # Analyze proof structure and validity
        proof_steps, proof_correctness = self.proof_analyzer.analyze_proof(reasoning)
        
        # Analyze code structure and complexity
        code_analysis = self.code_analyzer.analyze_code(code)
        
        # Calculate scores
        mathematical_rigor = self._calculate_mathematical_rigor(concepts, reasoning, code)
        code_elegance = code_analysis.get('code_structure_score', 0.0)
        concept_mastery = self._calculate_concept_mastery(concepts)
        
        # Generate feedback and suggestions
        feedback = self._generate_feedback(concepts, proof_steps, code_analysis)
        suggestions = self._generate_suggestions(concepts, proof_steps, code_analysis)
        
        return ValidationResult(
            mathematical_rigor=mathematical_rigor,
            proof_correctness=proof_correctness,
            code_elegance=code_elegance,
            concept_mastery=concept_mastery,
            concepts_identified=concepts,
            proof_steps=proof_steps,
            code_analysis=code_analysis,
            feedback=feedback,
            suggestions=suggestions
        )
    
    def _calculate_mathematical_rigor(self, concepts: List[ConceptUsage], 
                                    reasoning: str, code: str) -> float:
        """Calculate mathematical rigor score."""
        base_score = 0.3  # Base for having some reasoning
        
        if not reasoning.strip():
            return 0.0
        
        # Increased bonus for identified concepts
        concept_bonus = min(0.4, len(concepts) * 0.15)
        
        # Bonus for mathematical notation
        notation_patterns = [r'\\[a-zA-Z]+', r'[∀∃∈∉⊂⊆∪∩∧∨¬→↔]', r'\^[0-9]+']
        notation_bonus = min(0.25, sum(0.1 for pattern in notation_patterns 
                                    if re.search(pattern, reasoning)))
        
        # Bonus for proof keywords
        proof_keywords = ['theorem', 'lemma', 'proof', 'derive', 'show', 'prove', 'qed', 'therefore']
        proof_bonus = min(0.3, sum(0.05 for keyword in proof_keywords 
                                 if keyword in reasoning.lower()))
        
        # Bonus for code docstrings with mathematical explanations
        math_in_docstring = any(term in code.lower() for term in 
                               ['complexity', 'algorithm', 'o(', 'mathematical', 'time complexity'])
        docstring_bonus = 0.1 if math_in_docstring else 0.0
        
        return min(1.0, base_score + concept_bonus + notation_bonus + proof_bonus + docstring_bonus)
    
    def _calculate_concept_mastery(self, concepts: List[ConceptUsage]) -> float:
        """Calculate overall concept mastery score."""
        if not concepts:
            return 0.0
        
        # Weighted average of mastery levels, weighted by confidence
        total_weighted_mastery = sum(c.mastery_level * c.confidence for c in concepts)
        total_weight = sum(c.confidence for c in concepts)
        
        return total_weighted_mastery / total_weight if total_weight > 0 else 0.0
    
    def _generate_feedback(self, concepts: List[ConceptUsage], 
                          proof_steps: List[ProofStep],
                          code_analysis: Dict[str, Any]) -> List[str]:
        """Generate specific feedback for the submission."""
        feedback = []
        
        # Concept feedback
        if concepts:
            concept_names = [c.concept.value.replace('_', ' ').title() for c in concepts[:3]]
            feedback.append(f"✓ Mathematical concepts identified: {', '.join(concept_names)}")
            
            # Add feedback about specific concepts evidence
            for concept in concepts:
                if concept.evidence and len(concept.evidence) > 0:
                    # Include actual evidence in feedback
                    evidence_text = ', '.join(set(concept.evidence[:3]))
                    feedback.append(f"• {concept.concept.value.title()} concepts used: {evidence_text}")
        else:
            feedback.append("⚠ No clear mathematical concepts identified")
        
        # Proof feedback
        if proof_steps:
            valid_steps = sum(1 for step in proof_steps if step.is_valid)
            feedback.append(f"✓ Proof structure: {valid_steps}/{len(proof_steps)} steps validated")
        else:
            feedback.append("⚠ No clear proof structure found")
        
        # Code feedback
        if code_analysis.get('functions_defined', 0) > 0:
            feedback.append(f"✓ Code structure: {code_analysis['functions_defined']} functions defined")
        
        # Include algorithmic patterns in feedback
        patterns = code_analysis.get('algorithmic_patterns', [])
        if patterns:
            patterns_text = ', '.join(patterns)
            feedback.append(f"• Algorithmic approach: {patterns_text}")
        
        complexity = code_analysis.get('estimated_time_complexity', 'Unknown')
        feedback.append(f"• Estimated complexity: {complexity}")
        
        return feedback
    
    def _generate_suggestions(self, concepts: List[ConceptUsage],
                            proof_steps: List[ProofStep],
                            code_analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # Mathematical reasoning suggestions
        if len(concepts) < 2:
            suggestions.append("Consider explaining more mathematical concepts relevant to your solution")
        
        weak_steps = [step for step in proof_steps if not step.is_valid]
        if weak_steps:
            suggestions.append(f"Strengthen {len(weak_steps)} proof steps with better justification")
        
        # Code suggestions
        if code_analysis.get('functions_defined', 0) == 0:
            suggestions.append("Structure your code into functions for better organization")
        
        if code_analysis.get('documentation_quality', 0) < 0.5:
            suggestions.append("Add docstrings to explain your functions mathematically")
        
        # Complexity suggestions
        estimated_complexity = code_analysis.get('estimated_time_complexity', '')
        if 'O(n³)' in estimated_complexity or 'O(2ⁿ)' in estimated_complexity:
            suggestions.append("Consider optimizing your algorithm for better time complexity")
        
        return suggestions


# Integration with existing platform
def integrate_with_submission_api():
    """Example of how to integrate TaskValidator with the existing API."""
    
    from src.platform.api import submission_router
    from fastapi import Depends
    from src.validation.task_validator import TaskValidator
    
    validator = TaskValidator()
    
    @submission_router.post("/{submission_id}/validate")
    async def validate_submission_detailed(submission_id: int):
        """Enhanced validation endpoint using TaskValidator."""
        # This would integrate with your existing submission retrieval
        # submission = get_submission(submission_id)
        
        # Mock submission for example
        class MockSubmission:
            def __init__(self):
                self.code = '''
def mod_exp(base, exp, modulus):
    """
    Fast modular exponentiation using binary method.
    
    Mathematical basis: Uses the binary representation of the exponent
    to compute base^exp mod modulus efficiently.
    
    Time complexity: O(log exp) due to binary exponentiation.
    """
    result = 1
    base = base % modulus
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exp //= 2
    
    return result
                '''
                
                self.mathematical_reasoning = '''
Mathematical Derivation:
We want to compute base^exp mod modulus efficiently.

Key insight: Any integer exp can be written in binary as:
exp = b₀ + b₁×2¹ + b₂×2² + ... + bₖ×2ᵏ where bᵢ ∈ {0,1}

Therefore: base^exp = base^(b₀ + b₁×2¹ + b₂×2² + ... + bₖ×2ᵏ)
                    = (base^b₀) × (base^(b₁×2¹)) × ... × (base^(bₖ×2ᵏ))

Since base^(2ⁱ) = (base^(2^(i-1)))², we can compute all needed powers 
by successive squaring.

Proof of correctness:
By Fermat's Little Theorem, if p is prime and gcd(a,p) = 1, then a^(p-1) ≡ 1 (mod p).
Our algorithm maintains the invariant that result × base^exp ≡ original_base^original_exp (mod modulus).

Time complexity: O(log exp) since we process each bit of exp exactly once.
                '''
        
        submission = MockSubmission()
        result = validator.validate_mathematical_correctness(submission)
        
        return {
            "validation_result": {
                "overall_score": result.overall_score,
                "mathematical_rigor": result.mathematical_rigor,
                "proof_correctness": result.proof_correctness,
                "code_elegance": result.code_elegance,
                "concept_mastery": result.concept_mastery,
                "concepts_identified": [
                    {
                        "concept": c.concept.value,
                        "confidence": c.confidence,
                        "evidence": c.evidence,
                        "mastery_level": c.mastery_level
                    }
                    for c in result.concepts_identified
                ],
                "proof_steps": [
                    {
                        "statement": step.statement,
                        "justification": step.justification,
                        "is_valid": step.is_valid,
                        "confidence": step.confidence
                    }
                    for step in result.proof_steps
                ],
                "feedback": result.feedback,
                "suggestions": result.suggestions
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the TaskValidator
    validator = TaskValidator()
    
    class TestSubmission:
        def __init__(self):
            self.code = '''
def fibonacci_matrix(n):
    """
    Compute nth Fibonacci number using matrix exponentiation.
    
    Mathematical foundation: F(n) can be computed using the matrix equation:
    [F(n+1)]   [1 1]^n   [F(1)]
    [F(n)  ] = [1 0]   × [F(0)]
    
    Time complexity: O(log n) due to fast matrix exponentiation.
    """
    if n <= 1:
        return n
    
    def matrix_mult(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    
    def matrix_power(matrix, power):
        if power == 1:
            return matrix
        if power % 2 == 0:
            half = matrix_power(matrix, power // 2)
            return matrix_mult(half, half)
        else:
            return matrix_mult(matrix, matrix_power(matrix, power - 1))
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]
            '''
            
            self.mathematical_reasoning = '''
Mathematical Proof of Fibonacci Matrix Method:

Theorem: The nth Fibonacci number can be computed using matrix exponentiation.

Proof:
Let F(n) be the nth Fibonacci number where F(0) = 0, F(1) = 1, and F(n) = F(n-1) + F(n-2).

Define the matrix M = [1 1]
                      [1 0]

We claim that M^n = [F(n+1) F(n)  ]
                    [F(n)   F(n-1)]

Proof by induction:
Base case (n=1): M^1 = [1 1] = [F(2) F(1)] = [1 1] ✓
                       [1 0]   [F(1) F(0)]   [1 0]

Inductive step: Assume true for n=k, prove for n=k+1.
M^(k+1) = M^k × M = [F(k+1) F(k)  ] × [1 1]
                    [F(k)   F(k-1)]   [1 0]

= [F(k+1)×1 + F(k)×1    F(k+1)×1 + F(k)×0  ]
  [F(k)×1 + F(k-1)×1    F(k)×1 + F(k-1)×0  ]

= [F(k+1) + F(k)    F(k+1)]  = [F(k+2) F(k+1)]
  [F(k) + F(k-1)    F(k)  ]    [F(k+1) F(k)  ]

This proves our claim. Therefore F(n) = (M^n)[0][1].

Time Complexity Analysis:
Matrix exponentiation using repeated squaring gives us O(log n) complexity,
which is exponentially faster than the naive O(φ^n) recursive approach.
            '''
    
    test_submission = TestSubmission()
    result = validator.validate_mathematical_correctness(test_submission)
    
    print("=== TaskValidator Test Results ===")
    print(f"Overall Score: {result.overall_score:.3f}")
    print(f"Mathematical Rigor: {result.mathematical_rigor:.3f}")
    print(f"Proof Correctness: {result.proof_correctness:.3f}")
    print(f"Code Elegance: {result.code_elegance:.3f}")
    print(f"Concept Mastery: {result.concept_mastery:.3f}")
    
    print("\\nConcepts Identified:")
    for concept in result.concepts_identified:
        print(f"  • {concept.concept.value}: {concept.confidence:.2f} confidence")
    
    print("\\nFeedback:")
    for feedback in result.feedback:
        print(f"  {feedback}")
    
    print("\\nSuggestions:")
    for suggestion in result.suggestions:
        print(f"  • {suggestion}")
    
    print(f"\\nProof Steps Analyzed: {len(result.proof_steps)}")
    for i, step in enumerate(result.proof_steps[:3]):  # Show first 3 steps
        print(f"  Step {i+1}: {'✓' if step.is_valid else '✗'} {step.statement[:50]}...")