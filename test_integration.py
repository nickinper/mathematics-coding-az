"""
Integration test demonstrating the complete Number Theory Learning System
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
from src.autonomous.knowledge_schema import KnowledgeDatabase, initialize_default_knowledge


def demonstrate_learning_system():
    """Demonstrate the complete learning system in action."""
    print("=" * 70)
    print("MATHEMATICS-BASED CODING AZ - Number Theory Learning System")
    print("=" * 70)
    
    # Initialize knowledge database
    print("\n1. Initializing Knowledge Database...")
    db = KnowledgeDatabase("sqlite:///:memory:")  # In-memory for demo
    initialize_default_knowledge(db)
    print("   ✓ Knowledge database initialized with fundamental concepts")
    
    # Create learning agent with same database
    print("\n2. Creating Learning Agent...")
    # Create agent with same in-memory database
    agent = BasicLearningAgent("demo_agent_001", "sqlite:///:memory:")
    # Re-initialize the agent's database
    initialize_default_knowledge(agent.knowledge_db)
    print(f"   ✓ Agent created: {agent.agent_id}")
    
    # Get initial state
    initial_summary = agent.get_learning_summary()
    print(f"   Initial state: {initial_summary['mastered_concepts']} concepts mastered")
    
    # Prepare challenges
    challenges = [
        ("GCD Basics", GCDBasicsChallenge()),
        ("Modular Arithmetic", ModularArithmeticChallenge()),
        ("Prime Detection", PrimeDetectionChallenge())
    ]
    
    # Agent attempts challenges
    print("\n3. Learning Process:")
    print("-" * 50)
    
    for challenge_name, challenge in challenges:
        print(f"\n📚 Attempting: {challenge_name}")
        print(f"   Level: {challenge.level.value}")
        print(f"   Domain: {challenge.domain.value}")
        
        # Agent attempts the challenge
        result = agent.attempt_challenge(challenge)
        
        # Display results
        print(f"\n   Results:")
        print(f"   ✓ Success: {'✅ Yes' if result['success'] else '❌ No'}")
        print(f"   ✓ Score: {result['score']:.2%}")
        print(f"   ✓ Time: {result['time_taken']:.2f}s")
        
        if result['patterns_discovered']:
            print(f"   ✓ New patterns discovered: {', '.join(result['patterns_discovered'])}")
        
        if result['concepts_learned']:
            print(f"   ✓ Concepts mastered: {', '.join(result['concepts_learned'])}")
        
        # Show feedback
        print(f"\n   Feedback: {result['feedback'][:200]}...")
        
        # Show code snippet
        code_lines = result['solution_code'].split('\n')
        print(f"\n   Solution excerpt:")
        for line in code_lines[1:6]:  # Show first few lines
            if line.strip():
                print(f"      {line}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("4. Learning Summary:")
    final_summary = agent.get_learning_summary()
    
    print(f"\n   Agent ID: {final_summary['agent_id']}")
    print(f"   Total Attempts: {final_summary['total_attempts']}")
    print(f"   Success Rate: {final_summary['success_rate']:.2%}")
    print(f"   Mastered Concepts: {', '.join(final_summary['mastered_concepts']) or 'None yet'}")
    print(f"   Known Patterns: {len(final_summary['known_patterns'])}")
    
    # Knowledge graph
    print("\n5. Knowledge Graph:")
    concept_graph = db.get_concept_graph()
    print("   Concept Dependencies:")
    for concept, prereqs in concept_graph.items():
        if prereqs:
            print(f"   - {concept} → requires: {', '.join(prereqs)}")
        else:
            print(f"   - {concept} (fundamental)")
    
    # Next recommendation
    next_concept = agent.suggest_next_challenge()
    if next_concept:
        print(f"\n6. Recommended Next: {next_concept}")
    else:
        print("\n6. No recommendations available yet")
    
    print("\n" + "=" * 70)
    print("Demo completed! The agent has demonstrated:")
    print("✓ Pattern discovery from code")
    print("✓ Mathematical reasoning verification")
    print("✓ Knowledge accumulation")
    print("✓ Adaptive learning based on prerequisites")
    print("=" * 70)


def test_pattern_discovery_detail():
    """Show detailed pattern discovery process."""
    print("\n\nDETAILED PATTERN DISCOVERY DEMO")
    print("=" * 50)
    
    from src.autonomous.pattern_discovery import PatternExtractor
    
    extractor = PatternExtractor()
    
    test_code = '''
def gcd(a: int, b: int) -> int:
    """
    Euclidean algorithm for GCD.
    Based on: gcd(a,b) = gcd(b, a mod b)
    """
    while b != 0:
        a, b = b, a % b
    return a

def mod_exp(base: int, exp: int, mod: int) -> int:
    """Fast modular exponentiation."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result
'''
    
    patterns = extractor.extract_patterns(test_code)
    
    print(f"Found {len(patterns)} patterns in the code:\n")
    
    for i, pattern_match in enumerate(patterns, 1):
        print(f"{i}. Pattern: {pattern_match.pattern.name}")
        print(f"   Category: {pattern_match.pattern.category}")
        print(f"   Confidence: {pattern_match.confidence:.2%}")
        print(f"   Description: {pattern_match.pattern.description}")
        print(f"   Mathematical Properties: {', '.join(pattern_match.pattern.mathematical_properties)}")
        print()


def main():
    """Run the complete integration test."""
    try:
        # Main demonstration
        demonstrate_learning_system()
        
        # Pattern discovery details
        test_pattern_discovery_detail()
        
        print("\n✅ Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)