## Description

This repo contains work for the Northwestern University course Computer Science 396: Artificial Life. 
Branches up through 'ludobots-final-project' follow the [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics.

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
## Usage
Instructions on running the code are as follows:
Use the command 
```bash 
python search.py <seed>
``` 
to start running the simulation. 
For running multiple searches in a row, first set the list of desired seeds in line 1 of the file `run-search.sh`. Then run the command
```bash
sh search.py
```
Both error messages and console outputs will be saved in the file "out<seed>.txt". A numpy array of fitness values as well as brain.nndf and body.urdf files for the best robots will be saved in a folder named <seed>.
To analyze a certain search by showing and saving a fitness curve (plot of best fitness value for each generation), run the command:
```bash
python analyze.py GUI <solutionID> <seed>
```
To rerun a certain simulation in GUI mode, ensure the brain file is saved as "<seed>\brain<solutionID\>.nndf" and the body file is saved as "<seed>\body<solutionID\>.urdf". This will be the case if search.py is run properly. Then, run the command: 
```bash
python simulate.py GUI <solutionID> <seed>
```
Parameters such as number of generations and population size, and simulation length can be set in the file `constants.py`.

NOTE: certain lines use `os.system()` calls, which are operating system specific.
The code is currently written for a windows machine using a bash terminal. 
See [r/ludobots: parallelhillclimber](https://www.reddit.com/r/ludobots/wiki/parallelhc/) for details on how to change this.


## Assignment 7: random 3D morphologies
[Assignment 7](https://youtube.com/shorts/HM3KmLzGZqs?feature=share), found on the [`random-3D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-3D-bodies) branch, adds the capability to randomly generate morphologies.

### Method to generate bodies
3D bodies are recursively generated using graph-based body plans, a mehod that is heavily influenced by [Karl Sims'](https://www.karlsims.com/evolved-virtual-creatures.html) work<sup>[1]</sup>.

Properties of creatures are divided into two categories, those randomly generated for each creature and those determined by "DNA" genotype that identifies a general body plan. This means that it is *not* a direct encoding between phenotypes and genotypes. See Table 1  for a summary. The body plan genotype graph encodes the number of uniqe link types, number of children for each link, and number of clones of each link (self edges). Each unique link has its own link dimensions, joint axis, directionality, and presence of sensor and corresponding color. See Figure 1 for an example of how body plans are generated. 

Note that the indirect encoding mechanism has an important implication: a single genotype can lead to multiple phenotypes. 

| random | encoded |
| ------ | ------- |
| link dimensions | number of unique link types (nodes)
| sensor placement | number of clones (self edges)
| joint axis and directionality | number of new children (edges to next node)

Table 1. Summary of random vs encoded body part properties

![figure explaining how a numerical encoding of a body plan is transformed into a virtual creature](/figures/a7-fig1.png) 

Figure 1. Body plan encoding to pheontype relationship

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

### Method to generate brains
Brains are generated with a structure resembling that of a traditional feed forward neural network. There is one sensor neuron for each link with a sensor and one motor neuron for each link. Sensor neurons are connected to a layer of hidden neurons which are then connected to motor neurons. All synsapses start with a random weight between -1 and 1. The number of sensor and motor neurons is specific to each body plan, and `numHiddenNeurons` can be specified in `constants.py`. See Fig. 2 for an example of brain structure.

![figure illustrating structure that resembles a neural network](/figures/a7-fig2.png) 

Figure 2. Structure of robot brains

#### Parameters
The following parameters were used in the final simulations for this assignmment:
* `maxNumNodes = 5`
* `maxNumSelfEdges = 4`
* `maxNumChildEdges = 2`
* `minSideLen = 0.1`
* `maxSideLen = 1`
[1] "Evolving Virtual Creatures" K.Sims, Computer Graphics (Siggraph '94 Proceedings), July 1994, pp.15-22

## from A 6:
The robots consist of a chain of links on the floor connected by joints that can rotate around the z-axis. Touch sensors are placed on random links, and each link has a 50% chance of having a sensor. When running the simulation in GUI mode, links with sensors are colored green, and links without sensors are colored blue. Parameters dictating the range of link side lengths and the maximum number of links can be set in `constants.py`. There will always be a minimum of two links and one joint between them. 

## Past Assignments

## Assignment 6: random 1D morphologies
[Assignment 6](https://youtu.be/uXb1K-MACNE) adds the capability to randomly generate morphologies in one dimensions. See the branch [`random-1D-bodies`](https://github.com/taliabn/my-ludobots/tree/random-1D-bodies) for further details.

## Assignment 5: Ludobots Final Project
The [Ludobots final project](https://youtu.be/qypMeX9zdyQ),  demonstrates the use of a Parallel hillclimber and an evolution through random mutations to create robots that can climb a set of stairs. See the branch [`ludobots-final-project`](https://github.com/taliabn/my-ludobots/tree/ludobots-final-project) for further details.

## Assignments 1-4:
See [ludobots](https://www.reddit.com/r/ludobots/) online course on Evolutionary Robotics for further details. Code can be found in branches up until 'ludobots-final-project'.

## Contact

Talia Ben-Naim - taliaben-naim2025@u.northwestern.edu

## Acknowledgments

* [r/ludobots](https://www.reddit.com/r/ludobots/)
* [pyrosim](https://github.com/ccappelle/pyrosim)
* [pybullet](https://github.com/bulletphysics/bullet3)
* [Northwestern University Computer Science](https://www.mccormick.northwestern.edu/computer-science/)
* [Karl Sims](https://www.karlsims.com/evolved-virtual-creatures.html)
