import pyrosim.pyrosim as pyrosim


def Create_World():
	pyrosim.Start_SDF("world.sdf")
	width, length, height = 1, 1, 1 # box dimensions
	pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5] , size=[width, length, height])
	pyrosim.End()

def Create_Robot():
	pyrosim.Start_URDF("body.urdf") # stores description of robot's body
	width, length, height = 1, 1, 1 # torso dimensions
	pyrosim.Send_Cube(name="Link0", pos=[0, 0, 0.5] , size=[width, length, height])
	# joint naming convention: Parent_Child
	pyrosim.Send_Joint( name = "Link0_Link1" , parent= "Link0" , child = "Link1" , 
						type = "revolute", position = [0, 0, 1.0])
	pyrosim.Send_Cube(name="Link1", pos=[0, 0, 0.5] , size=[length, height, width])
	pyrosim.Send_Joint( name = "Link1_Link2" , parent= "Link1" , child = "Link2" , 
						type = "revolute", position = [0, 0, 1.0])
	pyrosim.Send_Cube(name="Link2", pos=[0, 0, 0.5] , size=[length, height, width])

	pyrosim.End()


Create_World()
Create_Robot()