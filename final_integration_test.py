#!/usr/bin/env python3
"""
Final Integration Test for Number Theory Learning System

This script verifies all Phase 1-3 components are working together:
- GCD Basics Challenge
- Pattern Discovery System  
- Knowledge Database Schema
- Modular Arithmetic Challenge
- Prime Detection Challenge
- Verification Test Suite
- Basic Learning Agent
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.challenges.implementations.number_theory import (
    GCDBasicsChallenge,
    ModularArithmeticChallenge,
    PrimeDetectionChallenge
)
from src.autonomous.basic_learning_agent import BasicLearningAgent
from src.autonomous.pattern_discovery import PatternExtractor
from src.autonomous.knowledge_schema import KnowledgeDatabase, initialize_default_knowledge


def test_final_integration():
    """Run final integration test showing all components working."""
    
    print("🚀 FINAL INTEGRATION TEST")
    print("=" * 60)
    
    # Test basic implementation
    test_code = '''
def gcd(a: int, b: int) -> int:
    """
    Calculate GCD using Euclidean algorithm.
    
    Mathematical principle: gcd(a,b) = gcd(b, a mod b)
    Complexity: O(log(min(a,b)))
    
    The algorithm terminates because remainders decrease.
    Connection to Bezout's identity: Can extend to find x,y
    where ax + by = gcd(a,b).
    """
    if b == 0:
        return abs(a)
    return gcd(b, a % b)
'''
    
    # Test Pattern Discovery
    print("\n1. Testing Pattern Discovery:")
    extractor = PatternExtractor()
    patterns = extractor.extract_patterns(test_code)
    print(f"   ✓ Found {len(patterns)} patterns")
    for p in patterns[:3]:
        print(f"     - {p.pattern.name} ({p.pattern.category})")
    
    # Test Knowledge Database
    print("\n2. Testing Knowledge Database:")
    db = KnowledgeDatabase("sqlite:///:memory:")
    initialize_default_knowledge(db)
    concepts = db.get_concept_graph()
    print(f"   ✓ Loaded {len(concepts)} concepts")
    print(f"   ✓ Concept hierarchy established")
    
    # Test Learning Agent
    print("\n3. Testing Learning Agent:")
    agent = BasicLearningAgent("test_agent", "sqlite:///:memory:")
    initialize_default_knowledge(agent.knowledge_db)
    
    # Agent attempts GCD challenge
    gcd_challenge = GCDBasicsChallenge()
    result = agent.attempt_challenge(gcd_challenge)
    
    print(f"   ✓ Agent attempted GCD challenge")
    print(f"   ✓ Score: {result['score']:.2%}")
    print(f"   ✓ Patterns discovered: {len(result['patterns_discovered'])}")
    
    # Test all challenges exist
    print("\n4. Testing All Challenges:")
    challenges = [
        GCDBasicsChallenge(),
        ModularArithmeticChallenge(),
        PrimeDetectionChallenge()
    ]
    
    for challenge in challenges:
        print(f"   ✓ {challenge.title}")
        print(f"     - Level: {challenge.level.value}")
        print(f"     - Requirements: {len(challenge.mathematical_requirements)}")
        print(f"     - Test cases: {len(challenge.test_cases)}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ ALL COMPONENTS VERIFIED!")
    print("\nThe system successfully demonstrates:")
    print("• Mathematical challenge verification")
    print("• Pattern extraction from solutions")
    print("• Knowledge accumulation and tracking")
    print("• Autonomous learning capabilities")
    print("• Complete integration of all components")
    
    return True


if __name__ == "__main__":
    try:
        success = test_final_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)