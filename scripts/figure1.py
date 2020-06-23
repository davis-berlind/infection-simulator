import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

T = 500
N = 1000
alpha = 0.95
days = np.arange(T) + 1
contacts = ['5', '10', '20']
probs = ['10','50']
pltnum = 1

fig = plt.figure()  # create a figure object
for contact in contacts:
	for prob in probs:
		ax = fig.add_subplot(3, 2, pltnum)  # create an axes object in the figure
		if (pltnum - 1) % 2 == 0:
			ax.set_ylabel(contact + ' Contacts')
		if pltnum == 1 or pltnum == 2:
			ax.set_title('Infection Rate = ' + prob + '%')	
		if pltnum == 5 or pltnum == 6:
			ax.set_xlabel('Days')		

		# Infections
		file = '../Data/'+'infected_C'+contact+'R'+prob+'%.txt'
		infections = np.loadtxt(file)          
		ci = norm.ppf(1-alpha)*infections.std(axis=0)/np.sqrt(N)
		upper = infections.mean(axis=0) + ci
		lower = infections.mean(axis=0) - ci
		ax.plot(days, infections.mean(axis=0), label = '# Infected')
		ax.fill_between(days, upper, lower, alpha=.5)

		# Immune
		file = '../Data/'+'recovered_C'+contact+'R'+prob+'%.txt'
		immune = np.loadtxt(file)         
		ci = norm.ppf(1-alpha)*immune.std(axis=0)/np.sqrt(N)
		upper = immune.mean(axis=0) + ci
		lower = immune.mean(axis=0) - ci
		ax.plot(days, immune.mean(axis=0), label = '# Immune')
		ax.fill_between(days, upper, lower, alpha=.5)

		# # Susceptible
		file = '../Data/'+'susceptible_C'+contact+'R'+prob+'%.txt'
		susceptible = np.loadtxt(file)          
		ci = norm.ppf(1-alpha)*susceptible.std(axis=0)/np.sqrt(N)
		upper = susceptible.mean(axis=0) + ci
		lower = susceptible.mean(axis=0) - ci
		ax.plot(days, susceptible.mean(axis=0), label = '# Susceptible')
		ax.fill_between(days, upper, lower, alpha=.5)

		# Dead
		file = '../Data/'+'deaths_C'+contact+'R'+prob+'%.txt'
		deaths = np.loadtxt(file)         
		ci = norm.ppf(1-alpha)*deaths.std(axis=0)/np.sqrt(N)
		upper = deaths.mean(axis=0) + ci
		lower = deaths.mean(axis=0) - ci
		ax.plot(days, deaths.mean(axis=0), label = '# Deaths')
		ax.fill_between(days, upper, lower, alpha=.5)

		pltnum += 1

fig.suptitle('Infection Dynamics with Network Structure')
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4)
plt.show()