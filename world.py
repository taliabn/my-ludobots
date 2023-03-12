import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c


class WORLD:

	def __init__(self):
		self.Create_World()

	# writes to "world.sdf"
	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		pyrosim.End()