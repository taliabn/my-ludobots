from solution import SOLUTION
import numpy as np

class HILL_CLIMBER:

	def __init__(self):
		self.parent = SOLUTION()
		self.weights = np.random.rand(3,2)
		self.weights = self.weights *2 - 1 # scale to range [-1, 1]