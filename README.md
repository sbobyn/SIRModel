# Running Simulation

To execute the simulation run the following command `./runsim.py`.

The program accepts the following optional parameter:

- `--seed [int]` the random seed used. Default: 42.
- `--N [int]` the size of the population. Default: 200.
- `--num_iter [int]` the number of time steps simulated. Default: 200.
- `--radius [float]` the size of the infection radius Default: 0.5.
- `--prob [float]` the infection rate. Default: 0.1.
- `--duration [int]` the length of infection in time steps. Default: 30.

For example, to run the simulation with a random seed of 42, 200 agents, for 200 iterations, with an infection radius of 0.5, rate of 0.1, and duration of 30 frames run the following command: `./runsim.py --seed 42 --N 200 --num_iter 200 --radius 0.5 --prob 0.1 --duration 30`.

Press p to toggle/pause/play the animation.

# Program requirements

See the `env.yml` file to get the program dependecy information.
