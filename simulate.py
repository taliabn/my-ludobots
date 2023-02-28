import sys
from simulation import SIMULATION

if __name__ == '__main__':
	directOrGUI = sys.argv[1]
	solutionID = sys.argv[2]
	seed = sys.argv[3]
	print(f"\n STARTING SIMULATION for seed {seed}, solution {solutionID}\n")
	simulation = SIMULATION(directOrGUI, solutionID, seed)
	simulation.Run()
	fitness = simulation.Return_Displacement()
	print(f"\n Final displacement for seed {seed}, solution {solutionID}: {fitness}\n")
