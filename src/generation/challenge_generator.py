"""
Challenge Generator module for automatically creating mathematical challenges.

This module generates new challenges based on:
- Mathematical domains (e.g., number theory, linear algebra)
- Difficulty levels
- Learning objectives
- Available templates
"""

import random
import json
import os
import yaml
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class GenerationStrategy(Enum):
    """Strategy for generating challenges."""
    TEMPLATE_BASED = "template_based"
    PARAMETERIZED = "parameterized"
    ADAPTIVE = "adaptive"
    LEARNING_PATH = "learning_path"


class ChallengeGenerator:
    """Generates new mathematical challenges."""
    
    def __init__(self, templates_dir: str = "templates/challenges"):
        """
        Initialize the challenge generator.
        
        Args:
            templates_dir: Directory containing challenge templates
        """
        self.templates_dir = templates_dir
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Any]:
        """Load challenge templates from the templates directory."""
        templates = {}
        
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            # Create a sample template if none exist
            self._create_sample_template()
        
        for domain_dir in os.listdir(self.templates_dir):
            domain_path = os.path.join(self.templates_dir, domain_dir)
            if os.path.isdir(domain_path):
                domain_templates = {}
                for level_dir in os.listdir(domain_path):
                    level_path = os.path.join(domain_path, level_dir)
                    if os.path.isdir(level_path):
                        level_templates = []
                        for template_file in os.listdir(level_path):
                            if template_file.endswith(".json"):
                                template_path = os.path.join(level_path, template_file)
                                try:
                                    with open(template_path, 'r') as f:
                                        template = json.load(f)
                                        level_templates.append(template)
                                except Exception as e:
                                    print(f"Error loading template {template_path}: {str(e)}")
                        
                        if level_templates:
                            domain_templates[level_dir] = level_templates
                
                if domain_templates:
                    templates[domain_dir] = domain_templates
        
        return templates
    
    def _create_sample_template(self):
        """Create a sample challenge template."""
        # Create directory structure
        number_theory_dir = os.path.join(self.templates_dir, "number_theory")
        intermediate_dir = os.path.join(number_theory_dir, "intermediate")
        os.makedirs(intermediate_dir, exist_ok=True)
        
        # Create sample template
        sample_template = {
            "title": "Prime Factorization Challenge",
            "description_template": """
# {{title}}

## Problem Statement

Find the prime factorization of the number {{number}}.

## Mathematical Foundation

A prime number is a natural number greater than 1 that is not a product of two smaller natural numbers.
The prime factorization of a number is the product of prime numbers that equals the original number.

## Task

Your task is to implement a function `prime_factorize(n)` that:

1. Takes an integer `n` as input
2. Returns a list of prime factors of `n` in ascending order
3. For repeated prime factors, the prime should appear multiple times in the result

## Example

```
Input: 60
Output: [2, 2, 3, 5]
```

Explanation: 60 = 2 × 2 × 3 × 5

## Requirements

1. Your solution should handle inputs up to 10^9
2. Time complexity analysis is required
3. Explain the mathematical principles behind your approach
            """,
            "parameters": {
                "number": {
                    "type": "integer",
                    "min": 100,
                    "max": 10000000,
                    "description": "The number to factorize"
                },
                "title": {
                    "type": "string",
                    "options": [
                        "Prime Factorization Challenge",
                        "Finding Prime Factors",
                        "Prime Decomposition Problem"
                    ],
                    "description": "The title of the challenge"
                }
            },
            "requirements": [
                {
                    "concept": "Prime Numbers",
                    "description": "Understanding of prime numbers and their properties",
                    "proof_required": True
                },
                {
                    "concept": "Factorization Algorithms",
                    "description": "Knowledge of efficient factorization techniques",
                    "proof_required": False,
                    "complexity_analysis": True
                }
            ],
            "test_case_generator": {
                "function_name": "prime_factorize",
                "test_cases": [
                    {"input": 60, "expected_output": [2, 2, 3, 5]},
                    {"input": 100, "expected_output": [2, 2, 5, 5]},
                    {"input": "{{number}}", "expected_output": "calculated"},
                    {"input": "{{number * 2}}", "expected_output": "calculated"}
                ]
            }
        }
        
        # Write sample template to file
        template_path = os.path.join(intermediate_dir, "prime_factorization.json")
        with open(template_path, 'w') as f:
            json.dump(sample_template, f, indent=2)
    
    def generate_challenge(
        self,
        domain: MathematicalDomain,
        level: ChallengeLevel,
        strategy: GenerationStrategy = GenerationStrategy.TEMPLATE_BASED,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Challenge:
        """
        Generate a new challenge.
        
        Args:
            domain: Mathematical domain for the challenge
            level: Difficulty level
            strategy: Generation strategy
            parameters: Optional parameters for challenge generation
            
        Returns:
            A new Challenge instance
        """
        parameters = parameters or {}
        
        if strategy == GenerationStrategy.TEMPLATE_BASED:
            return self._generate_from_template(domain, level, parameters)
        elif strategy == GenerationStrategy.PARAMETERIZED:
            return self._generate_parameterized(domain, level, parameters)
        elif strategy == GenerationStrategy.ADAPTIVE:
            return self._generate_adaptive(domain, level, parameters)
        elif strategy == GenerationStrategy.LEARNING_PATH:
            return self._generate_for_learning_path(domain, level, parameters)
        else:
            raise ValueError(f"Unknown generation strategy: {strategy}")
    
    def _generate_from_template(
        self,
        domain: MathematicalDomain,
        level: ChallengeLevel,
        parameters: Dict[str, Any]
    ) -> Challenge:
        """Generate a challenge from a template."""
        # Find appropriate templates
        domain_str = domain.value
        level_str = level.value
        
        if domain_str not in self.templates:
            raise ValueError(f"No templates found for domain: {domain_str}")
        
        if level_str not in self.templates[domain_str]:
            raise ValueError(f"No templates found for level: {level_str} in domain: {domain_str}")
        
        # Select a random template
        template = random.choice(self.templates[domain_str][level_str])
        
        # Fill in template parameters
        title = self._fill_parameter(template.get("title", ""), parameters)
        description_template = template.get("description_template", "")
        
        # Generate parameter values if not provided
        for param_name, param_spec in template.get("parameters", {}).items():
            if param_name not in parameters:
                parameters[param_name] = self._generate_parameter_value(param_spec)
        
        # Fill in the description template
        description = self._fill_template(description_template, parameters)
        
        # Create mathematical requirements
        requirements = []
        for req in template.get("requirements", []):
            requirements.append(MathematicalRequirement(
                concept=req["concept"],
                description=req["description"],
                proof_required=req.get("proof_required", False),
                complexity_analysis=req.get("complexity_analysis", False)
            ))
        
        # Generate test cases
        test_cases = self._generate_test_cases(template.get("test_case_generator", {}), parameters)
        
        # Create and return the challenge
        return Challenge(
            title=title,
            description=description,
            level=level,
            domain=domain,
            mathematical_requirements=requirements,
            test_cases=test_cases,
            time_limit=template.get("time_limit", 600.0)
        )
    
    def _generate_parameterized(
        self,
        domain: MathematicalDomain,
        level: ChallengeLevel,
        parameters: Dict[str, Any]
    ) -> Challenge:
        """Generate a parameterized challenge."""
        # This is a more sophisticated approach that would generate challenges
        # based on parameters without relying on templates
        # For now, it falls back to template-based generation
        return self._generate_from_template(domain, level, parameters)
    
    def _generate_adaptive(
        self,
        domain: MathematicalDomain,
        level: ChallengeLevel,
        parameters: Dict[str, Any]
    ) -> Challenge:
        """Generate an adaptive challenge based on user performance."""
        # This would take into account user performance data to generate
        # challenges that target areas for improvement
        # For now, it falls back to template-based generation
        return self._generate_from_template(domain, level, parameters)
    
    def _generate_for_learning_path(
        self,
        domain: MathematicalDomain,
        level: ChallengeLevel,
        parameters: Dict[str, Any]
    ) -> Challenge:
        """Generate a challenge that fits into a learning path."""
        # This would generate challenges that build on previous challenges
        # to create a coherent learning path
        # For now, it falls back to template-based generation
        return self._generate_from_template(domain, level, parameters)
    
    def _fill_parameter(self, template_str: str, parameters: Dict[str, Any]) -> str:
        """Fill in a single parameter in a template string."""
        if not isinstance(template_str, str):
            return template_str
        
        # Simple template filling with {{parameter}}
        for param_name, param_value in parameters.items():
            template_str = template_str.replace(f"{{{{{param_name}}}}}", str(param_value))
        
        return template_str
    
    def _fill_template(self, template_str: str, parameters: Dict[str, Any]) -> str:
        """Fill in a template string with parameters."""
        if not isinstance(template_str, str):
            return template_str
        
        # Simple template filling with {{parameter}}
        for param_name, param_value in parameters.items():
            template_str = template_str.replace(f"{{{{{param_name}}}}}", str(param_value))
        
        # Handle expressions like {{number * 2}}
        import re
        expr_pattern = r"{{(.*?)}}"
        
        def eval_expr(match):
            expr = match.group(1)
            try:
                # Create a safe environment for evaluating expressions
                safe_dict = {k: v for k, v in parameters.items()}
                safe_dict.update({
                    "abs": abs, "max": max, "min": min, "round": round,
                    "int": int, "float": float, "str": str
                })
                return str(eval(expr, {"__builtins__": {}}, safe_dict))
            except Exception as e:
                return f"{{{{Error: {str(e)}}}}}"
        
        return re.sub(expr_pattern, eval_expr, template_str)
    
    def _generate_parameter_value(self, param_spec: Dict[str, Any]) -> Any:
        """Generate a parameter value based on its specification."""
        param_type = param_spec.get("type", "string")
        
        if param_type == "integer":
            min_val = param_spec.get("min", 1)
            max_val = param_spec.get("max", 1000)
            return random.randint(min_val, max_val)
        
        elif param_type == "float":
            min_val = param_spec.get("min", 0.0)
            max_val = param_spec.get("max", 1.0)
            return random.uniform(min_val, max_val)
        
        elif param_type == "string":
            options = param_spec.get("options", ["Default Value"])
            return random.choice(options)
        
        elif param_type == "boolean":
            return random.choice([True, False])
        
        elif param_type == "array":
            element_type = param_spec.get("element_type", "integer")
            min_length = param_spec.get("min_length", 1)
            max_length = param_spec.get("max_length", 10)
            length = random.randint(min_length, max_length)
            
            element_spec = {
                "type": element_type,
                "min": param_spec.get("min", 1),
                "max": param_spec.get("max", 100)
            }
            
            return [self._generate_parameter_value(element_spec) for _ in range(length)]
        
        return None
    
    def _generate_test_cases(
        self, 
        test_case_spec: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> List[TestCase]:
        """Generate test cases based on specification and parameters."""
        test_cases = []
        
        function_name = test_case_spec.get("function_name", "solution")
        
        for tc in test_case_spec.get("test_cases", []):
            # Fill in parameter values
            input_data = self._fill_parameter(tc.get("input", None), parameters)
            
            expected_output = tc.get("expected_output", None)
            if expected_output == "calculated":
                # In a real implementation, this would calculate the expected output
                # For now, we use a placeholder
                expected_output = "To be calculated"
            else:
                expected_output = self._fill_parameter(expected_output, parameters)
            
            test_cases.append(TestCase(
                input_data={"input": input_data, "function": function_name},
                expected_output=expected_output,
                description=tc.get("description", f"Test case for {input_data}")
            ))
        
        return test_cases


class ChallengeFactory:
    """Factory for creating challenges of various types."""
    
    def __init__(self, generator: ChallengeGenerator = None):
        """
        Initialize the challenge factory.
        
        Args:
            generator: Challenge generator to use
        """
        self.generator = generator or ChallengeGenerator()
    
    def create_number_theory_challenge(
        self,
        level: ChallengeLevel = ChallengeLevel.INTERMEDIATE,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Challenge:
        """Create a number theory challenge."""
        return self.generator.generate_challenge(
            domain=MathematicalDomain.NUMBER_THEORY,
            level=level,
            parameters=parameters
        )
    
    def create_linear_algebra_challenge(
        self,
        level: ChallengeLevel = ChallengeLevel.INTERMEDIATE,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Challenge:
        """Create a linear algebra challenge."""
        return self.generator.generate_challenge(
            domain=MathematicalDomain.LINEAR_ALGEBRA,
            level=level,
            parameters=parameters
        )
    
    def create_calculus_challenge(
        self,
        level: ChallengeLevel = ChallengeLevel.INTERMEDIATE,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Challenge:
        """Create a calculus challenge."""
        return self.generator.generate_challenge(
            domain=MathematicalDomain.CALCULUS,
            level=level,
            parameters=parameters
        )
    
    def create_optimization_challenge(
        self,
        level: ChallengeLevel = ChallengeLevel.INTERMEDIATE,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Challenge:
        """Create an optimization challenge."""
        return self.generator.generate_challenge(
            domain=MathematicalDomain.OPTIMIZATION_TECHNIQUES,
            level=level,
            parameters=parameters
        )
    
    def create_random_challenge(
        self,
        level: Optional[ChallengeLevel] = None,
        domain: Optional[MathematicalDomain] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Challenge:
        """Create a random challenge."""
        level = level or random.choice(list(ChallengeLevel))
        domain = domain or random.choice(list(MathematicalDomain))
        
        return self.generator.generate_challenge(
            domain=domain,
            level=level,
            parameters=parameters
        )