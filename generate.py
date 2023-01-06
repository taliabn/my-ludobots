import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")
length, height, width = 1, 1, 1 # cube dimensions
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[length, height, width])
pyrosim.End()