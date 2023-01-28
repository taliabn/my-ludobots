from solution import SOLUTION
import constants as c
import copy
import os
from datetime import datetime
import pyrosim.pyrosim as pyrosim


class PARALLEL_HILL_CLIMBER:
	def __init__(self):
		os.system("rm brain*.nndf")
		os.system("rm fitness*.txt")

		self.parents = {}
		self.nextAvailableID = 0

		pyrosim.Start_SDF("world.sdf")
		pyrosim.End()

		for i in range(c.populationSize):
			self.parents[i] = SOLUTION(self.nextAvailableID)
			self.nextAvailableID += 1


	def Evolve(self):
		self.Evaluate(self.parents)
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()

	
	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children)
		self.Print()
		self.WriteToLog()
		self.Select()


	def Evaluate(self, solutions):
		for solution in solutions.values():
			print(solution)
			solution.Start_Simulation("DIRECT")
		for solution in solutions.values():
			solution.Wait_For_Simulation_To_End()
			print(solution.fitness)
	

	def Spawn(self):
		self.children = {}
		for i, parent in self.parents.items():
			self.children[i] = copy.deepcopy(parent)
			self.children[i].Set_ID(self.nextAvailableID)
			self.nextAvailableID += 1

	
	def Mutate(self):
		for child in self.children.values():
			child.Mutate()

	
	def Select(self):
		# parent's fitness is worse than child's
		for key in self.parents.keys():
			if self.parents[key].fitness > self.children[key].fitness:
				self.parents[key] = self.children[key]


	def WriteToLog(self):
		with open("log.txt", 'a') as f:
			f.write(f'\n\n\n{datetime.now().strftime("%H:%M:%S")}\n')
			for key in self.parents.keys():
				f.write(f"soln ID: parent {self.parents[key].myID}, child {self.children[key].myID}\n")
				f.write(f"{key}: parent's fitness = {self.parents[key].fitness}, child's fitness: {self.children[key].fitness}\n")

		
	def Print(self):
		for key in self.parents.keys():
			print(f"\n{key}: parent's fitness = {self.parents[key].fitness}, child's fitness: {self.children[key].fitness}\n")
		
	
	def Show_Best(self):
		winning_parent = self.parents[0]
		winning_fitness = self.parents[0].fitness
		for parent in self.parents.values():
			if parent.fitness > winning_fitness:
				winning_fitness = parent.fitness 
				winning_parent = parent
		print(f"winning parent: {winning_parent}")
		winning_parent.Start_Simulation("GUI")