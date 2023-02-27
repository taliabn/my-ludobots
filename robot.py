import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
from datetime import datetime
import os
import constants as c

class ROBOT:

	def __init__(self, directOrGUI, solutionID, seed):

		self.robotId = p.loadURDF(f"./{seed}/body{solutionID}.urdf") # floor
		# self.robotId = p.loadURDF(f"body.urdf") # floor
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.nn = NEURAL_NETWORK(f"./{seed}/brain{solutionID}.nndf")
		self.Prepare_To_Sense()
		self.Prepare_to_Act()


	def Prepare_To_Sense_old(self):
		self.sensors = {}
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName] = SENSOR(linkName)		


	def Prepare_To_Sense(self):
		self.sensors = {}
		for linkName in self.nn.Get_Sensor_Neurons_Links():
			self.sensors[linkName] = SENSOR(linkName)


	def Sense(self, i):
		for sensor in self.sensors.values():
			sensor.Get_Value(i) # modifies sensor.values in place


	def Prepare_to_Act(self):
		self.motors = {}
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName.decode()] = MOTOR(jointName)


	def Act(self, i):
		for neuronName in self.nn.Get_Neuron_Names():
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
				desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
				self.motors[jointName].Set_Value(self, desiredAngle) 


	def Think(self):
		self.nn.Update()


	def Return_Displacement(self, solutionID):
		# print(f"GETTING DISPLACEMENT FOR {solutionID}")
		basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
		basePosition = basePositionAndOrientation[0]
		base_x = basePosition[0]
		# print(f"RETURNING DISPLACEMENT FOR {solutionID}")
		return base_x

	def Record_Displacement(self, solutionID):
		basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
		basePosition = basePositionAndOrientation[0]
		base_x = basePosition[0]
		tmpFileName = f"tmp{solutionID}.txt"
		with open(tmpFileName, "w") as f:
			f.write(str(base_x))
		print(f"WRITING DISPLACEMENT FOR {solutionID}")
		displacementFileName = f"displacement{solutionID}.txt"
		os.rename(tmpFileName, displacementFileName)
		print(f"DONE WRITING DISPLACEMENT FOR {solutionID}")


	# returns euclidean distance to top, center point on pyramid
	# def Calculate_Fitness(self, basePosition):
	# 	link_x, link_y, link_z = basePosition
	# 	# return ((c.pyramid_x - link_x)**2 + 
	#   	# 		link_y**2 + 
	#   	# 		(c.layer_height*c.num_pyramid_layers - link_z)**2)**0.5
	# 	return - link_x