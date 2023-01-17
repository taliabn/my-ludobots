import pyrosim.pyrosim as pyrosim


def Create_World():
	pyrosim.Start_SDF("world.sdf")
	width, length, height = 1, 1, 1 # box dimensions
	pyrosim.Send_Cube(name="Box", pos=[-2, -2, 0.5] , size=[width, length, height])
	pyrosim.End()


def Generate_Body():
	pyrosim.Start_URDF("body.urdf") # stores description of robot's body
	width, length, height = 1, 1, 1 # link dimensions

	# joint naming convention: Parent_Child
	pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5] , size=[width, length, height])
	pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , 
						type = "revolute", position = [1.0, 0, 1.0])
	pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[length, height, width])
	pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , 
						type = "revolute", position = [2.0, 0, 1.0])
	pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[length, height, width])

	pyrosim.End()


def Generate_Brain():
	pyrosim.Start_NeuralNetwork("brain.nndf") # stores description of neural network

	pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")

	pyrosim.End()


def Create_Robot():
	Generate_Body()
	Generate_Brain()


Create_World()
Create_Robot()