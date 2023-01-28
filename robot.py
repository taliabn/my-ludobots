import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import os
import constants as c

class ROBOT:

	def __init__(self, solutionID):

		self.robotId = p.loadURDF("body.urdf") # floor
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_to_Act()
		self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
		os.system("rm brain" + solutionID + ".nndf") # OS specific call


	def Prepare_To_Sense(self):
		self.sensors = {}
		for linkName in pyrosim.linkNamesToIndices:
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
		# self.nn.Print()

	def Get_Fitness(self, solutionID):
		stateOfLinkZero = p.getLinkState(self.robotId, 0)
		positionOfLinkZero = stateOfLinkZero[0]
		xCoordinateOfLinkZero = positionOfLinkZero[0]
		tmpFileName = f"tmp{solutionID}.txt"
		with open(tmpFileName, "w") as f:
			f.write(str(xCoordinateOfLinkZero))
		fitnessFileName	 = f"fitness{solutionID}.txt"
		os.rename(tmpFileName, fitnessFileName)