import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import constants as c

class ROBOT:

	def __init__(self, solutionID, seed):

		self.robotId = p.loadURDF(f"./{seed}/body{solutionID}.urdf") # floor
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


	def Return_Displacement(self):
		basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
		basePosition = basePositionAndOrientation[0]
		base_x = basePosition[0]
		return base_x


	# returns euclidean distance to top, center point on pyramid
	# def Calculate_Fitness(self, basePosition):
	# 	link_x, link_y, link_z = basePosition
	# 	# return ((c.pyramid_x - link_x)**2 + 
	#   	# 		link_y**2 + 
	#   	# 		(c.layer_height*c.num_pyramid_layers - link_z)**2)**0.5
	# 	return - link_x