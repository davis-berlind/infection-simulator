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
for prob in probs:
	ax = fig.add_subplot(1, 2, pltnum)  # create an axes object in the figure
	ax.set_title('Infection Rate = ' + prob + '%')
	ax.set_xlabel('Days')
	for contact in contacts:
		# Infections
		file = '../Data/'+'infected_C'+contact+'R'+prob+'%.txt'
		infections = np.loadtxt(file)          
		ci = norm.ppf(1-alpha)*infections.std(axis=0)/np.sqrt(N)
		upper = infections.mean(axis=0) + ci
		lower = infections.mean(axis=0) - ci
		ax.plot(days, infections.mean(axis=0), label = contact + " Contacts")
		ax.fill_between(days, upper, lower, alpha=.5)

	pltnum += 1
ax.legend()
fig.suptitle('Effect of Number of Contatcts on Infection Duration')

plt.show()