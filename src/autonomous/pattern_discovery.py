"""
Pattern Discovery System - Extracts mathematical and algorithmic patterns from code.
"""

import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json


@dataclass
class Pattern:
    """Represents a discovered pattern."""
    name: str
    category: str  # algorithmic, mathematical, optimization, theoretical
    code_template: Optional[str]
    description: str
    mathematical_properties: List[str]
    complexity: Optional[str]
    prerequisites: List[str]
    confidence: float  # 0.0 to 1.0


@dataclass
class PatternMatch:
    """Represents a pattern found in code."""
    pattern: Pattern
    location: Tuple[int, int]  # start_line, end_line
    code_snippet: str
    confidence: float


class PatternExtractor:
    """Extracts patterns from mathematical code implementations."""
    
    def __init__(self):
        self.known_patterns = self._initialize_known_patterns()
        
    def _initialize_known_patterns(self) -> Dict[str, Pattern]:
        """Initialize database of known mathematical patterns."""
        patterns = {
            # Algorithmic patterns
            "recursive_structure": Pattern(
                name="recursive_structure",
                category="algorithmic",
                code_template="def f(n):\n    if base_case:\n        return base_value\n    return f(smaller_problem)",
                description="Recursive problem decomposition",
                mathematical_properties=["self-similarity", "problem_reduction"],
                complexity="depends on recursion depth",
                prerequisites=[],
                confidence=0.9
            ),
            "iterative_reduction": Pattern(
                name="iterative_reduction",
                category="algorithmic",
                code_template="while condition:\n    value = reduce(value)\n    update_state()",
                description="Iterative reduction to base case",
                mathematical_properties=["monotonic_decrease", "termination"],
                complexity="O(iterations)",
                prerequisites=[],
                confidence=0.9
            ),
            
            # Mathematical patterns
            "modular_arithmetic": Pattern(
                name="modular_arithmetic",
                category="mathematical",
                code_template="result = value % modulus",
                description="Modular arithmetic operations",
                mathematical_properties=["ring_operations", "congruence"],
                complexity="O(1)",
                prerequisites=["number_theory_basics"],
                confidence=0.95
            ),
            "euclidean_division": Pattern(
                name="euclidean_division",
                category="mathematical",
                code_template="quotient, remainder = divmod(a, b)",
                description="Division with quotient and remainder",
                mathematical_properties=["division_algorithm", "uniqueness"],
                complexity="O(1)",
                prerequisites=["arithmetic"],
                confidence=0.95
            ),
            
            # Optimization patterns
            "early_termination": Pattern(
                name="early_termination",
                category="optimization",
                code_template="if special_case:\n    return quick_result",
                description="Early exit for special cases",
                mathematical_properties=["edge_case_handling"],
                complexity="O(1) for special cases",
                prerequisites=[],
                confidence=0.85
            ),
            "memoization": Pattern(
                name="memoization",
                category="optimization",
                code_template="if key in cache:\n    return cache[key]\nresult = compute()\ncache[key] = result",
                description="Caching previously computed results",
                mathematical_properties=["referential_transparency"],
                complexity="O(1) lookup after first computation",
                prerequisites=["pure_functions"],
                confidence=0.9
            ),
            
            # Theoretical patterns
            "mathematical_invariant": Pattern(
                name="mathematical_invariant",
                category="theoretical",
                code_template="# Invariant: property holds throughout",
                description="Maintaining mathematical invariants",
                mathematical_properties=["invariant_preservation"],
                complexity="N/A",
                prerequisites=["mathematical_reasoning"],
                confidence=0.8
            ),
            "proof_by_induction": Pattern(
                name="proof_by_induction",
                category="theoretical",
                code_template="# Base case + Inductive step",
                description="Inductive reasoning in algorithm",
                mathematical_properties=["mathematical_induction"],
                complexity="N/A",
                prerequisites=["mathematical_logic"],
                confidence=0.75
            )
        }
        return patterns
    
    def extract_patterns(self, code: str, context: Optional[Dict[str, Any]] = None) -> List[PatternMatch]:
        """Extract all patterns from given code."""
        matches = []
        
        # Parse AST
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return matches
        
        # Extract different types of patterns
        matches.extend(self._extract_algorithmic_patterns(tree, code))
        matches.extend(self._extract_mathematical_patterns(tree, code))
        matches.extend(self._extract_optimization_patterns(tree, code))
        matches.extend(self._extract_theoretical_patterns(code))
        
        # Apply context-specific pattern recognition if provided
        if context:
            matches = self._refine_with_context(matches, context)
        
        return sorted(matches, key=lambda m: m.confidence, reverse=True)
    
    def _extract_algorithmic_patterns(self, tree: ast.AST, code: str) -> List[PatternMatch]:
        """Extract algorithmic patterns from AST."""
        matches = []
        
        for node in ast.walk(tree):
            # Check for recursion
            if isinstance(node, ast.FunctionDef):
                if self._is_recursive(node, node.name):
                    matches.append(PatternMatch(
                        pattern=self.known_patterns["recursive_structure"],
                        location=(node.lineno, node.end_lineno or node.lineno),
                        code_snippet=self._get_node_source(node, code),
                        confidence=0.9
                    ))
            
            # Check for iterative patterns
            elif isinstance(node, ast.While):
                matches.append(PatternMatch(
                    pattern=self.known_patterns["iterative_reduction"],
                    location=(node.lineno, node.end_lineno or node.lineno),
                    code_snippet=self._get_node_source(node, code),
                    confidence=0.85
                ))
        
        return matches
    
    def _extract_mathematical_patterns(self, tree: ast.AST, code: str) -> List[PatternMatch]:
        """Extract mathematical patterns from AST."""
        matches = []
        
        for node in ast.walk(tree):
            # Check for modular arithmetic
            if isinstance(node, ast.Mod):
                matches.append(PatternMatch(
                    pattern=self.known_patterns["modular_arithmetic"],
                    location=(node.lineno if hasattr(node, 'lineno') else 0, 
                             node.lineno if hasattr(node, 'lineno') else 0),
                    code_snippet="% operation",
                    confidence=0.95
                ))
            
            # Check for divmod usage
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "divmod":
                    matches.append(PatternMatch(
                        pattern=self.known_patterns["euclidean_division"],
                        location=(node.lineno, node.lineno),
                        code_snippet=self._get_node_source(node, code),
                        confidence=0.95
                    ))
        
        return matches
    
    def _extract_optimization_patterns(self, tree: ast.AST, code: str) -> List[PatternMatch]:
        """Extract optimization patterns."""
        matches = []
        
        for node in ast.walk(tree):
            # Check for early termination
            if isinstance(node, ast.If):
                # Look for return statements in if body
                for child in node.body:
                    if isinstance(child, ast.Return):
                        matches.append(PatternMatch(
                            pattern=self.known_patterns["early_termination"],
                            location=(node.lineno, child.lineno),
                            code_snippet=self._get_node_source(node, code),
                            confidence=0.8
                        ))
                        break
        
        return matches
    
    def _extract_theoretical_patterns(self, code: str) -> List[PatternMatch]:
        """Extract theoretical patterns from comments and docstrings."""
        matches = []
        
        # Look for invariant mentions
        if re.search(r"invariant|maintains?|preserves?", code, re.IGNORECASE):
            matches.append(PatternMatch(
                pattern=self.known_patterns["mathematical_invariant"],
                location=(0, 0),  # Can't determine exact location from regex
                code_snippet="Invariant mention in comments/docs",
                confidence=0.7
            ))
        
        # Look for induction mentions
        if re.search(r"base case|inductive|induction", code, re.IGNORECASE):
            matches.append(PatternMatch(
                pattern=self.known_patterns["proof_by_induction"],
                location=(0, 0),
                code_snippet="Inductive reasoning in comments/docs",
                confidence=0.65
            ))
        
        return matches
    
    def _is_recursive(self, func_node: ast.FunctionDef, func_name: str) -> bool:
        """Check if a function is recursive."""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_name:
                    return True
        return False
    
    def _get_node_source(self, node: ast.AST, source: str) -> str:
        """Extract source code for an AST node."""
        try:
            lines = source.split('\n')
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                return '\n'.join(lines[node.lineno-1:node.end_lineno])
            elif hasattr(node, 'lineno'):
                return lines[node.lineno-1]
        except:
            pass
        return "Source not available"
    
    def _refine_with_context(self, matches: List[PatternMatch], context: Dict[str, Any]) -> List[PatternMatch]:
        """Refine pattern matches based on context."""
        # Adjust confidence based on challenge type
        if context.get('challenge_type') == 'number_theory':
            for match in matches:
                if match.pattern.category == 'mathematical':
                    match.confidence *= 1.1  # Boost mathematical patterns
        
        return matches
    
    def calculate_pattern_similarity(self, pattern1: Pattern, pattern2: Pattern) -> float:
        """Calculate similarity score between two patterns."""
        score = 0.0
        
        # Category match
        if pattern1.category == pattern2.category:
            score += 0.3
        
        # Prerequisites overlap
        prereq_overlap = len(set(pattern1.prerequisites) & set(pattern2.prerequisites))
        max_prereqs = max(len(pattern1.prerequisites), len(pattern2.prerequisites))
        if max_prereqs > 0:
            score += 0.2 * (prereq_overlap / max_prereqs)
        
        # Mathematical properties overlap
        props_overlap = len(set(pattern1.mathematical_properties) & set(pattern2.mathematical_properties))
        max_props = max(len(pattern1.mathematical_properties), len(pattern2.mathematical_properties))
        if max_props > 0:
            score += 0.3 * (props_overlap / max_props)
        
        # Name similarity (simple check)
        if pattern1.name == pattern2.name:
            score += 0.2
        
        return min(score, 1.0)
    
    def suggest_patterns(self, current_patterns: List[Pattern], knowledge_base: Dict[str, Pattern]) -> List[Pattern]:
        """Suggest related patterns based on current patterns."""
        suggestions = []
        
        for current in current_patterns:
            for kb_name, kb_pattern in knowledge_base.items():
                if kb_pattern not in current_patterns:
                    similarity = self.calculate_pattern_similarity(current, kb_pattern)
                    if similarity > 0.5:
                        suggestions.append(kb_pattern)
        
        # Remove duplicates and sort by relevance
        seen = set()
        unique_suggestions = []
        for pattern in suggestions:
            if pattern.name not in seen:
                seen.add(pattern.name)
                unique_suggestions.append(pattern)
        
        return unique_suggestions


class PatternStorage:
    """Stores and retrieves patterns for learning agents."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path
        self.patterns: Dict[str, Pattern] = {}
        self.pattern_usage: Dict[str, int] = defaultdict(int)
        
    def add_pattern(self, pattern: Pattern) -> None:
        """Add a new pattern to storage."""
        self.patterns[pattern.name] = pattern
        
    def get_pattern(self, name: str) -> Optional[Pattern]:
        """Retrieve a pattern by name."""
        pattern = self.patterns.get(name)
        if pattern:
            self.pattern_usage[name] += 1
        return pattern
    
    def search_patterns(self, category: Optional[str] = None, 
                       prerequisites: Optional[List[str]] = None) -> List[Pattern]:
        """Search patterns by criteria."""
        results = []
        
        for pattern in self.patterns.values():
            if category and pattern.category != category:
                continue
            if prerequisites:
                if not all(prereq in pattern.prerequisites for prereq in prerequisites):
                    continue
            results.append(pattern)
        
        return results
    
    def get_most_used_patterns(self, limit: int = 10) -> List[Tuple[Pattern, int]]:
        """Get most frequently used patterns."""
        sorted_usage = sorted(self.pattern_usage.items(), 
                            key=lambda x: x[1], reverse=True)[:limit]
        return [(self.patterns[name], count) for name, count in sorted_usage 
                if name in self.patterns]
    
    def save_to_file(self, filepath: str) -> None:
        """Save patterns to JSON file."""
        data = {
            "patterns": {name: {
                "name": p.name,
                "category": p.category,
                "code_template": p.code_template,
                "description": p.description,
                "mathematical_properties": p.mathematical_properties,
                "complexity": p.complexity,
                "prerequisites": p.prerequisites,
                "confidence": p.confidence
            } for name, p in self.patterns.items()},
            "usage": dict(self.pattern_usage)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filepath: str) -> None:
        """Load patterns from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.patterns = {}
        for name, pattern_data in data.get("patterns", {}).items():
            self.patterns[name] = Pattern(**pattern_data)
        
        self.pattern_usage = defaultdict(int, data.get("usage", {}))