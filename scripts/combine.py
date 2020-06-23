import os
import re
import numpy as np

os.chdir('results')
tag = '_C20R10%'
names = ['statistics', 'infected', 'recovered', 'susceptible', 'deaths']
names = [name + tag for name in names]

for name in names:
	os.chdir('raw')
	data=[]
	r = re.compile(name)
	files = list(filter(r.match, os.listdir()))
	for file in files:
		line = list(np.loadtxt(file))
		data.append(line)
	data = np.array(data)
	os.chdir('..')
	np.savetxt(name+'.txt', data)
