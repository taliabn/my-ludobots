import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from body import BODY
import pickle


class SOLUTION:

	def __init__(self, ID):
		# self.dna = [[0,1],[0,1],[0,0]]
		self.myID = ID
		self.Generate_DNA()
		self.body = BODY(self.dna, self.myID)
		self.Generate_Random_Brain()


	def Start_Simulation(self, directOrGUI):
		# print(self.dna)
		# self.body.Save()
		# with open(f'BODY{self.myID}.pickle', 'rb') as handle:
		# 	self.body = pickle.load(handle)
		IDstr = str(self.myID)
		os.system("start /B python simulate.py " + directOrGUI + " " + IDstr) # OS specific call


	def Generate_DNA(self):
		self.dna = [[random.randint(0, c.maxNumSelfEdges),random.randint(1,c.maxNumChildEdges)] 
	      				for node in range(random.randint(2, (c.maxNumNodes)))]

	def Wait_For_Simulation_To_End(self):
		while not os.path.exists("fitness" + str(self.myID) + ".txt"): # do not know if previous simulation finished and fitness file is ready
			time.sleep(0.01)
		fitnessFileName  = f"fitness{self.myID}.txt"
		with open(fitnessFileName, "r") as f:
			self.fitness = float(f.read())
		os.remove(fitnessFileName) # OS specific call


	def Get_Fitness(self):
		return self.fitness


	def Generate_Random_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf") # stores description of neural network
		# print(self.body.allLinks)
		# print(self.body.allJoints)

		print("GENERATING BRAIN\n\n")

		numLinks = len(self.body.allLinks)
		numSensorNeurons = len(self.body.sensorLinks)

		neuronName = 0
		# create sensor neurons
		for link in self.body.sensorLinks:
			# print(f"sensor neuron {neuronName} for link {link}")
			pyrosim.Send_Sensor_Neuron(name = neuronName, linkName = f"{link}")
			neuronName += 1
		# create hidden neurons
		for i in  range(c.numHiddenNeurons):
			# print(f"hidden neuron {neuronName}")
			pyrosim.Send_Hidden_Neuron(name = neuronName)
			neuronName += 1
		# create motor neurons
		for joint in self.body.allJoints:
			# print(f"motor neuron {neuronName} for joint {joint}")
			pyrosim.Send_Motor_Neuron(name = neuronName,
			     					  jointName = joint)
			neuronName += 1
		
		# initialize neuron weights
		self.weights = [np.random.rand(c.numHiddenNeurons, numSensorNeurons) * 2 - 1,
						np.random.rand(c.numHiddenNeurons, numLinks) * 2 - 1,]
		
		# print("sensor to hidden:")
		# create synapses for sensor neurons to hidden neurons
		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(numSensorNeurons):
				pyrosim.Send_Synapse(sourceNeuronName = currColumn, 
			 						targetNeuronName = currRow + numSensorNeurons, 
									weight = self.weights[0][currRow][currColumn])
				# print(f"src = {currColumn} --> dst = {currRow + numSensorNeurons}")
		# print("hidden to motor")
		# create synapses for hidden neurons to motor neurons
		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(len(self.body.allJoints)): # 1 less joint than motor neuron
				pyrosim.Send_Synapse(sourceNeuronName = currRow + numSensorNeurons, 
			 						targetNeuronName = currColumn + numSensorNeurons + c.numHiddenNeurons, 
									weight = self.weights[1][currRow][currColumn])
				# print(f"src = {currRow + numSensorNeurons} --> dst = {currColumn + numSensorNeurons + c.numHiddenNeurons}")
				
		pyrosim.End()
	

	def Mutate(self):
		randomRow = random.randint(0, c.numHiddenNeurons - 1)
		# change weight of a random sensor neuron synapse, if at least one exists
		if self.body.numSensorNeurons > 0:
			randomSensorColumn = random.randint(0, self.body.numSensorNeurons - 1)
			self.weights[0][randomRow][randomSensorColumn] = random.random() * 2 - 1
		# change weight of a random motor neuron synapse
		randomMotorColumn = random.randint(0, self.body.numLinks - 1)
		self.weights[1][randomRow][randomMotorColumn] = random.random() * 2 - 1


	def Set_ID(self, newID):
		self.myID = newID