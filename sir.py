from enum import Enum
import numpy as np
from scipy.spatial import distance

class State(Enum):
    SUS = 0 # susceptible
    INF = 1 # infectious
    REM = 2 # removed

class Agent:
    max_speed = 3
    def __init__(self,boundary,state=State.SUS):
        self.boundary = boundary
        self.pos = np.random.uniform(-boundary,boundary,size=2)
        self.vel = np.random.uniform(-1,1,size=2)*self.max_speed
        self.state = state
        self.new_state = None
        self.position_history = []
        self.state_history = []
        self.infected_neighbours = []
        self.time_infected = 0

    def update_position(self,dt):
        self.position_history.append(self.pos)
        noise = np.random.uniform(-1,1,size=2)*0.01
        self.vel = np.clip( self.vel+noise,-self.max_speed,self.max_speed )
        pos = self.pos
        # keep in bounds
        if pos[0] < -self.boundary: self.vel[0] = - self.vel[0]
        if pos[0] > self.boundary: self.vel[0] = - self.vel[0]
        if pos[1] < -self.boundary: self.vel[1] = - self.vel[1]
        if pos[1] > self.boundary: self.vel[1] = - self.vel[1]
        pos = self.pos + self.vel*dt
        self.pos = pos

    def update_state(self):
        self.state_history.append(self.state)
        if self.new_state is None:
            return
        self.state = self.new_state
        self.new_state = None

class SIR:
    def __init__(
            self,
            seed,
            boundary,
            num_agents,
            num_iter,
            dt,
            infection_radius,
            infection_probability,
            infection_duration):
        np.random.seed(seed)
        self.agents = [ Agent(boundary) for _ in range(num_agents) ]
        self.agents[0].new_state = State.INF # patient zero
        self.num_agents = num_agents
        self.num_iter = num_iter
        self.dt = dt
        self.inf_rad = infection_radius
        self.inf_p = infection_probability
        self.inf_duration = infection_duration
        self.num_sus = num_agents-1
        self.num_inf = 1
        self.num_rem = 0
        self.sus_history = []
        self.inf_history = []
        self.rem_history = []
    
    def get_history(self):
        return self.sus_history,self.inf_history,self.rem_history

    def get_neighbors(self, current_point):
        agent_points = [agent.pos for agent in self.agents]
        distances = distance.cdist([current_point], agent_points)
        nearby = distances < self.inf_rad
        self_point = distances == 0
        self_point_index = np.nonzero(self_point)
        nearby[self_point_index] = False
        nearby = nearby[0]
        infected_neighbours = [ self.agents[idx] for idx,bool in enumerate(nearby) if bool == True ]
        return infected_neighbours

    def update_neighbors(self):
        for agent in self.agents:
            agent.infected_neighbours = self.get_neighbors(agent.pos)

    def update_states(self):
        for agent in self.agents:
            if agent.state == State.SUS:
                infect_threshold = self.inf_p * len(agent.infected_neighbours)
                infect_likelihood = np.random.random() # rand num between 0 and 1
                if infect_likelihood < infect_threshold:
                    agent.new_state = State.INF
                    self.num_sus -= 1
                    self.num_inf += 1
            elif agent.state == State.INF:
                agent.time_infected += 1
                if agent.time_infected > self.inf_duration:
                    agent.new_state = State.REM
                    self.num_inf -= 1
                    self.num_rem += 1
        # update states to new states
        for agent in self.agents:
            agent.update_state()

    def update_history(self):
        self.sus_history.append(self.num_sus)
        self.inf_history.append(self.num_inf)
        self.rem_history.append(self.num_rem)

    def step(self):
        self.update_neighbors()
        for agent in self.agents:
            agent.update_position(self.dt)
        # # record SIR history
        self.update_states()
        self.update_history()

    def run(self):
        for _ in range(self.num_iter):
            self.step()