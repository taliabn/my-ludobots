import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR


class ROBOT:

	def __init__(self):

		self.robotId = p.loadURDF("body.urdf") # floor
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_to_Act()
		self.nn = NEURAL_NETWORK("brain.nndf")


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
			self.motors[jointName] = MOTOR(jointName)
		for motor in self.motors.values():
			motor.Prepare_to_Act()


	def Act(self, i):
		for neuronName in self.nn.Get_Neuron_Names():
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
				desiredAngle = self.nn.Get_Value_Of(neuronName)
				print(f"joint name: {jointName}, neuron name: {neuronName}, desired angle: {desiredAngle}")

		for motor in self.motors.values():
			motor.Set_Value(self, i)

	def Think(self):
		self.nn.Update()
		self.nn.Print()

