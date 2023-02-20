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
		# get random orientation that isn't the previous one
		self.orientation = orientationsQueue.pop(0)
		random.shuffle(orientationsQueue)
		orientationsQueue.append(self.orientation)

		# possibly change min/max side length to be encoded in dna?
		self.dims = np.array([round(random.uniform(c.minSideLen, c.maxSideLen), 2)
											for dim in range(3)]) #random
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

	def __init__(self, dna, ID):
		print("INITIALIZING BODY CLASS INSTANCE")
		self.myID = ID
		self.dna = dna # list of [num selfEdges, num nextEdges] pairs
		orientationsQueue = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]
		# orientationsQueue = [np.array([1,0,0]), np.array([0,1,0])]
		random.shuffle(orientationsQueue)
		# initialize graph nodes
		self.uniqueNodeList = [uniqueNode(instruction[0], instruction[1], orientationsQueue)
							  	  for instruction in self.dna]
		for node in self.uniqueNodeList:
			node.Print()
		self.sensorLinks = ["root"] # listof node names (str)
		self.allLinks = ["root", "0-0"]
		self.availableID = 0
		self.numLinks = 2 # root
		self.Generate_Body()
		self.numSensorNeurons = len(self.sensorLinks)
	

	def SaveToPickle(self):
		with open(f'BODY{self.myID}.pickle', 'wb') as handle:
			pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)


	def fetchID(self):
		self.availableID += 1
		return self.availableID


	def switchDirection(self, dir, orientation):
		# orientation *= -1
		return np.logical_not(orientation)*dir + orientation*-1


	def add_root(self, start_pos):
		# sim crashes if this size is [0,0,0], so make one dim arbitrarily small
		# robot bounces if this dimension happens to be x, so we'll use z
		pyrosim.Send_Cube(name="root", 
							pos=start_pos, 
							size=[0,0,0.0001], 
							color="Green")
		pyrosim.Send_Joint(name="root_0-0" , 
							parent="root",
							child="0-0",
							type="revolute", 
							position=start_pos, 
							jointAxis="1 0 0")
		# first node always has sensor, ensure that body has at least one
		# add first real link
		currNode = self.uniqueNodeList[0]
		pyrosim.Send_Cube(name="0-0", 
							pos=currNode.dims/2, 
							size=currNode.dims, 
							color=currNode.color)
		if currNode.has_sensor:
			self.sensorLinks.append("0-0")	


	def Generate_Body(self):

		# function to recursively add links
		def add_link(prevUniqueNode,  prevClone, prevChild, prevLinkName, currUniqueNode, currClone, currChild, growthDir):
			currNode = self.uniqueNodeList[currUniqueNode]
			prevNode = self.uniqueNodeList[prevUniqueNode]

			# branch in new growth direction along orientation if
					# this is the second child
					# and going in a new orientation
			if currChild == 1:  
				if (prevNode.orientation != currNode.orientation).all():
					return # this link would be positioned directly in the previous link
				growthDir = self.switchDirection(dir=growthDir, orientation=currNode.orientation)

			currJointPos = (prevNode.orientation + currNode.orientation)  * prevNode.dims/2 * growthDir 
			currLinkPos = (currNode.orientation) * currNode.dims/2 * growthDir
			
			currLinkName = f"{currUniqueNode}-{self.fetchID()}"
			# # print(f"CURR: {currLinkName} ")
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

			# recursive call(s) to add clones
			if currClone < currNode.numSelfEdge :
				add_link(prevUniqueNode = currUniqueNode, prevClone = currClone, prevChild = currClone, prevLinkName = currLinkName, 
						 currUniqueNode = currUniqueNode, currClone = currClone + 1, currChild = currChild,
						 growthDir = growthDir)
			# recursive call(s) to add children
			if currUniqueNode + 1 < len(self.uniqueNodeList):
				for child in range(currNode.numChildEdge):
					add_link(prevUniqueNode = currUniqueNode, prevClone = currClone, prevChild = currClone, prevLinkName  = currLinkName, 
							currUniqueNode = currUniqueNode + 1, currClone = 0, currChild = child,
							growthDir = growthDir)

		# pyrosim.Start_URDF(f"body{self.myID}.urdf") # stores description of robot's body
		pyrosim.Start_URDF(f"body.urdf") # stores description of robot's body
		
		# add dummy root link and first real link
		self.add_root(start_pos=[0,0,3])
		# add clones of first link
		# print(currNode.numChildEdge, currNode.numSelfEdge, currNode)
		currNode = self.uniqueNodeList[0]
		growthDir = [1,1,1]
		if currNode.numSelfEdge > 0:
			add_link(prevUniqueNode = 0, prevClone = 0, prevChild = 0, prevLinkName = "0-0", 
						currUniqueNode = 0, currClone = 1, currChild = 0,
						growthDir = growthDir)
		# add children
		if 1 < len(self.uniqueNodeList):
			for child in range(currNode.numChildEdge):
				add_link(prevUniqueNode = 0, prevClone = 0, prevChild = 0, prevLinkName = "0-0", 
							currUniqueNode = 1, currClone = 0, currChild = child,
							growthDir = growthDir)
		pyrosim.End()


# TODO:
	# if leaf, add sensor
	# joint types?
	# consolidate randoms (random lib vs numpy)

# tradeoffs:
	# linear each unique node only connects to one unique node (linear)
	# root always has sensor
	# 2 children edges max
	# neighboring nodes always have diff orientations
	# can only branch at right angles
	