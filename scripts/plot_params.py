#!/usr/bin/env python

import math
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt

logs_ = "/home/amalia/Test/gim2d/logs"
iters_=[1,10,100, 250,500,1000, 1500,2000,50000,10000]
mdpar_d = {0:'Flux', 1:'B/T', 2:'bulge_Re', 3:'bulge_e', 4:'bulge_phi', 5:'exp_disc_scale', 6:'disc_incl_i', 7:'disk_phi', 8:'sp_x_gal', 9:'sp_y_gal', 10:'bkg', 11:'bulge_Sersic_index'}
'''
opens and reads a log file 
'''

def readlog(filename):
	values = []
	with open(filename) as f:
		for line in f:
			if line[0] == 'P' :
				data = line.split(" ")
				values.append(data[1:])
	return values

def readLogs(filename, iters):
	pairs = []
	i = 0
	with open(filename) as f:
		for line in f:
			values = readlog(line[:len(line)-1])
			pairs.append((values, iters[i]))
			i=i+1
	return pairs

def par_val(pairs, param_n):
	x=[]
	y=[]
	min_=[]
	max_=[]

	for p in pairs:
		y.append(p[0][param_n][0])
		x.append(p[1])
		min_.append(p[0][param_n][1])
		max_.append(p[0][param_n][2])

	p_vals = []
	p_vals.append([math.log(i,10) for i in x])
	p_vals.append(y)
	p_vals.append(min_)
	p_vals.append(max_)
	p_vals.append(param_n)

	return param_n

def main():

	pairs = readLogs()
	par_val(pairs, 0)
	


class Plotter(object):


	def __init__(self, x, y, min_, max_, param_name):

		'''
		x,y,min_ and max_ are arrays
		'''
		self.x = x
		self.y = y
		self.min = min_
		self.max = max_
 
	def make_graph(self):
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		plt.errorbar(x, y, xerr=0, yerr=[y-min_, max_-y], fmt ='o', color='blue')
		ax.set_title('Iteration vs'+ param_name)
		plt.show()

