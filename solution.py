import pyrosim.pyrosim as pyrosim
import os
import random
import constants as c
from body import BODY


class SOLUTION:

	def __init__(self, ID, seed, numHiddenLayers):
		self.seed = seed
		self.myID = ID
		self.Generate_DNA()
		self.body = BODY(self.dna, self.myID, self.seed, numHiddenLayers)


	def Generate_DNA(self):
		self.dna = [[random.randint(0, c.maxNumSelfEdges),random.randint(1,c.maxNumChildEdges)] 
	      				for node in range(random.randint(2, (c.maxNumNodes)))]
		self.dna[-1][-1] = 0


	def Get_Fitness(self):
		return self.fitness
	

	def Set_Fitness(self, displacement):
		# self.fitness = round(displacement/self.body.wingspan, 3) # num body lengths moved
		self.fitness = round(displacement, 3)


	def Reset_Fitness(self):
		self.fitness = None


	def Mutate(self, generation):
		# less likely to mutate body for later generations
		probBody = 0.5 - 0.45*generation/c.numberOfGenerations
		mutBody = random.choices(population=[0,1], weights=[1-probBody, probBody])[0]

		# for last 25 generations, only mutate brain to allow for fine motor control
		# mutBrain = (c.numberOfGenerations - generation) < 25 or (random.getrandbits(1))
		# probBody = random.getrandbits(1) # equally likely to mutate brain or body
		if mutBody:
			self.body.Mutate_Body()
		self.body.Generate_Body(self.myID)
		if not mutBody:
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