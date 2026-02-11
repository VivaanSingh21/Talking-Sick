#!/usr/bin/env python3
"""
Multi-Agent Simulation Example
Demonstrates the agent-based simulation with interactions
"""

from simulation import Simulation

def main():
    """Run example simulation"""
    
    print("=" * 60)
    print("Multi-Agent Simulation")
    print("=" * 60)
    
    # Create simulation
    sim = Simulation(
        boundary_width=800,
        boundary_height=600,
        interaction_radius=50.0,
        time_step=0.1,
        random_std_dev=0.5,  # Add some randomness to movement
    )
    
    # Initialize agents with varying energy levels
    sim.initialize_agents(
        num_agents=20,
        energy_range=(0.5, 1),  # Energy determines how long they move
        speed_range=(10.0, 30.0),   # Random speeds
        nrg_gain=0.01
    )
    
    # Print initial states
    print("\nInitial agent states (first 5):")
    for i, agent in enumerate(sim.agents[:5]):
        print(f"  Agent {i}: {agent}")
    
    # Run simulation
    print("\n")
    sim.run(duration=25.0)  # Run for 25 seconds
    
    # Print final states
    print("\nFinal agent states (first 5):")
    for i, agent in enumerate(sim.agents[:5]):
        print(f"  Agent {i}: {agent}")


if __name__ == "__main__":
    main()
