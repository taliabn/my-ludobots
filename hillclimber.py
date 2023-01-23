from solution import SOLUTION
import numpy as np

class HILL_CLIMBER:

	def __init__(self):
		self.parent = SOLUTION()


	def Evolve(self):
		self.parent.Evaluate()