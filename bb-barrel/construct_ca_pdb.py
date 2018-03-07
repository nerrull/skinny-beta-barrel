#!/usr/bin/python
import sys
sys.path.append('scripts')
from barrel_2zz import *
#import pdb_info
#info = pdb_info.read_pdb_info('pdb_info.list')

bmp51 = [ 'unkn' ]
dirns = [ 'w110030080_o2' ]

for pdb in bmp51:
	for dirn in dirns:
		# best params for 2zz model
		bb = Barrel(pdb, 3.345, 4.83, 0.85, 0.22, 'construction_inputs/results/'+dirn, True)
		write_pdb(bb.balls, 'pdbs/ca/'+pdb+'_reidx_ext.pdb', bb.strandlens, True, bb.reindexmap, 'pdbs/reindexmap/'+pdb+'.map')

