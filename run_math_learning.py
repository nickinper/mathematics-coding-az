#!/usr/bin/env python3
"""
Run the Mathematical Learning System
"""
import asyncio
import argparse
import json
from datetime import datetime

from src.learning.training.training_orchestrator import TrainingOrchestrator
from src.learning.curriculum.math_curriculum import MathematicalCurriculum
from src.learning.models.learning_agent import MathLearningAgent


async def main():
    parser = argparse.ArgumentParser(description="Mathematical Learning System for AI Agents")
    parser.add_argument("--agent", type=str, default="agent_001", help="Agent ID")
    parser.add_argument("--mode", choices=["train", "test", "benchmark", "report"], 
                      default="train", help="Operation mode")
    parser.add_argument("--concept", type=str, help="Specific concept to train on")
    parser.add_argument("--level", type=str, default="Intermediate", 
                      choices=["Beginner", "Intermediate", "Advanced", "Expert"],
                      help="Target training level")
    parser.add_argument("--problems", type=int, default=5, help="Number of problems per concept")
    parser.add_argument("--difficulty", type=str, default="1-3", 
                      help="Difficulty range (format: min-max)")
    parser.add_argument("--save_dir", type=str, default="training_data",
                      help="Directory to save training data")
    
    args = parser.parse_args()
    
    # Setup orchestrator
    orchestrator = TrainingOrchestrator(save_dir=args.save_dir)
    
    # Parse difficulty range
    difficulty_range = tuple(map(int, args.difficulty.split('-')))
    
    # Header
    print(f"\n{'='*60}")
    print(f"Mathematical Learning System")
    print(f"{'='*60}")
    print(f"Agent: {args.agent}")
    print(f"Mode: {args.mode}")
    print(f"Target Level: {args.level}")
    print(f"{'='*60}\n")
    
    # Create or load agent
    agent = orchestrator.load_agent(args.agent)
    if not agent:
        agent = orchestrator.create_agent(args.agent)
    
    # Execute requested operation
    if args.mode == "train":
        if args.concept:
            print(f"Training on specific concept: {args.concept}")
            results = await orchestrator.train_agent_on_concept(
                args.agent, 
                args.concept, 
                args.problems, 
                difficulty_range
            )
            print(f"\nTraining completed with success rate: {results['overall_success_rate']:.2%}")
        else:
            print(f"Progressive training to reach {args.level} level")
            results = await orchestrator.run_progressive_training(
                args.agent, 
                args.level
            )
            print(f"\nProgressive training completed.")
            print(f"Starting level: {results['concepts_trained'][0]['agent_level'] if results['concepts_trained'] else 'Beginner'}")
            print(f"Final level: {results['final_level']}")
            print(f"Total concepts trained: {len(results['concepts_trained'])}")
            print(f"Total problems solved: {results['total_problems']}")
    
    elif args.mode == "test":
        print("Diagnostic Assessment")
        
        # Default test concepts or use specific concept if provided
        test_concepts = [args.concept] if args.concept else ["arithmetic", "number_theory", "linear_algebra"]
        
        # Generate and run tests
        test_problems = orchestrator.problem_generator.generate_diagnostic_test(test_concepts)
        
        print(f"Testing agent on {len(test_problems)} problems across {len(test_concepts)} concepts")
        
        # Simulate benchmarking single agent
        results = await orchestrator.benchmark_agents([args.agent], test_concepts)
        
        # Display detailed results
        agent_result = results["agent_results"].get(args.agent, {})
        if agent_result:
            success_rate = agent_result["problems_solved"] / results["num_problems"]
            print(f"\nTest completed with success rate: {success_rate:.2%}")
            print(f"Total time: {agent_result['total_time']:.2f}s")
            
            print("\nConcept performance:")
            for concept, score in sorted(agent_result["concept_scores"].items(), key=lambda x: x[1], reverse=True):
                print(f"  {concept}: {score:.2%}")
    
    elif args.mode == "benchmark":
        print("Benchmark Mode - Compare Multiple Agents")
        
        # Create some additional agents for comparison if needed
        comparison_agents = [
            f"{args.agent}_v{i}" for i in range(1, 4)
        ]
        
        # Create agents if they don't exist
        for agent_id in comparison_agents:
            if agent_id not in orchestrator.agents:
                orchestrator.create_agent(agent_id)
        
        # Add main agent to list
        all_agents = [args.agent] + comparison_agents
        
        # Default benchmark concepts
        benchmark_concepts = ["arithmetic", "number_theory"]
        
        print(f"Benchmarking {len(all_agents)} agents on {len(benchmark_concepts)} concepts")
        await orchestrator.benchmark_agents(all_agents, benchmark_concepts)
    
    elif args.mode == "report":
        print("Analytics Report")
        
        # Generate comprehensive report
        report = orchestrator.generate_learning_analytics(args.agent)
        
        # Save report to file
        report_file = f"report_{args.agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Display key highlights
        print("\nKey Analytics Highlights:")
        print(f"Current Level: {report['current_state']['current_level']}")
        print(f"Mastered Concepts: {', '.join(report['current_state']['mastered_concepts'])}")
        
        # Check if learning trajectory data is available
        if 'learning_trajectory' in report and 'average_learning_velocity' in report['learning_trajectory']:
            print(f"Learning Velocity: {report['learning_trajectory']['average_learning_velocity']:.2f}")
        
        if report['strengths']:
            print("\nStrengths:")
            for strength in report['strengths'][:3]:  # Top 3 strengths
                print(f"- {strength}")
                
        if report['weaknesses']:
            print("\nAreas for Improvement:")
            for weakness in report['weaknesses'][:3]:  # Top 3 weaknesses
                print(f"- {weakness}")
        
        print(f"\nFull report saved to: {report_file}")
    
    print("\nMathematical Learning System completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())