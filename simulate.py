import numpy as np
import sys
import pybullet as p # type: ignore
import pyrosim.pyrosim as pyrosim
import constants as c
from simulation import SIMULATION

directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()
