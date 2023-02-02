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
		length, height = 8, 0.5 # box dimensions
		x, y, z = -6, 0, 0.5 # box starting position
		for k in range(5):
			length -= k*0.75
			pyrosim.Send_Cube(name="Box", pos=[x, y, z*k + height] , 
									size=[length, length, height] , mass=50) 
									# make pyramid heavy enough that robot cannot move it
		pyrosim.End()