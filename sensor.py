import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim


class SENSOR:

	def __init__(self, linkName):
		self.linkName = linkName
		self.values = np.zeros(c.steps) # initialize array
		print(self.values)

	def Get_Value(self, i):
		val = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
		self.values[i] = val

	#  I think this didn't go here?
	# def Sense(self):
	# 	pass

