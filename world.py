import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim


class WORLD:

	def __init__(self, initial_world):
		if initial_world:
			self.Create_World()

		self.planeId = p.loadURDF("plane.urdf") # floor
		p.loadSDF("world.sdf")


	# writes to "world.sdf"
	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		width, length, height = 1, 1, 1 # box dimensions
		pyrosim.Send_Cube(name="Box", pos=[-2, -2, 0.5] , size=[width, length, height], mass=20)
		pyrosim.End()