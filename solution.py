import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c


class SOLUTION:

	def __init__(self, ID):

		self.myID = ID
		self.sensorLinks = []
		self.numLinks = random.randint(2, c.maxNumLinks)


	def Start_Simulation(self, directOrGUI):
		self.Generate_Random_Body()
		self.Generate_Random_Brain()
		# print("\nDONE GENERATING BODY + BRAIN\n")
		# exit()
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


	def Generate_Random_Body(self):
		# pyrosim.Start_URDF(f"body{self.solutionID}.urdf") # stores description of robot's body
		pyrosim.Start_URDF(f"body.urdf") # stores description of robot's body
		
		sensorColor = {0: "Blue", 1: "Green"}
		l, w, h = [random.uniform(c.minSideLen, c.maxSideLen) for dim in range(3)]
		# pos = [0,0,h/2] // always start first link at origin

		has_sensor = random.randint(0,1)
		pyrosim.Send_Cube(name="0", pos=[0, 0, h/2], size=[l, w, h], color=sensorColor[has_sensor])
		if has_sensor:
			self.sensorLinks.append("0")	

		for i in range(1, self.numLinks):
			# print(f"joint name: {i-1}_{i}")
			pyrosim.Send_Joint( name = f"{i-1}_{i}" , parent= f"{i-1}" , child = f"{i}" , 
								type = "revolute", position = [l/2,w/2,0], jointAxis = "0 0 1") #prev block pos
			# pos[x,y] += [l/2, w/2] # prev
			l, w, h = [random.uniform(c.minSideLen, c.maxSideLen) for dim in range(3)]
			has_sensor = random.randint(0,1)		
			pyrosim.Send_Cube(name=f"{i}", pos=[l/2, w/2, h/2], size=[l, w, h], color=sensorColor[has_sensor])
			if has_sensor:
				self.sensorLinks.append(f"{i}")		

		self.numSensorNeurons = len(self.sensorLinks)
		
		pyrosim.End()
		

	def Generate_Body(self):
		pyrosim.Start_URDF("body.urdf") # stores description of robot's body

		# joint naming convention: Parent_Child
		pyrosim.Send_Cube(name="Torso", pos=[0, 0, 0.75] , size=[0.5, 0.5, 0.5],color="Blue")

		pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , 
							type = "revolute", position = [0.25, 0, 0.5], jointAxis = "1 0 0") # absolute
		pyrosim.Send_Cube(name="BackLeg", pos=[0.25, 0.25, -0.25] , size=[0.5, 0.5, 0.5], color="Green")

		pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , 
							type = "revolute", position = [0.-25, 0, 0.5], jointAxis = "1 0 0") # absolute
		pyrosim.Send_Cube(name="FrontLeg", pos=[0.25, 0.25, -0.25] , size=[0.5, 0.5, 0.5],color="Green") # relative

		pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , 
							type = "revolute", position = [0.25, 0, 0.5], jointAxis = "1 0 0") # absolute
		pyrosim.Send_Cube(name="LeftLeg", pos=[-0.25, -0.25, -0.25] , size=[0.5, 0.5, 0.5],color="Green") # relative

		pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , 
							type = "revolute", position = [-0.25, 0, 0.5], jointAxis = "1 0 0") # absolute
		pyrosim.Send_Cube(name="RightLeg", pos=[-0.25, -0.25, -0.25] , size=[0.5, 0.5, 0.5],color="Green") # relative

		pyrosim.End()


	def Generate_Random_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf") # stores description of neural network
		# print(f"total num links {self.numLinks}\n")
		# print(f"NUM SENSOR NEURONS: {numSensorNeurons}\n")
		# print(f"sensor links {self.sensorLinks}\n")

		# create sensor neurons
		for i, link in enumerate(self.sensorLinks):
			# print(f"sensor neuron {i} for link {link}")
			pyrosim.Send_Sensor_Neuron(name = i, linkName = f"{link}")

		offset = self.numSensorNeurons + c.numHiddenNeurons
		# create hidden neurons
		for i in  range(self.numSensorNeurons, offset):
			# print(f"hidden neuron {i}")
			pyrosim.Send_Hidden_Neuron(name = i)
		# create motor neurons
		for i in range(1, self.numLinks):
			# print(f"motor neuron {i  + offset} for joint {i-1}_{i}")
			pyrosim.Send_Motor_Neuron(name = i + offset, jointName = f"{i-1}_{i}")
		
		# initialize neuron weights
		self.weights = [np.random.rand(c.numHiddenNeurons, self.numSensorNeurons) * 2 - 1,
						np.random.rand(c.numHiddenNeurons, self.numLinks) * 2 - 1,]
		# print(f"self.weights: {self.weights}")
		# create synapses
		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(self.numSensorNeurons):
				pyrosim.Send_Synapse(sourceNeuronName = currColumn, 
			 						targetNeuronName = currRow + self.numSensorNeurons, 
									weight = self.weights[0][currRow][currColumn])

		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(self.numLinks):
				pyrosim.Send_Synapse(sourceNeuronName = currRow + self.numSensorNeurons, 
			 						targetNeuronName = currColumn + self.numSensorNeurons + c.numHiddenNeurons, 
									weight = self.weights[1][currRow][currColumn])
				
		pyrosim.End()
	

	def Generate_Brain(self):
		pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf") # stores description of neural network

		# create sensor neurons
		pyrosim.Send_Sensor_Neuron(name = 0, linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 1, linkName = "FrontLeg")
		pyrosim.Send_Sensor_Neuron(name = 2, linkName = "RightLeg")
		pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLeg")
		
		# create hidden neurons
		pyrosim.Send_Hidden_Neuron(name = 4)
		pyrosim.Send_Hidden_Neuron(name = 5)
		pyrosim.Send_Hidden_Neuron(name = 6)
		pyrosim.Send_Hidden_Neuron(name = 7)

		# create motor neurons
		pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_FrontLeg")
		pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_RightLeg")
		pyrosim.Send_Motor_Neuron(name = 11, jointName = "Torso_LeftLeg")

		# create synapses
		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(c.numSensorNeurons):
				pyrosim.Send_Synapse(sourceNeuronName = currColumn, 
			 						targetNeuronName = currRow + c.numSensorNeurons, 
									weight = self.weights[0][currRow][currColumn])

		for currRow in range(c.numHiddenNeurons):
			for currColumn in range(c.numMotorNeurons):
				pyrosim.Send_Synapse(sourceNeuronName = currRow + c.numSensorNeurons, 
			 						targetNeuronName = currColumn + c.numSensorNeurons + c.numHiddenNeurons, 
									weight = self.weights[1][currRow][currColumn])

		pyrosim.End()
	

	def Mutate(self):
		randomRow = random.randint(0, c.numHiddenNeurons - 1)
		# change weight of a random sensor neuron synapse
		randomSensorColumn = random.randint(0, self.numSensorNeurons - 1)
		self.weights[0][randomRow][randomSensorColumn] = random.random() * 2 - 1
		# change weight of a random motor neuron synapse
		randomMotorColumn = random.randint(0, self.numSensorNeurons - 1)
		self.weights[1][randomRow][randomMotorColumn] = random.random() * 2 - 1


	def Set_ID(self, newID):
		self.myID = newID