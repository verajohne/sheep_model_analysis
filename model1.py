import numpy as np
import scipy.io
import dataprocessor as dp

'''
given sample data for a heard of size i,
use data for flock of 100-6 to project around 6
output is a new trajectory matrix of 100 nodes based on

'''

def create_trajectory(trajectory6, trajectory94, rotation = False, rw = False):
	'''
	rw = random walk
	-option to feed in a list of a random walk to act as com/trajectory path of herd
	-mainly for testing
	'''
	if rw:
		com6 = dp.random_walk(15631)
	else:
		com6 = dp.get_com(trajectory6)

	com94 = dp.get_com(trajectory94)
	
	updated94 = 0
	for ts in range(trajectory6.shape[1]):
		#get 2D matrix of topology at ts
		temp = dp.returnTimeMap(ts, trajectory94)
		temp = np.swapaxes(temp,0,1)
		if rotation:
			angle_between_com = dp.angle_between_vectors(com94[ts],com6[ts])
			for i in range(temp.shape[0]):
				temp[i] = dp.rotate_about_point(temp[i], com6[ts], angle_between_com)
		
		d = com6[ts] - com94[ts]
		temp = np.add(temp, d)
	
		temp = np.swapaxes(temp,0,1)
		if ts == 0:
			updated94 = temp
		else:
			updated94 = np.dstack((updated94, temp))

	updated94 = np.swapaxes(updated94, 1,2)

	result = np.dstack((updated94, trajectory6))
	
	return result
	

