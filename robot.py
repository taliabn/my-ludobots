import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR

class ROBOT:

	def __init__(self):

		self.motors = {}
		self.robotId = p.loadURDF("body.urdf") # floor
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()


	def Prepare_To_Sense(self):

		self.sensors = {}
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName] = SENSOR(linkName)		

	def Sense(self, i):
		for sensor in self.sensors.values():
			sensor.Get_Value(i)
