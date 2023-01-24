from solution import SOLUTION
import numpy as np
import constants as c
import copy

class HILL_CLIMBER:

	def __init__(self):
		self.parent = SOLUTION()


	def Evolve(self):
		self.parent.Evaluate("GUI")
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()

	
	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.child.Evaluate("DIRECT")
		self.Print()
		self.Select()

	
	def Spawn(self):
		self.child = copy.deepcopy(self.parent)
		pass

	
	def Mutate(self):
		self.child.Mutate()

	
	def Select(self):
		# parent's fitness is worse than child's
		if self.parent.fitness > self.child.fitness:
			self.parent = self.child
		pass


	def Print(self):
		print(f"\nparent's fitness: {self.parent.fitness}, child's fitness: {self.child.fitness}")

	
	def Show_Best(self):
		self.parent.Evaluate("GUI")