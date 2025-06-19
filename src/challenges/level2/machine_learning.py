"""Machine learning challenges focusing on recommendation systems."""

import re
import numpy as np
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class RecommendationSystemChallenge(Challenge):
    """Recommendation system challenge requiring linear algebra and statistics."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Matrix Factorization",
                description="Implement SVD-based collaborative filtering",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Cosine Similarity",
                description="Derive and implement cosine similarity for item-based recommendations",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Gradient Descent",
                description="Implement gradient descent for matrix factorization",
                complexity_analysis=True
            ),
            MathematicalRequirement(
                concept="Evaluation Metrics",
                description="Implement and analyze RMSE, precision, and recall metrics",
                proof_required=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Collaborative Filtering Recommendation System",
            description="""
Implement a mathematical recommendation system using collaborative filtering techniques.

Your implementation must include:
1. A matrix factorization approach using Singular Value Decomposition (SVD)
2. An item-based collaborative filtering using cosine similarity
3. A gradient descent optimization for matrix factorization
4. Proper evaluation metrics (RMSE, precision, recall)

Mathematical Proof Requirements:
- Derive the SVD factorization for collaborative filtering
- Prove that cosine similarity is a valid similarity metric
- Derive the gradient descent update rules for minimizing prediction error
- Analyze the mathematical relationship between precision and recall

Example Usage:
```python
# Create recommendation system
recommender = CollaborativeFilteringRecommender()

# Train on user-item rating matrix
ratings = [
    [5, 3, 0, 1],  # User 1 ratings for items 1-4
    [4, 0, 0, 1],  # User 2 ratings for items 1-4
    [1, 1, 0, 5],  # User 3 ratings for items 1-4
    [1, 0, 0, 4],  # User 4 ratings for items 1-4
    [0, 1, 5, 4],  # User 5 ratings for items 1-4
]
recommender.train(ratings)

# Get top recommendations for a user
user_id = 0
recommendations = recommender.recommend(user_id, top_n=3)

# Calculate evaluation metrics
rmse = recommender.evaluate(test_data, metric="rmse")
precision = recommender.evaluate(test_data, metric="precision@5")
```
            """,
            level=ChallengeLevel.INTERMEDIATE,
            domain=MathematicalDomain.LINEAR_ALGEBRA,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=900.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for recommendation system implementations."""
        test_cases = []
        
        # Small user-item matrix for testing
        ratings = np.array([
            [5, 3, 0, 1],
            [4, 0, 0, 1],
            [1, 1, 0, 5],
            [1, 0, 0, 4],
            [0, 1, 5, 4],
        ])
        
        # Test case for SVD factorization
        test_cases.append(TestCase(
            input_data={
                "method": "svd",
                "ratings": ratings.tolist(),
                "k": 2  # Number of latent factors
            },
            expected_output={
                "reconstruction_error": lambda x: x < 2.0,  # RMSE should be less than 2.0
                "factors_shape_correct": True
            },
            description="SVD-based collaborative filtering"
        ))
        
        # Test case for cosine similarity
        test_cases.append(TestCase(
            input_data={
                "method": "item_similarity",
                "ratings": ratings.tolist(),
                "target_user": 0,
                "target_item": 2
            },
            expected_output={
                "prediction": lambda x: 0 <= x <= 5,  # Should be a valid rating
                "similarity_matrix_valid": True
            },
            description="Item-based collaborative filtering"
        ))
        
        # Test case for gradient descent
        test_cases.append(TestCase(
            input_data={
                "method": "sgd",
                "ratings": ratings.tolist(),
                "factors": 3,
                "iterations": 100,
                "learning_rate": 0.01,
                "regularization": 0.1
            },
            expected_output={
                "final_error": lambda x: x < 1.5,  # Final RMSE should be less than 1.5
                "converged": True
            },
            description="Gradient descent matrix factorization",
            timeout=5.0
        ))
        
        # Test case for recommendation quality
        test_cases.append(TestCase(
            input_data={
                "method": "recommend",
                "ratings": ratings.tolist(),
                "user_id": 0,
                "top_n": 2
            },
            expected_output={
                "recommendations": lambda x: len(x) == 2 and all(isinstance(item, (int, float)) for item in x),
                "contains_unrated_items": True
            },
            description="Top-N recommendations"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in recommendation system solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for SVD explanation
        if self._contains_svd_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ SVD factorization for collaborative filtering explained")
        else:
            feedback_parts.append("✗ Missing explanation of SVD factorization")
        
        # Check for cosine similarity derivation
        if self._contains_cosine_similarity_derivation(submission):
            score += 0.25
            feedback_parts.append("✓ Cosine similarity metric properly derived")
        else:
            feedback_parts.append("✗ Missing derivation of cosine similarity")
        
        # Check for gradient descent derivation
        if self._contains_gradient_descent_derivation(submission):
            score += 0.25
            feedback_parts.append("✓ Gradient descent update rules derived")
        else:
            feedback_parts.append("✗ Missing derivation of gradient descent update rules")
        
        # Check for evaluation metrics analysis
        if self._contains_evaluation_metrics_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Evaluation metrics mathematically analyzed")
        else:
            feedback_parts.append("✗ Missing analysis of evaluation metrics")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_svd(submission) and 
            self._has_efficient_similarity_calculation(submission)):
            return True, "Efficient algorithms for SVD and similarity calculations detected"
        elif self._has_efficient_svd(submission):
            return False, "SVD implementation is efficient, but similarity calculations need improvement"
        elif self._has_efficient_similarity_calculation(submission):
            return False, "Similarity calculations are efficient, but SVD implementation needs improvement"
        else:
            return False, "Both SVD and similarity calculations need efficiency improvements"
    
    def _contains_svd_explanation(self, text: str) -> bool:
        """Check if submission explains SVD for collaborative filtering."""
        patterns = [
            r'singular\s+value\s+decomposition',
            r'U.*Sigma.*V',
            r'low-rank\s+approximation',
            r'latent\s+factor',
            r'dimensionality\s+reduction'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_cosine_similarity_derivation(self, text: str) -> bool:
        """Check if submission derives cosine similarity."""
        patterns = [
            r'cosine\s+similarity',
            r'dot\s+product.*magnitude',
            r'angle\s+between\s+vectors',
            r'normalized\s+dot\s+product',
            r'A \cdot B / \|A\| \|B\|'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_gradient_descent_derivation(self, text: str) -> bool:
        """Check if submission derives gradient descent for matrix factorization."""
        patterns = [
            r'gradient\s+descent.*update',
            r'partial\s+derivative',
            r'loss\s+function',
            r'squared\s+error',
            r'regularization'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_evaluation_metrics_analysis(self, text: str) -> bool:
        """Check if submission analyzes evaluation metrics."""
        patterns = [
            r'root\s+mean\s+squared\s+error|rmse',
            r'precision.*recall',
            r'true\s+positive',
            r'false\s+positive',
            r'receiver\s+operating\s+characteristic|ROC'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_svd(self, code: str) -> bool:
        """Check for efficient SVD implementation."""
        patterns = [
            r'numpy\.linalg\.svd',
            r'scipy\.sparse\.linalg',
            r'randomized.*svd',
            r'truncated.*svd',
            r'sklearn'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_efficient_similarity_calculation(self, code: str) -> bool:
        """Check for efficient similarity calculation."""
        patterns = [
            r'numpy\.dot',
            r'vectorized',
            r'precompute.*similarity',
            r'sklearn\.metrics\.pairwise',
            r'scipy\.spatial\.distance'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)