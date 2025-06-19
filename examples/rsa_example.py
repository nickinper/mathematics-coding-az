"""
Example RSA implementation for the Mathematics-Based Coding AZ platform.

This serves as a reference implementation showing how to integrate
mathematical reasoning with code implementation.
"""

import random
import math
from typing import Tuple


class RSA:
    """
    RSA encryption implementation with mathematical reasoning.
    
    Mathematical Foundation:
    ------------------------
    RSA security relies on the computational difficulty of factoring large integers.
    The algorithm is based on Euler's theorem and Fermat's Little Theorem.
    
    Key Generation:
    1. Choose two large prime numbers p and q
    2. Compute n = p * q (public modulus)
    3. Compute φ(n) = (p-1)(q-1) (Euler's totient function)
    4. Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
    5. Compute d such that d * e ≡ 1 (mod φ(n))
    
    Encryption: c = m^e mod n
    Decryption: m = c^d mod n
    
    Mathematical Proof of Correctness:
    ----------------------------------
    We need to prove that (m^e)^d ≡ m (mod n) for any message m.
    
    By construction: d * e ≡ 1 (mod φ(n))
    Therefore: d * e = 1 + k * φ(n) for some integer k
    
    So: (m^e)^d = m^(de) = m^(1 + k*φ(n)) = m * (m^φ(n))^k
    
    By Euler's theorem: if gcd(m, n) = 1, then m^φ(n) ≡ 1 (mod n)
    Therefore: m * (m^φ(n))^k ≡ m * 1^k ≡ m (mod n)
    
    This proves RSA decryption works correctly.
    """
    
    def __init__(self):
        self.phi = 0  # Store φ(n) for verification
    
    def miller_rabin_primality_test(self, n: int, k: int = 5) -> bool:
        """
        Miller-Rabin probabilistic primality test.
        
        Mathematical Basis:
        ------------------
        If n is prime, then for any a: either a^d ≡ 1 (mod n)
        or a^(d*2^r) ≡ -1 (mod n) for some r ∈ [0, s-1]
        where n-1 = d * 2^s with d odd.
        
        The test finds witnesses to compositeness.
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Write n-1 as d * 2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        
        # Perform k rounds of testing
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = self.mod_exp(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(s - 1):
                x = self.mod_exp(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False  # Composite
        
        return True  # Probably prime
    
    def mod_exp(self, base: int, exp: int, modulus: int) -> int:
        """
        Fast modular exponentiation using binary method.
        
        Mathematical Derivation:
        -----------------------
        To compute base^exp mod modulus efficiently, we use the
        binary representation of the exponent.
        
        If exp = b_k * 2^k + b_{k-1} * 2^{k-1} + ... + b_1 * 2 + b_0
        then base^exp = base^(b_k * 2^k) * ... * base^(b_1 * 2) * base^b_0
        
        We can compute this by repeatedly squaring the base and
        multiplying by the result when the corresponding bit is 1.
        
        Time Complexity: O(log exp)
        Proof: The algorithm performs at most log₂(exp) iterations,
        each involving constant-time modular arithmetic operations.
        """
        result = 1
        base = base % modulus
        
        while exp > 0:
            # If exp is odd, multiply base with result
            if exp % 2 == 1:
                result = (result * base) % modulus
            
            # Square the base and halve the exponent
            base = (base * base) % modulus
            exp //= 2
        
        return result
    
    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm.
        
        Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    def mod_inverse(self, a: int, m: int) -> int:
        """
        Compute modular multiplicative inverse of a modulo m.
        
        Mathematical Requirement:
        ------------------------
        We need to find x such that a*x ≡ 1 (mod m)
        This exists if and only if gcd(a, m) = 1
        """
        gcd, x, _ = self.extended_gcd(a, m)
        
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        
        return (x % m + m) % m
    
    def generate_prime(self, bits: int) -> int:
        """
        Generate a prime number with specified bit length.
        
        Mathematical Note:
        -----------------
        By the Prime Number Theorem, the density of primes near n
        is approximately 1/ln(n). For cryptographic purposes,
        we need primes with sufficient bit length for security.
        """
        while True:
            # Generate random odd number with specified bit length
            candidate = random.getrandbits(bits)
            candidate |= (1 << bits - 1) | 1  # Ensure MSB and LSB are set
            
            if self.miller_rabin_primality_test(candidate):
                return candidate
    
    def generate_keys(self, bits: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generate RSA key pair.
        
        Returns:
        -------
        ((n, e), (n, d)) where (n, e) is public key and (n, d) is private key
        
        Mathematical Requirements:
        -------------------------
        1. p and q must be large primes
        2. e must be coprime to φ(n) = (p-1)(q-1)
        3. d must satisfy d*e ≡ 1 (mod φ(n))
        """
        # Generate two distinct primes
        p = self.generate_prime(bits // 2)
        q = self.generate_prime(bits // 2)
        
        # Ensure p ≠ q
        while p == q:
            q = self.generate_prime(bits // 2)
        
        # Compute public modulus
        n = p * q
        
        # Compute Euler's totient function
        self.phi = (p - 1) * (q - 1)
        
        # Choose public exponent e
        # Common choice: e = 65537 (Fermat number F4 = 2^16 + 1)
        e = 65537
        
        # Ensure gcd(e, φ(n)) = 1
        while math.gcd(e, self.phi) != 1:
            e += 2  # Keep e odd
        
        # Compute private exponent d
        d = self.mod_inverse(e, self.phi)
        
        return (n, e), (n, d)
    
    def encrypt(self, message: str, public_key: Tuple[int, int]) -> list:
        """
        Encrypt message using RSA public key.
        
        Mathematical Operation: c = m^e mod n
        """
        n, e = public_key
        
        # Convert message to integers (simple ASCII encoding)
        encrypted = []
        for char in message:
            m = ord(char)
            if m >= n:
                raise ValueError("Message too large for key size")
            
            c = self.mod_exp(m, e, n)
            encrypted.append(c)
        
        return encrypted
    
    def decrypt(self, ciphertext: list, private_key: Tuple[int, int]) -> str:
        """
        Decrypt ciphertext using RSA private key.
        
        Mathematical Operation: m = c^d mod n
        
        Correctness Proof:
        -----------------
        We have shown above that (m^e)^d ≡ m (mod n)
        by Euler's theorem and the construction of d.
        """
        n, d = private_key
        
        # Decrypt each ciphertext integer
        decrypted = []
        for c in ciphertext:
            m = self.mod_exp(c, d, n)
            decrypted.append(chr(m))
        
        return ''.join(decrypted)


def demonstrate_rsa():
    """Demonstrate RSA encryption with mathematical verification."""
    print("RSA Encryption Demonstration")
    print("=" * 50)
    
    rsa = RSA()
    
    # Generate keys
    print("Generating RSA keys...")
    public_key, private_key = rsa.generate_keys(bits=512)  # Small for demo
    
    n, e = public_key
    _, d = private_key
    
    print(f"Public key (n, e): ({n}, {e})")
    print(f"Private key (n, d): ({n}, {d})")
    
    # Verify mathematical property: e*d ≡ 1 (mod φ(n))
    print(f"\\nMathematical Verification:")
    print(f"φ(n) = {rsa.phi}")
    print(f"e*d mod φ(n) = {(e * d) % rsa.phi}")
    print(f"✓ e*d ≡ 1 (mod φ(n)): {(e * d) % rsa.phi == 1}")
    
    # Encrypt and decrypt message
    message = "HELLO"
    print(f"\\nOriginal message: {message}")
    
    ciphertext = rsa.encrypt(message, public_key)
    print(f"Encrypted: {ciphertext}")
    
    decrypted = rsa.decrypt(ciphertext, private_key)
    print(f"Decrypted: {decrypted}")
    
    print(f"✓ Decryption successful: {message == decrypted}")


if __name__ == "__main__":
    demonstrate_rsa()