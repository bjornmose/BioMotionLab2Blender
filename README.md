# BioMotionLab2Blender

Walk Cycle Generator

This script implements the BMLwalker developed by the BioMotion Lab 
(http://www.biomotionlab.ca) . The collection of motion capture data and 
the development of the algorithm implemented in this script were done by 
N. Troje. Any publication related to the usage of data and algorithm 
should cite the following two publications:
Troje, N. F. (2002) Decomposing biological motion: A framework for 
analysis and synthesis of human gait patterns. Journal of Vision 2:371-387.
Troje, N. F. (2008) Retrieving information from human movement patterns. 
In: Shipley, T. F. and Zacks, J. M. (eds.) Understanding Events: How 
Humans See, Represent, and Act on Events. Oxford University Press, pp. 
308-334.

The upper part contains the class BioMotionLabGenrator
it is pure python and should be usefull to many projects not directly dealing with blender
it contains data drawn from https://www.biomotionlab.ca/html5-bml-walker/  .. no deep linking .. Walker.js 
did take some code reading and put things to python BM

the lower part ports data to Blender (www.blender.org) generates objects in blender to view and control them.
Control is minimal but works .. that is in blender 3.79 
needs an active time line  (start 0.. end 39) with key frames set to position
you can run the script .. start the animation (alt-a) 
modify the parameters gender and others  .... run the script again .. it works on the allready created tree
so almost live
