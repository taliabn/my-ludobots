import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c


class WORLD:

	def __init__(self):
		self.Create_World()


	# writes to "world.sdf"
	def Create_World(self):
		pyrosim.Start_SDF("world.sdf")
		# length = c.pyramid_length
		# for k in range(c.num_pyramid_layers):
		# 	length -= c.gap_width
		# 	pyrosim.Send_Cube(name="Box", pos=[c.pyramid_x, 0, c.layer_height*(k+1)] , 
		# 							size=[length, length, c.layer_height] , mass=50) 
									# make pyramid heavy enough that robot cannot move it
		pyrosim.End()