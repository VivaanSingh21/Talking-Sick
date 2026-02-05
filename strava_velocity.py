import gpxpy
import numpy as np
import pandas as pd
from pyproj import Proj, transform

# -----------------------------
# Load GPX file
# -----------------------------
gpx_file = "Afternoon_Walk2.gpx"  # CHANGE THIS

with open(gpx_file, "r") as f:
    gpx = gpxpy.parse(f)

# -----------------------------
# Extract GPS data
# -----------------------------
lat, lon, time = [], [], []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if point.time:
                lat.append(point.latitude)
                lon.append(point.longitude)
                time.append(point.time)

df = pd.DataFrame({
    "lat": lat,
    "lon": lon,
    "time": pd.to_datetime(time)
})

# -----------------------------
# Convert lat/lon → x,y (meters)
# -----------------------------
wgs84 = Proj(init="epsg:4326")
utm = Proj(init="epsg:32633")  # OK for Europe; change if needed

x, y = transform(
    wgs84,
    utm,
    df["lon"].values,
    df["lat"].values
)

df["x"] = x
df["y"] = y

# Re-center coordinates
df["x"] -= df["x"].iloc[0]
df["y"] -= df["y"].iloc[0]

# -----------------------------
# Compute velocities
# -----------------------------
dt = df["time"].diff().dt.total_seconds()

df["vx"] = df["x"].diff() / dt
df["vy"] = df["y"].diff() / dt

df = df.dropna().reset_index(drop=True)

speed = np.sqrt(df["vx"]**2 + df["vy"]**2)

print("Average speed (m/s):", speed.mean())

# -----------------------------
# Save output
# -----------------------------
df.to_csv("walk_velocities.csv", index=False)
print("Saved walk_velocities.csv")

# Average velocities
avg_vx = df["vx"].mean()
avg_vy = df["vy"].mean()

print(f"Average vx (m/s): {avg_vx:.3f}")
print(f"Average vy (m/s): {avg_vy:.3f}")

