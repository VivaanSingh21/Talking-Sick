import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Simulation parameters
# -----------------------------
num_agents = 10
box_size = 1.0
dt = 0.01
num_steps = 500
base_speed = 0.05       # base speed (scaled by energy)
std_random = 0.02       # standard deviation for velocity randomness

# Times (steps) at which to take snapshots for plotting
snapshot_steps = [0, 100, 250, 499]

# -----------------------------
# Initialize agent properties
# -----------------------------
# Random starting positions inside the box
positions = np.random.rand(num_agents, 2) * box_size  

# Energy per agent (affects speed)
energies = np.random.uniform(0.5, 1.5, size=num_agents)  

# -----------------------------
# Store snapshots for plotting
# -----------------------------
snapshots = []

# -----------------------------
# Simulation loop
# -----------------------------
for t in range(num_steps):
    # Random velocity vector for each agent at this step
    random_velocity = np.random.normal(0, std_random, size=(num_agents, 2))
    
    # Base velocity scaled by energy
    velocities = (base_speed * energies)[:, None] + random_velocity
    
    # Update positions
    positions += velocities * dt
    
    # Bounce off walls (agents stay in the box)
    for i in range(num_agents):
        for dim in [0, 1]:
            if positions[i, dim] < 0:
                positions[i, dim] = 0
                velocities[i, dim] *= -1
            elif positions[i, dim] > box_size:
                positions[i, dim] = box_size
                velocities[i, dim] *= -1
    
    # Save snapshot if this step is one we want
    if t in snapshot_steps:
        snapshots.append(positions.copy())

# -----------------------------
# Plot snapshots
# -----------------------------
plt.figure(figsize=(8, 8))
colors = plt.cm.tab10(np.arange(num_agents))  # unique color per agent

for s_idx, pos in enumerate(snapshots):
    plt.scatter(pos[:, 0], pos[:, 1], s=100, c=colors, label=f'Step {snapshot_steps[s_idx]}', alpha=0.7)

plt.xlim(0, box_size)
plt.ylim(0, box_size)
plt.xlabel("X position")
plt.ylabel("Y position")
plt.title("Randomly Moving Agents in 1x1 Box (Crowd Simulation)")
plt.legend()
plt.show()

