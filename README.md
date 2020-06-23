# Simulating the Spread of an Infection through Networks

This repository contains my final project for STOR-672: Simulation Modeling and Analysis, a course I took with Dr. Mariana Olvera-Cravioto
at the University of North Carolina in Spring 2020. The report in this repo `Final Project.pdf` describes a continuous-time model for 
simulating the spread of disease through a graph network. The parameters of the model are selected to mimic the conditions of the spread
of COVID-19 in a small city. Multiple experiments are conducted to test the effect of social distancing on slowing the spread of disease.

If you have access to a cluster with Slurm Workload Manager, then you can clone this repo and conduct your own infection simulations.
Simulations are relatively easy to set up with the [infection_simulation.sh](scripts/infection_simulation.sh) script. 

```
#!/bin/bash
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=sim
#SBATCH -c 1
#SBATCH -a 1-1000

contacts=20
infection_rate=0.1

python3 infection_simulation.py $contacts $infection_rate
```

Simply change the assumed number of average `contacts` each agent in the model has and the assumed `infection_rate`. The output will be saved
in [results/raw/](results/raw/) and you will need to run [combine.py](scripts/combine.py) to the files into a usable format. 
