"""
Crowd movement starter sim (R^2 box, reflective walls, energy decay scaling velocity).

What you can tweak:
- N, L, dt, steps, fps
- X0, decay_rate
- base_speed_mean, base_speed_std
- sigma_speed (magnitude randomness)
- sigma_angle (direction randomness)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class CrowdSim:
    def __init__(
        self,
        N=300,
        L=10.0,
        dt=0.05,
        X0=100.0,
        decay_rate=0.1,
        base_speed_mean=1.0,
        base_speed_std=0.4,
        sigma_speed=0.10,
        sigma_angle=0.20,
        seed=0,
    ):
        self.N = int(N)
        self.L = float(L)
        self.dt = float(dt)

        self.X0 = float(X0)
        self.decay_rate = float(decay_rate)

        self.base_speed_mean = float(base_speed_mean)
        self.base_speed_std = float(base_speed_std)

        self.sigma_speed = float(sigma_speed)
        self.sigma_angle = float(sigma_angle)

        self.rng = np.random.default_rng(seed)

        # State
        self.pos = self.rng.uniform(0.0, self.L, size=(self.N, 2))  # (N,2)
        self.X = np.full(self.N, self.X0, dtype=float)              # (N,)

        self.base_vel = np.zeros((self.N, 2), dtype=float)          # NEW: persistent base velocity
        self.vel = np.zeros((self.N, 2), dtype=float)               # actual velocity used for integration

        # Initialize base velocity with random directions
        self._resample_base_velocity()


    def _resample_base_velocity(self):
        """Pick a fresh base velocity (Vx, Vy) with random direction + speed."""
        angles = self.rng.uniform(0.0, 2.0 * np.pi, size=self.N)
        dirs = np.column_stack([np.cos(angles), np.sin(angles)])  # unit vectors

        speeds = self.rng.normal(self.base_speed_mean, self.base_speed_std, size=self.N)
        speeds = np.clip(speeds, 0.0, None)  # avoid negative speeds

        self.base_vel = dirs * speeds[:, None]

    def _apply_randomness_to_velocity(self, v):
        """
        Randomness epsilon affecting both magnitude (speed) and direction:
        - multiplicative speed noise
        - small random rotation
        """
        # Speed noise
        mag = 1.0 + self.sigma_speed * self.rng.normal(0.0, 1.0, size=self.N)
        v = v * mag[:, None]

        # Direction noise via rotation
        theta = self.rng.normal(0.0, self.sigma_angle, size=self.N)
        c, s = np.cos(theta), np.sin(theta)

        vx, vy = v[:, 0], v[:, 1]
        v_rot = np.column_stack([c * vx - s * vy, s * vx + c * vy])
        return v_rot

    def _reflect_boundaries(self):
        """
        Reflective boundary handling on [0, L] x [0, L].
        If an agent crosses a wall, mirror position back into the box
        and flip the corresponding velocity component.
        """
        for axis in (0, 1):
            low = self.pos[:, axis] < 0.0
            high = self.pos[:, axis] > self.L

            if np.any(low):
                self.pos[low, axis] = -self.pos[low, axis]
                self.vel[low, axis] *= -1.0

            if np.any(high):
                self.pos[high, axis] = 2.0 * self.L - self.pos[high, axis]
                self.vel[high, axis] *= -1.0

    def step(self):
        dt = self.dt

        # 1) Energy decay: X(t+dt) = X(t) * exp(-decay_rate * dt)
        self.X *= np.exp(-self.decay_rate * dt)

        # 2) Optionally re-sample a "base" velocity direction occasionally
        #    (Comment out if you want purely persistent velocities)
        # if self.rng.random() < 0.02:  # 2% chance per step
        #     self._resample_base_velocity()

        # 3) Apply randomness + energy scaling (normalize X/X0)
        v_noisy = self._apply_randomness_to_velocity(self.base_vel)  # CHANGED
        energy_factor = np.clip(self.X / self.X0, 0.0, 1.0)
        self.vel = v_noisy * energy_factor[:, None]

        # 4) Integrate position
        self.pos += self.vel * dt

        # 5) Reflect on boundaries
        self._reflect_boundaries()


def run_animation(
    N=300,
    L=10.0,
    dt=0.05,
    steps=600,
    fps=30,
    seed=1,
):
    sim = CrowdSim(N=N, L=L, dt=dt, seed=seed)

    fig, ax = plt.subplots()
    ax.set_xlim(0.0, sim.L)
    ax.set_ylim(0.0, sim.L)
    ax.set_aspect("equal", adjustable="box")

    # Keep title short / static
    ax.set_title("Crowd Simulation")

    scat = ax.scatter(sim.pos[:, 0], sim.pos[:, 1], s=12)

    # Dynamic stats in a corner text box (inside the axes)
    stats_text = ax.text(
        0.02, 0.98, "",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.25", alpha=0.6)  # optional: remove if you want no box
    )

    interval_ms = int(1000 / fps)

    def update(frame_idx):
        sim.step()
        scat.set_offsets(sim.pos)

        t = frame_idx * sim.dt
        stats_text.set_text(
            f"t = {t:.2f}\n"
            f"mean(X/X0) = {(sim.X / sim.X0).mean():.3f}"
        )
        return scat, stats_text

    ani = FuncAnimation(fig, update, frames=steps, interval=interval_ms, blit=True)
    plt.show()


if __name__ == "__main__":
    run_animation(N=50)
