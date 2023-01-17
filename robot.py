import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR


class ROBOT:

	def __init__(self):

		self.robotId = p.loadURDF("body.urdf") # floor
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_to_Act()


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
		for motor in self.motors.values():
			motor.Set_Value(self, i)
