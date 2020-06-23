#!/bin/bash
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=sim
#SBATCH -c 1
#SBATCH -a 1-1000

contacts=20
infection_rate=0.1

python3 infection_simulation.py $contacts $infection_rate
