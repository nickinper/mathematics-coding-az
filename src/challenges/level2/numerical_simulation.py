"""Numerical simulation challenges focusing on physics simulations."""

import re
import numpy as np
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class PhysicsSimulationChallenge(Challenge):
    """Physics simulation challenge requiring differential equations and numerical methods."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Ordinary Differential Equations",
                description="Derive the equations of motion for a physical system",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Numerical Integration",
                description="Implement Runge-Kutta methods for solving ODEs",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Error Analysis",
                description="Analyze truncation and roundoff errors in numerical solutions",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Conservation Laws",
                description="Verify energy and momentum conservation in the simulation",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="N-Body Gravitational Simulation",
            description="""
Implement a physics simulation of the gravitational N-body problem using numerical methods.

Your implementation must include:
1. A mathematical model of the N-body problem using Newton's laws
2. A numerical integration scheme (at least 4th-order Runge-Kutta)
3. Error analysis and stability considerations
4. Verification of conservation laws (energy, momentum)

Mathematical Proof Requirements:
- Derive the system of differential equations for the N-body problem
- Analyze the accuracy and stability of your numerical method
- Derive expressions for total energy and momentum in the system
- Prove the conservation laws that should hold in your simulation

Example Usage:
```python
# Create simulation with 3 bodies
bodies = [
    {'mass': 1.0, 'position': [0, 0, 0], 'velocity': [0, 0, 0]},
    {'mass': 0.1, 'position': [1, 0, 0], 'velocity': [0, 1, 0]},
    {'mass': 0.1, 'position': [0, 1, 0], 'velocity': [-1, 0, 0]}
]
simulation = NBodySimulation(bodies)

# Run simulation for 100 time steps
dt = 0.01
for i in range(100):
    simulation.step(dt)

# Get final positions and velocities
final_state = simulation.get_state()

# Check conservation laws
energy_initial = simulation.total_energy(0)
energy_final = simulation.total_energy(100)
print(f"Energy conservation error: {abs(energy_final - energy_initial)}")
```
            """,
            level=ChallengeLevel.INTERMEDIATE,
            domain=MathematicalDomain.NUMERICAL_ANALYSIS,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=900.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for physics simulation implementations."""
        test_cases = []
        
        # Test case for two-body problem (analytical solution exists)
        two_body_system = [
            {'mass': 1.0, 'position': [0, 0, 0], 'velocity': [0, 0, 0]},
            {'mass': 0.001, 'position': [1, 0, 0], 'velocity': [0, 1, 0]}
        ]
        
        test_cases.append(TestCase(
            input_data={
                "system": two_body_system,
                "method": "rk4",
                "dt": 0.01,
                "steps": 100
            },
            expected_output={
                "orbit_valid": True,
                "energy_conservation": lambda x: abs(x) < 1e-3,  # Energy should be conserved within 0.1%
                "angular_momentum_conservation": lambda x: abs(x) < 1e-3
            },
            description="Two-body orbital simulation"
        ))
        
        # Test case for three-body problem
        three_body_system = [
            {'mass': 1.0, 'position': [-1, 0, 0], 'velocity': [0, -0.1, 0]},
            {'mass': 1.0, 'position': [1, 0, 0], 'velocity': [0, 0.1, 0]},
            {'mass': 1.0, 'position': [0, 0, 0], 'velocity': [0, 0, 0]}
        ]
        
        test_cases.append(TestCase(
            input_data={
                "system": three_body_system,
                "method": "rk4",
                "dt": 0.01,
                "steps": 1000
            },
            expected_output={
                "simulation_stable": True,
                "momentum_conservation": lambda x: abs(x) < 1e-3
            },
            description="Three-body chaotic simulation",
            timeout=10.0
        ))
        
        # Test case for accuracy analysis
        test_cases.append(TestCase(
            input_data={
                "system": two_body_system,
                "methods": ["euler", "rk2", "rk4"],
                "dt": 0.01,
                "steps": 100
            },
            expected_output={
                "error_ratio_valid": True,  # Higher order methods should have lower errors
                "convergence_rates_valid": True
            },
            description="Numerical method comparison"
        ))
        
        # Test case for conservation laws
        solar_system = [
            {'mass': 1.0, 'position': [0, 0, 0], 'velocity': [0, 0, 0]},  # Sun
            {'mass': 0.0001, 'position': [0.4, 0, 0], 'velocity': [0, 2, 0]},  # Mercury
            {'mass': 0.001, 'position': [0.7, 0, 0], 'velocity': [0, 1.6, 0]},  # Venus
            {'mass': 0.001, 'position': [1.0, 0, 0], 'velocity': [0, 1.0, 0]},  # Earth
            {'mass': 0.0001, 'position': [1.5, 0, 0], 'velocity': [0, 0.8, 0]}  # Mars
        ]
        
        test_cases.append(TestCase(
            input_data={
                "system": solar_system,
                "method": "symplectic",
                "dt": 0.01,
                "steps": 1000
            },
            expected_output={
                "energy_drift": lambda x: abs(x) < 1e-4,  # Symplectic methods should have minimal energy drift
                "orbits_stable": True
            },
            description="Solar system simulation with symplectic integrator",
            timeout=15.0
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in physics simulation solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for ODE derivation
        if self._contains_ode_derivation(submission):
            score += 0.25
            feedback_parts.append("✓ Differential equations for N-body problem derived")
        else:
            feedback_parts.append("✗ Missing derivation of N-body differential equations")
        
        # Check for numerical method analysis
        if self._contains_numerical_method_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Numerical integration methods properly analyzed")
        else:
            feedback_parts.append("✗ Missing analysis of numerical methods")
        
        # Check for error analysis
        if self._contains_error_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Error analysis for numerical simulation provided")
        else:
            feedback_parts.append("✗ Missing error analysis for the simulation")
        
        # Check for conservation laws
        if self._contains_conservation_laws(submission):
            score += 0.25
            feedback_parts.append("✓ Conservation laws properly derived and verified")
        else:
            feedback_parts.append("✗ Missing derivation of conservation laws")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_force_calculation(submission) and 
            self._has_efficient_integration(submission)):
            return True, "Efficient algorithms for force calculation and numerical integration detected"
        elif self._has_efficient_force_calculation(submission):
            return False, "Force calculation is efficient, but numerical integration needs improvement"
        elif self._has_efficient_integration(submission):
            return False, "Numerical integration is efficient, but force calculation needs improvement"
        else:
            return False, "Both force calculation and numerical integration need efficiency improvements"
    
    def _contains_ode_derivation(self, text: str) -> bool:
        """Check if submission derives the ODE system for the N-body problem."""
        patterns = [
            r'newton.*universal.*gravitation',
            r'F = G.*m1.*m2.*r',
            r'second.*law.*motion',
            r'differential.*equation',
            r'system.*ode'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_numerical_method_analysis(self, text: str) -> bool:
        """Check if submission analyzes numerical methods."""
        patterns = [
            r'runge.*kutta',
            r'euler.*method',
            r'midpoint.*method',
            r'local.*truncation.*error',
            r'global.*error'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_error_analysis(self, text: str) -> bool:
        """Check if submission provides error analysis."""
        patterns = [
            r'truncation.*error',
            r'round.*off.*error',
            r'stability.*analysis',
            r'convergence.*rate',
            r'error.*propagation'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_conservation_laws(self, text: str) -> bool:
        """Check if submission discusses conservation laws."""
        patterns = [
            r'energy.*conservation',
            r'momentum.*conservation',
            r'angular.*momentum',
            r'symplectic.*integrator',
            r'hamiltonian'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_force_calculation(self, code: str) -> bool:
        """Check for efficient force calculation."""
        patterns = [
            r'numpy.*array',
            r'vectorized',
            r'O\(n\^2\)',
            r'barnes.*hut',
            r'fast.*multipole'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_efficient_integration(self, code: str) -> bool:
        """Check for efficient numerical integration."""
        patterns = [
            r'rk4',
            r'leapfrog',
            r'verlet',
            r'symplectic',
            r'adaptive.*step'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)