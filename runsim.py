#!/usr/bin/env python3

from sir import *
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

boundary = 10
num_agents = 100
num_iter = 1000
dt = 1/50 # 50 Hz

print("Running simulation...")
start_time = time.time()
sim = SIR(boundary,num_agents,num_iter,dt)
sim.run()
end_time = time.time()
elapsed_time = end_time - start_time
print("Total sim time\t{:.2f} seconds".format(elapsed_time))

fig_size=6
fig, ax = plt.subplots(figsize=(fig_size, fig_size))
ax.set_xlim(-boundary, boundary)
ax.set_ylim(-boundary, boundary)
ax.set_title(f"Step 0/{num_iter}")
x = [agent.position_history[0][0] for agent in sim.agents]
y = [agent.position_history[0][1] for agent in sim.agents]
point_size = 0.1
# Create a scatter plot with the specified point size
circles = [Circle((x[i], y[i]), point_size, edgecolor='black', facecolor='black') for i in range(num_agents)]
for circle in circles:
    ax.add_patch(circle)

def animate(i):
    ax.set_title(f"Step {i}/{num_iter}")
    x = [agent.position_history[i][0] for agent in sim.agents]
    y = [agent.position_history[i][1] for agent in sim.agents]
    for i in range(num_agents):
        circles[i].center = (x[i], y[i])

sim_speed = 2
frames = sim.num_iter
interval = (1000*sim.dt)/sim_speed

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=interval, blit=False)

# code to toggle animation
ani_paused = False
def on_press(event):
    global ani_paused
    if event.key == 'p':
        if ani_paused:
            ani.resume()
        else:
            ani.pause()
        ani_paused = not ani_paused

fig.canvas.mpl_connect('key_press_event', on_press)

plt.show()