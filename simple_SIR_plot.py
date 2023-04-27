#!/usr/bin/env python

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt

def SIR(y,t,beta,mew):
    S,I,R = y
    dSdt = -beta*S*I
    dIdt = beta*S*I - mew*I
    dRdt = mew*I
    return (dSdt,dIdt,dRdt)
S0,I0,R0 = 0.9,0.1,0.
beta,mew = 0.3,0.1
t = np.linspace(0,100,10000)

soln = scipy.integrate.odeint(SIR,[S0,I0,R0],t,args=(beta,mew))
soln = np.array(soln)

fig_size = 6
fig, ax = plt.subplots(figsize=(fig_size, fig_size))
ax.set_title(f'SIR Trajectories beta: {beta} mew: {mew}')
ax.set_xlabel('Time')
ax.set_ylabel('Population')
ax.set_xticks([])
ax.set_yticks([])
ax.plot(t,soln[:,0],label='Susceptible',color='blue') 
ax.plot(t,soln[:,1],label='Infected',color='red') 
ax.plot(t,soln[:,2],label='Recovered',color='grey') 
ax.legend()
plt.show()