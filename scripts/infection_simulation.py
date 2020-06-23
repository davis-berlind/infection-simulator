import sys, os, random
import numpy as np
import pandas as pd
import networkx as nx
from simFunctions import days_to, configGraph, simulation

## Slurm Parameters ##
jobid = str(os.getenv('SLURM_ARRAY_TASK_ID'))

## Population Parameters ##
pop = 50000                                                   # total population
contacts = int(sys.argv[1])                                   # average number of edges (contacts) between nodes (people)
init_pct_infected = 0.001                                     # initial percent of population infected

## Infection Parameters ##
days_to_recovered = 25                                        # average length of infection
lambda_recovered = 1 / days_to_recovered                      # length of intection ~ exp(lambda_recovery)
days_to_susceptible = 270                                     # average duration of immunity
lambda_susceptible = 1 / days_to_susceptible                  # length of immunity ~ exp(lambda_recovery)
mortality_rate = 0.07                                         # probability of dying if infected
infection_rate = float(sys.argv[2])                           # probability of getting infected from an infected neighbor 

days_to_death = days_to(mortality_rate, days_to_recovered)    # days to mortality if infected; chosen so that 
                                                              # p(dying before recovering) = mortality_rate
lambda_death = 1 / days_to_death
days_to_infected = days_to(infection_rate, days_to_recovered) # days to infection if neighbor is infected; chosen so that 
                                                              # p(infected before neighbor recovers) = infection_rate
lambda_infected = 1 / days_to_infected

## Generate random graph with configuration model ##
G = configGraph(contacts, pop, model='poisson')

## Simulation Parameters ##
nsim = 1000
T = 500

stats, event_list = simulation(G,T,init_pct_infected,lambda_recovered,lambda_susceptible,lambda_death,lambda_infected,return_event_list=True)
stat = np.array(stats)
event_list = np.array(event_list)
summary = []
for t in range(T):
	dex = np.logical_and(event_list[:,0] < t+1, event_list[:,0] >= t)
	if dex.sum() != 0:
		sum_t = event_list[dex].mean(axis=0)
	summary.append(sum_t[1:])

summary = np.array(summary)
infected = summary[:,0]
recovered = summary[:,1]
susceptible = summary[:,2]
deaths = summary[:,3]

files = ['statistics', 'infected', 'recovered', 'susceptible', 'deaths']
files = [file+'_C'+str(contacts)+'R'+str(int(100*infection_rate))+'%_J'+jobid+'.txt' for file in files]

os.chdir('results/raw')
np.savetxt(files[0], stats)
np.savetxt(files[1], infected)
np.savetxt(files[2], recovered)
np.savetxt(files[3], susceptible)
np.savetxt(files[4], deaths)
