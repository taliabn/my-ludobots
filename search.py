from parallelhillclimber import PARALLEL_HILL_CLIMBER


phc = PARALLEL_HILL_CLIMBER()
try:
	phc.Evolve()
except PermissionError:
	print("ERROR: permission error")
finally:
	phc.Show_Best()