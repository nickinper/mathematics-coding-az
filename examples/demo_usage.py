"""
Demo usage of the Mathematics-Based Coding AZ platform.

This script demonstrates how students would interact with the platform
and shows the key features of mathematical reasoning verification.
"""

import asyncio
import json
from src.challenges.level1.number_theory import RSAChallenge, ModularExponentiationChallenge
from src.core.failure_analysis import FailureAnalyzer
from src.assessment.scoring import ScoringEngine


def demo_modular_exponentiation_challenge():
    """Demonstrate the modular exponentiation challenge."""
    print("=" * 60)
    print("MATHEMATICS-BASED CODING AZ - DEMO")
    print("Challenge: Fast Modular Exponentiation")
    print("=" * 60)
    
    challenge = ModularExponentiationChallenge()
    
    print(f"Title: {challenge.title}")
    print(f"Level: {challenge.level.value}")
    print(f"Domain: {challenge.domain.value}")
    print(f"Time Limit: {challenge.time_limit} seconds")
    print()
    
    # Show mathematical requirements
    print("Mathematical Requirements:")
    for req in challenge.mathematical_requirements:
        print(f"  • {req.concept}: {req.description}")
        if req.proof_required:
            print("    [Proof Required]")
        if req.complexity_analysis:
            print("    [Complexity Analysis Required]")
    print()
    
    # Simulate student submissions with different quality levels
    submissions = [
        {
            "name": "Novice Student (Naive Implementation)",
            "code": '''
def mod_exp(base, exp, modulus):
    """Simple but inefficient implementation."""
    result = 1
    for i in range(exp):
        result = (result * base) % modulus
    return result
            ''',
            "reasoning": "I used a simple loop to multiply base exp times."
        },
        {
            "name": "Intermediate Student (Correct Algorithm, Poor Explanation)",
            "code": '''
def mod_exp(base, exp, modulus):
    result = 1
    base = base % modulus
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % modulus
        exp = exp >> 1
        base = (base * base) % modulus
    return result
            ''',
            "reasoning": "I used binary exponentiation because it's faster."
        },
        {
            "name": "Advanced Student (Complete Mathematical Understanding)",
            "code": '''
def mod_exp(base, exp, modulus):
    """
    Fast modular exponentiation using binary method.
    
    Mathematical Derivation:
    -----------------------
    We represent the exponent in binary: exp = Σ(b_i * 2^i)
    Then base^exp = base^(Σ(b_i * 2^i)) = Π(base^(b_i * 2^i))
    
    Since base^(2^i) = (base^(2^(i-1)))^2, we can compute
    successive powers by squaring.
    
    Time Complexity: O(log exp)
    Proof: We process each bit of exp exactly once, and exp has
    ⌊log₂(exp)⌋ + 1 bits, giving us O(log exp) operations.
    """
    result = 1
    base = base % modulus
    
    while exp > 0:
        # If current bit is 1, multiply by current base power
        if exp & 1:
            result = (result * base) % modulus
        
        # Square the base for next bit position
        base = (base * base) % modulus
        
        # Move to next bit
        exp >>= 1
    
    return result
            ''',
            "reasoning": '''
Mathematical Foundation:
The algorithm exploits the binary representation of the exponent.
For any integer exp, we can write: exp = b₀ + b₁×2¹ + b₂×2² + ... + bₖ×2ᵏ
where each bᵢ ∈ {0,1}.

Therefore: base^exp = base^(b₀ + b₁×2¹ + b₂×2² + ... + bₖ×2ᵏ)
                    = (base^b₀) × (base^(b₁×2¹)) × ... × (base^(bₖ×2ᵏ))

Key insight: base^(2ⁱ) = (base^(2^(i-1)))² 

This allows us to compute all needed powers by successive squaring,
examining one bit of the exponent at a time.

Complexity Analysis:
- Time: O(log exp) - we process log₂(exp) bits
- Space: O(1) - constant additional storage

Correctness Proof:
The invariant is that at iteration i, base = original_base^(2ⁱ) mod modulus
and result contains the product of all base^(2ʲ) where bit j of exp was 1.
            '''
        }
    ]
    
    # Evaluate each submission
    scoring_engine = ScoringEngine()
    failure_analyzer = FailureAnalyzer()
    
    for i, submission in enumerate(submissions):
        print(f"\\n{'='*40}")
        print(f"SUBMISSION {i+1}: {submission['name']}")
        print(f"{'='*40}")
        
        # Verify mathematical reasoning
        math_score, math_feedback = challenge.verify_mathematical_reasoning(
            submission['code'] + "\\n" + submission['reasoning']
        )
        
        # Check complexity
        complexity_ok, complexity_feedback = challenge.analyze_complexity(submission['code'])
        
        # Create mock test function
        namespace = {}
        try:
            exec(submission['code'], namespace)
            test_function = namespace.get('mod_exp')
            
            if test_function:
                # Run tests
                test_results = challenge.run_tests(test_function)
                passed_tests = sum(1 for _, passed, _ in test_results if passed)
                correctness_score = passed_tests / len(test_results)
            else:
                correctness_score = 0.0
                test_results = []
        except Exception as e:
            correctness_score = 0.0
            test_results = []
            print(f"Code execution failed: {e}")
        
        # Display results
        print(f"Correctness Score: {correctness_score:.2f}")
        print(f"Mathematical Reasoning Score: {math_score:.2f}")
        print(f"Complexity Requirement Met: {complexity_ok}")
        print()
        print("Feedback:")
        print(f"  Mathematical: {math_feedback}")
        print(f"  Complexity: {complexity_feedback}")
        
        # Overall assessment
        total_score = correctness_score * 0.4 + math_score * 0.6
        print(f"\\nTotal Score: {total_score:.2f}/1.00")
        
        if total_score >= 0.8:
            print("🏆 EXCELLENT - Deep mathematical understanding demonstrated!")
        elif total_score >= 0.6:
            print("✅ GOOD - Solid implementation with room for improvement")
        elif total_score >= 0.4:
            print("⚠️  NEEDS WORK - Basic understanding but missing key concepts")
        else:
            print("❌ INSUFFICIENT - Requires fundamental review")


def demo_failure_analysis():
    """Demonstrate the failure analysis and recovery system."""
    print("\\n" + "=" * 60)
    print("FAILURE ANALYSIS DEMO")
    print("=" * 60)
    
    # Simulate a failing submission
    failing_submission = '''
def mod_exp(base, exp, modulus):
    # I think this should work
    return pow(base, exp) % modulus
    '''
    
    failing_reasoning = "I used Python's built-in pow function."
    
    print("Failing Submission Analysis:")
    print("Code:", failing_submission)
    print("Reasoning:", failing_reasoning)
    
    challenge = ModularExponentiationChallenge()
    failure_analyzer = FailureAnalyzer()
    
    # Mock challenge result for failed submission
    from src.core.challenge import ChallengeResult
    
    mock_result = ChallengeResult(
        passed=False,
        test_results=[],
        mathematical_score=0.1,
        code_quality_score=0.3,
        innovation_score=0.0,
        total_score=0.15,
        feedback="Implementation lacks mathematical insight and efficiency requirements",
        errors=["Timeout on large inputs", "Missing complexity analysis"]
    )
    
    # Analyze failure
    failure_analysis = failure_analyzer.analyze_failure(
        failing_submission + failing_reasoning,
        mock_result,
        {
            'domain': challenge.domain.value,
            'level': challenge.level.value,
            'title': challenge.title
        },
        "demo_student",
        1  # First attempt
    )
    
    print("\\nFailure Analysis Results:")
    print(json.dumps(failure_analysis, indent=2))
    
    # Simulate progressive hint system
    print("\\n" + "-" * 40)
    print("PROGRESSIVE HINT SYSTEM")
    print("-" * 40)
    
    from src.core.failure_analysis import HintGenerator, FailureProfile, FailureType
    
    hint_generator = HintGenerator()
    
    # Create failure profile
    failure_profile = FailureProfile(
        failure_type=FailureType.COMPLEXITY_ERROR,
        mathematical_concept="Binary Exponentiation",
        specific_issue="Using built-in pow without understanding",
        severity=0.8,
        learning_opportunity="Understanding the mathematical basis of efficient exponentiation",
        suggested_approach="Derive the binary exponentiation algorithm from first principles"
    )
    
    # Generate hints for multiple attempts
    for attempt in range(1, 4):
        hints = hint_generator.generate_hints(failure_profile, attempt)
        print(f"\\nAttempt {attempt} Hints:")
        for j, hint in enumerate(hints, 1):
            print(f"  {j}. {hint}")


def demo_api_simulation():
    """Simulate API interactions."""
    print("\\n" + "=" * 60)
    print("API SIMULATION DEMO")
    print("=" * 60)
    
    # Simulate API calls (this would normally go through HTTP)
    print("Available Challenges:")
    challenges = [
        {"id": 1, "title": "Fast Modular Exponentiation", "level": "foundation"},
        {"id": 2, "title": "RSA Encryption from Scratch", "level": "foundation"},
    ]
    
    for challenge in challenges:
        print(f"  {challenge['id']}. {challenge['title']} ({challenge['level']})")
    
    print("\\nSubmitting solution to Challenge 1...")
    
    # Mock successful submission
    submission_response = {
        "id": 123,
        "challenge_id": 1,
        "passed": True,
        "total_score": 0.87,
        "feedback": {
            "mathematical_rigor": "Excellent derivation of binary exponentiation",
            "code_quality": "Clean, well-documented implementation",
            "innovation": "Creative optimization insights"
        },
        "attempt_number": 2
    }
    
    print("Submission Result:")
    print(json.dumps(submission_response, indent=2))


async def main():
    """Run the complete demo."""
    print("🧮 MATHEMATICS-BASED CODING ABSOLUTEZERO")
    print("   Where Mathematical Reasoning Meets Code")
    print()
    
    try:
        # Run demos
        demo_modular_exponentiation_challenge()
        demo_failure_analysis()
        demo_api_simulation()
        
        print("\\n" + "=" * 60)
        print("DEMO COMPLETE")
        print("=" * 60)
        print("Key Features Demonstrated:")
        print("✓ Mathematical reasoning verification")
        print("✓ Complexity analysis enforcement") 
        print("✓ Progressive hint system")
        print("✓ Failure pattern analysis")
        print("✓ Comprehensive scoring")
        print("✓ API integration ready")
        print()
        print("Next Steps:")
        print("• Run 'python -m src.platform.server' to start the web platform")
        print("• Visit http://localhost:8000 to access the API")
        print("• Check /docs for interactive API documentation")
        
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())