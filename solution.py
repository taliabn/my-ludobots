import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from body import BODY
import pickle
from simulation import SIMULATION

class SOLUTION:

	def __init__(self, ID, seed):
		# self.dna = [[2,2], [1,0]]
		self.seed = seed
		self.myID = ID
		self.Generate_DNA()
		# print(self.dna)
		self.body = BODY(self.dna, self.myID, self.seed)


	# def Run_Parallel_Simulation(self, directOrGUI):
	# 	print(f"\n STARTING SEIMULATION FOR SEED {self.seed}, SOLUTION {self.myID}\n")
	# 	simulation = SIMULATION(directOrGUI, self.myID, self.seed)
	# 	simulation.Run()
	# 	self.fitness =  simulation.Return_Displacement()


	def Start_Simulation(self, directOrGUI):
		# self.body.Save()
		# with open(f'BODY{self.myID}.pickle', 'rb') as handle:
		# 	self.body = pickle.load(handle)
		os.system(f"start /B python simulate.py  {directOrGUI} {self.myID} {self.seed}") # OS specific call


	def Generate_DNA(self):
		self.dna = [[random.randint(0, c.maxNumSelfEdges),random.randint(1,c.maxNumChildEdges)] 
	      				for node in range(random.randint(2, (c.maxNumNodes)))]
		self.dna[-1][-1] = 0


	def Wait_For_Simulation_To_End(self):
		print(f"WAITING FOR {self.myID}.....")
		while not os.path.exists("displacement" + str(self.myID) + ".txt"): # do not know if previous simulation finished and fitness file is ready
			time.sleep(0.01)
		print(f"ESCAPED WAIT, READING DISPLACEMENT FILE FOR {self.myID}")
		displacementFileName  = f"displacement{self.myID}.txt"
		with open(displacementFileName, "r") as f:
			displacement = float(f.read())
		self.fitness = displacement/self.body.wingspan
		os.remove(displacementFileName) # OS specific call
		print(f"REMOVED DISPLACEMENT FILE FOR {self.myID}")


	def Get_Fitness(self):
		return self.fitness
	

	def Set_Fitness(self, displacement):
		self.fitness = round(displacement/self.body.wingspan, 3)


	def Reset_Fitness(self):
		self.fitness = None


	def Mutate(self, generation):
		# less likely to mutate body for later generations
		probBody = 0.5 - 0.45*generation/c.numberOfGenerations
		mutBody = random.choices(population=[0,1], weights=[1-probBody, probBody])[0]
		# m = (random.getrandbits(1))
		if mutBody:
			print(f"ID: {self.myID}, gen: {generation}, mutating BODY")
			self.body.Mutate_Body()
		self.body.Generate_Body(self.myID)
		if not mutBody:
			print(f"ID: {self.myID}, gen: {generation}, mutating BRAIN")
			self.body.Mutate_Brain()
		self.body.Generate_Brain(self.myID)


	def Set_ID(self, newID):
		self.myID = newID


	def Delete_Files(self):
		try:
			os.remove(f"./{self.seed}/brain{self.myID}.nndf") # parent was worse
			os.remove(f"./{self.seed}/body{self.myID}.urdf") # parent was worse
		except FileNotFoundError:
			print(f"Files for {self.myID} with seed {self.seed} is not present in the system.")