from parallelhillclimber import PARALLEL_HILL_CLIMBER
from world import WORLD
import time
import sys 
import random
import pickle
import os

if __name__ == '__main__':
	seed = sys.argv[1]
	numHiddenLayers = sys.argv[2]
	start_time = time.time()

	# load or create parallel hillclimber object
	if os.path.exists(f"./{seed}/picklePHC.obj"):
		f =  open(f"./{seed}/picklePHC.obj", "rb")
		phc = pickle.load(f)
		print("search.py: loading existing PHC from pickle")
		phc.Resume_From_Pickle()
		startGen = phc.currGen
	else:
		print("search.py: creating new PHC")
		random.seed(seed)
		phc = PARALLEL_HILL_CLIMBER(seed, numHiddenLayers)
		startGen=0

	WORLD()

	try:
		phc.Evolve(startGen)
	except Exception as e:
		print(f"ERROR OCCURRED:\n{e}")
		time.sleep(60) # time to cooldown
	finally:
		phc.Save()
		print(f"\n\nEXITED FOR SEED {phc.seed} at generation {phc.currGen}")
		print("--- %s seconds ---" % (time.time() - start_time))
		# phc.Show_Best()
		