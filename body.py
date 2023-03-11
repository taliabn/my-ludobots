import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c


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

	def __init__(self, dna, solutionID, seed, numHiddenLayers):
		# print("\nINTIALIZING BODY CLASS\n")
		self.seed = seed
		self.dna = dna # list of [num selfEdges, num nextEdges] pairs
		self.numHiddenLayers = int(numHiddenLayers)
		self.orientationsQueue = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]
		random.shuffle(self.orientationsQueue)
		# initialize graph nodes
		self.uniqueNodeList = [uniqueNode(instruction[0], instruction[1], self.orientationsQueue)
							  	  for instruction in self.dna]
		# self.PrintUniqueNodes()
		self.initialPos = np.array(c.startingPos)
		self.Generate_Body(solutionID)
		# self.prevSensortoMotorWeights = {}
		# self.prevSensortoHiddenWeights = {}
		# self.prevHiddentoMotorWeights = {}
		# self.prevHiddentoHiddenWeights = {} 
		self.currSensortoMotorWeights = {}
		self.currSensortoHiddenWeights = {}
		self.currHiddentoMotorWeights = {}
		self.currHiddentoHiddenWeights = {}
		self.Generate_Brain(solutionID)
		# if self.numHiddenLayers == 0:
		# 	self.Gen_No_Hidden_Brain_nndf(solutionID)
		# elif self.numHiddenLayers == 1:
		# 	self.Gen_1_Hidden_Brain_nndf(solutionID)
		# elif self.numHiddenLayers == 2:
		# 	self.Gen_2_Hidden_Brain_nndf(solutionID)
		# else:
		# 	raise Exception(f"ERROR: {self.numHiddenLayers} is an invalid num hidden layers")


	def PrintUniqueNodes(self):
		for node in self.uniqueNodeList:
			node.Print()


	def switchDirection(self, dir, orientation):
		return np.logical_not(orientation)*dir + orientation*-1 #type: ignore
	

	def has_space(self, absPos, size, tol=0.01):
		if [absPos - size/2][0][2] <= 0:
			# below floor
			return False 
		for block in self.filledSpaces:
			if (sum(block[0] >= (absPos + size/2)) == 0) and  (sum((absPos - size/2) >= block[1]) == 0):
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
		pyrosim.Send_Joint(name="root_000" , 
							parent="root",
							child="000",
							type="revolute", 
							position=self.initialPos, 
							jointAxis="1 0 0")
		# first node always has sensor, ensure that body has at least one
		# add first real link
		currNode = self.uniqueNodeList[0]
		currPos = growth_dir * currNode.orientation * currNode.dims/2
		pyrosim.Send_Cube(name="000", 
							pos=currPos,
							size=currNode.dims, 
							color=currNode.color)
		if currNode.has_sensor:
			self.sensorLinks.append("000")	
		
		currAbsPos = currPos + self.initialPos
		self.fill_space(currAbsPos, currNode.dims)
		return currAbsPos


	def Generate_Body(self, ID):
		self.filledSpaces = [] # listof [lower_dim: np array(1,3), upper_dim: np array(1,3)]
		self.sensorLinks = ["root"] # listof node names (str)
		self.allLinks = ["root", "000"]
		self.allJoints = ["root_000"]
		self.availableLinkID = 0
		self.Generate_Body_urdf(ID)
		self.Calculate_Wingspan()


	def Generate_Body_urdf(self, myID):
		# function to recursively add links
		def add_link(prevUniqueNode,  prevAbsPos, prevLinkName, currUniqueNode, currClone, currChild, currLinkName, growthDir):

			# pyrosim allows a maximum of 128 links per body
			if len(self.allLinks) > 127:
				# print(f"{len(self.allLinks)} is too much man, returning")
				return

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
			
			# currLinkName = f"{currUniqueNode}-{self.fetchLinkID()}"
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
			if currNode.has_sensor:
				self.sensorLinks.append(currLinkName)	
			self.allLinks.append(currLinkName)
			self.allJoints.append(f"{prevLinkName}_{currLinkName}" )

			# naming convention: "{prevlinkname}-{node}{clone}{child}"
			# recursive call(s) to add clones
			if currClone < currNode.numSelfEdge :
				newLinkName = f"{currLinkName[:-2]}{currClone+1}{currChild}"
				# print(f"CLONE {currClone + 1}:\n\tprev name: {prevLinkName}\n\tcurr name: {currLinkName}\n\tnext name: {newLinkName}\n\n")
				add_link(prevUniqueNode = currUniqueNode, prevAbsPos = currAbsPos, prevLinkName = currLinkName, 
						 currUniqueNode = currUniqueNode, currClone = currClone + 1, currChild = currChild,
						 currLinkName = newLinkName, growthDir = growthDir)
			# recursive call(s) to add children
			if currUniqueNode + 1 < len(self.uniqueNodeList):
				for child in range(currNode.numChildEdge):
					newLinkName = f"{currLinkName}-{currUniqueNode + 1}0{child}"
					# print(f"CHILD {child}:\n\tprev name: {prevLinkName}\n\tcurr name: {currLinkName}\n\nmext name: {newLinkName}\n\n")
					add_link(prevUniqueNode = currUniqueNode, prevAbsPos = currAbsPos,  prevLinkName  = currLinkName, 
							currUniqueNode = currUniqueNode + 1, currClone = 0, currChild = child,
							currLinkName = newLinkName, growthDir = growthDir)

		pyrosim.Start_URDF(f"./{self.seed}/body{myID}.urdf") # stores description of robot's body
		
		growthDir = [1, 1, -1]
		# add dummy root link and first real link
		currAbsPos = self.add_root(growth_dir=growthDir)
		# add clones of first link
		currNode = self.uniqueNodeList[0]
		# naming convention: "{prevlinkname}-{node}{clone}{child}"
		if currNode.numSelfEdge > 0:
			# print(f"CLONE 1 INIT:\n\tprev name: 000\n\tcurr name: 010\n")
			add_link(prevUniqueNode = 0, prevAbsPos = currAbsPos,  prevLinkName = "000", 
						currUniqueNode = 0, currClone = 1, currChild = 0,
						currLinkName = '010', growthDir = growthDir)
		# add children
		if 1 < len(self.uniqueNodeList):
			for child in range(currNode.numChildEdge):
				# print(f"CHILD {child} INIT:\n\tprev name: 000\n\tcurr name: 000-10{child}\n")
				add_link(prevUniqueNode = 0, prevAbsPos = currAbsPos,  prevLinkName = "000", 
							currUniqueNode = 1, currClone = 0, currChild = child,
							currLinkName = f'000-10{child}', growthDir = growthDir)
		pyrosim.End()
		# print(f"body SENSOR LINKS: {self.sensorLinks}\n")
		if len(set(self.allLinks)) != len(self.allLinks):
			raise Exception(f"ERROR: Duplicate links for body {myID}")


	def Mutate_Body(self):
		# print("MUTATING BODY")
		mutation_type = random.randint(0,3)
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
			case 3: # make one of these mutations half as likely
				if (random.getrandbits(1)):
					children = node.numChildEdge
					if children == 2:
						node.numChildEdge = 1
					else:
						node.numChildEdge = 2
				else:
					clones = node.numSelfEdge
					if clones == 0 or random.getrandbits(1):
						node.numSelfEdge = clones + 1
					else:
						node.numChildEdge = clones - 1
			

	def Generate_Brain(self, myID):
		self.prevSensortoMotorWeights = self.currSensortoMotorWeights
		self.prevSensortoHiddenWeights = self.currSensortoHiddenWeights
		self.prevHiddentoHiddenWeights = self.currHiddentoHiddenWeights
		self.prevHiddentoMotorWeights = self.currHiddentoMotorWeights
		self.currSensortoMotorWeights = {}
		self.currSensortoHiddenWeights = {}
		self.currHiddentoHiddenWeights = {}
		self.currHiddentoMotorWeights = {}
		# print(f"ALL SENSOR:\n{self.sensorLinks}")
		# print(f"ALL JOINTS:\n{self.allJoints}\n")
		# print(f"SENSOR TO MOTOR\n: {self.prevSensortoMotorWeights}")
		# print(f"SENSOR TO HIDDEN\n: {self.prevSensortoHiddenWeights}")
		# print(f"HIDDEN TO HIDDEN\n: {self.prevHiddentoHiddenWeights}")
		# print(f"HIDDEN TO MOTOR\n: {self.prevHiddentoMotorWeights}\n\n\n")
		if self.numHiddenLayers == 0:
			self.Gen_No_Hidden_Brain_nndf(myID)
		elif self.numHiddenLayers == 1:
			self.Gen_1_Hidden_Brain_nndf(myID)
		elif self.numHiddenLayers == 2:
			self.Gen_2_Hidden_Brain_nndf(myID)
		else:
			raise Exception("ERROR: invalid num hidden layers")



	def Gen_No_Hidden_Brain_nndf(self, myID):
		# print("generating brain with 0 hidden layers")
		pyrosim.Start_URDF(f"./{self.seed}/brain{myID}.nndf")

		currNeuronName = 0
		# create sensor neurons
		for link in self.sensorLinks: 
			# print(f"sending sensor neuron {currNeuronName} for link {link}")
			pyrosim.Send_Sensor_Neuron(name = currNeuronName, linkName = link)
			currNeuronName += 1

		# create motor neurons
		for joint in self.allJoints: 
			# print(f"sending motor neuron {currNeuronName} for joint {joint}")
			pyrosim.Send_Motor_Neuron(name = currNeuronName, jointName = joint)
			currNeuronName += 1

		# sensor-->motor synapses
		numSensor = len(self.sensorLinks)
		for i, link in enumerate(self.sensorLinks):
			for j, joint in enumerate(self.allJoints):
			# get weight if joint previously existed, else random
				synapseName = f"S{link}_M{joint}"
				# print(f"Sending synapse {synapseName} between {i} and {j + numSensor}")
				weight =  self.prevSensortoMotorWeights.get(synapseName, random.random() * 2 -1)
				self.currSensortoMotorWeights[synapseName] = weight
				pyrosim.Send_Synapse(sourceNeuronName = i, 
									targetNeuronName = j + numSensor, 
									weight = weight)
		pyrosim.End()


	def Gen_1_Hidden_Brain_nndf(self, myID):
		# print("generating brain with 1 hidden layers")

		pyrosim.Start_URDF(f"./{self.seed}/brain{myID}.nndf")
		# create hidden neurons
		for i in  range(c.numHiddenNeurons):
			# print(f"sending hidden neuron {i}")
			pyrosim.Send_Hidden_Neuron(name = i)

		currNeuronName = c.numHiddenNeurons
		# sensor neurons and sensor-->hidden synapses
		# print("SENSOR to HIDDEN")
		for link in self.sensorLinks: 
			# print(f"sending sensor neuron {currNeuronName} for link {link}")
			pyrosim.Send_Sensor_Neuron(name = currNeuronName, linkName = link)
			for i in range(c.numHiddenNeurons):
				synapseName = f'S{link}_HA{i}'
				# get weight if same link (also with a sensor) previously existed, else random
				weight =  self.prevSensortoHiddenWeights.get(synapseName, random.random() * 2 -1)
				self.currSensortoHiddenWeights[synapseName] = weight
				# print(f"sending synapse {synapseName} from {currNeuronName} to {i}")
				pyrosim.Send_Synapse(sourceNeuronName = currNeuronName, 
			 						targetNeuronName = i, 
									weight = weight)
			currNeuronName += 1
		# sensor neurons and sensor-->hidden synapses
		# print("HIDDEN TO MOTOR")
		for joint in self.allJoints: 
			# print(f"sending motor neuron {currNeuronName} for joint {joint}")
			pyrosim.Send_Motor_Neuron(name = currNeuronName, jointName = joint)
			for i in range(c.numHiddenNeurons):
				synapseName = f'HA{i}_M{joint}'
				# get weight if joint previously existed, else random
				# print(f"sending synapse {synapseName} from {i} to {currNeuronName}")
				weight =  self.prevHiddentoMotorWeights.get(synapseName, random.random() * 2 -1)
				self.currHiddentoMotorWeights[synapseName] = weight
				pyrosim.Send_Synapse(sourceNeuronName = i, 
			 						targetNeuronName = currNeuronName, 
									weight = weight)
			currNeuronName += 1

		pyrosim.End()


	def Gen_2_Hidden_Brain_nndf(self, myID):
		pyrosim.Start_URDF(f"./{self.seed}/brain{myID}.nndf")
		# print("generating brain with 2 hidden layers")

		# create hidden neurons
		for i in range(c.numHiddenNeurons*2):
			# print(f"sending hidden neuron {i}")
			pyrosim.Send_Hidden_Neuron(name = i)

		# print("HIDDEN A to HIDDEN B")
		for i in range(c.numHiddenNeurons):
			for j in range(c.numHiddenNeurons, 2*c.numHiddenNeurons):
				synapseName = f'HA{i}_HB{j}'
				weight = self.prevHiddentoHiddenWeights.get(synapseName, random.random() * 2 -1)
				self.currHiddentoHiddenWeights[synapseName] = weight
				# print(f"sending hidden-hidden synapse from {i} to {j}")
				pyrosim.Send_Synapse(sourceNeuronName = i, 
			 						targetNeuronName = j, 
									weight = weight)
		
		currNeuronName = c.numHiddenNeurons * 2

		# sensor neurons and sensor-->hidden synapses
		# print("SENSOR to HIDDEN A")
		for link in self.sensorLinks: 
			# print(f"sending sensor neuron {currNeuronName} for link {link}")
			pyrosim.Send_Sensor_Neuron(name = currNeuronName, linkName = link)
			for i in range(c.numHiddenNeurons):
				synapseName = f'S{link}_HA{i}'
				# get weight if same link (also with a sensor) previously existed, else random
				weight =  self.prevSensortoHiddenWeights.get(synapseName, random.random() * 2 -1)
				self.currSensortoHiddenWeights[synapseName] = weight
				# print(f"sending synapse from {currNeuronName} to {i}")
				pyrosim.Send_Synapse(sourceNeuronName = currNeuronName, 
			 						targetNeuronName = i, 
									weight = weight)
			currNeuronName += 1

		# sensor neurons and sensor-->hidden synapses
		# print("HIDDEN B to motor")
		for joint in self.allJoints: 
			pyrosim.Send_Motor_Neuron(name = currNeuronName, jointName = joint)
			# print(f"sending motor neuron {currNeuronName} for joint {joint}")
			for j in range(c.numHiddenNeurons, c.numHiddenNeurons*2):
				synapseName = f'HB{j}_M{joint}'
				# get weight if joint previously existed, else random
				weight =  self.prevHiddentoMotorWeights.get(synapseName, random.random() * 2 -1)
				self.currHiddentoMotorWeights[synapseName] = weight
				# print(f"sending synapse from {j} to {currNeuronName}")
				pyrosim.Send_Synapse(sourceNeuronName = j, 
			 						targetNeuronName = currNeuronName, 
									weight = weight)
			currNeuronName += 1

		pyrosim.End()
		# print(self.currHiddentoHiddenWeights)
		# print(self.currHiddentoMotorWeights)

	def Mutate_Brain(self):
		if self.numHiddenLayers == 0:
			self.Mutate_No_Hidden_Brain()
		elif self.numHiddenLayers == 1:
			self.Mutate_1_Hidden_Brain()
		elif self.numHiddenLayers == 2:
			self.Mutate_2_Hidden_Brain()
		else:
			raise Exception("ERROR: invalid num hidden layers")

	def Mutate_No_Hidden_Brain(self):
		# print("MUTATING sensor to motor")
		self.currSensortoMotorWeights[random.choice(list(self.currSensortoMotorWeights.keys()))] = random.random() * 2 -1
	

	def Mutate_1_Hidden_Brain(self):
		# print("MUTATING 1 hidden brain")
		m = (random.getrandbits(1))
		if m:
			# print("MUTATING sensor to hidden")
			self.currSensortoHiddenWeights[random.choice(list(self.currSensortoHiddenWeights.keys()))] = random.random() * 2 -1
		else:
			# print("MUTATING hidden to motor")
			self.currHiddentoMotorWeights[random.choice(list(self.currHiddentoMotorWeights.keys()))]= random.random() * 2 -1
	
	
	def Mutate_2_Hidden_Brain(self):
		# print("MUTATING 2 hidden brain")
		m = random.randint(0, 2)
		match m:
			case 0:
				# print("MUTATING sensor to hidden")
				self.currSensortoHiddenWeights[random.choice(list(self.currSensortoHiddenWeights.keys()))] = random.random() * 2 -1
			case 1:
				# print("MUTATING hidden to hidden")
				self.currHiddentoHiddenWeights[random.choice(list(self.currHiddentoHiddenWeights.keys()))] = random.random() * 2 -1
			case 2:
				# print("MUTATING hidden to motor")
				self.currHiddentoMotorWeights[random.choice(list(self.currHiddentoMotorWeights.keys()))] = random.random() * 2 -1


	def Calculate_Wingspan(self):
		# get the length of robot in x direction
		max_x = 0
		min_x = 0
		for link in self.filledSpaces:
			if link[0][0] < min_x:
				min_x = link[0][0]
			if link[1][0] > max_x:
				max_x = link[1][0]
		self.wingspan =  max_x - min_x