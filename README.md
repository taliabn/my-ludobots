## Description

This repo contains work for the Northwestern University course Computer Science 396: Artificial Life. 
Branches up until and including 'ludobots-final-project' follow the [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics

## Installation

This code runs on Python 3.11.0.
Dependencies are managed through an Anaconda environment.
To copy this the environment, first install Anaconda. Then, run 
```bash
conda env create --name <new environment name> --file ludobot_env.txt
```
Before running anything, make sure to first activate the environment with
```bash
conda activate <new environment name>
```

Use the command 
```bash 
python search.py
``` 
to start running the simulation. 
To rerun a certain simulation, ensure the brain file is saved as "brain\<solutionID\>.nndf. 
Then run the command 
```bash
python simulate.py GUI <solutionID>
```
Parameters such as number of generations and population size, and simulation length can be set in the file `constants.py`.

NOTE: certain lines use `os.system()` calls, which are operating system specific.
The code is currently written for a windows machine using a bash terminal. 
See [r/ludobots: parallelhillclimber](https://www.reddit.com/r/ludobots/wiki/parallelhc/) for details on how to change this.

## Assignment 7: random 3D morphologies
[Assignment 7](https://youtube.com/shorts/HM3KmLzGZqs?feature=share), found on the [`random-3D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-3D-bodies) branch, adds the capability to randomly generate morphologies.

#### Method to generate bodies
3D bodies are recursively generated using graph-based body plans, a mehod that is heavily influenced by [Karl Sims'](https://www.karlsims.com/evolved-virtual-creatures.html) work<sup>[1]</sup>.

Properties of creatures are divided into two categories, those randomly generated for each creature and those determined by "DNA" genotype that identifies a general body plan. This means that it is *not* a direct encoding between phenotypes and genotypes. See Table 1  for a summary. The body plan genotype graph encodes the number of uniqe link types, number of children for each link, and number of clones of each link. Each unique link has its own link dimensions, joint axis, directionality, and presence of sensor and corresponding color. See Figure 1 for a summary of how body plans are generated. 


| random | encoded |
| ------ | ------- |
| link dimensions | number of unique link types (nodes)
| sensor placement | number of clones (self edges)
| joint axis and directionality | number of new children (edges to next node)

Table 1. Summary of random vs encoded body part properties

![figure explaining how a numerical encoding of a body plan is transformed into a virtual creature](".\figures\fig2-a7.png") 
Figure 1. Body plan generation process

Note that the indirect encoding mechanism has an important implication: a single genotype can lead to multiple phenotypes. 

To ensure that body plans follow basic laws of physics, before adding a link to the body, we check that there is no existing link in the same absolute position, preventing overlapping body parts. This means that some links specified by the genotype may not end up in the final body. To allow for freer growth in the z-direction, the robot starts at an absolute position of [0,0,3] and drops to the ground when the simulation starts. Additionally, we check that the absolute z position of a link isn't negative (i.e below the floor) before adding it.


#### Benefits:
* Duplicated body parts create symmetry, which mimics nature
* Indirect encoding enables diversity of creatures and also mimics nature

#### Drawbacks:
* linear graph structure: each unique node only connects to next unique node
* 2 children edges per node maximum
* can only branch at right angles
* symmetry can limit the potential morphospace
	
[1] "Evolving Virtual Creatures" K.Sims, Computer Graphics (Siggraph '94 Proceedings), July 1994, pp.15-22

## Assignment 6: random 1D morphologies
[Assignment 6](https://youtu.be/uXb1K-MACNE), found on the [`random-1D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-1D-bodies) branch, adds the capability to randomly generate morphologies. The robots consist of a chain of links on the floor connected by joints that can rotate around the z-axis. Touch sensors are placed on random links, and each link has a 50% chance of having a sensor. When running the simulation in GUI mode, links with sensors are colored green, and links without sensors are colored blue. Parameters dictating the range of link side lengths and the maximum number of links can be set in `constants.py`. There will always be a minimum of two links and one joint between them. The following parameters were used in the final simulations for this assignmment:
* `maxNumLinks = 10`
* `minSideLen = 0.1`
* `maxSideLen = 2`
* `populationSize = 1`
* `numberOfGenerations = 1`


## Assignment 5: Ludobots Final Project
The [final project](https://youtu.be/qypMeX9zdyQ), found on the [`ludobots-final-project`](https://github.com/taliabn/my-ludobots/tree/ludobots-final-project) branch, demonstrates the use of a Parallel hillclimber and an evolution through random mutations to create robots that can climb a set of stairs.
The fitness function used to evaluate the robots is total euclidean distance from the top of the pyramid to the final position of the robot's root link (torso).
The goal is to minimize fitness, where 0 is the best possible fitness.
Brains also feature a layer of hidden neurons.

## Assignments 1-4:
See [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics for more info.

## Contact

Talia Ben-Naim - taliaben-naim2025@u.northwestern.edu

## Acknowledgments

* [r/ludobots](https://www.reddit.com/r/ludobots/)
* [pyrosim](https://github.com/ccappelle/pyrosim)
* [pybullet](https://github.com/bulletphysics/bullet3)
* [Northwestern University Computer Science](https://www.mccormick.northwestern.edu/computer-science/)
* [Karl Sims](https://www.karlsims.com/evolved-virtual-creatures.html)
