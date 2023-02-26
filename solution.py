import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from body import BODY
import pickle


class SOLUTION:

	def __init__(self, ID, seed):
		# self.dna = [[0,1],[0,1],[0,0]]
		self.seed = seed
		self.myID = ID
		self.Generate_DNA()
		print(self.dna)
		self.body = BODY(self.dna, self.myID, self.seed)


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
		while not os.path.exists("fitness" + str(self.myID) + ".txt"): # do not know if previous simulation finished and fitness file is ready
			time.sleep(0.01)
		fitnessFileName  = f"fitness{self.myID}.txt"
		with open(fitnessFileName, "r") as f:
			self.fitness = float(f.read())
		os.remove(fitnessFileName) # OS specific call


	def Get_Fitness(self):
		return self.fitness
	

	def Mutate(self):
		m = (random.getrandbits(1))
		if m:
			self.body.Mutate_Body()
		self.body.Generate_Body(self.myID)
		if not m:
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