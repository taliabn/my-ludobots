from parallelhillclimber import PARALLEL_HILL_CLIMBER
import time
import sys 
import random

if __name__ == '__main__':
	seed = sys.argv[1]
	start_time = time.time()
	random.seed(seed)
	phc = PARALLEL_HILL_CLIMBER(seed)
	try:
		phc.Evolve()
	except PermissionError:
		print("ERROR: permission error")
	finally:
		print(f"\n\nEXITED FOR SEED {phc.seed}")
		print("--- %s seconds ---" % (time.time() - start_time))
		phc.Save_Fitness_Values()
		# phc.Show_Best()