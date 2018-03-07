#!/usr/bin/python
import glob
import numpy as np

for resol in ['ca', 'bb', 'sc']:
	for fn in glob.glob('pdbs/'+resol+'/????_reidx_ext.pdb'):
		pdb = fn[fn.find('pdbs/'+resol+'/')+len('pdbs/'+resol+'/'):fn.find('_reidx_ext.pdb')]
		foutn = 'pdbs/'+resol+'/'+pdb+'.pdb'
    
		reindexmap = np.loadtxt('pdbs/reindexmap/'+pdb+'.map').astype(int)
		index = [ str(i).rjust(4) for i in reindexmap[:,0].tolist() ]
		seqindex = [ str(i).rjust(4) for i in reindexmap[:,1].tolist() ]
    
		idxdict = dict( zip( index, seqindex ) )
    
		#print pdb
		#print idxdict
		with open(fn) as f:
			lines = f.readlines()
    
		with open(foutn,'w') as fout:
			for line in lines:
				if len(line)>26:
					if line[22:26] in idxdict:
						fout.write(line[:22]+idxdict[line[22:26]]+line[26:])
				else:
					fout.write(line)
    
