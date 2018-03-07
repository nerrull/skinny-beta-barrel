#!/usr/bin/env python

import numpy as np


def fit(P, Q):
	"""
	Varies the distance between P and Q, and optimizes rotation for each step
	until a minimum is found.
	"""
	step_size = P.max(0)
	threshold = step_size*1e-9
	rmsd_best = kabsch_rmsd(P, Q)
	while True:
		for i in range(3):
			temp = np.zeros(3)
			temp[i] = step_size[i]
			rmsd_new = kabsch_rmsd(P+temp, Q)
			if rmsd_new < rmsd_best:
				rmsd_best = rmsd_new
				P[:, i] += step_size[i]
			else:
				rmsd_new = kabsch_rmsd(P-temp, Q)
				if rmsd_new < rmsd_best:
					rmsd_best = rmsd_new
					P[:, i] -= step_size[i]
				else:
					step_size[i] /= 2
		if (step_size <= threshold).all():
			break
	return rmsd_best


def kabsch_rmsd(P, Q):
	"""
	Rotate matrix P unto Q and calculate the RMSD
	"""
	P = rotate(P, Q)
	return rmsd(P, Q)


def rotate(P, Q):
	"""
	Rotate matrix P unto matrix Q using Kabsch algorithm
	"""
	U = kabsch(P, Q)

	# Rotate P
	P = np.dot(P, U)
	return P


def kabsch(P, Q):
	"""
	The optimal rotation matrix U is calculated and then used to rotate matrix
	P unto matrix Q so the minimum root-mean-square deviation (RMSD) can be
	calculated.
	Using the Kabsch algorithm with two sets of paired point P and Q,
	centered around the center-of-mass.
	Each vector set is represented as an NxD matrix, where D is the
	the dimension of the space.
	The algorithm works in three steps:
	- a translation of P and Q
	- the computation of a covariance matrix C
	- computation of the optimal rotation matrix U
	http://en.wikipedia.org/wiki/Kabsch_algorithm
	Parameters:
	P -- (N, number of points)x(D, dimension) matrix
	Q -- (N, number of points)x(D, dimension) matrix
	Returns:
	U -- Rotation matrix
	"""

	# Computation of the covariance matrix
	C = np.dot(np.transpose(P), Q)

	# Computation of the optimal rotation matrix
	# This can be done using singular value decomposition (SVD)
	# Getting the sign of the det(V)*(W) to decide
	# whether we need to correct our rotation matrix to ensure a
	# right-handed coordinate system.
	# And finally calculating the optimal rotation matrix U
	# see http://en.wikipedia.org/wiki/Kabsch_algorithm
	V, S, W = np.linalg.svd(C)
	d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

	if d:
		S[-1] = -S[-1]
		V[:, -1] = -V[:, -1]

	# Create Rotation matrix U
	U = np.dot(V, W)

	return U


def centroid(X):
	"""
	Calculate the centroid from a vectorset X
	"""
	C = sum(X)/len(X)
	return C


def rmsd(V, W):
	"""
	Calculate Root-mean-square deviation from two sets of vectors V and W.
	"""
	D = len(V[0])
	N = len(V)
	rmsd = 0.0
	for v, w in zip(V, W):
		rmsd += sum([(v[i]-w[i])**2.0 for i in range(D)])
	return np.sqrt(rmsd/N)


def get_coordinates(pdbfn, atomset):
	with open(pdbfn) as f:
		lines = f.readlines()
	#tmpdat = []
	dat = []
	for i in range(len(lines)):
		if not lines[i].startswith('ATOM'):
			continue
		seqid = int(lines[i][22:26])
		atom = lines[i][12:16].strip()
		if (seqid,atom) not in atomset:
			continue
		x = float(lines[i][30:38])
		y = float(lines[i][38:46])
		z = float(lines[i][46:54])
		dat.append([(seqid,atom),(x,y,z)])
		#tmpdat.append([seqid,atom])
	#for ha in sorted(tmpdat):
	#	print ha

	coords = []
	for itm in sorted(dat):
		coords.append(itm[1])
	return np.array(coords)


def get_atom_set(pdbfn):
	rtn = set()
	with open(pdbfn) as f:
		lines = f.readlines()
	for line in lines:
		try:
			seqid = int(line[22:26])
			atom = line[12:16].strip()
			rtn.add((seqid,atom))
		except:
			pass
	return rtn


if __name__ == "__main__":
	import sys

	if len(sys.argv)<3:
		print 'Usage: '+sys.argv[0]+' <pdb1> <pdb2> [resi list]'
		sys.exit(0)

	pdbfn1 = sys.argv[1]
	pdbfn2 = sys.argv[2]
	atomset1 = get_atom_set(pdbfn1)
	atomset2 = get_atom_set(pdbfn2)
	tmpatomset = atomset1.intersection(atomset2)
	atomset = set()
	if len(sys.argv)>3:
		resiset = set(np.loadtxt(sys.argv[3]).astype(int).tolist())
		for itm in tmpatomset:
			if itm[0] in resiset:
				atomset.add(itm)
	else:
		atomset = tmpatomset

	#TODO read seqids first find common
	P = get_coordinates(pdbfn1,atomset)
	Q = get_coordinates(pdbfn2,atomset)

	# Calculate 'dumb' RMSD
	normal_rmsd = rmsd(P, Q)

	# Create the centroid of P and Q which is the geometric center of a
	# N-dimensional region and translate P and Q onto that center.
	# http://en.wikipedia.org/wiki/Centroid
	Pc = centroid(P)
	Qc = centroid(Q)
	P -= Pc
	Q -= Qc

	#print "Normal RMSD:", normal_rmsd
	#print "Kabsch RMSD:", kabsch_rmsd(P, Q)
	#print pdbfn1[pdbfn1.rfind('/')+1:pdbfn1.rfind('.')],len(P), fit(P, Q)
	print pdbfn1[pdbfn1.rfind('/')+1:pdbfn1.rfind('.')],len(P), kabsch_rmsd(P, Q)
