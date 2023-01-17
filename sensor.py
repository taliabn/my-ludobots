import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
from os.path import join


class SENSOR:

	def __init__(self, linkName):
		self.linkName = linkName
		self.values = np.zeros(c.steps) # initialize array

	def Get_Value(self, i):
		val = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
		self.values[i] = val

	def Save_Values(self):
		file_path = join("data", self.linkName + "-SensorValues")
		np.save(file_path, self.values)

