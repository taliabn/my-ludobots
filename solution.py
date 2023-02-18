import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from body import BODY


class SOLUTION:

	def __init__(self, ID):
		self.dna = [[3,2],[1,1]]	
		self.myID = ID
		self.body = BODY(self.dna, self.myID)
		self.Generate_Random_Brain()
		# self.sensorLinks = []
		# self.numLinks = random.randint(2, c.maxNumLinks)
		


	def Start_Simulation(self, directOrGUI):
		# self.body = BODY(self.dna, self.myID)
		# self.Generate_Random_Brain()
		IDstr = str(self.myID)
		os.system("start /B python simulate.py " + directOrGUI + " " + IDstr) # OS specific call


	def Wait_For_Simulation_To_End(self):
		while not os.path.exists("fitness" + str(self.myID) + ".txt"): # do not know if previous simulation finished and fitness file is ready
			time.sleep(0.01)
		fitnessFileName  = f"fitness{self.myID}.txt"
		with open(fitnessFileName, "r") as f:
			self.fitness = float(f.read())
		os.remove(fitnessFileName) # OS specific call


	def Get_Fitness(self):
		return self.fitness


	# def Generate_Random_Body(self):
	# 	if os.path.exists(f"body{self.myID}.urdf"):
	# 		return
	# 	pyrosim.Start_URDF(f"body{self.myID}.urdf") # stores description of robot's body
		
	# 	sensorColor = {0: "Blue", 1: "Green"}
	# 	l, w, h = [random.uniform(c.minSideLen, c.maxSideLen) for dim in range(3)]
	# 	has_sensor = random.randint(0,1)
	# 	pyrosim.Send_Cube(name="0", pos=[l/2, w/2, h/2], size=[l, w, h], color=sensorColor[has_sensor])
	# 	if has_sensor:
	# 		self.sensorLinks.append("0")	

	# 	for i in range(1, self.numLinks):
	# 		pyrosim.Send_Joint(name = f"{i-1}_{i}" , parent= f"{i-1}" , child = f"{i}" , 
	# 						   type = "spherical", position = [l, w, 0], jointAxis = "0 0 1") # prev block pos
	# 		l, w, h = [random.uniform(c.minSideLen, c.maxSideLen) for dim in range(3)]
	# 		has_sensor = random.randint(0,1)		
	# 		pyrosim.Send_Cube(name=f"{i}", pos=[l/2, w/2, h/2], size=[l, w, h], color=sensorColor[has_sensor])
	# 		if has_sensor:
	# 			self.sensorLinks.append(f"{i}")		

	# 	self.numSensorNeurons = len(self.sensorLinks)
	# 	pyrosim.End()


	def Generate_Random_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf") # stores description of neural network

		# create sensor neurons
		for i, link in enumerate(self.body.sensorLinks):
			# print(f"sensor neuron {i} for link {link}")
			pyrosim.Send_Sensor_Neuron(name = i, linkName = f"{link}")
		# create hidden neurons
		for i in  range(self.body.numSensorNeurons, self.body.numSensorNeurons + c.numHiddenNeurons):
			pyrosim.Send_Hidden_Neuron(name = i)
		# create motor neurons
		for i in range(1, self.body.numLinks):
			pyrosim.Send_Motor_Neuron(name = i + self.body.numSensorNeurons + c.numHiddenNeurons,
			     					  jointName = f"{i-1}_{i}")
		
		# initialize neuron weights
		self.weights = [np.random.rand(c.numHiddenNeurons, self.body.numSensorNeurons) * 2 - 1,
						np.random.rand(c.numHiddenNeurons, self.body.numLinks) * 2 - 1,]
		
		# create synapses for sensor neurons to hidden neurons
		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(self.body.numSensorNeurons):
				pyrosim.Send_Synapse(sourceNeuronName = currColumn, 
			 						targetNeuronName = currRow + self.body.numSensorNeurons, 
									weight = self.weights[0][currRow][currColumn])

		# create synapses for hidden neurons to motor neurons
		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(self.body.numLinks):
				pyrosim.Send_Synapse(sourceNeuronName = currRow + self.body.numSensorNeurons, 
			 						targetNeuronName = currColumn + self.body.numSensorNeurons + c.numHiddenNeurons, 
									weight = self.weights[1][currRow][currColumn])
				
		pyrosim.End()
	

	def Mutate(self):
		randomRow = random.randint(0, c.numHiddenNeurons - 1)
		# change weight of a random sensor neuron synapse, if at least one exists
		if self.numSensorNeurons > 0:
			randomSensorColumn = random.randint(0, self.body.numSensorNeurons - 1)
			self.weights[0][randomRow][randomSensorColumn] = random.random() * 2 - 1
		# change weight of a random motor neuron synapse
		randomMotorColumn = random.randint(0, self.body.numLinks - 1)
		self.weights[1][randomRow][randomMotorColumn] = random.random() * 2 - 1


	def Set_ID(self, newID):
		self.myID = newID