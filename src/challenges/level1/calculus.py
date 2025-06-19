"""Calculus challenges focusing on neural network implementation."""

import re
import math
from typing import Any, Tuple, List
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class NeuralNetworkChallenge(Challenge):
    """Neural network implementation challenge requiring calculus understanding."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Partial Derivatives",
                description="Derive and implement partial derivatives for gradient descent",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Chain Rule",
                description="Apply the chain rule for backpropagation",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Activation Functions",
                description="Implement and analyze different activation functions",
                proof_required=False
            ),
            MathematicalRequirement(
                concept="Gradient Descent",
                description="Implement gradient descent optimization algorithm",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Neural Network from First Principles",
            description="""
Implement a simple neural network from calculus first principles.

Your implementation must include:
1. A simple feedforward neural network with at least one hidden layer
2. Backpropagation algorithm derived from calculus principles
3. At least two activation functions (sigmoid, ReLU, tanh)
4. Gradient descent optimization algorithm

Mathematical Proof Requirements:
- Derive the gradient descent update rule from calculus principles
- Apply the chain rule to derive the backpropagation algorithm
- Analyze activation functions and their derivatives
- Analyze convergence properties of gradient descent

Example Usage:
```python
# Create a simple neural network
model = NeuralNetwork([2, 3, 1])  # 2 inputs, 3 hidden neurons, 1 output

# Train the model
model.train(X_train, y_train, learning_rate=0.01, epochs=1000)

# Make predictions
predictions = model.predict(X_test)
```
            """,
            level=ChallengeLevel.FOUNDATION,
            domain=MathematicalDomain.CALCULUS,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=900.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for neural network implementation."""
        test_cases = []
        
        # XOR problem - classic test case for neural networks
        test_cases.append(TestCase(
            input_data={
                "operation": "train_xor",
                "hidden_size": 4,
                "learning_rate": 0.1,
                "epochs": 5000
            },
            expected_output={
                "accuracy": 1.0,
                "loss": lambda x: x < 0.1  # Loss should be less than 0.1
            },
            description="Train on XOR problem",
            timeout=10.0  # Allow more time for training
        ))
        
        # Activation function test
        test_cases.append(TestCase(
            input_data={
                "operation": "activation",
                "function": "sigmoid",
                "values": [-2.0, -1.0, 0.0, 1.0, 2.0]
            },
            expected_output=[
                1/(1+math.exp(2)), 1/(1+math.exp(1)), 0.5, 
                1/(1+math.exp(-1)), 1/(1+math.exp(-2))
            ],
            description="Sigmoid activation function"
        ))
        
        # Gradient descent test
        test_cases.append(TestCase(
            input_data={
                "operation": "gradient_descent",
                "function": "x^2",  # Simple parabola
                "start": 10.0,
                "learning_rate": 0.1,
                "steps": 50
            },
            expected_output=lambda x: abs(x) < 0.1,  # Should be close to minimum at x=0
            description="Gradient descent optimization"
        ))
        
        # Backpropagation test
        test_cases.append(TestCase(
            input_data={
                "operation": "backpropagation",
                "network": {
                    "layers": [2, 2, 1],
                    "weights": [[[0.15, 0.20], [0.25, 0.30]], [[0.40, 0.45]]]
                },
                "input": [0.05, 0.10],
                "target": [0.01]
            },
            expected_output={
                "output": lambda x: abs(x[0] - 0.75) < 0.05,  # Expected output ~0.75
                "gradients_exist": True
            },
            description="Backpropagation algorithm"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in neural network implementation."""
        score = 0.0
        feedback_parts = []
        
        # Check for gradient descent derivation
        if self._contains_gradient_descent_derivation(submission):
            score += 0.25
            feedback_parts.append("✓ Gradient descent derivation found")
        else:
            feedback_parts.append("✗ Missing derivation of gradient descent")
        
        # Check for backpropagation derivation
        if self._contains_backprop_derivation(submission):
            score += 0.25
            feedback_parts.append("✓ Backpropagation derivation with chain rule found")
        else:
            feedback_parts.append("✗ Missing chain rule application in backpropagation")
        
        # Check for activation function analysis
        if self._contains_activation_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Activation function analysis present")
        else:
            feedback_parts.append("✗ Missing analysis of activation functions and derivatives")
        
        # Check for convergence analysis
        if self._contains_convergence_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Convergence analysis for gradient descent found")
        else:
            feedback_parts.append("✗ Missing convergence analysis for gradient descent")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient neural network implementation
        if self._has_efficient_neural_network(submission):
            return True, "Efficient neural network implementation detected"
        else:
            return False, "Neural network forward and backward pass should be O(n²) for layer size n"
    
    def _contains_gradient_descent_derivation(self, text: str) -> bool:
        """Check if submission contains derivation of gradient descent."""
        patterns = [
            r'gradient.*descent.*derivative',
            r'minimize.*function.*derivative',
            r'partial.*derivative.*weight',
            r'∂[Ee]/∂[Ww]'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_backprop_derivation(self, text: str) -> bool:
        """Check if submission contains backpropagation derivation with chain rule."""
        patterns = [
            r'chain.*rule.*backpropagation',
            r'∂[Ee]/∂[Ww].*chain.*rule',
            r'backpropagation.*calculus',
            r'∂[Ee]/∂[Oo].*∂[Oo]/∂[Nn].*∂[Nn]/∂[Ww]'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_activation_analysis(self, text: str) -> bool:
        """Check if submission analyzes activation functions."""
        activation_functions = [
            r'sigmoid.*derivative',
            r'tanh.*derivative',
            r'relu.*derivative',
            r'activation.*function.*derivative',
            r'non-linear.*activation'
        ]
        return any(re.search(pattern, text.lower()) for pattern in activation_functions)
    
    def _contains_convergence_analysis(self, text: str) -> bool:
        """Check if submission analyzes convergence of gradient descent."""
        patterns = [
            r'convergence.*gradient.*descent',
            r'learning.*rate.*convergence',
            r'local.*minimum',
            r'convex.*function',
            r'convergence.*rate'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_neural_network(self, code: str) -> bool:
        """Check for efficient neural network implementation."""
        # Signs of vectorized implementation
        efficient_patterns = [
            r'matrix.*multiplication',
            r'numpy|np\.',
            r'vectorized',
            r'dot.*product'
        ]
        return any(re.search(pattern, code.lower()) for pattern in efficient_patterns)