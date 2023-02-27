import numpy as np
import sys
# import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c
from simulation import SIMULATION

if __name__ == '__main__':
	directOrGUI = sys.argv[1]
	solutionID = sys.argv[2]
	seed = sys.argv[3]
	print(f"\n STARTING SEIMULATION FOR SEED {seed}, SOLUTION {solutionID}\n")
	simulation = SIMULATION(directOrGUI, solutionID, seed)
	simulation.Run()
	simulation.Record_Displacement()
