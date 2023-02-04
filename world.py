import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c


class WORLD:

	def __init__(self, initial_world):
		if initial_world:
			self.Create_World()

		self.planeId = p.loadURDF("plane.urdf") # floor
		p.loadSDF("world.sdf")


	# writes to "world.sdf"
	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		length = c.pyramid_length
		for k in range(c.pyramid_layers):
			length -= k*0.75
			pyrosim.Send_Cube(name="Box", pos=[c.pyramid_x, 0, c.layer_height*(k+1)] , 
									size=[length, length, c.layer_height] , mass=50) 
									# make pyramid heavy enough that robot cannot move it
		pyrosim.End()