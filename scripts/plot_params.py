#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import scipy as sc
import numpy as np
import matplotlib as mpl




pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         ]
}

mpl.rcParams.update(pgf_with_pdflatex)

logs = "/home/amalia/Tests/gim2d/gim2d-test/inputs/logs"
mpl.use("pgf")
iters=[100, 10000,1000, 10, 1500, 1, 2000, 250, 5000, 500]
mdpar_d = {0:"Flux", 1:"B_T", 2:'bulge_Re', 3:'bulge_e', 4:'bulge_phi', 5:'exp_disc_scale', 6:'disc_incl_i', 7:'disk_phi', 8:'sp_x_gal', 9:'sp_y_gal', 10:'bkg', 11:'bulge_Sersic_index'}
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

def readLogs(filename, it):
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

	return p_vals

def main():

	pairs = readLogs(logs, iters)
	for k in mdpar_d.keys():
		p_vals = par_val(pairs, k)
		pl = Plotter(p_vals[0], p_vals[1], p_vals[2], p_vals[3], mdpar_d[k])
		pl.make_graph()
	#for p in pairs:
	#	print p[1]
	
import matplotlib.pyplot as plt

class Plotter(object):


	def __init__(self, x, y, min_, max_, param_name):

		'''
		x,y,min_ and max_ are arrays
		'''
		self.x = x
		self.y = y
		self.min_ = min_
		self.max_ = max_
		self.pname = param_name
 
	def make_graph(self):
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		ax.set_xlabel(u"Iterations")
		ax.set_ylabel(self.pname)
		y=np.asarray(self.y, np.float)
		min_=np.asarray(self.min_, np.float)
		max_=np.asarray(self.max_, np.float) 
		x=np.asarray(self.x, np.float)
		y_min = min(y-y*0.5)#min(min_)
		y_max=max(y+y*0.5)#max(max_)
		plt.ylim((y_min, y_max))
		plt.errorbar(x, y, xerr=0, yerr=[y-min_,max_-y], fmt ='o', color='black')
		if self.pname == "B/T":
			ax.set_title('Iteration vs '+ u"B/T")
		else:
			ax.set_title('Iteration vs '+ self.pname)
		plt.savefig(self.pname+'.pdf')
		plt.close()
		#plt.show()

