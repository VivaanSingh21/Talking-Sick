# Multi-Agent Simulation System

## Overview
An object-oriented Python implementation of a multi-agent simulation where agents move with randomness, interact with each other, and respect boundary constraints.

## Architecture

### Class Structure

```
Vector2D          - 2D vector operations (position, velocity)
    ↓
Agent             - Individual agent with position, velocity, energy
    ↓
Boundary          - Simulation boundaries (rectangular)
    ↓
Simulation        - Main simulation manager
```

## Classes

### 1. Vector2D (`vector2d.py`)
Handles all 2D vector mathematics.

**Properties:**
- `x`, `y` - vector components

**Key Methods:**
- `magnitude()` - vector length
- `normalize()` - unit vector
- `distance_to(other)` - distance between vectors
- `rotate(angle)` - rotate by angle in radians
- `add_randomness(std_dev)` - add Gaussian noise

### 2. Agent (`agent.py`)
Represents individual agents in the simulation.

**Properties:**
- `position` - Vector2D location
- `velocity` - Vector2D velocity
- `energy` - float (determines movement duration)
- `is_moving` - boolean status
- `movement_time` - accumulated movement time
- `radius` - collision detection radius

**Key Methods:**
- `update(delta_time, std_dev)` - update position with optional randomness
- `can_move()` - check if agent has energy remaining
- `detect_collision(other, radius)` - check if within interaction radius
- `interact_with_agent(other)` - move tangentially when agents meet
- `interact_with_boundary(boundary)` - handle boundary collisions

**Energy System:**
Currently implements: **Energy = Movement Duration**
- Higher energy → agents move for longer time
- When `movement_time >= energy`, agent stops
- Velocity remains constant while moving (acceleration = 0)

### 3. Boundary (`boundary.py`)
Defines the simulation space boundaries.

**Properties:**
- `width`, `height` - rectangular dimensions
- `min_x`, `max_x`, `min_y`, `max_y` - boundary limits

**Key Methods:**
- `is_within_bounds(position)` - check if position is valid
- `is_near_boundary(position, threshold)` - proximity check
- `get_tangent_at_point(position)` - tangent vector at boundary
- `get_normal_at_point(position)` - normal vector (inward)

### 4. Simulation (`simulation.py`)
Manages the entire simulation.

**Properties:**
- `agents` - list of Agent objects
- `boundary` - Boundary object
- `interaction_radius` - distance for agent interactions
- `time_step` - simulation time increment
- `random_std_dev` - standard deviation for velocity randomness
- `current_time` - elapsed simulation time

**Key Methods:**
- `initialize_agents(num, energy_range, speed_range)` - create agents
- `update()` - main simulation step
- `check_interactions()` - handle agent-agent interactions
- `check_boundary_collisions()` - handle agent-boundary interactions
- `run(duration)` - run simulation for specified time
- `get_agent_positions()` - get all agent positions
- `get_agent_states()` - get detailed agent states

## How It Works

### Initialization
1. Agents are created with random positions within boundary
2. Random velocity directions and magnitudes
3. Random energy levels within specified range

### Simulation Loop (each timestep)
1. **Update agents**: Move based on velocity + randomness
2. **Check agent-agent interactions**: 
   - If distance < interaction_radius
   - Both agents turn tangentially to each other
   - Continue moving in new direction
3. **Check boundary interactions**:
   - If agent near boundary
   - Turn tangentially along boundary
   - Pushed slightly inward to prevent sticking

### Movement Rules
- Agents move at constant velocity (acceleration = 0)
- Randomness is added to velocity at each timestep
- When `movement_time >= energy`, agent stops permanently
- Higher energy = longer movement duration

### Interaction Behavior
**Agent-Agent:**
- When within interaction radius, both agents rotate 90° from their radial direction
- This creates tangential movement (like orbiting)

**Agent-Boundary:**
- Agent moves tangent to boundary wall
- Pushed slightly inward to maintain valid position

## Usage Example

```python
from simulation import Simulation

# Create simulation
sim = Simulation(
    boundary_width=800,
    boundary_height=600,
    interaction_radius=50.0,
    time_step=0.1,
    random_std_dev=0.5
)

# Initialize 20 agents
sim.initialize_agents(
    num_agents=20,
    energy_range=(5.0, 20.0),   # 5-20 seconds of movement
    speed_range=(10.0, 30.0)    # 10-30 units/second
)

# Run for 25 seconds
sim.run(duration=25.0)

# Get results
positions = sim.get_agent_positions()
states = sim.get_agent_states()
```

## Parameters to Adjust

### Simulation Level
- `boundary_width`, `boundary_height` - simulation area size
- `interaction_radius` - how close agents must be to interact
- `time_step` - simulation time resolution (smaller = more accurate)
- `random_std_dev` - amount of randomness in movement

### Agent Level
- `num_agents` - population size
- `energy_range` - min/max energy (movement duration)
- `speed_range` - min/max velocity magnitude
- `agent_radius` - agent size for collisions

## Customization Options

### 1. Change Energy System
**Current:** Energy = movement duration

**Alternative:** Energy = velocity magnitude
```python
# In Agent.__init__():
self.velocity = velocity.normalize() * energy  # Speed based on energy
```

### 2. Change Interaction Behavior
**Current:** Tangential movement (90° rotation)

**Alternative:** Reflection or velocity swap
```python
# In Agent.interact_with_agent():
# Reflection
self.velocity = self.velocity - 2 * direction.normalize() * self.velocity.dot(direction.normalize())
```

### 3. Add Energy Regeneration
```python
# In Agent.update():
if not self.is_moving:
    self.movement_time -= delta_time * regeneration_rate
    if self.movement_time < self.energy:
        self.is_moving = True
```

### 4. Change Boundary Shape
Modify `Boundary` class for circular boundaries or custom shapes.

## Files
- `vector2d.py` - Vector mathematics
- `agent.py` - Agent class
- `boundary.py` - Boundary class
- `simulation.py` - Simulation manager
- `main.py` - Example usage (text output)
- `run_visual.py` - **Visual simulation with animation** ⭐
- `visualizer.py` - Visualization class (advanced)
- `README.md` - This file

## How to Run

### Option 1: Visual Animation (Recommended!)
```bash
python run_visual.py
```
This creates an animated visualization showing agents moving around, interacting, and stopping when energy runs out. Agents fade out when they stop moving.

### Option 2: Text Output Only
```bash
python main.py
```
This runs the simulation and prints statistics to the console without visualization.

### Requirements
- Python 3.6+
- matplotlib (for visualization)
- numpy (for visualization)

**Install requirements:**
```bash
pip install matplotlib numpy
```

## Next Steps
1. ✅ Basic OOP structure implemented
2. ✅ Agent movement with randomness
3. ✅ Agent-agent interactions
4. ✅ Boundary interactions
5. 🔲 Visualization (matplotlib/pygame)
6. 🔲 Data export (CSV, JSON)
7. 🔲 Parameter tuning interface
8. 🔲 Performance optimization for large agent counts

## Notes
- All agents currently stop permanently when energy runs out
- Acceleration is zero (constant velocity)
- Interactions are symmetric (both agents affected equally)
- Randomness is applied at each timestep independently
