from parallelhillclimber import PARALLEL_HILL_CLIMBER
import time
import sys 
import random
import pickle
import os

if __name__ == '__main__':
	seed = sys.argv[1]
	start_time = time.time()

	# load or create parallel hillclimber object
	if os.path.exists(f"./{seed}/picklePHC.obj"):
		f =  open(f"./{seed}/picklePHC.obj", "rb")
		phc = pickle.load(f)
		phc.Resume_From_Pickle()
		startGen = phc.currGen
	else:
		random.seed(seed)
		phc = PARALLEL_HILL_CLIMBER(seed)
		startGen=0

	try:
		phc.Evolve(startGen)
	except Exception as e:
		print(f"ERROR OCCURRED:\n{e}")
		time.sleep(5) # time to cooldown
	finally:
		phc.Save()
		print(f"\n\nEXITED FOR SEED {phc.seed} at generation {phc.currGen}")
		print("--- %s seconds ---" % (time.time() - start_time))
		# phc.Show_Best()
		