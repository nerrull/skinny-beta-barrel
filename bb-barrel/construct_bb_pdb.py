#!/usr/bin/python
import glob
import os
import numpy as np
import sys

cwd = os.getcwd()

#for fn in glob.glob('pdbs/ca/3emn_reidx_ext.pdb'):
for fn in glob.glob('pdbs/ca/????_reidx_ext.pdb'):

	# modify the pdb to fit BBQ input format
	pdb = fn[ fn.find('pdbs/ca/')+len('pdbs/ca/') : fn.find('_reidx_ext.pdb') ]
	print pdb
	with open(fn) as fin:
		lines = fin.readlines()
	for i in range(len(lines)):
		lines[i] = lines[i].replace(' CA   ', '  CA  ')
	prebbqfn = 'pdbs/tmppdbs/'+pdb+'_prebbq.pdb'
	with open(prebbqfn,'w') as fout:
		fout.writelines(lines)

	
	# run bbq
	postbbqfn = './pdbs/bb/'+pdb+'_reidx_ext.pdb'
	#print( '/usr/bin/java -classpath /home/wtian7/projects/bb-barrel/scripts/BBQ:/home/wtian7/projects/bb-barrel/scripts/BBQ/jbcl.jar BBQ -d=/home/wtian7/projects/bb-barrel/scripts/BBQ/q_50_xyz.dat -r=/home/wtian7/projects/bb-barrel/' +prebbqfn+' > /home/wtian7/projects/bb-barrel/'+postbbqfn )
	#os.system( '/usr/bin/java -classpath /home/wtian7/projects/bb-barrel/scripts/BBQ:/home/wtian7/projects/bb-barrel/scripts/BBQ/jbcl.jar BBQ -d=/home/wtian7/projects/bb-barrel/scripts/BBQ/q_50_xyz.dat -r=/home/wtian7/projects/bb-barrel/' +prebbqfn+' > /home/wtian7/projects/bb-barrel/'+postbbqfn )
	os.system( '/usr/bin/java -classpath '+cwd+'/scripts/BBQ:'+cwd+'/scripts/BBQ/jbcl.jar BBQ -d='+cwd+'/scripts/BBQ/q_50_xyz.dat -r='+cwd+'/'+prebbqfn+' > '+cwd+'/'+postbbqfn )

