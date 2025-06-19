"""
Orchestrate the training of AI agents on mathematical concepts
"""
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import os

from src.learning.curriculum.math_curriculum import MathematicalCurriculum
from src.learning.curriculum.problem_generator import MathProblemGenerator
from src.learning.models.learning_agent import MathLearningAgent


class TrainingOrchestrator:
    """Orchestrate training of multiple AI agents"""
    
    def __init__(self, save_dir: str = "training_data"):
        self.curriculum = MathematicalCurriculum()
        self.problem_generator = MathProblemGenerator()
        self.agents: Dict[str, MathLearningAgent] = {}
        self.save_dir = save_dir
        self.training_sessions = []
        
        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
    
    def create_agent(self, agent_id: str, initial_knowledge: Optional[Dict] = None) -> MathLearningAgent:
        """Create a new learning agent"""
        agent = MathLearningAgent(agent_id, initial_knowledge)
        agent.curriculum = self.curriculum
        agent.problem_generator = self.problem_generator
        
        self.agents[agent_id] = agent
        print(f"Created agent: {agent_id}")
        
        return agent
    
    def load_agent(self, agent_id: str) -> Optional[MathLearningAgent]:
        """Load agent from saved state"""
        save_path = os.path.join(self.save_dir, f"agent_{agent_id}.json")
        
        if os.path.exists(save_path):
            with open(save_path, 'r') as f:
                saved_state = json.load(f)
            
            agent = self.create_agent(agent_id, saved_state)
            print(f"Loaded agent: {agent_id} with {len(agent.state.mastered_concepts)} mastered concepts")
            return agent
        
        print(f"No saved state found for agent: {agent_id}")
        return None
    
    def save_agent(self, agent_id: str):
        """Save agent state"""
        if agent_id not in self.agents:
            print(f"Agent {agent_id} not found")
            return
        
        agent = self.agents[agent_id]
        save_path = os.path.join(self.save_dir, f"agent_{agent_id}.json")
        
        with open(save_path, 'w') as f:
            json.dump(agent.state.to_dict(), f, indent=2)
        
        print(f"Saved agent: {agent_id}")
    
    async def train_agent_on_concept(self, agent_id: str, concept: str, 
                                   num_problems: int = 5, difficulty_range: tuple = (1, 3)) -> Dict:
        """Train an agent on a specific concept"""
        if agent_id not in self.agents:
            print(f"Agent {agent_id} not found")
            return {}
        
        agent = self.agents[agent_id]
        print(f"\n=== Training {agent_id} on {concept} ===")
        
        # Generate problems
        problems = self.problem_generator.generate_problem_set(
            concept, num_problems, difficulty_range
        )
        
        training_results = {
            "agent_id": agent_id,
            "concept": concept,
            "start_time": datetime.now().isoformat(),
            "problems_attempted": [],
            "overall_success_rate": 0,
            "concept_mastered": False
        }
        
        # Train on each problem
        for i, problem in enumerate(problems):
            print(f"\nProblem {i+1}/{num_problems}: {problem.problem_statement[:100]}...")
            
            # Attempt problem
            result = agent.attempt_problem(problem)
            
            # Display results
            self._display_attempt_result(result)
            
            # Store results
            training_results["problems_attempted"].append({
                "problem_id": problem.id,
                "success": result["learning_outcome"]["success"],
                "time_taken": result["time_taken"],
                "test_success_rate": result["test_results"]["success_rate"]
            })
            
            # Small delay to simulate thinking time
            await asyncio.sleep(0.5)
        
        # Calculate overall results
        successes = sum(1 for p in training_results["problems_attempted"] if p["success"])
        training_results["overall_success_rate"] = successes / num_problems
        training_results["concept_mastered"] = concept in agent.state.mastered_concepts
        training_results["end_time"] = datetime.now().isoformat()
        
        # Save progress
        self.save_agent(agent_id)
        
        return training_results
    
    def _display_attempt_result(self, result: Dict):
        """Display the result of a problem attempt"""
        test_results = result["test_results"]
        complexity = result["complexity_analysis"]
        outcome = result["learning_outcome"]
        
        print(f"  Tests: {test_results['passed']}/{test_results['total']} passed")
        print(f"  Complexity: {complexity['time_complexity']} (optimal: {complexity['is_optimal']})")
        print(f"  Success: {'✓' if outcome['success'] else '✗'}")
        
        if outcome["insights_gained"]:
            print(f"  Insights: {outcome['insights_gained'][0]}")
    
    async def run_progressive_training(self, agent_id: str, target_level: str = "Advanced") -> Dict:
        """Run progressive training following the curriculum"""
        if agent_id not in self.agents:
            agent = self.create_agent(agent_id)
        else:
            agent = self.agents[agent_id]
        
        print(f"\n{'='*60}")
        print(f"Progressive Training for Agent: {agent_id}")
        print(f"Target Level: {target_level}")
        print(f"{'='*60}\n")
        
        training_session = {
            "agent_id": agent_id,
            "start_time": datetime.now().isoformat(),
            "target_level": target_level,
            "concepts_trained": [],
            "total_problems": 0,
            "total_successes": 0
        }
        
        # Continue until target level reached
        while agent.state.current_level != target_level:
            # Get next concepts to learn
            next_concepts = self.curriculum.get_next_concepts(agent.state.mastered_concepts)
            
            if not next_concepts:
                print("No more concepts to learn!")
                break
            
            # Train on next concept
            next_concept = next_concepts[0]
            print(f"\nNext concept: {next_concept}")
            
            # Determine difficulty based on current level
            if agent.state.current_level == "Beginner":
                difficulty_range = (1, 2)
                num_problems = 3
            elif agent.state.current_level == "Intermediate":
                difficulty_range = (2, 3)
                num_problems = 5
            else:
                difficulty_range = (2, 4)
                num_problems = 7
            
            # Train on concept
            results = await self.train_agent_on_concept(
                agent_id, next_concept, num_problems, difficulty_range
            )
            
            training_session["concepts_trained"].append(results)
            training_session["total_problems"] += len(results["problems_attempted"])
            training_session["total_successes"] += sum(
                1 for p in results["problems_attempted"] if p["success"]
            )
            
            # Update agent level
            agent.state.current_level = self.curriculum._determine_level(
                agent.state.mastered_concepts
            )
            
            # Display progress
            self._display_training_progress(agent)
            
            # Check if we should continue
            if len(training_session["concepts_trained"]) >= 10:  # Safety limit
                print("\nReached training limit for this session")
                break
        
        training_session["end_time"] = datetime.now().isoformat()
        training_session["final_level"] = agent.state.current_level
        
        # Save training session
        self.training_sessions.append(training_session)
        self._save_training_session(training_session)
        
        return training_session
    
    def _display_training_progress(self, agent: MathLearningAgent):
        """Display current training progress"""
        print(f"\n--- Progress Report ---")
        print(f"Current Level: {agent.state.current_level}")
        print(f"Mastered Concepts: {', '.join(agent.state.mastered_concepts)}")
        print(f"Total Problems Solved: {agent.state.total_problems_solved}")
        
        # Show concept scores
        if agent.state.concept_scores:
            print("\nConcept Scores:")
            for concept, score in sorted(agent.state.concept_scores.items(), 
                                       key=lambda x: x[1], reverse=True):
                bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
                print(f"  {concept:20} [{bar}] {score:.2f}")
    
    def _save_training_session(self, session: Dict):
        """Save training session data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.save_dir, f"session_{session['agent_id']}_{timestamp}.json")
        
        with open(save_path, 'w') as f:
            json.dump(session, f, indent=2)
    
    async def benchmark_agents(self, agent_ids: List[str], test_concepts: List[str]) -> Dict:
        """Benchmark multiple agents on the same test set"""
        print(f"\n{'='*60}")
        print(f"Benchmarking {len(agent_ids)} agents")
        print(f"{'='*60}\n")
        
        # Generate diagnostic test
        test_problems = self.problem_generator.generate_diagnostic_test(test_concepts)
        
        benchmark_results = {
            "test_time": datetime.now().isoformat(),
            "num_problems": len(test_problems),
            "agent_results": {}
        }
        
        # Test each agent
        for agent_id in agent_ids:
            if agent_id not in self.agents:
                print(f"Agent {agent_id} not found, skipping")
                continue
            
            agent = self.agents[agent_id]
            print(f"\nTesting agent: {agent_id}")
            
            agent_results = {
                "problems_solved": 0,
                "total_time": 0,
                "concept_scores": {}
            }
            
            # Test on each problem
            for problem in test_problems:
                result = agent.attempt_problem(problem)
                
                if result["learning_outcome"]["success"]:
                    agent_results["problems_solved"] += 1
                
                agent_results["total_time"] += result["time_taken"]
                
                # Track per-concept performance
                if problem.concept not in agent_results["concept_scores"]:
                    agent_results["concept_scores"][problem.concept] = []
                
                agent_results["concept_scores"][problem.concept].append(
                    result["test_results"]["success_rate"]
                )
            
            # Calculate averages
            for concept in agent_results["concept_scores"]:
                scores = agent_results["concept_scores"][concept]
                agent_results["concept_scores"][concept] = sum(scores) / len(scores)
            
            benchmark_results["agent_results"][agent_id] = agent_results
        
        # Display benchmark summary
        self._display_benchmark_summary(benchmark_results)
        
        return benchmark_results
    
    def _display_benchmark_summary(self, results: Dict):
        """Display benchmark results summary"""
        print(f"\n{'='*60}")
        print("Benchmark Summary")
        print(f"{'='*60}\n")
        
        # Sort agents by performance
        agent_scores = []
        for agent_id, agent_results in results["agent_results"].items():
            score = agent_results["problems_solved"] / results["num_problems"]
            agent_scores.append((agent_id, score, agent_results))
        
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Display rankings
        print("Agent Rankings:")
        for rank, (agent_id, score, agent_results) in enumerate(agent_scores, 1):
            print(f"{rank}. {agent_id}: {score:.2%} success rate")
            print(f"   Time: {agent_results['total_time']:.2f}s")
            print(f"   Best concept: {max(agent_results['concept_scores'].items(), key=lambda x: x[1])[0]}")
            print()
    
    def generate_learning_analytics(self, agent_id: str) -> Dict:
        """Generate detailed learning analytics for an agent"""
        if agent_id not in self.agents:
            return {"error": f"Agent {agent_id} not found"}
        
        agent = self.agents[agent_id]
        report = agent.get_learning_report()
        
        # Add curriculum progress
        report["curriculum_progress"] = self.curriculum.generate_learning_report({
            "mastered_concepts": agent.state.mastered_concepts,
            "attempted_concepts": {
                concept: {"average_score": agent.state.concept_scores.get(concept, 0)}
                for concept in agent.state.attempted_problems.keys()
            }
        })
        
        return report


# Example usage script
async def main():
    """Example training session"""
    orchestrator = TrainingOrchestrator()
    
    # Create or load an agent
    agent_id = "math_learner_001"
    agent = orchestrator.load_agent(agent_id)
    if not agent:
        agent = orchestrator.create_agent(agent_id)
    
    # Train on specific concept
    await orchestrator.train_agent_on_concept(agent_id, "arithmetic", num_problems=3)
    
    # Progressive training
    await orchestrator.run_progressive_training(agent_id, target_level="Intermediate")
    
    # Generate analytics
    analytics = orchestrator.generate_learning_analytics(agent_id)
    print(f"\n{'='*60}")
    print("Learning Analytics")
    print(f"{'='*60}")
    print(json.dumps(analytics, indent=2))


if __name__ == "__main__":
    asyncio.run(main())