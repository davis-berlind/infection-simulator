import numpy as np
import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt

def days_to(prob, infection_length):
	"""
	Calculate mean number of days to event given 
	P(event occurs before infection ends).

	Parameters:
		prob (float): P(event occurs before infection ends).
		infection_length (float): Average duration of infection in days.

	Returns:
		days (float): Average days to event corresponding to 
		P(event occurs before infection ends) and average duration 
		of infection.
	"""
	days = infection_length*(1 - prob) / prob
	return days
	
def get_susceptible_neighbors(node, infected, recovered, G):
	"""
	Finds the neighbors of a node in graph G that are neither infected 
	nor immune.

	Parameters: 
		node (int): Name of node whose neighbors we want to check.
		infected (list): List of the names of infected nodes.
		recovered (list): List of the names of immune nodes.
		G (Graph)

	Returns:
		neighbors (list): Node's neighbors that are neither infected nor immune.
	"""
	neighbors = [k for k in G[node].keys() if k not in infected and k not in recovered]
	return neighbors

def get_susceptible(infected, recovered, G):
	"""
	Finds all nodes in graph G that neighbor an infected node and are neither
	infected nor immune.

	Parameters: 
		infected (list): List of the names of infected nodes.
		recovered (list): List of the names of immune nodes.
		G (Graph)

	Returns:
		susceptible (list): List of nodes neighboring an infected node
		that are neither infected nor immune.
	"""
	susceptible = []
	for node in infected:
		neighbors = get_susceptible_neighbors(node, infected, recovered, G)
		susceptible.extend(neighbors)
	return susceptible

def configGraph(avg_degree, n, model='poisson'):
	"""
	Generates a random graph according to the configuration model
	without any self loops and no duplicate edeges.

	Parameters:
		avg_degree (int): The average degree of the nodes.
		n (int): Number of nodes.
		model (str): Model for generating degree sequence.

	Returns:
		G (Graph)
	"""
	if model == 'poisson':
		degree_seq = np.random.poisson(lam=avg_degree, size=n)
	
	ledge = np.repeat(np.arange(n), degree_seq)
	redge = np.random.permutation(ledge)
	edges = [(l,r) for l, r in zip(ledge, redge) if l != r]
	G = nx.Graph()
	G.add_edges_from(edges)
	return G

def simulation(G, T, init_pct_infected, lambda_recovered, lambda_susceptible, lambda_death, lambda_infected, 
			   return_event_list=False, finish=True):
	"""
	Simulates infection on graph G

	Parameters:
		G (Graph)
		T (float): Maximum simulation days.
		init_pct_infected (float): Initial percent of the population that is infected.
		lambda_recovered (float): Days to Revovery | Infected ~ Exp(lambda_recovered).
		lambda_susceptible (float): Days to No Longer Immune | Immune ~ Exp(lambda_susceptible).
		lambda_death (float): Days to Death | Infected ~ Exp(lambda_death).
		lambda_infected (float): Days to Infected | Neighbor Infected ~ Exp(lambda_infected).
		return_event_list (bool): Return complete event list if True.
		finish (bool): Whether to keep simulating after infection ends.

	Returns:
		stats (list): Simulation statistics including time simulation ends, # infected at end, 
		# immune at end, # susceptible at end, # deaths at end, time # immune first intersects # infected,
		maximumn # infected, time of maximumn # infected, maximumn # immune, time of maximumn # immune.

		event_list (list): Complete event list.
	"""
	t = 0
	nodes = [node for node in G.nodes] 

	## initializing parameters and counters ##
	n_infected = int(init_pct_infected * len(nodes)) 	  # intial number of infected nodes
	infected = random.sample(nodes, k=n_infected)    	  # initial infected nodes
	recovered = []                                   	  # initial nodes with immunity
	n_recovered = 0                                  	  # initial number of recovered nodes
	susceptible = get_susceptible(infected, recovered, G) # initial nodes with infected neighbors
	n_susceptible = len(set(susceptible))                 # initial number of nodes with infected neighbors
	e_susceptible = len(susceptible)                      # initial number of edges from susceptible to infected nodes
	n_deaths = 0                                          # initial number of deaths
	t_intersect = None									  # time that # immune first excedes # infected
	ri_intersect = False                                  # tracker for if # immune has exceded # infected
	max_infected = n_infected						      # maximum number of infected nodes during simulation
	max_recovered = n_recovered						      # maximum number of immune nodes during simulation
	t_max_infected = 0
	t_max_recovered = 0

	event_list = [[t, n_infected, n_recovered, n_susceptible, n_deaths]]

	while t < T:
		# calulate probability of next event
		p_vals = [n_infected*lambda_recovered, n_infected*lambda_death, e_susceptible*lambda_infected, n_recovered*lambda_susceptible]
		lambda_all = n_infected*(lambda_recovered + lambda_death) + e_susceptible*lambda_infected + n_recovered*lambda_susceptible

		# sample time of next event
		t += np.random.exponential(1 / lambda_all)

		# sample type of next event
		event = np.random.multinomial(n=1, pvals=[p / lambda_all for p in p_vals])

		# next event is a recovery
		if event[0] == 1:
			random.shuffle(infected)                       					  # shuffle to randomly select recovered node
			recoverer = infected.pop()                     					  # sample recovering node
			for rm in G[recoverer].keys():                 					  # removing suscepitble neighbors of recovered node
				if rm in susceptible:
					susceptible.remove(rm)      
			recovered.append(recoverer)                    					  # move infected node to recovered
			 
		# next event is a death 
		if event[1] == 1:
			random.shuffle(infected)                       					  # shuffle to randomly select dead node
			dead = infected.pop()                          					  # sample dying node
			for rm in G[dead].keys():                    					  # removing suscepitble neighbors of dying node
				if rm in susceptible:
					susceptible.remove(rm)      
			G.remove_node(dead)                            					  # remove dying node from graph
			n_deaths += 1
			
		# next event is an infection 
		if event[2] == 1:
			random.shuffle(susceptible)                                       # shuffle to randomly select infected node
			sick = susceptible.pop()                                          # sample newly infected node
			susceptible = [s for s in susceptible if s != sick]               # delete duplicates of susceptible node 
			new_sus = get_susceptible_neighbors(sick, infected, recovered, G) # get newly susceptible nodes
			susceptible.extend(new_sus)                                       # add newly susceptible nodes
			infected.append(sick)                                             # add sampled node to infected nodes
				
		# next event is a loss of immunity 
		if event[3] == 1:
			random.shuffle(recovered)                                         # shuffle to randomly select node losing immunity
			sus = recovered.pop()                                             # sample node losing immunity
			new_sus = [sus for k in G[sus].keys() if k in infected]           # repeat sampled node for each infected neighbor
			susceptible.extend(new_sus)                                       # add newly susceptible nodes        

		# updating counters and stats
		n_infected = len(infected)
		n_recovered = len(recovered)
		n_susceptible = len(set(susceptible)) 
		e_susceptible = len(susceptible)

		if n_recovered > n_infected and not ri_intersect:
			t_intersect = t
			ri_intersect = True

		if n_recovered > max_recovered:
			max_recovered = n_recovered
			t_max_recovered = t

		if n_infected > max_infected:
			max_infected = n_infected
			t_max_infected = t

		if return_event_list:
			event_list.append([t, n_infected, n_recovered, n_susceptible, n_deaths])

		# check if infection over
		if not finish:
			if n_infected == 0:
				break

		print("Time: %.5f, Infected: %d, Recovered: %d, Dead: %d \t" % (t, n_infected, n_recovered, n_deaths), end = "\r")

	stats = [t, n_infected, n_recovered, n_susceptible, n_deaths, 
			 t_intersect, max_infected, t_max_infected, max_recovered, 
			 t_max_recovered]

	if return_event_list:
		return (stats, event_list)
	else:
		return stats
