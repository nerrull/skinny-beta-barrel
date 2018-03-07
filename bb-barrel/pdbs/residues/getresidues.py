import numpy as np
import glob
for fn in glob.glob('../inputs/????/????.tmstrands'):
	pdb = fn[fn.rfind('/')+1:fn.rfind('.')]
	strands = np.loadtxt(fn).astype(int)
	print pdb
	residues = []
	for start,end in strands:
		residues += range(start,end+1)
	np.savetxt(pdb+'.tmres', residues, fmt='%d')

for fn in glob.glob('../inputs/????/????.strands'):
	pdb = fn[fn.rfind('/')+1:fn.rfind('.')]
	strands = np.loadtxt(fn).astype(int)
	print pdb
	residues = []
	for start,end in strands:
		residues += range(start,end+1)
	np.savetxt(pdb+'.bbres', residues, fmt='%d')

loopthrsd = 17
for fn in glob.glob('../inputs/????/????.strands'):
	pdb = fn[fn.rfind('/')+1:fn.rfind('.')]
	strands = np.loadtxt(fn).astype(int)
	print pdb
	extras = []
	peris = []
	for i in range(len(strands)-1):
		if strands[i+1][0]-strands[i][1]-1>loopthrsd:
			continue
		if i%2==0:
			extras += range(strands[i][1], strands[i+1][0]+1)
		else:
			peris += range(strands[i][1], strands[i+1][0]+1)
	np.savetxt(pdb+'.elres', extras, fmt='%d')
	np.savetxt(pdb+'.plres', peris, fmt='%d')
