from parallelhillclimber import PARALLEL_HILL_CLIMBER
import time
if __name__ == '__main__':
	start_time = time.time()
	phc = PARALLEL_HILL_CLIMBER()
	try:
		phc.Evolve()
	except PermissionError:
		print("ERROR: permission error")
	finally:
		print(f"\n\nEXITED FOR SEED {phc.seed}")
		print("--- %s seconds ---" % (time.time() - start_time))
		phc.Save_Fitness_Values()
		# phc.Show_Best()