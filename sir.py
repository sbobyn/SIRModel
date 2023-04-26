from enum import Enum
import numpy as np

class State(Enum):
    SUS = 0 # susceptible
    INF = 1 # infectious
    REM = 2 # removed

class Agent:
    def __init__(self,boundary,state=State.SUS):
        self.boundary = boundary
        self.pos = np.random.uniform(-boundary,boundary,size=2)
        self.vel = np.random.uniform(-1,1,size=2)
        self.state = state
        self.position_history = []

    def update_position(self,dt):
        self.position_history.append(self.pos)
        noise = np.random.uniform(-1,1,size=2)*0.1
        self.vel = np.clip( self.vel+noise,-1,1 )
        pos = self.pos + self.vel*dt
        # keep in bounds
        if pos[0] < -self.boundary: pos[0] = self.boundary
        if pos[0] > self.boundary: pos[0] = -self.boundary
        if pos[1] < -self.boundary: pos[1] = self.boundary
        if pos[1] > self.boundary: pos[1] = -self.boundary
        self.pos = pos

    def update_state_to(self,new_state):
        self.state = new_state

class SIR:
    def __init__(self,boundary,num_agents,num_iter,dt):
        self.agents = [ Agent(boundary,dt) for _ in range(num_agents) ]
        self.num_agents = num_agents
        self.num_iter = num_iter
        self.dt = dt

    def step(self):
        for agent in self.agents:
            agent.update_position(self.dt)

    def run(self):
        for _ in range(self.num_iter):
            self.step()