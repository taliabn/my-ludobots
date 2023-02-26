import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import constants as c
import pickle


class uniqueNode:

	def __init__(self, numSelfEdge, numChildEdge, orientationsQueue):
		# from dna:
		self.numSelfEdge: int = numSelfEdge
		self.numChildEdge: int = numChildEdge

		# randomly chosen:
		self.has_sensor: bool = bool(random.getrandbits(1)) # random
		self.Set_Color()
		# self.orientation = random.choice(orientationsQueue)
		# get random orientation that isn't the previous one
		self.orientation = orientationsQueue.pop(0)
		random.shuffle(orientationsQueue)
		orientationsQueue.append(self.orientation)

		# possibly change min/max side length to be encoded in dna?
		self.dims = np.array([round(random.uniform(c.minSideLen, c.maxSideLen), 1)
											for dim in range(3)]) #random

	def Set_Color(self):
		if self.has_sensor:
			self.color = "Green"
		else:
			self.color = "Blue"

	def Print(self):
		print(f"class uniqueNode:\n\tnumSelfEdge: {self.numSelfEdge}\n\tnumChildEdge: {self.numChildEdge} \
			\n\thas_sensor: {self.has_sensor}\n\torientation: {self.orientation}\n\tdims: {self.dims}\n")


	def axisStr(self):
		return f"{self.orientation[0]} {self.orientation[1]} {self.orientation[2]}"


class BODY:

	def __init__(self, dna, solutionID, seed):
		self.seed = seed
		self.dna = dna # list of [num selfEdges, num nextEdges] pairs
		self.orientationsQueue = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]
		# orientationsQueue = [np.array([0,0,1]), np.array([0,1,0])]
		random.shuffle(self.orientationsQueue)
		# initialize graph nodes
		self.uniqueNodeList = [uniqueNode(instruction[0], instruction[1], self.orientationsQueue)
							  	  for instruction in self.dna]
		self.PrintUniqueNodes()
		self.initialPos = np.array([0, 0, 3])
		self.Generate_Body(solutionID)
		self.prevSensortoHiddenWeights = {} # {link name: float [-1,1]}
		self.prevHiddentoMotorWeights = {} # {joint name: float [-1,1]}
		self.currSensortoHiddenWeights = {} # {link name: float [-1,1]}
		self.currHiddentoMotorWeights = {} # {joint name: float [-1,1]}
		self.Generate_Brain_nndf(solutionID)


	def PrintUniqueNodes(self):
		for node in self.uniqueNodeList:
			node.Print()


	def SaveToPickle(self, ID):
		with open(f'BODY{ID}.pickle', 'wb') as handle:
			pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)


	def fetchLinkID(self):
		self.availableLinkID += 1
		return self.availableLinkID


	def switchDirection(self, dir, orientation):
		return np.logical_not(orientation)*dir + orientation*-1 #type: ignore
	

	def has_space(self, absPos, size, tol=0.01):
		if [absPos - size/2][0][2] <= 0:
			# below floor
			# print(f"has_space false: underground")
			return False 
		for block in self.filledSpaces:
			if (sum(block[0] >= (absPos + size/2)) == 0) and  (sum((absPos - size/2) >= block[1]) == 0):
				# print(f"has_space false: overlapped with : {block}")
				return False	#overlap

		return True
	

	def fill_space(self, absPos, size):
		self.filledSpaces.append((absPos - size/2, absPos + size/2))


	def PrintFilledSpaces(self):
		print("self.filled spaces:")
		for arr in self.filledSpaces:
			print(arr)


	def add_root(self, growth_dir):
		# sim crashes if this size is [0,0,0], so make one dim arbitrarily small
		# robot bounces if this dimension happens to be x, so we'll use z
		pyrosim.Send_Cube(name="root", 
							pos=self.initialPos, 
							size=[0,0,0.0001], 
							color="Green")
		pyrosim.Send_Joint(name="root_0-0" , 
							parent="root",
							child="0-0",
							type="revolute", 
							position=self.initialPos, 
							jointAxis="1 0 0")
		# first node always has sensor, ensure that body has at least one
		# add first real link
		currNode = self.uniqueNodeList[0]
		currPos = growth_dir * currNode.orientation * currNode.dims/2
		pyrosim.Send_Cube(name="0-0", 
							pos=currPos,
							size=currNode.dims, 
							color=currNode.color)
		if currNode.has_sensor:
			self.sensorLinks.append("0-0")	
		
		currAbsPos = currPos + self.initialPos
		self.fill_space(currAbsPos, currNode.dims)
		return currAbsPos


	def Generate_Body(self, ID):
		self.filledSpaces = [] # listof [lower_dim: np array(1,3), upper_dim: np array(1,3)]
		self.sensorLinks = ["root"] # listof node names (str)
		self.allLinks = ["root", "0-0"]
		self.allJoints = ["root_0-0"]
		self.availableLinkID = 0
		self.numLinks = 2 # root
		self.numSensorNeurons = len(self.sensorLinks)		
		self.Generate_Body_urdf(ID)
		self.Calculate_Wingspan()


	def Generate_Body_urdf(self, myID):
		# print(f"GENERATING BODY {myID}")
		# function to recursively add links
		def add_link(prevUniqueNode,  prevAbsPos, prevLinkName, currUniqueNode, currClone, currChild, growthDir):
			# print("RECRUSING\n")
			currNode = self.uniqueNodeList[currUniqueNode]
			prevNode = self.uniqueNodeList[prevUniqueNode]

			# branch in new growth direction along orientation if
					# this is the second child
					# and going in a new orientation
			if currChild == 1:  
				if (prevNode.orientation != currNode.orientation).all():
					return # this link would be positioned directly in the previous link
				growthDir = self.switchDirection(dir=growthDir, orientation=currNode.orientation)

			currJointPos = (prevNode.orientation + currNode.orientation)  * (prevNode.dims/2) * growthDir 
			currLinkPos = (currNode.orientation) * (currNode.dims/2)  * growthDir
			
			currLinkName = f"{currUniqueNode}-{self.fetchLinkID()}"
			currAbsPos = prevAbsPos + currJointPos + currLinkPos
			# print(f"checking {currLinkName} at pos {currAbsPos} with dims {currNode.dims}")
			if not self.has_space(currAbsPos, currNode.dims):
				# print(f"{currLinkName}: NO SPACE\n")
				return
				# print(f"{currLinkName}: has space")
			self.fill_space(currAbsPos, currNode.dims)
			# self.PrintFilledSpaces()
			# print("\n\n")
			# print(f"CURR: {currLinkName} ")
			# print(f"{prevLinkName}_{currLinkName}" )
			# print(f"currJointPos: {currJointPos}" )
			# print(f"currLinkPos: {currLinkPos}" )
			
			pyrosim.Send_Joint(name=f"{prevLinkName}_{currLinkName}" , 
							   parent=f"{prevLinkName}",
							   child=f"{currLinkName}",
							   type="revolute", 
							   position=currJointPos, 
							   jointAxis=currNode.axisStr())
			pyrosim.Send_Cube(name=currLinkName, 
							  pos=currLinkPos, 
							  size=currNode.dims, 
							  color=currNode.color)
			
			# maintain invariants
			self.numLinks += 1
			if currNode.has_sensor:
				self.sensorLinks.append(currLinkName)	
			self.allLinks.append(currLinkName)
			self.allJoints.append(f"{prevLinkName}_{currLinkName}" )

			# recursive call(s) to add clones
			if currClone < currNode.numSelfEdge :
				add_link(prevUniqueNode = currUniqueNode, prevAbsPos = currAbsPos, prevLinkName = currLinkName, 
						 currUniqueNode = currUniqueNode, currClone = currClone + 1, currChild = currChild,
						 growthDir = growthDir)
			# recursive call(s) to add children
			if currUniqueNode + 1 < len(self.uniqueNodeList):
				for child in range(currNode.numChildEdge):
					add_link(prevUniqueNode = currUniqueNode, prevAbsPos = currAbsPos,  prevLinkName  = currLinkName, 
							currUniqueNode = currUniqueNode + 1, currClone = 0, currChild = child,
							growthDir = growthDir)

		pyrosim.Start_URDF(f"./{self.seed}/body{myID}.urdf") # stores description of robot's body
		
		growthDir = [1, 1, -1]
		# add dummy root link and first real link
		currAbsPos = self.add_root(growth_dir=growthDir)
		# add clones of first link
		currNode = self.uniqueNodeList[0]
		if currNode.numSelfEdge > 0:
			add_link(prevUniqueNode = 0, prevAbsPos = currAbsPos,  prevLinkName = "0-0", 
						currUniqueNode = 0, currClone = 1, currChild = 0,
						growthDir = growthDir)
		# add children
		if 1 < len(self.uniqueNodeList):
			for child in range(currNode.numChildEdge):
				add_link(prevUniqueNode = 0, prevAbsPos = currAbsPos,  prevLinkName = "0-0", 
							currUniqueNode = 1, currClone = 0, currChild = child,
							growthDir = growthDir)
		pyrosim.End()


	def Mutate_Body(self):

		mutation_type = random.randint(0,2)
		nodeidx = random.randint(0,len(self.uniqueNodeList)-1)
		node = self.uniqueNodeList[nodeidx]
		match mutation_type:
			case 0: # change sensor presence
				node.has_sensor = not node.has_sensor
				node.Set_Color()
			case 1: # change orientation
				random.shuffle(self.orientationsQueue)
				orientation = self.orientationsQueue[0]
				if (orientation == node.orientation).all():
					node.orientation = self.orientationsQueue[1]
				else:
					node.orientation = orientation
			case 2:
				node.dims = np.array([round(random.uniform(c.minSideLen, c.maxSideLen), 1)
											for dim in range(3)]) #random


	def Generate_Brain(self, myID):
		self.prevHiddentoMotorWeights = self.currHiddentoMotorWeights
		self.prevSensortoHiddenWeights = self.currSensortoHiddenWeights
		self.currSensortoHiddenWeights = {}
		self.currSensortoHiddenWeights = {}
		self.Generate_Brain_nndf(myID)


	def Generate_Brain_nndf(self, myID):
		pyrosim.Start_URDF(f"./{self.seed}/brain{myID}.nndf")
		# create hidden neurons
		for i in  range(c.numHiddenNeurons):
			# print(f"hidden neuron {neuronName}")
			pyrosim.Send_Hidden_Neuron(name = i)

		currNeuronName = c.numHiddenNeurons

		# sensor neurons and sensor-->hidden synapses
		for i in  range(c.numHiddenNeurons):
			for link in self.sensorLinks: 

				# get weight if same link (also with a sensor) previously existed, else random
				weight =  self.prevSensortoHiddenWeights.get(link, random.random() * 2 -1)
				self.currSensortoHiddenWeights[link] = weight

				pyrosim.Send_Sensor_Neuron(name = currNeuronName, linkName = link)
				pyrosim.Send_Synapse(sourceNeuronName = currNeuronName, 
			 						targetNeuronName = i, 
									weight = weight)
				currNeuronName += 1
		# print("hidden to motor")
		# sensor neurons and sensor-->hidden synapses
		for i in  range(c.numHiddenNeurons):
			for joint in self.allJoints: 
				# get weight if joint previously existed, else random
				weight =  self.prevHiddentoMotorWeights.get(joint, random.random() * 2 -1)
				self.currHiddentoMotorWeights[joint] = weight

				pyrosim.Send_Motor_Neuron(name = currNeuronName, jointName = joint)
				pyrosim.Send_Synapse(sourceNeuronName = i, 
			 						targetNeuronName = currNeuronName, 
									weight = weight)
				currNeuronName += 1

		pyrosim.End()


	def Mutate_Brain(self):
		m = (random.getrandbits(1))
		if m:
			self.currSensortoHiddenWeights[random.choice(self.sensorLinks)] = random.random() * 2 -1
		else:
			self.currHiddentoMotorWeights[random.choice(self.allJoints)] = random.random() * 2 -1


	def Calculate_Wingspan(self):
		# get the length of robot in x direction
		max_x = 0
		min_x = 0
		for link in self.filledSpaces:
			if link[0][0] < min_x:
				min_x = link[0][0]
			if link[1][0] > max_x:
				max_x = link[1][0]
		# print(f"WINGSPAN: {max_x - min_x}")
		self.wingspan =  max_x - min_x