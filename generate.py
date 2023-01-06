import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")
length, height, width = 1, 1, 1 # box dimensions
x, y, z = 0, 0, 0.5 # box starting position
pyrosim.Send_Cube(name="Box", pos=[x, y, z] , size=[length, height, width])
pyrosim.Send_Cube(name="Box2", pos=[x, y, z] , size=[length, height, width])
pyrosim.End()