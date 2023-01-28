import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random


class SOLUTION:

	def __init__(self):
		self.weights = np.random.rand(3,2)
		self.weights = self.weights *2 - 1 # scale to range [-1, 1]

	
	def Evaluate(self, directOrGUI):
		self.Create_World()
		self.Generate_Body()
		self.Generate_Brain()

		os.system("start /B python simulate.py " + directOrGUI ) # specific to windows

		fitnessFile = "./data/fitness.txt"
		with open(fitnessFile, "r") as f:
			self.fitness = float(f.read())


	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		width, length, height = 1, 1, 1 # box dimensions
		pyrosim.Send_Cube(name="Box", pos=[-2, -2, 0.5] , size=[width, length, height])
		pyrosim.End()


	def Generate_Body(self):
		pyrosim.Start_URDF("body.urdf") # stores description of robot's body
		width, length, height = 1, 1, 1 # link dimensions

		# joint naming convention: Parent_Child
		pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5] , size=[width, length, height])
		pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , 
							type = "revolute", position = [1.0, 0, 1.0])
		pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[length, height, width])
		pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , 
							type = "revolute", position = [2.0, 0, 1.0])
		pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[length, height, width])

		pyrosim.End()


	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork("brain.nndf") # stores description of neural network

		# create sensor neurons
		pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")

		# create motor neurons
		pyrosim.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")
		# create synapses
		for currentRow in range(3):
			for currentColumn in range(2):
				pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + 3 , weight = self.weights[currentRow][currentColumn])

		pyrosim.End()


	def Mutate(self):
		randomRow = random.randint(0, 2)
		randomColumn = random.randint(0, 1)
		self.weights[randomRow][randomColumn] = random.random() * 2 - 1