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
	pyrosim.Send_Joint( name = "Link2_Link3" , parent= "Link2" , child = "Link3" , 
						type = "revolute", position = [0, 0.5, 0.5])
	pyrosim.Send_Cube(name="Link3", pos=[0, 0.5, 0] , size=[length, height, width])
	pyrosim.Send_Joint( name = "Link3_Link4" , parent= "Link3" , child = "Link4" , 
						type = "revolute", position = [0, 1, 0])
	pyrosim.Send_Cube(name="Link4", pos=[0, 0.5, 0] , size=[length, height, width])
	pyrosim.Send_Joint( name = "Link4_Link5" , parent= "Link4" , child = "Link5" , 
						type = "revolute", position = [0, 0.5, -0.5])
	pyrosim.Send_Cube(name="Link5", pos=[0, 0, -0.5] , size=[length, height, width])
	pyrosim.Send_Joint( name = "Link5_Link6" , parent= "Link5" , child = "Link6" , 
						type = "revolute", position = [0, 0, -1])
	pyrosim.Send_Cube(name="Link6", pos=[0, 0, -0.5] , size=[length, height, width])

	pyrosim.End()


Create_World()
Create_Robot()