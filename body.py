import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import constants as c


class uniqueNode:

	def __init__(self, numSelfEdge, numChildEdge, orientation):
		# from dna:
		self.numSelfEdge: int = numSelfEdge
		self.numChildEdge: int = numChildEdge
		# randomly chosen:
		self.has_sensor: bool = bool(random.getrandbits(1)) # random
		self.orientation = orientation # random
		# possibly change min/max side length to be encoded in dna?
		# dimensions
		# self.l, self.w, self.h: float = [random.uniform(c.minSideLen, c.maxSideLen)
		# 									for dim in range(3)] #random
		self.dims = np.array([random.uniform(c.minSideLen, c.maxSideLen)
											for dim in range(3)]) #random
		if self.has_sensor:
			self.color = "Green"
		else:
			self.color = "Blue"


	def axisStr(self):
		return f"{self.orientation[0]} {self.orientation[1]} {self.orientation[2]}"


class BODY:

	def __init__(self, dna, ID):
		print("INITIALIZING BODY CLASS INSTANCE")
		self.myID = ID
		self.dna = dna # list of [num selfEdges, num nextEdges] pairs
		# initialize graph nodes
		self.uniqueNodeList = [uniqueNode(instruction[0], instruction[1], self.randomOrientation())
							  	  for instruction in self.dna]
		self.sensorLinks = [] # listof node names (str)
		self.allLinks = []
		self.availableID = 0
		self.numLinks = 1 # root
		self.Generate_Body()
		self.numSensorNeurons = len(self.sensorLinks)

	def fetchID(self):
		self.availableID += 1
		return self.availableID

	def switchDirection(self, dir, orientation):
		orientation *= -1
		return np.logical_not(orientation)*dir + orientation


	def randomOrientation(self):
		return np.array(random.choice([[1,0,0], [0,1,0], [0,0,1]]))


	def Generate_Body(self):
		# function to recursively add links
		def add_link(prevUniqueNode,  prevClone, prevChild, prevLinkName, currUniqueNode, currClone, currChild, growthDir):
			# print(locals(), "\n")
			currNode = self.uniqueNodeList[currUniqueNode]
			prevNode = self.uniqueNodeList[prevUniqueNode]

			currJointPos = prevNode.dims * (prevNode.orientation + currNode.orientation) * growthDir 
			currLinkPos = currNode.dims * (currNode.orientation) * growthDir

			currLinkName = f"{currUniqueNode}-{self.fetchID()}"
			# print(f"CURR: {currLinkName} ")
			print(f"{prevLinkName}_{currLinkName}" )
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
				newName = self.fetchID()
				add_link(prevUniqueNode = currUniqueNode, prevClone = currClone, prevChild = currClone, prevLinkName = currLinkName, 
						 currUniqueNode = currUniqueNode, currClone = currClone + 1, currChild = currChild,
						 growthDir = growthDir)
			# recursive call(s) to add children
			if len(self.uniqueNodeList) > currUniqueNode + 1:
				for child in range(currNode.numChildEdge):
					# branch in new growth direction along orientation if this is the second child
					if child == 1:
						newDir = self.switchDirection(dir=growthDir, orientation=currNode.orientation)
					else:
						newDir = growthDir	
					
									
					add_link(prevUniqueNode = currUniqueNode, prevClone = currClone, prevChild = currClone, prevLinkName  = currLinkName, 
							currUniqueNode = currUniqueNode + 1, currClone = 0, currChild = child,
							growthDir = newDir)

		# pyrosim.Start_URDF(f"body{self.myID}.urdf") # stores description of robot's body
		pyrosim.Start_URDF(f"body.urdf") # stores description of robot's body
		print(f"body{self.myID}.urdf")
		# add root link
		currNode = self.uniqueNodeList[0]
		# LINK NAMING CONVENTION: uniqueNodeIndex-self-child	
		pyrosim.Send_Cube(name="0-0", 
						  pos=currNode.dims/2, 
						  size=currNode.dims, 
						  color="Green")
		# root link always has a sensor, even if uniqueNode 0 does not
		self.sensorLinks.append("0-0")
		growthDir = [1,1,1]
		# add clones
		# print(currNode.numChildEdge, currNode.numSelfEdge, currNode)
		if currNode.numSelfEdge > 0:
			add_link(prevUniqueNode = 0, prevClone = 0, prevChild = 0, prevLinkName = "0-0", 
						currUniqueNode = 0, currClone = 1, currChild = 0,
						growthDir = growthDir)
		# add children
		if len(self.uniqueNodeList) > 2:
			for child in range(currNode.numChildEdge): # assumed to be 1 or 2

				# branch in new growth direction along orientation if this is the second child
				if child == 1:
					newDir = self.switchDirection(dir=growthDir, orientation=currNode.orientation)
				else:
					newDir = growthDir
				add_link(prevUniqueNode = 0, prevClone = 0, prevChild = 0, prevLinkName = "0-0", 
							currUniqueNode = 1, currClone = 0, currChild = child,
							growthDir = newDir)
		print("\n\nESCAPED RECURSION\n")
		pyrosim.End()
		print("ENDED PYROSIM\n")


# TODO:
	# if leaf, add sensor
	# naming conventions
	# jointaxis / type
	# consolidate randoms (random lib vs numpy)

# tradeoffs:
	#linear each unique node only connects to one unique node (linear)
	# root always has sensor
	# 2 children edges max