import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c


class SOLUTION:

	def __init__(self, ID):
		self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
		self.weights = self.weights *2 - 1 # scale to range [-1, 1]
		self.myID = ID


	def Start_Simulation(self, directOrGUI):
		# self.Generate_Body()
		self.Generate_Brain()
		IDstr = str(self.myID)
		os.system("start /B python simulate.py " + directOrGUI + " " + IDstr) # OS specific call


	def Wait_For_Simulation_To_End(self):
		while not os.path.exists("fitness" + str(self.myID) + ".txt"): # do not know if previous simulation finished and fitness file is ready
			time.sleep(0.01)
		fitnessFileName  = f"fitness{self.myID}.txt"
		with open(fitnessFileName, "r") as f:
			self.fitness = float(f.read())
		os.remove(fitnessFileName) # OS specific call
		# print(self.fitness)


	def Get_Fitness(self):
		return self.fitness


	def Generate_Body(self):
		pyrosim.Start_URDF("body.urdf") # stores description of robot's body
		width, length, height = 1, 1, 1 # link dimensions

		# joint naming convention: Parent_Child
		pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1] , size=[1, 1, 0.5])

		pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , 
							type = "revolute", position = [0, -0.5, 1], jointAxis = "0 1 0") # absolute
		pyrosim.Send_Cube(name="BackLeg", pos=[0, 0, -0.5] , size=[0.25, 0.25, 1])

		pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , 
							type = "revolute", position = [0, 0.5, 1], jointAxis = "0 1 0") # absolute
		pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0, -0.5] , size=[0.25, 0.25, 1]) # relative

		pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , 
							type = "revolute", position = [-0.5, 0, 1], jointAxis = "1 0 0") # absolute
		pyrosim.Send_Cube(name="LeftLeg", pos=[0, 0, -0.5] , size=[0.25, 0.25, 1]) # relative

		pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , 
							type = "revolute", position = [0.5, 0, 1], jointAxis = "1 0 0") # absolute
		pyrosim.Send_Cube(name="RightLeg", pos=[0, 0, -0.5] , size=[0.25, 0.25, 1]) # relative

		pyrosim.Send_Joint(name = "Torso_MiddleLeg" , parent= "Torso" , child = "MiddleLeg" , 
							type = "prismatic", position = [0, 0, 1], jointAxis = "0 0 1") # absolute
		pyrosim.Send_Cube(name="MiddleLeg", pos=[0, 0, -0.5] , size=[0.25, 0.25, 0.9]) # relative

		pyrosim.End()


	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf") # stores description of neural network

		# create sensor neurons
		pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
		pyrosim.Send_Sensor_Neuron(name = 3, linkName = "RightLeg")
		pyrosim.Send_Sensor_Neuron(name = 4, linkName = "LeftLeg")
		pyrosim.Send_Sensor_Neuron(name = 5, linkName = "MiddleLeg")


		# create motor neurons
		pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso_FrontLeg")
		pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso_RightLeg")
		pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_LeftLeg")
		pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_MiddleLeg")


		# create synapses
		for currentRow in range(c.numSensorNeurons):
			for currentColumn in range(c.numMotorNeurons):
				pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

		pyrosim.End()


	def Mutate(self):
		randomRow = random.randint(0, 2)
		randomColumn = random.randint(0, 1)
		self.weights[randomRow][randomColumn] = random.random() * 2 - 1

	def Set_ID(self, newID):
		self.myID = newID