#!/usr/bin/python
import sys
import os
from subprocess import Popen, PIPE

pdbs = ['unkn']
#pdbs = ['3emn']

allsetting = []
for part in ['tm']:
#for part in ['tm','bb']:
	for resol in ['ca']:
	#for resol in ['ca','bb','sc']:
		onesetting = []
		for pdb in pdbs:
			cmd = ['python', 'calc_rmsd.py', 'pdbs/'+resol+'/'+pdb+'.pdb', 'pdbs/pdb_'+resol+'/'+pdb+'.'+resol+'.pdb', 'pdbs/residues/'+pdb+'.'+part+'res']
			(stdout, stderr) = Popen(cmd, stdout=PIPE).communicate()
			onesetting.append(stdout[4:].strip()) # remove pdb
		allsetting.append(onesetting)

tot = 0
#for row in range(len(allsetting[0])):
for row in range(len(pdbs)):
	pdb = pdbs[row]

	aline = ' '.join( allsetting[col][row] for col in range(len(allsetting)) )
	aline = pdb+'\t'+ aline.replace(' ','\t')
	print aline
	tot+= float(aline.split()[2])
print tot/len(pdbs)
