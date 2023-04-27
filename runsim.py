#!/usr/bin/env python

from sir import *
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import argparse

parser = argparse.ArgumentParser(description='process simulator parameters')
parser.add_argument('--seed', type=int, help='population size')
parser.add_argument('--N', type=int, help='population size')
parser.add_argument('--num_iter', type=int, help='number of time steps simulated')
parser.add_argument('--radius', type=float, help='infection radius')
parser.add_argument('--prob', type=float, help='infection probability')
parser.add_argument('--duration', type=float, help='infection duration')
args = parser.parse_args() 

seed = args.seed
N = args.N
num_iter = args.num_iter
radius = args.radius
prob = args.prob
duration = args.duration

# default simulation parameters
if not seed:
    seed = 42
if not N:
    N = 200
if not num_iter:
    num_iter = 200
if not radius:
    radius = 0.5
if not prob:
    prob = 0.1
if not duration :
    duration = 30

boundary = 10
dt = 1/50 # 50 Hz

print("Simulation parameters:")
print(f"Seed: {seed}")
print(f"Population: {N}")
print(f"Iterations: {num_iter}")
print(f"Infection radius: {radius}")
print(f"Infection probability: {prob}")
print(f"Infection duration: {duration}")
print("Running simulation...")

start_time = time.time()
sim = SIR(
    seed=seed,
    boundary=boundary,
    num_agents=N,
    num_iter=num_iter,
    dt=dt,
    infection_radius=radius,
    infection_probability=prob,
    infection_duration=duration)
sim.run()
end_time = time.time()
elapsed_time = end_time - start_time
print("Total sim time\t{:.2f} seconds".format(elapsed_time))

fig_size=6
fig, (graph_ax,traj_ax,sim_ax) = plt.subplots(1,3,figsize=(fig_size*3, fig_size))

time_steps = list(range(num_iter))
sus_history,inf_history,rem_history = sim.get_history()

color_map = {
    State.SUS : 'blue',
    State.INF : 'red',
    State.REM : 'grey',
}

def setup_graph(ax):
    ax.set_xlim(0,num_iter-1)
    ax.set_ylim(0,N)
    colors = ['blue', 'red', 'gray']
    labels = ['Susceptible', 'Infected', 'Recovered'] 
    legend_elements = [plt.Rectangle((0,0), 1, 1, color=color) for color in colors]
    ax.legend(legend_elements, labels, loc='upper left',facecolor='white')
    ax.set_title("SIR Distribution")
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.set_xticks([])
    ax.set_yticks([])

setup_graph(graph_ax)

traj_ax.set_xlim(0,num_iter-1)
traj_ax.set_ylim(0,N)
traj_ax.set_title("SIR Trajectories")
traj_ax.set_xlabel('Time')
traj_ax.set_ylabel('Population')
traj_ax.set_xticks([])
traj_ax.set_yticks([])
sus_line = Line2D([], [], color='blue')
traj_ax.add_line(sus_line) 
inf_line = Line2D([], [], color='red')
traj_ax.add_line(inf_line) 
rem_line = Line2D([], [], color='grey')
traj_ax.add_line(rem_line) 

sim_ax.set_xlim(-boundary, boundary)
sim_ax.set_ylim(-boundary, boundary)
sim_ax.set_title(f"Susceptible: {sus_history[0]} Infected: {inf_history[0]} Recovered: {rem_history[0]}")
x = [agent.position_history[0][0] for agent in sim.agents]
y = [agent.position_history[0][1] for agent in sim.agents]
state_history = [agent.state_history for agent in sim.agents]
point_size = 0.1
sim_ax.set_xticks([])
sim_ax.set_yticks([])

# Create a scatter plot with the specified point size
circles = [Circle((x[i], y[i]), point_size, edgecolor=color_map[state_history[i][0]], facecolor=color_map[state_history[i][0]]) for i in range(N)]
for circle in circles:
    sim_ax.add_patch(circle)

def animate(step):
    if step == 0:
        graph_ax.clear()
        setup_graph(graph_ax)

    inf_count = inf_history[step]
    rem_count = rem_history[step]
    sus_count = sus_history[step]

    # Add a new bar for the current state of each group (S, I, R)
    graph_ax.bar(step, inf_count, color=color_map[State.INF], width=1, align='edge')
    graph_ax.bar(step, rem_count, bottom=inf_count, color=color_map[State.REM], width=1, align='edge')
    graph_ax.bar(step, sus_count, bottom=inf_count + rem_count, color=color_map[State.SUS], width=1, align='edge')
    
    sus_line.set_data(
        time_steps[:step+1],
        sus_history[:step+1]
    )
    inf_line.set_data(
        time_steps[:step+1],
        inf_history[:step+1]
    )
    rem_line.set_data(
        time_steps[:step+1],
        rem_history[:step+1]
    )

    sim_ax.set_title(f"Susceptible: {sus_history[step]} Infected: {inf_history[step]} Recovered: {rem_history[step]}")
    x = [agent.position_history[step][0] for agent in sim.agents]
    y = [agent.position_history[step][1] for agent in sim.agents]
    for i in range(N):
        circles[i].center = (x[i], y[i])
        circles[i].set_edgecolor(color_map[state_history[i][step]])
        circles[i].set_facecolor(color_map[state_history[i][step]])

sim_speed = 5
interval = (1000*sim.dt)/sim_speed

ani = animation.FuncAnimation(fig, animate, frames=sim.num_iter, interval=interval, blit=False)

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
