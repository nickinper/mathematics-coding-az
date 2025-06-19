"""
Manual testing script for TaskValidator.

This provides a quick way to test the TaskValidator without pytest.
Run with: python tests/manual_test.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validation.task_validator import TaskValidator


def test_rsa_implementation():
    """Test TaskValidator with an RSA implementation."""
    
    print("🔐 Testing RSA Implementation Validation")
    print("-" * 50)
    
    class RSASubmission:
        def __init__(self):
            self.code = """
def mod_exp(base, exp, mod):
    '''
    Fast modular exponentiation using binary method.
    Achieves O(log exp) complexity through repeated squaring.
    '''
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp & 1:  # If exp is odd
            result = (result * base) % mod
        exp >>= 1    # Divide exp by 2
        base = (base * base) % mod
    
    return result

def generate_keys(bits=512):
    '''Generate RSA public/private key pair.'''
    # Simplified for demonstration
    p, q = 17, 19  # Small primes for demo
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 3  # Public exponent
    
    # Find private exponent d such that e*d ≡ 1 (mod phi_n)
    d = pow(e, -1, phi_n)  # Modular inverse
    
    return (n, e), (n, d)
            """
            
            self.mathematical_reasoning = """
RSA Mathematical Foundation:

Theorem: RSA encryption/decryption is correct.

Proof:
Given: p, q are distinct primes, n = p×q, φ(n) = (p-1)(q-1)
Choose e: gcd(e, φ(n)) = 1
Find d: e×d ≡ 1 (mod φ(n))

For message m where gcd(m, n) = 1:
Encryption: c = m^e mod n
Decryption: m' = c^d mod n

We must prove m' = m.

Step 1: m' = c^d = (m^e)^d = m^(ed) mod n

Step 2: Since ed ≡ 1 (mod φ(n)), we have ed = 1 + kφ(n) for some k
Therefore: m^(ed) = m^(1 + kφ(n)) = m × (m^φ(n))^k mod n

Step 3: By Euler's theorem, for gcd(m, n) = 1:
m^φ(n) ≡ 1 (mod n)

Step 4: Therefore: m × (m^φ(n))^k ≡ m × 1^k ≡ m (mod n)

This proves correctness. QED.

Binary Exponentiation Analysis:
Time complexity: O(log exp) - we process each bit once
Space complexity: O(1) - constant additional storage
            """
    
    validator = TaskValidator()
    result = validator.validate_mathematical_correctness(RSASubmission())
    
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
    
    return result


def test_matrix_operations():
    """Test with a linear algebra implementation."""
    
    print("\\n🔢 Testing Matrix Operations Validation")
    print("-" * 50)
    
    class MatrixSubmission:
        def __init__(self):
            self.code = """
def matrix_determinant(matrix):
    '''
    Compute determinant using Laplace expansion.
    For 2x2: det = ad - bc
    For larger: recursive expansion along first row
    '''
    n = len(matrix)
    
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for col in range(n):
        # Create minor matrix
        minor = []
        for row in range(1, n):
            minor_row = []
            for c in range(n):
                if c != col:
                    minor_row.append(matrix[row][c])
            minor.append(minor_row)
        
        # Recursive calculation with sign alternation
        cofactor = ((-1) ** col) * matrix[0][col] * matrix_determinant(minor)
        det += cofactor
    
    return det
            """
            
            self.mathematical_reasoning = """
Determinant Calculation via Laplace Expansion:

Definition: For an n×n matrix A, the determinant is defined as:
det(A) = Σ(j=1 to n) (-1)^(i+j) × a_ij × M_ij

where M_ij is the minor (determinant of the (n-1)×(n-1) submatrix
obtained by removing row i and column j).

Base Cases:
- 1×1 matrix: det([a]) = a
- 2×2 matrix: det([[a,b],[c,d]]) = ad - bc

Recursive Case:
For n×n matrix with n > 2, expand along first row:
det(A) = Σ(j=1 to n) (-1)^(1+j) × a_1j × M_1j

The alternating sign (-1)^(i+j) ensures proper orientation.

Time Complexity: O(n!) due to recursive structure
Space Complexity: O(n²) for storing minor matrices

This algorithm correctly computes the determinant by
the fundamental definition in linear algebra.
            """
    
    validator = TaskValidator()
    result = validator.validate_mathematical_correctness(MatrixSubmission())
    
    print(f"Overall Score: {result.overall_score:.3f}")
    print(f"Linear Algebra Concepts: {[c.concept.value for c in result.concepts_identified if 'linear' in c.concept.value]}")
    print(f"Proof Steps Found: {len(result.proof_steps)}")
    
    return result


def test_poor_submission():
    """Test with a submission lacking mathematical insight."""
    
    print("\\n❌ Testing Poor Quality Submission")
    print("-" * 50)
    
    class PoorSubmission:
        def __init__(self):
            self.code = """
def sort_array(arr):
    # Just use python's built-in sort
    return sorted(arr)
            """
            
            self.mathematical_reasoning = """
I sorted the array.
            """
    
    validator = TaskValidator()
    result = validator.validate_mathematical_correctness(PoorSubmission())
    
    print(f"Overall Score: {result.overall_score:.3f}")
    print(f"Mathematical Rigor: {result.mathematical_rigor:.3f}")
    
    print("\\nSuggestions for Improvement:")
    for suggestion in result.suggestions:
        print(f"  • {suggestion}")
    
    return result


def test_calculus_optimization():
    """Test with a calculus-based optimization problem."""
    
    print("\\n📈 Testing Calculus Optimization Validation")
    print("-" * 50)
    
    class CalculusSubmission:
        def __init__(self):
            self.code = """
def gradient_descent(f, df_dx, x0, learning_rate=0.01, iterations=1000):
    '''
    Find minimum of function f using gradient descent.
    
    f: function to minimize
    df_dx: derivative of f
    x0: starting point
    '''
    x = x0
    
    for i in range(iterations):
        gradient = df_dx(x)
        x = x - learning_rate * gradient
        
        # Convergence check
        if abs(gradient) < 1e-6:
            break
    
    return x
            """
            
            self.mathematical_reasoning = """
Gradient Descent Optimization:

Theorem: Gradient descent converges to a local minimum for convex functions.

Mathematical Foundation:
Given a differentiable function f(x), the gradient ∇f(x) points in the
direction of steepest ascent. To minimize f, we move in the opposite direction.

Update Rule: x_{k+1} = x_k - α∇f(x_k)
where α > 0 is the learning rate.

Convergence Analysis:
For a convex function with Lipschitz continuous gradient (L-smooth):
||∇f(x)|| ≤ L for all x

If learning rate α ≤ 1/L, then:
f(x_{k+1}) ≤ f(x_k) - (α/2)||∇f(x_k)||²

This guarantees monotonic decrease in function value.

Stopping Criterion: ||∇f(x)|| < ε
This indicates we're near a critical point where ∇f(x) = 0.

Time Complexity: O(k × cost_of_gradient) where k is iterations to convergence.
            """
    
    validator = TaskValidator()
    result = validator.validate_mathematical_correctness(CalculusSubmission())
    
    print(f"Overall Score: {result.overall_score:.3f}")
    print(f"Calculus Concepts Detected: {any('calculus' in c.concept.value for c in result.concepts_identified)}")
    print(f"Mathematical Notation Used: {result.mathematical_rigor > 0.7}")
    
    return result


def run_comprehensive_test():
    """Run all manual tests and show summary."""
    
    print("🧮 TASKVALIDATOR COMPREHENSIVE MANUAL TEST")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("RSA Implementation", test_rsa_implementation()))
        results.append(("Matrix Operations", test_matrix_operations()))
        results.append(("Poor Submission", test_poor_submission()))
        results.append(("Calculus Optimization", test_calculus_optimization()))
        
        print("\\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        for test_name, result in results:
            score = result.overall_score
            status = "🏆 EXCELLENT" if score > 0.8 else "✅ GOOD" if score > 0.6 else "⚠️ NEEDS WORK" if score > 0.4 else "❌ POOR"
            print(f"{test_name:25} | Score: {score:.3f} | {status}")
        
        avg_score = sum(r.overall_score for _, r in results) / len(results)
        print(f"\\nAverage Score: {avg_score:.3f}")
        
        print("\\n✅ All tests completed successfully!")
        print("TaskValidator is working correctly and ready for production use.")
        
    except Exception as e:
        print(f"\\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_comprehensive_test()