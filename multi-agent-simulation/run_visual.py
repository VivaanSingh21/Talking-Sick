#!/usr/bin/env python3
"""
Simple Visual Simulation
Uses the OOP classes but with matplotlib animation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from simulation import Simulation

# ============================================================
# Simulation Parameters
# ============================================================
num_agents = 300
boundary_width = 800
boundary_height = 600
interaction_radius = 50.0
time_step = 0.1
random_std_dev = 0.5
num_frames = 500
nrg_gain_rate = 0.01

energy_range = (0.5, 1)   # How long agents move
speed_range = (15.0, 100.0)   # How fast agents move

# ============================================================
# Create Simulation
# ============================================================
print("Initializing simulation...")
sim = Simulation(
    boundary_width=boundary_width,
    boundary_height=boundary_height,
    interaction_radius=interaction_radius,
    time_step=time_step,
    random_std_dev=random_std_dev,
)

# Initialize agents
sim.initialize_agents(
    num_agents=num_agents,
    energy_range=energy_range,
    speed_range=speed_range,
    nrg_gain=nrg_gain_rate
)

# ============================================================
# Set up Matplotlib Figure
# ============================================================
fig, ax = plt.subplots(figsize=(10, 8))

# Get initial positions
positions = np.array(sim.get_agent_positions())

# Create unique colors for each agent
colors = plt.cm.tab20(np.linspace(0, 1, num_agents))

# Create scatter plot
scat = ax.scatter(
    positions[:, 0], 
    positions[:, 1], 
    s=150, 
    c=colors,
    alpha=0.7,
    edgecolors='black',
    linewidths=1.5
)

# Set plot limits and labels
ax.set_xlim(0, boundary_width)
ax.set_ylim(0, boundary_height)
ax.set_xlabel("X Position", fontsize=12)
ax.set_ylabel("Y Position", fontsize=12)
ax.set_title("Multi-Agent Simulation with Interactions", fontsize=14, fontweight='bold')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3, linestyle='--')

# Draw boundary rectangle
boundary_rect = plt.Rectangle(
    (0, 0), 
    boundary_width, 
    boundary_height,
    fill=False, 
    edgecolor='red', 
    linewidth=3,
    linestyle='-'
)
ax.add_patch(boundary_rect)

# Add info text
info_text = ax.text(
    0.02, 0.98, '', 
    transform=ax.transAxes,
    verticalalignment='top',
    fontsize=11,
    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
    family='monospace'
)

print(f"Animation ready! Running {num_frames} frames...")
print("Close the window to stop the simulation.")

# ============================================================
# Animation Update Function
# ============================================================
def update(frame):
    """Update function called for each animation frame"""
    
    # Update the simulation one step
    sim.update()
    
    # Get new positions
    positions = np.array(sim.get_agent_positions())
    
    # Update scatter plot positions
    scat.set_offsets(positions)
    
    # Update colors based on whether agents are moving
    # Fade out agents that have stopped
    agent_colors = []
    for i, agent in enumerate(sim.agents):
        color = list(colors[i])
        if agent.is_moving:
            color[3] = 0.8  # Active agents: more opaque
        else:
            color[3] = 0.2  # Stopped agents: faded
        agent_colors.append(color)
    
    scat.set_facecolors(agent_colors)
    
    # Update info text
    moving_count = sum(1 for agent in sim.agents if agent.is_moving)
    stopped_count = num_agents - moving_count
    
    info = (f"Frame: {frame:4d}  |  Time: {sim.current_time:6.2f}s\n"
            f"Moving: {moving_count:2d}  |  Stopped: {stopped_count:2d}")
    info_text.set_text(info)
    
    # Update title with current state
    ax.set_title(
        f"Multi-Agent Simulation - Frame {frame} ({moving_count} agents moving)",
        fontsize=14,
        fontweight='bold'
    )
    
    # Don't return anything when blit=False

# ============================================================
# Run Animation
# ============================================================
ani = FuncAnimation(
    fig, 
    update, 
    frames=num_frames, 
    interval=20,      # 20ms between frames = ~50 FPS
    blit=False,       # Set to False for better compatibility
    repeat=False
)

plt.tight_layout()
plt.show()

print("\nSimulation finished!")
print(f"Final time: {sim.current_time:.2f}s")
sim.print_statistics()
