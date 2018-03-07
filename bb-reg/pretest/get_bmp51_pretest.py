#!/usr/bin/python


import numpy as np
pdbs = [ '1a0s']

pdbs=[ 'unkn']


import sys

if len(sys.argv)<2:
	print 'Usage :', sys.argv[0], '<max_strand_len>'
	print 'No max_strand_len provided, using default value 12'
	sys.argv.append(12)

maxlen = int(sys.argv[1])
with open('bmp51_len'+str(maxlen).zfill(2)+'.pretest','w') as f:
	for pdb in pdbs:
		f.write(pdb)
		strands = np.loadtxt('../inputs/'+pdb+'/'+pdb+'.strands').astype(int)
		for i in range(len(strands)):
			if i%2==0:
				start = strands[i][0]
				end = start+maxlen-1
				if end > strands[i][1]:
					end = strands[i][1]

			else:
				end = strands[i][1]
				start = end-maxlen+1
				if start < strands[i][0]:
					start = strands[i][0]
			f.write(' '+str(start)+' '+str(end))
		f.write('\n')
