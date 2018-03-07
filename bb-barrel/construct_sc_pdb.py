#!/usr/bin/python
import glob
import os

print 'Sidechain construction depends on Scwrl4.'
print 'You can find the software through this link http://dunbrack.fccc.edu/scwrl4/'

print 'please enter the path of your Scwrl4 executable (eg. /path/to/scwrl4/ ):'
path = raw_input()


for fn in glob.glob('pdbs/bb/*_reidx_ext.pdb'):
	pdb = fn[fn.find('pdbs/bb/')+len('pdbs/bb/'):fn.find('_reidx_ext.pdb')]

	foutn = 'pdbs/sc/'+pdb+'_reidx_ext.pdb'
	os.system(path+'/Scwrl4 -h -i '+fn+' -o '+ foutn )
