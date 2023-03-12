import copy
import os
from datetime import datetime
import pyrosim.pyrosim as pyrosim
import numpy as np
import pickle
from pathos.multiprocessing import ProcessingPool as Pool
from solution import SOLUTION
from simulation import SIMULATION
import constants as c
import random


class PARALLEL_HILL_CLIMBER:

	def __init__(self, seed, numHiddenLayers):
		self.seed = seed
		self.numHiddenLayers = numHiddenLayers

		if not os.path.exists(f"./{self.seed}"):
			os.makedirs(f"./{self.seed}")
		else:
			raise Exception(f"ERROR: SEED DIR ALREADY EXISTS")
		
		self.fitnessValues = np.empty((c.numberOfGenerations, c.populationSize))
		self.parents = {}
		self.nextAvailableID = 0
		self.currGen = 0


		for i in range(c.populationSize):
			self.parents[i] = SOLUTION(self.nextAvailableID, self.seed, self.numHiddenLayers)
			self.nextAvailableID += 1


	def Save(self):
		self.Save_Fitness_Values()
		f =  open(f"./{self.seed}/picklePHC.obj", "wb")
		pickle.dump(self, f)
		print(f"SAVING TO PICKLE AT GENERATION {self.currGen}")


	def Resume_From_Pickle(self):
		print(f"\n\nRESUMING FROM PICKLE AT GENERATION {self.currGen}\n\n")
		random.setstate(self.state) # restore random state
		self.fitnessValues = np.load(f"./{self.seed}/fitnessValues.npy")
		if c.numberOfGenerations > len(self.fitnessValues):
			extra = c.numberOfGenerations - len(self.fitnessValues)
			print(f"Allocating {extra} additional rows in fitness values array")
			self.fitnessValues = np.append(self.fitnessValues, np.empty((extra, c.populationSize)), axis=0)


	def Evolve(self, startingGeneration):
		self.Evaluate(self.parents)
		for currentGeneration in range(startingGeneration, c.numberOfGenerations):
			print(f"\n\n################ CURRENT GENERATION: {currentGeneration} ################ ")
			self.state = random.getstate() # save state in case there's an error
			self.Evolve_For_One_Generation(currentGeneration)
			self.fitnessValues[currentGeneration, :] = np.array([parent.fitness for parent in self.parents.values()])
			self.Save()
			self.currGen += 1
		
	
	def Evolve_For_One_Generation(self, currentGeneration):
		self.Spawn()
		self.Mutate(currentGeneration)
		self.Evaluate(self.children)
		self.Print()
		# self.WriteToLog()
		self.Select()


	def Evaluate(self, solutions):
		# task to run
		def Run_Parallel_Simulation(solutionID):
			simulation = SIMULATION("DIRECT", solutionID, self.seed)
			simulation.Run()
			displacement = simulation.Return_Displacement()
			return displacement
		
		# workers = mp.cpu_count() - 1 = 7
		pool = Pool(processes = 7)
		inputs = [solution.myID for solution in solutions.values()]
		outputs = pool.map(Run_Parallel_Simulation, inputs)
		for i, solution in solutions.items():
			solution.Set_Fitness(displacement = outputs[i])


	def Spawn(self):
		self.children = {}
		for i, parent in self.parents.items():
			self.children[i] = copy.deepcopy(parent)
			self.children[i].Set_ID(self.nextAvailableID)
			self.children[i].Reset_Fitness()
			self.nextAvailableID += 1

	
	def Mutate(self, currentGeneration):
		for child in self.children.values():
			child.Mutate(currentGeneration)


	def Select(self):
		for key in self.parents.keys():
			# minimize fitness
			if self.parents[key].fitness > self.children[key].fitness:
				self.parents[key].Delete_Files()
				self.parents[key] = self.children[key]
			else:
				self.children[key].Delete_Files()


	def WriteToLog(self):
		with open("log.txt", 'a') as f:
			f.write(f'\n\n\n{datetime.now().strftime("%H:%M:%S")}\n')
			for key in self.parents.keys():
				f.write(f"soln ID: parent {self.parents[key].myID}, child {self.children[key].myID}\n")
				f.write(f"{key}: parent's fitness = {self.parents[key].fitness}, child's fitness: {self.children[key].fitness}\n")

		
	def Print(self):
		print("\n")
		for key in self.parents.keys():
			print(f"parent {self.parents[key].myID} fitness = {self.parents[key].fitness}, child {self.children[key].myID} fitness: {self.children[key].fitness}")
		print("\n")
		

	def Get_Best(self):
		winning_parent = self.parents[0]
		winning_fitness = self.parents[0].Get_Fitness()
		for parent in self.parents.values():
			if parent.Get_Fitness() < winning_fitness:
				winning_fitness = parent.Get_Fitness() 
				winning_parent = parent
		return winning_parent


	def Show_Best(self):
		winning_parent = self.Get_Best()
		print("SHOWING BEST")
		print(f"BEST FITNESS: {winning_parent.fitness} from solution {winning_parent.myID}")
		winning_parent.Start_Simulation("GUI")


	def Save_Fitness_Values(self):
		w = self.Get_Best()
		print(f"WINNER for seed {self.seed} at generation {self.currGen}: solution {w.myID} with fitness {w.fitness}")
		file_path = f"./{self.seed}/fitnessValues"
		try:
			np.save(file_path, self.fitnessValues)
		except:
			print(f"ERROR: Unable to save fitness values")