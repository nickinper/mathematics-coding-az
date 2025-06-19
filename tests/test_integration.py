"""
Integration tests for TaskValidator with the platform API.

These tests ensure the TaskValidator properly integrates with the FastAPI endpoints.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from src.platform.server import create_app


@pytest.fixture
def client():
    """Create a test client for the API."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_submission_data():
    """Sample submission data for testing."""
    return {
        "challenge_id": 1,
        "code": """
def gcd(a, b):
    '''
    Compute greatest common divisor using Euclidean algorithm.
    Time complexity: O(log(min(a, b)))
    '''
    while b != 0:
        a, b = b, a % b
    return a
        """,
        "mathematical_reasoning": """
Mathematical Foundation:
The Euclidean algorithm is based on the principle that:
gcd(a, b) = gcd(b, a mod b)

Proof of correctness:
Let d = gcd(a, b). Then d divides both a and b.
Since a = qb + r where r = a mod b, we have:
r = a - qb

If d divides a and b, then d also divides r.
Therefore, any common divisor of a and b is also a common divisor of b and r.

Conversely, any common divisor of b and r divides a = qb + r.
Thus gcd(a, b) = gcd(b, r) = gcd(b, a mod b).

Termination: Since r < b at each step, the algorithm terminates when r = 0.
At this point, gcd(a, b) = b.
        """
    }


class TestAPIIntegration:
    """Test TaskValidator integration with API endpoints."""
    
    def test_health_check(self, client):
        """Test basic API health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_list_challenges(self, client):
        """Test challenge listing endpoint."""
        response = client.get("/api/challenges/")
        assert response.status_code == 200
        challenges = response.json()
        assert len(challenges) > 0
        assert "title" in challenges[0]
    
    def test_get_challenge_details(self, client):
        """Test challenge details endpoint."""
        response = client.get("/api/challenges/1/details")
        assert response.status_code == 200
        details = response.json()
        assert "mathematical_requirements" in details
        assert "time_limit" in details
    
    def test_submission_creation(self, client, sample_submission_data):
        """Test creating a submission."""
        response = client.post("/api/submissions/", json=sample_submission_data)
        assert response.status_code == 200
        
        submission = response.json()
        assert "id" in submission
        assert submission["challenge_id"] == 1
        assert submission["total_score"] >= 0.0
    
    def test_advanced_validation_endpoint(self, client, sample_submission_data):
        """Test the advanced validation endpoint."""
        # First create a submission
        response = client.post("/api/submissions/", json=sample_submission_data)
        assert response.status_code == 200
        submission_id = response.json()["id"]
        
        # Then validate it with TaskValidator
        response = client.post(f"/api/submissions/{submission_id}/validate-advanced")
        assert response.status_code == 200
        
        validation = response.json()
        assert "submission_id" in validation
        assert "validation_result" in validation
        
        result = validation["validation_result"]
        assert "overall_score" in result
        assert "scores" in result
        assert "concepts_identified" in result
        assert "proof_analysis" in result
        assert "feedback" in result
        assert "suggestions" in result
        
        # Check score structure
        scores = result["scores"]
        assert "mathematical_rigor" in scores
        assert "proof_correctness" in scores
        assert "code_elegance" in scores
        assert "concept_mastery" in scores
        
        # Scores should be between 0 and 1
        for score_name, score_value in scores.items():
            assert 0.0 <= score_value <= 1.0
    
    def test_validation_with_poor_submission(self, client):
        """Test validation with a low-quality submission."""
        poor_submission = {
            "challenge_id": 1,
            "code": "def bad(): return 42",
            "mathematical_reasoning": "no reasoning"
        }
        
        # Create submission
        response = client.post("/api/submissions/", json=poor_submission)
        assert response.status_code == 200
        submission_id = response.json()["id"]
        
        # Validate
        response = client.post(f"/api/submissions/{submission_id}/validate-advanced")
        assert response.status_code == 200
        
        result = response.json()["validation_result"]
        
        # Should have low scores
        assert result["overall_score"] < 0.5
        assert result["scores"]["mathematical_rigor"] < 0.3
        
        # Should have suggestions for improvement
        assert len(result["suggestions"]) > 0
    
    def test_validation_with_excellent_submission(self, client):
        """Test validation with a high-quality submission."""
        excellent_submission = {
            "challenge_id": 1,
            "code": """
def rsa_modular_exponentiation(base, exponent, modulus):
    '''
    Compute (base^exponent) mod modulus using binary exponentiation.
    
    Mathematical foundation: Uses the binary representation of the exponent
    to achieve O(log exponent) time complexity.
    '''
    result = 1
    base = base % modulus
    
    while exponent > 0:
        # If exponent is odd, multiply base with result
        if exponent % 2 == 1:
            result = (result * base) % modulus
        
        # Square the base and halve the exponent
        exponent = exponent >> 1
        base = (base * base) % modulus
    
    return result
            """,
            "mathematical_reasoning": """
Mathematical Derivation of Binary Exponentiation:

Theorem: For any integers base, exponent, and modulus > 0,
we can compute (base^exponent) mod modulus in O(log exponent) time.

Proof:
Any positive integer exponent can be written in binary as:
exponent = b₀ + b₁×2¹ + b₂×2² + ... + bₖ×2ᵏ where bᵢ ∈ {0,1}

Therefore:
base^exponent = base^(b₀ + b₁×2¹ + b₂×2² + ... + bₖ×2ᵏ)
              = (base^b₀) × (base^(b₁×2¹)) × ... × (base^(bₖ×2ᵏ))
              = (base^b₀) × (base²)^b₁ × ... × (base^(2ᵏ))^bₖ

Key insight: base^(2ⁱ) = (base^(2^(i-1)))²

This allows us to compute all needed powers by successive squaring,
examining one bit of the exponent at a time.

Complexity Analysis:
- Time: O(log exponent) since we process log₂(exponent) bits
- Space: O(1) constant additional storage

Correctness:
The algorithm maintains the invariant that result × base^exponent ≡ original_base^original_exponent (mod modulus)
throughout the loop, ensuring correctness upon termination.
            """
        }
        
        # Create submission
        response = client.post("/api/submissions/", json=excellent_submission)
        assert response.status_code == 200
        submission_id = response.json()["id"]
        
        # Validate
        response = client.post(f"/api/submissions/{submission_id}/validate-advanced")
        assert response.status_code == 200
        
        result = response.json()["validation_result"]
        
        # Should have high scores
        assert result["overall_score"] > 0.7
        assert result["scores"]["mathematical_rigor"] > 0.6
        assert result["scores"]["proof_correctness"] > 0.5
        
        # Should identify number theory concepts
        concepts = result["concepts_identified"]
        assert len(concepts) > 0
        assert any(c["concept"] == "number_theory" for c in concepts)
    
    def test_user_endpoints(self, client):
        """Test user-related endpoints."""
        # Get user profile
        response = client.get("/api/users/1")
        assert response.status_code == 200
        
        user = response.json()
        assert "username" in user
        assert "mathematics_score" in user
        
        # Get user progress
        response = client.get("/api/users/1/progress")
        assert response.status_code == 200
        
        progress = response.json()
        assert "total_submissions" in progress
        assert "challenges_attempted" in progress
    
    def test_submission_listing(self, client, sample_submission_data):
        """Test submission listing endpoint."""
        # Create a few submissions
        for i in range(3):
            response = client.post("/api/submissions/", json=sample_submission_data)
            assert response.status_code == 200
        
        # List submissions
        response = client.get("/api/submissions/")
        assert response.status_code == 200
        
        submissions = response.json()
        assert isinstance(submissions, list)
    
    def test_error_handling(self, client):
        """Test error handling in validation endpoints."""
        # Test with non-existent submission
        response = client.post("/api/submissions/99999/validate-advanced")
        assert response.status_code == 404
        
        # Test with invalid submission data
        invalid_submission = {
            "challenge_id": 999,  # Non-existent challenge
            "code": "def f(): pass",
            "mathematical_reasoning": "test"
        }
        
        response = client.post("/api/submissions/", json=invalid_submission)
        # Should handle gracefully (specific error depends on implementation)
        assert response.status_code in [200, 400, 404]


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v", "--tb=short"])